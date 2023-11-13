import cv2
import numpy as np
from CONST import *
from ultralytics import YOLO
import hashlib
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

class Tracker:
    def __init__(self, threshold, age_threshold, show_history=False):
        self.next_id = 0
        self.tracks = []
        self.last_center10 = []
        self.threshold = threshold
        self.age_threshold = age_threshold
        self.model = YOLO(model_path, "v8")
        self.show_history = show_history
        print ("Tracker initialized")

    def get_center(self, bbox):
        x = int(bbox[0] + (bbox[2] - bbox[0]) / 2)
        y = int(bbox[1] + (bbox[3] - bbox[1]) / 2)
        return np.array([x, y], dtype=np.float32)

    def update(self, frame):
        # Without logging
        detections_model = self.model(frame, agnostic_nms=True, verbose=False)[0]
        boxes = detections_model.boxes.data
        scores = detections_model.boxes.conf
        cls = detections_model.boxes.cls
        detections = []
        for i in range(len(boxes)):
            if scores[i] > confThreshold:
                detection = {
                    'bbox': boxes[i],
                    'score': scores[i],
                    'class': cls[i],
                }
                detections.append(detection)

        if len(self.tracks) == 0:
            if len(detections) > 0:
                for detection in detections:
                    if float(detection['score']) > confThreshold:
                        track = {
                            'id': self.next_id,
                            'bbox': detection['bbox'],
                            'class': detection['class'],
                            'score': detection['score'],
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
                    best_match['score'] = detection['score']
                    best_match['class'] = detection['class']
                    

                else:
                    # Create new track
                    track = {
                        'id': self.next_id,
                        'bbox': detection['bbox'],
                        'class': detection['class'],
                        'age': 1,
                        'score': detection['score'],
                    }
                    self.tracks.append(track)
                    self.next_id += 1

            # Remove old tracks
            self.tracks = [t for t in self.tracks if t['age']
                           < self.age_threshold]
            # Add center to last 10
            if len(self.tracks) > 0:
                self.last_center10.append(self.get_center(self.tracks[0]['bbox']))
                if len(self.last_center10) > 10:
                    self.last_center10.pop(0)

        classes_ids = []
        detections_boxes = []
        detections_ids = []
        for track in self.tracks:
            classes_ids.append(track['class'])
            detections_boxes.append(track['bbox'])
            detections_ids.append(track['id'])
        
        if(self.show_history):
            for i in range(len(self.last_center10)):
                color = (int(255 * i / len(self.last_center10)), 0, 0)
                cv2.circle(frame, (int(self.last_center10[i][0]), int(self.last_center10[i][1])), 5, color, -1)

                
        return classes_ids,detections_ids, detections_boxes 