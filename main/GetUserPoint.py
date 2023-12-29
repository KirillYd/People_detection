import cv2
from Point import Point
from Line import Line

# Функция обработки событий мыши



class GetUserPoint():
    points: list

    def __init__(self, name):
        self.name = name
        self.image = cv2.imread(name)
        self.points = []

    def mouse_callback(self, event, x, y, *args, **kwargs):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append(Point(x, y))
            cv2.circle(self.image, (x, y), 2, (0, 0, 255), 5)
            cv2.imshow('image', self.image)
            print("Координаты точки: ({}, {})".format(x, y))

    def CreateLines(self):
        lines_list = []
        if len(self.points) == 2:
            print(Exception("Ошибка: Введена 1 точка"))
            return []
        if len(self.points) == 2:
            return [Line(self.points[0], self.points[1])]
        for i in range(len(self.points)):
            if i == len(self.points) - 1:
                lines_list.append(Line(self.points[i], self.points[0]))
            else: lines_list.append(Line(self.points[i], self.points[i + 1]))
        return lines_list

    def call_window(self):
        #cv2.namedWindow('image')

        # Установка обработчика событий мыши
        cv2.namedWindow('image', cv2.WINDOW_KEEPRATIO)
        cv2.setMouseCallback('image', self.mouse_callback)

        # Отображение изображения в окне
        #cv2.imshow('image', self.image)


        cv2.imshow('image', self.image)
        cv2.resizeWindow('image', 1280, 720)

        # Ожидание нажатия клавиши "q" для выхода из программы
        while cv2.waitKey(1) != ord('q'):
            pass

        # Закрытие окна
        cv2.destroyAllWindows()
        return self.points


# user = GetUserPoint('image.jpg')
# x = user.call_window()
# print(len(x))
