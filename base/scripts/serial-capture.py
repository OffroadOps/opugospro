import argparse
import sys
import time

import serial

parser = argparse.ArgumentParser()
parser.add_argument("--port", default="COM10")
parser.add_argument("--baud", type=int, default=115200)
parser.add_argument("--out", default=r"D:/img/base/out/a5e-serial-capture.log")
args = parser.parse_args()

ser = serial.Serial(args.port, args.baud, bytesize=8, parity="N", stopbits=1, timeout=1)
ser.dtr = False
ser.rts = False
print(f"capturing {args.port} @ {args.baud} -> {args.out}", flush=True)

log = open(args.out, "ab", buffering=0)
log.write(f"\n===== capture start {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n".encode())
start = time.time()
idle_reset = False
try:
    while True:
        data = ser.read(4096)
        if data:
            stamp = time.strftime("%H:%M:%S")
            log.write(f"[{stamp}] ".encode() + data)
            idle_reset = True
        else:
            if idle_reset and time.time() - start > 1800:
                break  # bounded: 30 min after first data; restart for a new capture
except KeyboardInterrupt:
    pass
finally:
    log.write(f"\n===== capture end {time.strftime('%H:%M:%S')} =====\n".encode())
    log.close()
    ser.close()
