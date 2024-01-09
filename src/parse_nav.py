import re
from datetime import datetime, timedelta

shared_fields = [
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
]
gps_fields = [
    *shared_fields,
    "codes_L2",
    "gps_week",
    "l2_p_flag",
    "sv_acc",
    "sv_health",
    "tgd",
    "iodc",
    "tom",
    "fit_interval",
]

gal_fields = [
    *shared_fields,
    "data_sources",
    "gal_week",
    "spare",
    "sisa",
]
f_pat = lambda name: f"(?P<{name}>[ -]\d\.\d{{12}}E[+-]\d{{2}})"
epoch = r"(?P<epoch>\d{4} \d{2} \d{2} \d{2} \d{2} \d{2})"

gps_sv = r"(?P<sv>G\d{2})"
gps_data = r"\n? *".join(f_pat(f) for f in gps_fields)
gps_pat = re.compile(f"^{gps_sv} {epoch}{gps_data}", re.MULTILINE)

gal_sv = r"(?P<sv>E\d{2})"
gal_data = r"\n? *".join(f_pat(f) for f in gal_fields)
gal_pat = re.compile(f"^{gal_sv} {epoch}{gal_data}", re.MULTILINE)


def parse_gps_nav(text: str) -> dict:
    out = []
    for m in gps_pat.finditer(text):
        out.append(d := m.groupdict())
        d.update((k, float(d[k])) for k in gps_fields)
        d["epoch"] = datetime.strptime(d["epoch"], "%Y %m %d %H %M %S")
        d["toe"] = timedelta(weeks=d["gps_week"], seconds=d["toe_sow"]).total_seconds()
    return out


def parse_gal_nav(text: str) -> dict:
    out = []
    for m in gal_pat.finditer(text):
        out.append(d := m.groupdict())
        d.update((k, float(d[k])) for k in gal_fields)
        d["epoch"] = datetime.strptime(d["epoch"], "%Y %m %d %H %M %S")
        d["toe"] = timedelta(weeks=d["gal_week"], seconds=d["toe_sow"]).total_seconds()
        d["toe"] -= 1024
    return out
