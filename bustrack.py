#!/usr/bin/env python3
import argparse
import time
import datetime
import sys
from mpkwroclaw import FEEDS
from utils import parse_ecsv, extract_segments


def _parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    record_parser = subparsers.add_parser('record', help='record line\'s position')
    record_parser.add_argument('--line', type=str, required=True)

    feeds = list(FEEDS.keys())
    record_parser.add_argument('--feed', type=str, default=feeds[0], help='where take the data from', choices=feeds)

    segment_parser = subparsers.add_parser('segment', help='extract segment from previously recorded data')
    segment_parser.add_argument('segment', metavar='point', nargs='+', help='points for constructing a segment')

    subparsers.add_parser('info', help='some brief info about gathered data')

    return parser.parse_args()


def _record(args):
    print(f'# recording started at {datetime.datetime.now()}')
    print('$ time;identity;line;position')
    feed = FEEDS[args.feed]([args.line])
    while True:
        for record in feed:
            print(f'{record.time};{record.identity};{record.line};{record.lat},{record.lon}')
        time.sleep(5)


def _parse_segment(args):
    return [p.split(',') for p in args.segment]


class RecordedPoint:
    '''Geo-algorithms works on tuple-like points, this class acts
    like one while storing more stuff that we'll need later.'''

    def __init__(self, record):
        self._record = record
        self.lat, self.lon = self._record.position.split(',')

    def __iter__(self):
        yield from (self.lat, self.lon)

    def __str__(self):
        return f'{self._record.time}'


def _segment(args):
    # this is so slow and stupid but it was faster to write
    data = list(parse_ecsv(sys.stdin))
    vehicles = set(r.identity for r in data)
    segment = _parse_segment(args)
    print(f'segment: {segment}')
    for vehicle in vehicles:
        record = [RecordedPoint(r) for r in data if r.identity == vehicle]
        try:
            for start, stop in extract_segments(record, [_parse_segment(args)], sensitivity=100):
                print(f'{start} -> {stop}')
        except RuntimeError as e:
            print(f'some part of the data for {vehicle} is corrupted: {e}')


def _info(args):
    data = parse_ecsv(sys.stdin)
    print(f'vehicles: {set(r.identity for r in data)}')


if __name__ == "__main__":
    args = _parse_args()

    if args.command == 'record':
        _record(args)
    elif args.command == 'segment':
        _segment(args)
    elif args.command == 'info':
        _info(args)