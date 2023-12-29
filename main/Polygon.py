from typing import Any, Dict, List, Optional, Set, Tuple, Union
from Point import Point

class Polygon:
    points: List[Point]

    def __init__(self, points: List[Point]):
        """
        points - список вершин по часовой стреллке
        """
        self.points = points

        self.inf = max(p.x for p in points)

    def area(self) -> float:
        """
        Разбиваем полигон на треугольники и ищем площадь многоугольника как
        сумму площадей треугольника.
        Площадь треугольника считаем по формуле Герона
        """
        S = 0.0
        A = self.points[0]
        for i in range(2, len(self.points)):
            B = self.points[i - 1]
            C = self.points[i]
            lengths = [A.get_distance_to(B), A.get_distance_to(C),
                       B.get_distance_to(C)]
            p = sum(lengths) / 2
            S += (p * (p - lengths[0]) * (p - lengths[1]) * (p - lengths[2])) ** .5
        return S

    def ccw(self, A, B, C):
        return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

    # Return true if line segments AB and CD intersect
    def intersect(self, A, B, C, D):
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)

    def contains(self, point: Point) -> bool:
        result = False
        for i in range(len(self.points) - 1):
            if self.intersect(
                    self.points[i], self.points[i + 1],
                    point, Point(self.inf, point.y)
            ):
                result = not result
        if self.intersect(
                self.points[-1], self.points[0],
                point, Point(self.inf, point.y)
        ):
            result = not result
        return result