#!/usr/bin/env python3

import argparse
import json
import socket
import sys
import time

from serial import Serial


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--serial-port", default="/dev/ttyACM0",
                    dest="tty", help="Serial port device to connect to.")
parser.add_argument("-b", "--bauds", default=9600, type=int,
                    help="Serial port speed")
parser.add_argument("-c", "--carbon-address", default="graphite-carbon.service.consul:2003")
parser.add_argument("-m", "--metric-name", default="test.temperature")


def main():
    args = parser.parse_args()

    while True:
        try:
            export_temperature(args)
        except KeyboardInterrupt:
            return None
        except Exception as exc:
            print(exc)

        time.sleep(30)

def export_temperature(args):
    temperature = get_temperature(args)
    if temperature is None:
        return

    print("Temperature is: {}°C".format(temperature))
    write_graphite(args, temperature)

def write_graphite(args, temperature):
    host, port = args.carbon_address.split(':', 1)
    port = int(port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        line = "{} {} {}\n".format(
            args.metric_name, temperature, int(time.time()))
        s.send(line.encode("ascii"))


def get_temperature(args):
    serial = Serial(args.tty, args.bauds)

    try:
        while True:
            line = serial.readline().decode('utf-8').rstrip("\n")
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            else:
                try:
                    temperature = data['temperature']
                except KeyError:
                    print("Bad JSON")
                    print(line)
                    print(data)
                    raise

                return temperature
    except OSError as err:
        if err.errno != 11:
            raise
    finally:
        serial.close()


if __name__ == '__main__':
    main()
