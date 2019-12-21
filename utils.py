
import logging
from typing import NamedTuple
from geopy.distance import geodesic


logger = logging.getLogger(__name__)


class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self):
        return f"{self.x:.3f},{self.y:.3f}"


def _same_place(first, second):
    dist = geodesic(first, second).meters
    logger.debug(f'distance between {first} and {second} is {dist}m')
    return dist < 20