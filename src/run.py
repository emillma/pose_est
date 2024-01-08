from cpos_link import CPOSLink
import time
# import sympy as sp
# import pyubx2
# from pyrtcm import RTCMReader
from pathlib import Path
import datetime

from credentials import username, password


def main():
    data = bytearray()
    time_str = datetime.datetime.now().strftime("%H%M%S.000")
    init_pos = f"$GPGGA,{time_str},6325.306,N,01023.558,E,1,12,1.0,0.0,M,0.0,M,,*60"

    with CPOSLink(username, password, init_pos) as kv_link:
        m = 0
        while m < 10:
            while msg := kv_link.read_nonblocking():
                data.extend(msg)
                print(msg)
                m += 1
            time.sleep(1)

    fname =  Path("data/cpos.bin")
    fname.write_bytes(data)


if __name__ == "__main__":
    main()
