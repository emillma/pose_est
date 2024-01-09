import re
import requests
from multiprocessing.pool import ThreadPool
from datetime import datetime, timedelta
import gzip
from credentials import password, username
from pathlib import Path
import aiohttp
import asyncio


class KartverketClient:
    base = "https://etpos.kartverket.no/"

    def __init__(self, cache_dir=None):
        self.session = None
        self.entered = False
        self.cache_dir = cache_dir

    async def __aenter__(self):
        self.entered = True
        return self

    async def __aexit__(self, *args):
        await self.session.__aexit__(*args)

    async def set_session(self):
        assert self.entered
        self.session = await aiohttp.ClientSession().__aenter__()
        async with self.session.post(
            self.base + "Web Client/Login.xml",
            params={"Command": "Login"},
            data={"pword": password, "user": username},
        ) as r:
            chunk = await r.content.readany()
        self.token = re.search(b"(<CsrfToken>)(.*?)(</CsrfToken>)", chunk)[2].decode()
        return self

    async def get_file(self, file: str):
        if self.session is None:
            await self.set_session()

        async with self.session.get(
            self.base,
            params={"Command": "Download", "File": file, "CsrfToken": self.token},
        ) as r:
            try:
                return await r.content.read()
            except aiohttp.ClientPayloadError:
                return b""


async def main():
    async with KartverketClient() as client:
        content = await client.get_file(
            # "rnx3/1hour/1sec/2024/008/DGLS/DGLS00NOR_S_20240081100_01H_01S_MO.rnx.gz"
            "rnx3/1hour/1sec/2024/008/DGasdfLS/DGLS00NOR_S_20240081100_01H_01S_MO.rnx.gz"
        )
        gzip.decompress(content)


if __name__ == "__main__":
    asyncio.run(main())
