import datetime
import logging

import cv2
import dataclasses
from typing import Any, List
import torch
from Point import Point
from TrackableObject import TrackableObject
from CentroidTracker import CentroidTracker
from GetUserPoint import GetUserPoint
from Figure import Figure
from ConfigParser import MyConfigParser
import os


if not os.path.exists("images"):
    os.mkdir("images")


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Model(metaclass=Singleton):
    def __init__(self) -> None:
        self.model = torch.hub.load('ultralytics/yolov5','custom', 'last2.pt')


@dataclasses.dataclass
class State:
    inside: bool
    outside: bool
    was_inside: bool
    was_outside: bool
    reported_no: bool


def get_bounding_box(
        frame: Any,
        frame_count: int,
        yolo_classes: list = [0]
) -> List[TrackableObject]:
    '''
    функция фильтрует боксы и выбирает только нужные классы
    в yolo 0 - это класс Person
    так же убирает метку класса и степень уверности
    остаются только координаты бокса
    '''
    list_of_people = []
    for i in frame.xyxy[0]:
        if len(i) == 0:
            continue

        if i[-1] in yolo_classes:
            list_of_people.append(TrackableObject(
                Point(float(i[0]), float(i[1])),
                Point(float(i[2]), float(i[3])),
                frame_count))
    return list_of_people


video_path = os.getenv("VIDEO_PATH")
logging.info(video_path)

videocap = cv2.VideoCapture(video_path)

model = Model().model
# tracker = CentroidTracker(max_disappeared=200, max_distance=500)

succ, img = videocap.read()

cv2.imwrite("image.jpg", img)

# user = GetUserPoint("image.jpg")
# pointsArr = user.call_window()

config = MyConfigParser('example.ini')
# config.writeCoords(pointsArr, 2)

coords = config.readCoords(2)

fig = Figure(coords)
abc = logging.getLogger()
abc.setLevel(logging.INFO)
#logging.basicConfig(level=logging.INFO ,filename='/output.log', filemode='a', format="%(asctime)s %(levelname)s %(message)s", encoding='UTF-8', datefmt="%Y-%m-%d %H:%M:%S")
textLogging = logging.FileHandler(filename='/main/output.log', mode='a', encoding='UTF-8')
textLogging.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
textLogging.setLevel(logging.INFO)
abc.addHandler(textLogging)

# logging.info('a')

count = 0
frame_number = 0

temp = model(img)
bb = get_bounding_box(temp, 0)
prev_status = True if len(bb) > 0 else False

while succ:
    status = []

    time = datetime.datetime.now()
    temp = model(img)
    bb = get_bounding_box(temp, 0)

    #Отрисовка линий области
    # for i in range(len(coords)):
    #     if i == len(coords) - 1:
    #         cv2.line(img, (coords[i][0], coords[i][1]), (coords[0][0], coords[0][1]), (0, 0, 255), 3, 1)
    #     else:
    #         cv2.line(img, (coords[i][0], coords[i][1]), (coords[i+1][0], coords[i+1][1]), (0, 0, 255), 3, 1)

    # Display the resulting frame
    if len(bb) > 0:
        for i in bb:
            cv2.rectangle(img, (round(i.point1.x), round(i.point1.y)), (round(i.point2.x), round(i.point2.y)), (255, 0 ,0), 2, 1)
            status.append(fig.is_inside_figure2(i.get_center()))

    if status.count(False) == len(status):
        count += 1
    else:
        count = 0

    if True in status and prev_status:
        logging.info('На объекте присутствуют люди')
        print('На объекте присутствуют люди')
        prev_status = False
    elif status.count(False) == len(status) and not prev_status and count > 10:
        logging.info('Людей на объекте нет')
        print('Людей на объекте нет')
        prev_status = True

    # for i in range(len(status)):
    #     if prev_status[i] != status[i]:
    #         if status == True:
    #             logging.info('Человек вошел')
    #         else: logging.info('Человек вышел')

    size = cv2.resize(img, (1280, 720))

    if frame_number % 30 == 0:
        cv2.imwrite('images/{}.jpg'.format(time.strftime("%Y-%m-%d %H%M%S")), size)

    #cv2.imshow('image', size)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_number += 1
    succ, img = videocap.read()

videocap.release()
cv2.destroyAllWindows()

