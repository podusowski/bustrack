import logging
from typing import NamedTuple, Any, Iterable
from types import SimpleNamespace
from geopy.distance import geodesic


logger = logging.getLogger(__name__)


class Point(NamedTuple):
    lat: int
    lon: int

    def __repr__(self):
        return f"{self.lat:.3f},{self.lon:.3f}"


class RecordPoint(NamedTuple):
    lat: float
    lon: float
    time: Any


def same_place(first, second, *, sensitivity=20):
    if first is None or second is None:
        return False
    try:
        dist = geodesic(tuple(first), tuple(second)).meters
    except Exception as e:
        raise RuntimeError(f'could not figure out if {first} is in the same place as {second}: {e}') from e
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


class _Segment(_ValueIter):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.record_starting_point = None
        self.record_last_point = None


def extract_segments(record: Iterable[RecordPoint], segments, sensitivity=20):
    '''Extract each found segment in record.'''
    current = _ValueIter(record)
    segments = [_Segment(s) for s in segments]

    while True:
        for segment in segments:
            if segment.value is None:
                yield segment.record_starting_point, segment.record_last_point
                segment.reset()
            elif same_place(segment.value, current.value, sensitivity=sensitivity):
                if segment.record_starting_point is None:
                    segment.record_starting_point = current.value
                segment.record_last_point = current.value
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