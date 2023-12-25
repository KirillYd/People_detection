from collections import OrderedDict

class CentroidTracker:
    # id который мы присвоим следующему появившемуся в кадре объекту
    next_id: int

    # максимум кадров которых объекта не должно быть выидно
    # чтобы считалось что он покинул область видимости
    max_disappeared: int

    # максимальная допустимая дистанция перемещения объекта за 1 кадр
    # если расстояние между центрами больше этого значения
    # считаем что появился новый объект, а не продолжает двигаться старый
    max_distance: int

    # ключи в словарях - id объекта

    # словарь со всеми отслеживаемыми объектами на данный момент

    # словарь с историей движения объекта по пикселям
    tracks: OrderedDict

    # словарь в котором для каждого объекта считается есть ли он в кадре
    # если его нет self.disappeared[id] += 1
    # если self.disappeared[id] > self.max_disappeared
    # то считаем что объект ушел и удаляем из self.objects
    # но в self.tracks история движеня объекта сохраняется
    disappeared: OrderedDict

    def __init__(self, max_disappeared=50, max_distance=50):
        self.next_id = 0
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance

        self.objects = dict()
        self.tracks = dict()
        self.disappeared = dict()

    def add_object(self, centroid):
        """
        обнаружен новый объект
        """
        self.objects[self.next_id] = centroid
        self.objects[self.next_id].id = self.next_id
        self.tracks[self.next_id] = []
        self.disappeared[self.next_id] = 0
        self.next_id += 1

    def remove_object(self, id):
        '''
        объект ушел из кадра дольше чем на self.max_disappeared
        '''
        del self.objects[id]
        del self.disappeared[id]

    def remove_small_tracks(self, accept_length: int):
        '''
        функция удаляет все треки меньше заданного значения из истории
        self.tracks

        полезно в случаях когда случайно пиксели отрываются от трека в отдельный
        '''
        res = OrderedDict()
        for track_id in self.tracks.keys():
            if len(self.tracks[track_id]) > accept_length:
                res[track_id] = self.tracks[track_id]
        self.tracks = res

    def track(self, frame):

        '''
        функция отслеживает объекты на кадре
        на вход подается следующий кадр видео
        :return: словарь объектов в поле зрения на текущий момент
        '''

        # копируем кадр и объекты чтобы понять изменились ли объекты после работы функции
        current_frame = frame.copy()
        current_objects = self.objects.copy()
        # centers = {i.get_center(): i for i in frame}

        # TODO протестировать
        # если нет объектов на кадре - добавляем self.disappeared[id] +1
        # для каждого отслеживаемого сейчас объекта
        # пропускаем кадр
        if len(frame) == 0:
            for obj in list(self.disappeared.keys()):
                self.disappeared[obj] += 1
                if self.disappeared[obj] > self.max_disappeared:
                    self.remove_object(obj)
            return self.objects

        # если это первый кадр с объектами, добавляем все объекты
        if len(self.objects.keys()) == 0:
            for obj in frame:
                self.add_object(obj)
        else:
            for obj_id, obj in self.objects.items():
                # вычисляем ближайшую точку из нового кадра для каждого объекта
                nearest_point = obj \
                    .get_center() \
                    .get_nearest_point(*frame)
                # если точка далеко то пропускаем её
                if nearest_point[1] > self.max_distance:
                    continue

                # иначе меняем у текушего объекта координаты и обнуляем disappeared
                # удаляем из текущего кадра просмотренную точку
                self.tracks[obj_id].append(obj)
                self.objects[obj_id] = nearest_point[0]
                self.disappeared[obj_id] = 0
                if nearest_point[0] in current_frame:
                    current_frame.remove(nearest_point[0])

            # если остались точки созадем новые объекты
            if len(current_frame) > 0:
                for obj in current_frame:
                    self.add_object(obj)

            # если объект не изменялся self.disappeared[id] += 1
            # если объекта нет в кадре max_disappeared кадров то удаляем его
            for id in current_objects:
                if id in self.objects.keys() and self.objects[id] == current_objects[id]:
                    self.disappeared[id] += 1
                    if self.disappeared[id] > self.max_disappeared:
                        self.remove_object(id)

        return self.objects