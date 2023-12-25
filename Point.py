import sys
from typing import Tuple, Optional, Union

Number = Union[int, float]
class Point:
    x: Number
    y: Number

    def __init__(self, x: Number, y: Number):
        self.x = x
        self.y = y

    def to_pair(self) -> Tuple[Number, Number]:
        return self.x, self.y

    def get_distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def get_nearest_point(self, *args: 'TrackableObject') -> Tuple[Optional['TrackableObject'], Number]:
        result = None
        min = sys.maxsize
        for obj in args:
            distance = self.get_distance_to(obj.get_center())
            if distance < min:
                min = distance
                result = obj
        return (result, min)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __truediv__(self, x: Number):
        return Point(self.x / x, self.y / x)

    def cross_product(self, other: 'Point') -> float:
        return self.x * other.y - self.y + other.x

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'