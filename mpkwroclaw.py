import argparse
import requests
import time
from typing import NamedTuple
from collections import defaultdict


_URL = 'http://mpk.wroc.pl/position.php'


class VehicleIdentity(NamedTuple):
    line: int
    course: int


class Position(NamedTuple):
    x: int
    y: int


def fetch_positions(buses):
    '''Only buses for now!'''
    post_data = {'busList[bus][]': buses}
    r = requests.post(_URL, data=post_data)
    for sample in r.json():
        identity = VehicleIdentity(line=sample['name'], course=sample['k'])
        position = Position(x=sample['x'], y=sample['y'])
        yield identity, position


class TrackedVehicle(NamedTuple):
    seen_at_start: int = None
    seen_at_middle: int = None
    seen_at_stop: int = None


def track_travel_time(line, start, middle, stop):
    db = defaultdict(TrackedVehicle)
    for identity, position in fetch_positions([line]):
        tracked_vehicle = db[identity]


def _parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    watch_parser = subparsers.add_parser('watch', help='watch vehicle\'s position live')
    watch_parser.add_argument('--line', type=int, required=True)

    travel_time_parser = subparsers.add_parser('travel_time', help='watch vehicle\'s travel time between two points')
    travel_time_parser.add_argument('--start', type=str, required=True)
    travel_time_parser.add_argument('--middle', type=str, required=True)
    travel_time_parser.add_argument('--stop', type=str, required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    if args.command == 'watch':
        while True:
            for identity, position in fetch_positions([args.line]):
                print(f'{identity}: {position}')
            time.sleep(1)

    elif args.command == 'travel_time':
        pass
