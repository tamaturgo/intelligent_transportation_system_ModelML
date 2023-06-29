import cv2
from SETTINGSNEW import *
from ultralytics import YOLO
from vidgear.gears import CamGear
from Tracker import Tracker

stream = CamGear(source=SOURCE,
                 stream_mode=True,
                 logging=LOGGING, **options).start()

model = YOLO(model_path, "v8")
tracker = Tracker(threshold=40, age_threshold=10)
count_frame = 0
skip_rate = 30


    


while True:
    count_frame += 1
    if count_frame % skip_rate != 0:
        continue
    frame = stream.read()

    # Resize frame
    frame = cv2.resize(frame, (640, 480))


    # Pass the frame to the model
    results = model(frame, agnostic_nms=True)[0]
    frame = tracker.update(results, frame)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(25) & 0xFF
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