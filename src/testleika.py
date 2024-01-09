from laika import AstroDog
from laika.helpers import ConstellationId
from laika.gps_time import GPSTime
from datetime import datetime


constellations = (ConstellationId.GALILEO,ConstellationId.GLONASS,ConstellationId.GPS, ConstellationId.BEIDOU, ConstellationId.QZNSS)
dog = AstroDog(valid_const = constellations)

ts = GPSTime.from_datetime(datetime(2023, 1, 1, 20, 0, 0))
# prn = "E03"

eph = dog.get_orbit_data(ts)

here = True
