import argparse
import requests
import time
import datetime
import logging
from typing import NamedTuple
from collections import defaultdict
from types import SimpleNamespace

from geopy.distance import geodesic


_URL = 'http://mpk.wroc.pl/position.php'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class VehicleIdentity(NamedTuple):
    line: int
    course: int

    def __repr__(self):
        return f"{self.line}/{self.course}"


class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"{self.x:.3f},{self.y:.3f}"


def fetch_positions(buses):
    '''Only buses for now!'''
    logger.debug(f'fetching positions of {buses}')
    post_data = {'busList[bus][]': buses}
    r = requests.post(_URL, data=post_data)
    for sample in r.json():
        identity = VehicleIdentity(line=sample['name'], course=sample['k'])
        position = Position(x=sample['x'], y=sample['y'])
        yield identity, position


def _same_place(first, second):
    dist = geodesic(first, second).meters
    logger.debug(f'distance between {first} and {second} is {dist}m')
    return dist < 20


def _display_tavel_time_db(db, start, stop):
    for identity, vehicle in db.items():
        print(f"{identity} {vehicle.position}, {_distance(vehicle.position, start)}m to start, {_distance(vehicle.position, stop)}m to stop")
        if (vehicle.seen_at_start is None): 
            print(f"{_distance(vehicle.position, start)}m to start")
        else:
            print(f"seen at start at: {vehicle.seen_at_start}, {_distance(vehicle.position, stop)}m to stop")
        print("")


def _distance(a, b):
    return int(geodesic(a, b).meters)


def track_travel_time(line, start, stop):
    logger.debug(f'tracking {line}')
    db = defaultdict(lambda: SimpleNamespace(seen_at_start=None, travel_times=[]))
    while True:
        for identity, position in fetch_positions([line]):
            logger.debug(f"{identity} is {_distance(position, start)}m far from start and {_distance(position, stop)}m from stop")
            tracked_vehicle = db[identity]
            tracked_vehicle.position = position
            if _same_place(position, start):
                logger.debug(f'{identity} is at starting point')
                tracked_vehicle.seen_at_start = datetime.datetime.now()
            elif _same_place(position, stop):
                logger.debug(f'{identity} got to the end')
                tracked_vehicle.seen_at_start = None
                tracked_vehicle.travel_times.append(datetime.datetime.now() - tracked_vehicle.seen_at_start)
        _display_tavel_time_db(db, start, stop)
        time.sleep(1)


def _parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command', required=True)

    watch_parser = subparsers.add_parser('watch', help='watch vehicle\'s position live')
    watch_parser.add_argument('--line', type=int, required=True)

    travel_time_parser = subparsers.add_parser('travel_time', help='watch vehicle\'s travel time between two points')
    travel_time_parser.add_argument('--line', type=int, required=True)
    travel_time_parser.add_argument('--start', type=str, required=True)
    travel_time_parser.add_argument('--stop', type=str, required=True)

    return parser.parse_args()


def _decode_coords(s):
    '''Transforms string like '51.106425, 16.950267' into tuple of floats.'''
    return tuple(float(x) for x in s.split(','))


if __name__ == "__main__":
    args = _parse_args()

    if args.command == 'watch':
        while True:
            for identity, position in fetch_positions([args.line]):
                print(f'{identity}: {position}')
            time.sleep(1)

    elif args.command == 'travel_time':
        start = _decode_coords(args.start)
        stop = _decode_coords(args.stop)

        print(start, stop)
        track_travel_time(args.line, start, stop)
