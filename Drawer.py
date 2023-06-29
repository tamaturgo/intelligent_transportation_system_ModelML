import cv2
from SETTINGSNEW import *

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')


class Drawer:
    def __init__(self, frame):
        self.frame = frame

    def draw_boxes(self, boxes, scores, cls):
        # Draw bounding boxes and labels of detections
        for i in range(len(boxes)):
            if scores[i] > confThreshold:

                box = boxes[i]
                score = scores[i]
                label = classes[int(cls[i])]
                selected_color = color_palette[int(cls[i])]

                # Convert box coordinates to x, y, w, h
                x = int(box[0])
                y = int(box[1])
                w = int(box[2] - box[0])
                h = int(box[3] - box[1])
                cv2.rectangle(self.frame, (x, y), (x + w, y + h),
                              selected_color, 1)
                label = '%s %.2f' % (label, score)

                cv2.putText(self.frame, label, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, selected_color, 1)

        return self.frame

    def draw_polygons(self, polygons):
        for polygon in polygons:
            cv2.polylines(self.frame, [polygon], True, (0, 255, 255), 1)
       
        return self.frame