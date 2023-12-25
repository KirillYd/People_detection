import secrets
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from Point import Point

class TrackableObject:
    point1: Point
    point2: Point
    frame_number: Optional[int]
    id: Any
    classes: list

    def __init__(
            self,
            point1: Point,
            point2: Point,
            frame_number: Optional[int] = None,
            id: Any = None
    ):
        if id is None:
            id = secrets.token_hex(8)
        self.point1 = point1
        self.point2 = point2
        self.frame_number = frame_number
        self.id = id
        self.classes = []

    def get_center(self) -> Point:
        return (self.point1 + self.point2) / 2

    def get_corners(self):
        """
        Returns:
            Список углов рамки вокруг объекта
        """
        return [
            self.point1,
            Point(self.point2.x, self.point1.y),
            self.point2,
            Point(self.point1.x, self.point2.y),
        ]

    def __repr__(self) -> str:
        return f"{self.id} {self.point1}--{self.point2}"