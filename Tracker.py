import cv2
import numpy as np
from SETTINGSNEW import *
import time 
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

class Tracker:
    def __init__(self, threshold, age_threshold):
        self.next_id = 0
        self.tracks = []
        self.frame = None
        self.threshold = threshold
        self.age_threshold = age_threshold

    def get_center(self, bbox):
        x = int(bbox[0] + (bbox[2] - bbox[0]) / 2)
        y = int(bbox[1] + (bbox[3] - bbox[1]) / 2)
        return np.array([x, y], dtype=np.float32)

    def update(self, detections_model, frame):
        self.frame = frame
        boxes = detections_model.boxes.data
        scores = detections_model.boxes.conf
        cls = detections_model.boxes.cls

        detections = []
        for i in range(len(boxes)):
            if scores[i] > confThreshold:
                box = boxes[i]
                score = scores[i]
                label = classes[int(cls[i])]
                detection = {
                    'bbox': box,
                    'score': score,
                    'class': label,
                }
                detections.append(detection)


        if len(self.tracks) == 0:
            if len(detections) > 0:
                for detection in detections:
                    print("DEBUG DETECTION: ", detection)
                    if float(detection['score']) > confThreshold:
                        track = {
                            'id': self.next_id,
                            'bbox': detection['bbox'],
                            'class': detection['class'],
                            'age': 1,
                        }
                        self.tracks.append(track)
                        self.next_id += 1
        else:
            for track in self.tracks:
                track['age'] += 1

            for detection in detections:
                detection_center = self.get_center(detection['bbox'])
                best_match = None
                best_distance = float('inf')

                for track in self.tracks:
                    track_center = self.get_center(track['bbox'])
                    distance = np.linalg.norm(detection_center - track_center)
                    if distance < best_distance:
                        best_distance = distance
                        best_match = track

                if best_distance < self.threshold:
                    best_match['bbox'] = detection['bbox']
                    best_match['age'] = 1

                else:
                    # Create new track
                    track = {
                        'id': self.next_id,
                        'bbox': detection['bbox'],
                        'class': detection['class'],
                        'age': 1,
                    }
                    self.tracks.append(track)
                    self.next_id += 1

            # Remove old tracks
            self.tracks = [t for t in self.tracks if t['age']
                           < self.age_threshold]

        # Draw tracks
        for track in self.tracks:
            x1 = int(track['bbox'][0])
            y1 = int(track['bbox'][1])
            x2 = int(track['bbox'][2])
            y2 = int(track['bbox'][3])
            cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
            cv2.putText(self.frame, str(track['id']) + ' - ' + track['class'],
                        (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        return self.frame
