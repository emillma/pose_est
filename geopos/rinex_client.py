import re
import requests
from multiprocessing.pool import ThreadPool
from datetime import datetime, timedelta
import gzip
from geopos.credentials import password, username
from pathlib import Path
import aiohttp
import asyncio


class RinexClient:
    base = "https://etpos.kartverket.no/"

    def __init__(self, cache_dir: Path | None = None):
        self.session = None
        self.entered = False
        self.cache_dir = cache_dir

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, *args):
        if self.session is not None:
            await self.session.__aexit__(*args)

    async def set_session(self):
        async with asyncio.locks.Lock():
            if self.session is not None:
                return self

            assert self.entered
            self.session = await aiohttp.ClientSession().__aenter__()
            async with self.session.post(
                self.base + "Web Client/Login.xml",
                params={"Command": "Login"},
                data={"pword": password, "user": username},
            ) as r:
                chunk = await r.content.readany()

            pat = re.compile(b"(<CsrfToken>)(.*?)(</CsrfToken>)")
            self.token = pat.search(chunk)[2].decode()
            return self

    async def get_file(self, file: str):
        if self.cache_dir and (f := self.cache_dir.joinpath(file)).exists():
            return f.read_bytes()

        if self.session is None:
            await self.set_session()

        async with self.session.get(
            self.base,
            params={"Command": "Download", "File": file, "CsrfToken": self.token},
        ) as r:
            try:
                out = await r.content.readany()
                if self.cache_dir:
                    f.parent.mkdir(parents=True, exist_ok=True)
                    f.write_bytes(out)
                return out

            except aiohttp.ClientPayloadError:
                raise FileNotFoundError(file)

    async def get_data(self, time: datetime, mast: str, const: str):
        file = "/".join(
            [
                f"rnx3/1hour/1sec/",
                time.strftime("%Y"),
                time.strftime("%j"),
                mast,
                f"{mast}00NOR_S_{time.strftime('%Y%j%H')}00_01H_{const}.rnx.gz",
            ]
        )
        return await self.get_file(file)


async def main():
    async with RinexClient(cache_dir=Path("data/cache")) as client:
        content = await client.get_data(datetime(2024, 1, 8, 11), "BATC", "EN")
        Path("data/tmp.txt").write_text(gzip.decompress(content).decode())


if __name__ == "__main__":
    asyncio.run(main())
