import logging
from typing import NamedTuple
from geopy.distance import geodesic


logger = logging.getLogger(__name__)


class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"{self.x:.3f},{self.y:.3f}"


def same_place(first, second, *, sensitivity=20):
    dist = geodesic(first, second).meters
    print(f'distance between {first} and {second} is {dist}m')
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
