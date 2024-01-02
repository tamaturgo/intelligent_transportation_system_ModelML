import cv2
import numpy as np
from CONST import  model_path, classesFile, confThreshold
from ultralytics import YOLO
from its.AreaService import AreaManager
classes = None

with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')


class DetectionFilter:
    @staticmethod
    def filter_detections(detections_model):
        return [
            {
                'bbox': box,
                'score': score,
                'class': cls
            }
            for box, score, cls in zip(
                detections_model.boxes.data,
                detections_model.boxes.conf,
                detections_model.boxes.cls
            )
            if score > confThreshold
        ]


class TrackManager:
    @staticmethod
    def create_track(next_id, detection):
        return {
            'id': next_id,
            'bbox': detection['bbox'],
            'class': detection['class'],
            'score': detection['score'],
            'age': 1,
        }

    @staticmethod
    def update_tracks_age(tracks):
        for track in tracks:
            track['age'] += 1

    @staticmethod
    def update_existing_tracks(detections, tracks, threshold):
        for detection in detections:
            detection_center = TrackManager.get_center(detection['bbox'])
            best_match = min(
                tracks,
                key=lambda track: np.linalg.norm(
                    detection_center - TrackManager.get_center(track['bbox']))
            )

            if np.linalg.norm(detection_center - TrackManager.get_center(best_match['bbox'])) < threshold:
                best_match.update({
                    'bbox': detection['bbox'],
                    'age': 1,
                    'score': detection['score'],
                    'class': detection['class']
                })
            else:
                new_track = TrackManager.create_track(
                    Tracker.next_id, detection)
                tracks.append(new_track)
                Tracker.next_id += 1

    @staticmethod
    def remove_old_tracks(tracks, age_threshold):
        return [t for t in tracks if t['age'] < age_threshold]

    @staticmethod
    def get_center(bbox):
        x = int(bbox[0] + (bbox[2] - bbox[0]) / 2)
        y = int(bbox[1] + (bbox[3] - bbox[1]) / 2)
        return np.array([x, y], dtype=np.float32)


class Tracker:
    next_id = 0

    def __init__(self, threshold, age_threshold, show_history=False, areas_file="./areas.txt"):
        self.threshold = threshold
        self.age_threshold = age_threshold
        self.model = YOLO(model_path, "v8")
        self.show_history = show_history
        self.areas_manager = AreaManager(areas_file)
        self.tracks = []
        self.last_center10 = []
        print("Tracker initialized")

    def update(self, frame):
        detections_model = self.model(
            frame, agnostic_nms=True, verbose=False)[0]
        detections = DetectionFilter.filter_detections(detections_model)

        if not self.tracks:
            self.initialize_tracks(detections)
        else:
            TrackManager.update_tracks_age(self.tracks)
            TrackManager.update_existing_tracks(
                detections, self.tracks, self.threshold)
            self.tracks = TrackManager.remove_old_tracks(
                self.tracks, self.age_threshold)

        classes_ids, detections_ids, detections_boxes = self.extract_track_info()

        if self.show_history:
            self.draw_history(frame)

        return classes_ids, detections_ids, detections_boxes

    def initialize_tracks(self, detections):
        for detection in detections:
            track = TrackManager.create_track(Tracker.next_id, detection)
            self.tracks.append(track)
            Tracker.next_id += 1

    def extract_track_info(self):
        classes_ids = [track['class'] for track in self.tracks]
        detections_boxes = [track['bbox'] for track in self.tracks]
        detections_ids = [track['id'] for track in self.tracks]
        return classes_ids, detections_ids, detections_boxes

    def draw_history(self, frame):
        for i, center in enumerate(self.last_center10):
            color = (int(255 * i / len(self.last_center10)), 0, 0)
            cv2.circle(frame, (int(center[0]), int(center[1])), 5, color, -1)
