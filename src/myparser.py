import re
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta
from keplerian import kepler2ecef

gpd_fields = [
    "clock_bias",
    "clock_drift",
    "clock_drift_rate",
    "iode",
    "crs",
    "delta_n",
    "m0",
    "cuc",
    "e",
    "cus",
    "sqrt_a",
    "toe_sow",
    "cic",
    "omega0",
    "cis",
    "i0",
    "crc",
    "omega",
    "omega_dot",
    "idot",
    "codes",
    "gps_week",
    "l2_p_flag",
    "sv_acc",
    "sv_health",
    "tgd",
    "iodc",
    "tom",
    "fit_interval",
]
f_pat = lambda name: f"(?P<{name}>[ -]\d\.\d{{12}}E[+-]\d{{2}})"
epoch = r"(?P<epoch>\d{4} \d{2} \d{2} \d{2} \d{2} \d{2})"

gps_sv = r"(?P<sv>G\d{2})"
gps_data = r"\n? *".join(f_pat(f) for f in gpd_fields)
gps_pat = re.compile(f"^{gps_sv} {epoch}{gps_data}", re.MULTILINE)


def parse_gps_nav(text: str) -> dict:
    """
    parse GPS navigation message
    """
    out = []
    for m in gps_pat.finditer(text):
        d = m.groupdict()
        for k in floats:
            d[k] = float(d[k].replace(" ", ""))
        d["epoch"] = datetime.strptime(d["epoch"], "%Y %m %d %H %M %S")
        if d["sat"].startswith("G"):
            w, s = d["gps_week"], d["toe_sow"]
            d["toe"] = timedelta(weeks=w, seconds=s).total_seconds()
        out.append(d)
    return out


file = Path("/workspaces/pose_est/data/DGLS00NOR_S_20240081100_01H_GN.rnx")
text = file.read_text()
kepler2ecef(0, **parse_gps_nav(text)[0])
