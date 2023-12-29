from Point import Point

class Line():

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def is_point_above_line(self, point):
        v1 = Point(self.point2.x - self.point1.x, self.point2.y - self.point1.y)
        v2 = Point(point.x - self.point1.x, point.y - self.point2.y)
        #cross_product = v1.x * v2.y - v1.y * v2.x
        cross_product = (point.x - self.point1.x) * (self.point2.y - self.point1.y) - (point.y - self.point1.y) * (self.point2.x - self.point1.x)
        if cross_product <= 0:
            return True
        else:
            return False