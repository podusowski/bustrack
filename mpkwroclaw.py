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
    timestamp: int


def fetch_positions(buses):
    '''Only buses for now!'''
    post_data = {'busList[bus][]': buses}
    r = requests.post(_URL, data=post_data)
    return r.json()


def print_database(db):
    for identity, samples in db.items():
        print(f'{identity}: {len(samples)} samples')


if __name__ == "__main__":
    vehicles = defaultdict(list)
    while True:
        p = fetch_positions([132, 107])
        for sample in p:
            identity = VehicleIdentity(line=sample['name'], course=sample['k'])
            position = Position(x=sample['x'], y=sample['y'], timestamp=0)
            vehicles[identity].append(position)
            #print(vehicles)
        print_database(vehicles)
        time.sleep(1)
