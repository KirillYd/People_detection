import datetime

from Line import Line
from Point import Point

# point1 = Point(1011, 420)
# point2 = Point(903, 4)
# line = Line(point1, point2)
# testpoint1 = Point(989, 84)
# testpoint2 = Point(900, 280)
# print(line.is_point_above_line(testpoint2), )

from shapely.geometry import Point, Polygon

# Задаем координаты вершин многоугольника
polygon = Polygon([(100, 0), (200, 0), (200, 200), (0, 200), (0,100), (100, 100)])

# Задаем координаты точки
point = Point(100, 100)

# Проверяем, находится ли точка внутри многоугольника
if polygon.contains(point):
    print("Точка находится внутри многоугольника.")
else:
    print("Точка находится вне многоугольника.")

now = datetime.datetime.now()

print(now.strftime("%Y-%m-%d %H%M%S"))

# import configparser
# import json
#
# config = configparser.ConfigParser()
# print("{}".format([1, 2, 3, 4]))
#
# config.add_section('Settings')
# config.set('Settings', 'username', "{}".format([1, 2, 3, 4]))
#
# with open('example.ini', 'w') as configfile:
#     config.write(configfile)


# config['forge.example'] = {}
# config['forge.example']['User'] = 'hg'
# config['topsecret.server.example'] = {}
# topsecret = config['topsecret.server.example']
# topsecret['Port'] = '50022'     # mutates the parser
# topsecret['ForwardX11'] = 'no'  # same here
# config['DEFAULT']['ForwardX11'] = 'yes'

# config = configparser.ConfigParser()
# config.read('example.ini')
#
# # Reading the list using JSON
# fibonacci_list = json.loads(config.get("Foo", "fibs"))[0]
#
# print(fibonacci_list)