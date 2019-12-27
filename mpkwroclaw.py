import argparse
import requests
import time
import datetime
import logging
from typing import NamedTuple
from collections import defaultdict
from types import SimpleNamespace

from geopy.distance import geodesic
from utils import Position


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class VehicleIdentity(NamedTuple):
    line: int
    course: int

    def __repr__(self):
        return f"{self.line}/{self.course}"


class OpenDataRecord(NamedTuple):
    id: int
    side_number: int
    licence_plate_number: int
    brigade: int
    line: str
    lat: float
    lon: float
    time: str


class OpenData:
    _URL = 'https://www.wroclaw.pl/open-data/datastore/dump/17308285-3977-42f7-81b7-fdd168c210a2'

    def __iter__(self):
        r = requests.get(OpenData._URL)
        print(r.text)
        data = r.text
        for line in data.splitlines()[1:]:  # 1st line is a header
            record = OpenDataRecord(*line.split(','))
            if record.line != 'None':
                yield record


class Mpk:
    _URL = 'http://mpk.wroc.pl/position.php'

    def __init__(self, buses):
        '''Only buses for now!'''
        self._lines = buses

    def __iter__(self):
        logger.debug(f'fetching positions of {self._lines}')
        post_data = {'busList[bus][]': self._lines}
        r = requests.post(Mpk._URL, data=post_data)
        for sample in r.json():
            identity = VehicleIdentity(line=sample['name'], course=sample['k'])
            position = Position(x=sample['x'], y=sample['y'])
            yield identity, position


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
