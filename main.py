import cv2
from CONST import *
from vidgear.gears import CamGear
from Tracker import Tracker
from argparse import ArgumentParser
import numpy as np
import time

arg = ArgumentParser()
arg.add_argument("-v", "--video", action="store_true", help="Video mode")
arg.add_argument("-s", "--stream", action="store_true", help="Stream mode")

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

# Auxiliar variables
vehicle_at_central_area = {}
vehicle_at_central_area_time = {}

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


    # North america video
    central_area = [(200, 590), (1000, 515),
                    (1300, 655), (350, 800)]  # 1920x1080
    central_area = [(int(x / 2), int(y / 2)) for x, y in central_area]

    pista_1 = [(120, 320), (380, 320), (620, 480), (250, 520)] # 1920x1080
    pista_1 = [(int(x / 2), int(y / 2)) for x, y in pista_1]

    # Redimensiona o frame
    camera1 = frame[0:height, 0:width]  # Constantino
    camera2 = frame[0:height, width:width * 2]  # Djalma
    camera3 = frame[height:height * 2, 0:width]  # Efigenio
    camera4 = frame[height:height * 2, width:width * 2]  # Arena
    frame = camera4

    frame = cv2.resize(frame, (1920 // 2, 1080 // 2))

    # save a copy of the frame without draw
    frame_without_draw = frame.copy()

    # Pass the frame to the model
    (classes_id, object_ids, boxes) = tracker.update(frame)


    for (classid, objid, box) in zip(classes_id, object_ids, boxes):
        classes_id = int(classid)
        color = COLORS[classes_id % len(COLORS)]
        label = "%s:%d" % (CLASSES[classes_id], objid)
        startX = int(box[0])
        startY = int(box[1])
        endX = int(box[2])
        endY = int(box[3])

        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 1)
        cv2.rectangle(frame, (startX, startY), (endX, startY - 10), color, -1)
        cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        center_x = int((startX + endX) / 2)
        center_y = int((startY + endY) / 2)


    #     contact = cv2.pointPolygonTest(np.array(central_area, np.int32), (center_x, center_y), False)
    #     if contact >= 0:
    #         if objid not in vehicle_at_central_area:
    #             vehicle_at_central_area[objid] = time.time()

    #     if objid in vehicle_at_central_area:
    #         contact = cv2.pointPolygonTest(np.array(central_area, np.int32), (center_x, center_y), False)
    #         elepsed_time = time.time() - vehicle_at_central_area[objid]
    #         print("Elepsed time: ", elepsed_time)

    #         if contact >= 0:
    #             vehicle_at_central_area_time[objid] = elepsed_time

    #         cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
    #         cv2.rectangle(frame, (startX, startY), (endX, startY - 15), color, -1)
    #         cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    #         cv2.putText(frame, 'E.T: %.2f' % vehicle_at_central_area_time[objid], (startX, startY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    #         # Alerta de tempo
    #         if elepsed_time > 30:
    #             with open('alerta.txt', 'a') as f:
    #                 hash_para_imagem = str(hash(frame.tostring()))
    #                 cv2.imwrite('alerta/%s.jpg' % hash_para_imagem, frame_without_draw)
    #                 f.write("### ALERTA DE TEMPO\n")
    #                 f.write('### VEICULO %d ESTA A MAIS DE 30 SEGUNDOS NA AREA CENTRAL\n' % objid)
    #                 f.write('### TEMPO: %.2f\n' % elepsed_time)
    #                 f.write('### DATA: %s\n' % time.strftime("%d/%m/%Y %H:%M:%S"))
    #                 f.write('### IMAGEM: %s.jpg\n' % hash_para_imagem)
    #                 f.write('###\n\n')

    # for i, area in enumerate([central_area]):
    #     if i == 0:
    #         cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 0, 255), 2)
    #     else:
    #         cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 0), 2)





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
