from laika import AstroDog
from laika.helpers import ConstellationId
from laika.gps_time import GPSTime
from datetime import datetime


constellations = (ConstellationId.GALILEO,)
dog = AstroDog(valid_const=constellations)

ts = GPSTime.from_datetime(datetime(2018, 1, 7, 21, 12, 21))
prn = "G07"

eph = dog.download_parse_prediction_orbit(ts)

here = True
