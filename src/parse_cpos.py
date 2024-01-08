import datetime
from pathlib import Path
from pyrtcm import RTCMReader
from pyrtcm import RTCM_DATA_FIELDS, RTCM_MSGIDS
import re

fpath = Path("data/cpos.bin")
data = fpath.read_bytes()

pattern = re.compile(b"\xd3[\x00-\x03].*?(?=^|\xd3)", re.DOTALL)
identities = dict()
messages: dict[list] = dict()
break_key = '1033'
while m := re.search(b"\xd3[\x00-\x03].", data):
    start = m.start()
    end = start + m[0][2] + (m[0][1] << 2) + 6
    part = data[start:end]
    data = data[end:]
    
    try:
        msg = RTCMReader.parse(part, validate=True)
    except Exception as e:
        continue
    
    key = f"{msg.identity} {RTCM_MSGIDS.get(msg.identity)}"
    messages.setdefault(key, []).append(msg._get_dict())
    if msg.identity == break_key:
        pass
    identities[msg.identity] = identities.get(msg.identity, 0) + 1
    dict_ = msg._get_dict()
    if not dict_:
        continue
    for key, desctiption in dict_.items():
        if "group" not in key:
            pass
            # print(key, desctiption, getattr(msg, key))
        else:
            key, dict_ = desctiption
            num = int(getattr(msg, key))
            key_inner = next(iter(dict_))
            desctiption_inner = dict_[key_inner]
            # for i in range(1, num + 1):
                # subkey = f"{key_inner}_{i:02d}" if num > 1 else key_inner
                # print(key, subkey, desctiption_inner, getattr(msg, subkey))

    # print("\n")

[print(i, RTCM_MSGIDS.get(i, None)) for i in sorted(identities.keys())]
