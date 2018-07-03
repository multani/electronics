#!/usr/bin/env python3

import argparse
import time
import sys
from serial import Serial


parser = argparse.ArgumentParser(description=(
    "Read information sent on the serial interface for "
    "Arduino-based devices (and others).\n\n"
    ""
))
parser.add_argument('-n', '--no-reset', dest="do_reset", action="store_false",
                    default=True, help="Send a reset signal before reading data.")
parser.add_argument("-s", "--serial-port", default="/dev/ttyACM0",
                    dest="tty", help="Serial port device to connect to.")
parser.add_argument("-b", "--bauds", default=9600, type=int,
                    help="Serial port speed")
args = parser.parse_args()

print("** Using TTY %s." % (args.tty, ))

if args.do_reset:
    print("** Opening serial port %s..." % (args.tty, ))
    serial = Serial(args.tty)

    print("** Reinitializing Arduino...")
    serial.setDTR(1)
    time.sleep(0.5)
    serial.setDTR(0)
    serial.close()

print("** (re)Opening %s at %d bauds..." % (args.tty, args.bauds))
serial = Serial(args.tty, args.bauds)

try:
    while True:
        line = serial.readline().decode('ascii').rstrip("\n")
        print(line)
except KeyboardInterrupt:
    pass
except OSError as err:
    if err.errno != 11:
        raise
    print("** Disconnected (resource unavailable)")
finally:
    print("** Closing serial port...")
    serial.close()
