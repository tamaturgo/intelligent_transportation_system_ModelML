import cv2
from CONST import *
from vidgear.gears import CamGear
from Tracker import Tracker
from argparse import ArgumentParser
import numpy as np
import time
from controllers import *

arg = ArgumentParser()
arg.add_argument("-v", "--video", action="store_true", help="Video mode")
arg.add_argument("-s", "--stream", action="store_true", help="Stream mode")
# Select Camera location
arg.add_argument("-c", "--camera", type=int, default=0,
                 help="Camera location: 0 - DownTown, 1 - Arena, 2 - Constantino, 3 - Djalma, 4 - Efigenio")

if arg.parse_args().video:
    SOURCE = 'datasets/videos/batecarroarena.mkv'
elif arg.parse_args().stream:
    SOURCE = 'https://www.youtube.com/watch?v=_3o-_5AIOWs'
else:
    SOURCE = 0

if arg.parse_args().stream:
    stream = CamGear(source=SOURCE,
                     stream_mode=True,
                     logging=LOGGING, **options).start()


tracker = Tracker(threshold=90, age_threshold=5)
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
    frame = camera2

    frame = cv2.resize(frame, (1920 // 2, 1080 // 2)) # 960 x 540
    cv2.imwrite('frame.jpg', frame)

    # save a copy of the frame without draw
    frame_without_draw = frame.copy()

    # Pass the frame to the model
    (classes_id, object_ids, boxes) = tracker.update(frame)

    for (classid, objid, box) in zip(classes_id, object_ids, boxes):
        classes_id = int(classid)
        color = COLORS[classes_id % len(COLORS)]
        label = "%s:%d" % (CLASSES[classes_id], objid)

        # If camera location is Downtown
        if arg.parse_args().camera == 0:
            print
            frame = track_downtown(
                frame, frame_without_draw, objid, box, label, color)
            
        if arg.parse_args().camera == 3:
            frame = track_djalma(
                frame, frame_without_draw, objid, box, label, color)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


cv2.destroyAllWindows()
stream.stop()
