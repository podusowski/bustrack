#!/usr/bin/env python3
import argparse
import time
import datetime
from mpkwroclaw import fetch_positions


def _parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    record_parser = subparsers.add_parser('record', help='record line\'s position')
    record_parser.add_argument('--line', type=int, required=True)

    return parser.parse_args()


def _record(args):
    print(f'# recording started at {datetime.datetime.now()}')
    print(f'# lines tracked: {args.line}')
    print('$ identity;position')
    while True:
        for identity, position in fetch_positions([args.line]):
            print(f'{identity};{position}')
        time.sleep(5)


if __name__ == "__main__":
    args = _parse_args()

    if args.command == 'record':
        _record(args)