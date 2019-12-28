import argparse
import requests
import time
import datetime
import logging
from typing import NamedTuple
from collections import defaultdict
from types import SimpleNamespace

from geopy.distance import geodesic


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

    @property
    def identity(self):
        return self.side_number


class OpenData:
    _URL = 'https://www.wroclaw.pl/open-data/datastore/dump/17308285-3977-42f7-81b7-fdd168c210a2'

    def __init__(self, lines):
        self._lines = lines

    def __iter__(self):
        r = requests.get(OpenData._URL)
        data = r.text
        for line in data.splitlines()[1:]:  # 1st line is a header
            record = OpenDataRecord(*line.split(','))
            if record.line in self._lines:
                yield record


class MpkRecord(NamedTuple):
    course: int
    line: str
    lat: float
    lon: float
    time: str

    @property
    def identity(self):
        return f'{self.line}[{self.course}]'


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
            yield MpkRecord(course=sample['k'], line=sample['name'], lat=sample['x'], lon=sample['y'], time=datetime.datetime.now())


FEEDS = {'opendata': OpenData, 'mpk': Mpk}