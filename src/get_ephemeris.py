import re
import requests
from multiprocessing.pool import ThreadPool
import datetime
import itertools
import gzip
from io import BytesIO
from credentials import password, username
from pathlib import Path


def get_files(files: list[str], base_dir: Path | None):
    base = "https://etpos.kartverket.no/"
    
    with requests.Session() as s:
        rep = s.post(
            base + "Web Client/Login.xml",
            params={"Command": "Login"},
            data={"pword": password, "user": username},
            timeout=1,
        )
        token = re.search(b"(<CsrfToken>)(.*?)(</CsrfToken>)", rep.content)[2]

        def inner(file:str):
            rep = s.get(
                base,
                params={
                    "Command": "Download",
                    "File": file,
                    "CsrfToken": token,
                },
                timeout=1,
            )
            if base_dir is not  None:
                base_dir.joinpath(file.rpartition('/')[-1]).write_bytes(rep.content)

        with ThreadPool(10) as pool:
            return pool.map(inner, files)


if __name__ == "__main__":
    # NOTE: \x2f = /
    file = "\x2fstationlist\x2fstationlist2022-11-18.xml"

    start = datetime.datetime.now() - datetime.timedelta(days=1)

    times = [start + datetime.timedelta(hours=i) for i in range(3)]
    masts = ["VIKE", "BIRK"]

    files = [
        "\x2f".join(
            [
                "rnx3",
                "1hour",
                "1sec",
                t.strftime("%Y"),
                t.strftime("%j"),
                m,
                f"{m}00NOR_S_{t.strftime('%Y%j%H')}00_01H_01S_MO.rnx.gz",
            ]
        )
        for t, m in itertools.product(times, masts)
    ]
    reps = get_files(files, Path('data'))
    
    pass
