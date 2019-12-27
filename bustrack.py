#!/usr/bin/env python3
import argparse
import time
import datetime
from mpkwroclaw import OpenData


def _parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    record_parser = subparsers.add_parser('record', help='record line\'s position')
    record_parser.add_argument('--line', type=int, required=True)

    return parser.parse_args()


def _record(args):
    print(f'# recording started at {datetime.datetime.now()}')
    print('$ time;identity;line;position')
    feed = OpenData()
    while True:
        for record in feed:
            print(f'{record.time};{record.side_number};{record.line};{record.lat},{record.lon}')
        time.sleep(5)


if __name__ == "__main__":
    args = _parse_args()

    if args.command == 'record':
        _record(args)