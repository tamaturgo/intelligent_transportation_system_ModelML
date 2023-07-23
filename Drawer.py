import cv2
from CONST import *

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')


class Drawer:
    def __init__(self, frame):
        self.frame = frame

    def draw_centroids(self, center):
        radius = 2
        cv2.circle(
            self.frame, (int(center[0]), center[1]), radius, (0, 255, 0), -1)

    def draw_polygons(self, polygons):
        for polygon in polygons:
            cv2.polylines(self.frame, [polygon], True, (0, 255, 255), 1)

        return self.frame
