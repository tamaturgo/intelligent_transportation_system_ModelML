import cv2
import numpy as np
from CONST import *
from ultralytics import YOLO

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

class Tracker:
    def __init__(self, threshold, age_threshold):
        self.next_id = 0
        self.tracks = []
        self.threshold = threshold
        self.age_threshold = age_threshold
        self.model = YOLO(model_path, "v8")

    def get_center(self, bbox):
        x = int(bbox[0] + (bbox[2] - bbox[0]) / 2)
        y = int(bbox[1] + (bbox[3] - bbox[1]) / 2)
        return np.array([x, y], dtype=np.float32)

    def update(self, frame):
        detections_model = self.model(frame, agnostic_nms=True)[0]
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

        classes_ids = []
        detections_boxes = []
        detections_ids = []
        for track in self.tracks:
            classes_ids.append(track['class'])
            detections_boxes.append(track['bbox'])
            detections_ids.append(track['id'])
        
        return classes_ids,detections_ids, detections_boxes 