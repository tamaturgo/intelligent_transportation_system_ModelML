import cv2
from CONST import *
from vidgear.gears import CamGear
from Tracker import Tracker
from argparse import ArgumentParser
import numpy as np

arg = ArgumentParser()
arg.add_argument("-v", "--video", action="store_true", help="Video mode")
arg.add_argument("-s", "--stream", action="store_true", help="Stream mode")

if arg.parse_args().video:
    SOURCE = 'datasets/videos/batecarro.mp4'
elif arg.parse_args().stream:
    SOURCE = 'https://www.youtube.com/watch?v=_3o-_5AIOWs'
else:
    SOURCE = 0

if arg.parse_args().stream:
    stream = CamGear(source=SOURCE,
                     stream_mode=True,
                     logging=LOGGING, **options).start()

tracker = Tracker(threshold=70, age_threshold=15)
count_frame = 0
cap = cv2.VideoCapture(SOURCE)
while True:
    count_frame += 1

    if arg.parse_args().stream:
        frame = stream.read()
    else:
        _, frame = cap.read()
    if count_frame % skip_rate != 0:
        continue

    # Divide o frame em 4 partes
    width = int(frame.shape[1] / 2)
    height = int(frame.shape[0] / 2)

    # Redimensiona o frame
    camera1 = frame[0:height, 0:width]  # Constantino
    camera2 = frame[0:height, width:width * 2]  # Djalma
    camera3 = frame[height:height * 2, 0:width]  # Efigenio
    camera4 = frame[height:height * 2, width:width * 2]  # Arena
    # frame = camera2

    frame = cv2.resize(frame, (1920 // 2, 1080 // 2))


    # Pass the frame to the model
    (classes_id, object_ids, boxes) = tracker.update(frame)


    for (classid, objid, box) in zip(classes_id, object_ids, boxes):
        classes_id = int(classid)
        print (classes_id, objid, box)
        color = COLORS[classes_id % len(COLORS)]
        label = "%s:%d" % (CLASSES[classes_id], objid)
        startX = int(box[0])
        startY = int(box[1])
        endX = int(box[2])
        endY = int(box[3])

        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, startY - 15), color, -1)
        cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # North america video
    central_area = [(200, 590), (1000, 515),
                    (1300, 655), (350, 800)]  # 1920x1080
    central_area = [(int(x / 2), int(y / 2)) for x, y in central_area]

    pista_1 = [(120, 320), (380, 320), (620, 480), (250, 520)] # 1920x1080
    pista_1 = [(int(x / 2), int(y / 2)) for x, y in pista_1]

    for i, area in enumerate([central_area, pista_1]):
        if i == 0:
            cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 0, 255), 2)
        else:
            cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 0), 2)





    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


cv2.destroyAllWindows()
stream.stop()


def process_frame(frame):
    count_frame += 1
    if count_frame % skip_rate != 0:
        return
    frame = cv2.resize(frame, (640, 480))
    results = model(frame, agnostic_nms=True)[0]
    frame = tracker.update(results, frame)
    return frame
