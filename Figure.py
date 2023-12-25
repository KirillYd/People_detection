from Point import Point as pnt
from shapely.geometry import Point, Polygon


class Figure():
    def __init__(self, array: list):
        self.array = array
        self.polygon = Polygon(self.array)

    # def is_inside_figure(self, point):
    #     for line in self.array:
    #         if not line.is_point_above_line(point):
    #             return False
    #     return True

    def is_inside_figure2(self, point: pnt):
        point = Point(point.x, point.y)
        return self.polygon.contains(point)
