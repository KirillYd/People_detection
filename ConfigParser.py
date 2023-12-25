import configparser
import os
import ast


class MyConfigParser(object):
    def __init__(self, path):
        self.config = configparser.ConfigParser()
        if os.path.exists(path):
            self.config.read(path)

    def writeCoords(self, coords: list, cam_id: int):
        coords = [(point.x, point.y) for point in coords]
        if not self.config.has_section('AREA'):
            self.config.add_section('AREA')
        self.config.set('AREA', "coords{}".format(cam_id), '{}'.format(coords))

        with open('example.ini', 'w') as configfile:
            self.config.write(configfile)

    def readCoords(self, cam_id: int):
        return ast.literal_eval(self.config.get("AREA", "coords{}".format(cam_id)))





