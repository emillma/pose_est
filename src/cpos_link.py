import time
import socket
import select
import base64
import logging

"""Check out https://github.com/jcmb/NTRIP
and https://github.com/LORD-MicroStrain/ntrip_client/tree/ros"""

init_pos = "$GPGGA,165657.611,6325.306,N,01023.558,E,1,12,1.0,0.0,M,0.0,M,,*61"


class CPOSLink:
    def __init__(self, username, password, initial_pos=init_pos):
        self.host = "159.162.103.14"
        self.port = 2101
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.login = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode(
            "utf-8"
        )
        self.Mountpoint = "CPOSRTCM32"
        self.set_pos(init_pos)

        self.last_pos_update = 0
        self.tape = bytearray()

    def __enter__(self):
        self.socket.__enter__()
        self.socket.connect((self.host, self.port))
        self.socket.sendall(
            (
                f"GET /{self.Mountpoint} HTTP/1.1\r\n"
                "Ntrip-Version: Ntrip/2.0\r\n"
                "User-Agent: NTRIP CPOSemil\r\n"
                f"Authorization: Basic {self.login}\r\n\r\n"
            ).encode("utf-8")
        )
        return self

    def __exit__(self, *args):
        self.socket.__exit__(*args)

    def set_pos(self, nmea):
        self.pos = self.fix_pos(nmea)
        self.pos = nmea

    def send_pos(self):
        self.socket.sendall(
            (f"GET /{self.Mountpoint} HTTP/1.1\r\n{self.pos}\r\n\r\n").encode("utf-8")
        )

    def read(self, n: int):
        return self.socket.recv(n)

    def read_nonblocking(self):
        if (ts := time.time()) - self.last_pos_update > 30:
            self.last_pos_update = ts
            self.send_pos()
        ready_to_read, _, _ = select.select([self.socket], [], [], 0)
        return ready_to_read[0].recv(4096) if ready_to_read else b""

    @staticmethod
    def fix_pos(nmea):
        if (checksum := CPOSLink.calcultateCheckSum(nmea[1:-3])) != nmea[-2:]:
            logging.warning(f"fixing checksum to {checksum}")
            nmea = nmea[:-2] + checksum
        return nmea

    @staticmethod
    def calcultateCheckSum(stringToCheck):
        xsum_calc = 0
        for char in stringToCheck:
            xsum_calc = xsum_calc ^ ord(char)
        return "%02X" % xsum_calc


if __name__ == "__main__":
    import datetime
    from geopos.credentials import username, password
    from pathlib import Path

    data = bytearray()
    time_str = datetime.datetime.now().strftime("%H%M%S.000")
    init_pos = f"$GPGGA,{time_str},6325.306,N,01023.558,E,1,12,1.0,0.0,M,0.0,M,,*60"

    with CPOSLink(username, password, init_pos) as kv_link:
        m = 0
        while m < 500:
            while msg := kv_link.read_nonblocking():
                data.extend(msg)
                print(msg)
                m += 1
            time.sleep(1)

    fname = Path("data/cpos.bin")
    fname.write_bytes(data)
