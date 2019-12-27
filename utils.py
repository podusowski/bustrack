import logging
from typing import NamedTuple
from types import SimpleNamespace
from geopy.distance import geodesic


logger = logging.getLogger(__name__)


class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"{self.x:.3f},{self.y:.3f}"


def same_place(first, second, *, sensitivity=20):
    if first is None or second is None:
        return False
    try:
        dist = geodesic(first, second).meters
    except Exception as e:
        raise RuntimeError(f'could not figure out if {first} is in the same place as {second}') from e
    return dist <= sensitivity


def contains_segment(route, segment, *, sensitivity=20):
    '''Checks if vehicle's route passed trough a given segment.'''
    route = iter(route)
    segment = iter(segment)

    route_point = next(route, None)
    segment_point = next(segment, None)

    while True:
        if route_point is None and segment_point is not None:
            # route has ended before the segment
            return False

        if same_place(route_point, segment_point, sensitivity=sensitivity):
            segment_point = next(segment, None)

        route_point = next(route, None)

        if segment_point is None:
            # this means that we have passed all segment's point
            # and matched them with the route
            return True


class _ValueIter:
    def __init__(self, iterable):
        self.iterable = iterable
        self.reset()

    def advance(self):
        self.value = next(self._iter, None)

    def reset(self):
        self._iter = iter(self.iterable)
        self.advance()


def extract_segments(record, segments, sensitivity=20):
    '''Extract each found segment in the record.'''
    current = _ValueIter(record)
    segments = [_ValueIter(s) for s in segments]

    while True:
        for segment in segments:
            if segment.value is None:
                yield segment.iterable
                segment.reset()
            elif same_place(segment.value, current.value, sensitivity=sensitivity):
                segment.advance()

        if current.value is None:
            return
        current.advance()


def parse_ecsv(iterable):
    '''Parse extended CSV.'''
    fmt = None
    for line in iterable:
        if len(line) == 0 or line.startswith('#'):
            continue
        elif line.startswith('$'):
            fmt = line[1:].strip().split(';')
            print(f'new format: {fmt}')
        elif fmt is not None:
            data = line.strip().split(';')
            yield SimpleNamespace(**dict(zip(fmt, data)))