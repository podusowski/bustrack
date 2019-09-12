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
    for sample in r.json():
        identity = VehicleIdentity(line=sample['name'], course=sample['k'])
        position = Position(x=sample['x'], y=sample['y'], timestamp=int(time.time()))
        yield identity, position


if __name__ == "__main__":
    while True:
        for identity, position in fetch_positions([132, 107]):
            print(f'{identity}: {position}')
        time.sleep(1)
