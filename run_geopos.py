from datetime import datetime, timedelta
from pathlib import Path
import gzip

from laika import AstroDog
from laika.helpers import ConstellationId
from laika.gps_time import GPSTime

from geopos.rinex_client import RinexClient
from geopos.rinex_parser import parse_gps_nav
from geopos.keplerian import kepler2ecef
import asyncio


def utc_to_gnss(time: datetime):
    return time - datetime(1980, 1, 6)


async def main():
    constellations = (ConstellationId.GPS,)
    dog = AstroDog(valid_const=constellations)

    async with RinexClient(cache_dir=Path("data/cache")) as client:
        content = await client.get_data(datetime(2024, 1, 8, 11), "BATC", "GN")
        content_str = gzip.decompress(content).decode()
        parsed = parse_gps_nav(content_str)

        sat = parsed[0]
        print(sat["sv"], kepler2ecef(0, **sat)[0:])

    ts = GPSTime.from_datetime(sat["epoch"])
    # prn = "E03"
    # G17    129600.0
    eph = dog.get_sat_info("G17", ts)
    print(eph[0])


if __name__ == "__main__":
    asyncio.run(main())
