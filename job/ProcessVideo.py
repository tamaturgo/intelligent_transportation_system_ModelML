import os
import cv2
import re
import threading
import time
from CONST import CLASSES, COLORS
from Tracker import Tracker
from job.rulerManager import RulerManager

class VideoProcessor:
    def __init__(self):
        self.processed_video = []
        self.processing_video = []
        self.to_process_video = []
        self.queued_video = []
        self.workers_queue = []
        self.worker_list = []
        self.worker_limit = 3

    def check_video_dir(self):
        if not os.path.exists("videos"):
            os.makedirs("videos")
        if not os.path.exists("videos/processed"):
            os.makedirs("videos/processed")

        # check if there is any video to process
        for file in os.listdir("videos"):
            if file not in self.processed_video and file not in self.processing_video and file not in self.to_process_video and file not in self.queued_video:
                regex_file_with_ext = r"(.*)\.(.*)"
                if re.match(regex_file_with_ext, file):
                    self.to_process_video.append(file)
                    print(f"Added {file} to process list")
            else:
                print(f"File {file} already processed or processing")
    def process_frame(self, frame, tracker:Tracker, ruler: RulerManager):


        # Resize frame 720px 360px
        frame = cv2.resize(frame, (720, 360))


        (classes_id, object_ids, boxes) = tracker.update(frame)

        frame = ruler.update(frame, object_ids, boxes)

        for (classid, objid, box) in zip(classes_id, object_ids, boxes):
            classes_id = int(classid)
            color = COLORS[classes_id % len(COLORS)]
            label = "{}:{}".format(CLASSES[classes_id], objid)

            startX = int(box[0])
            startY = int(box[1])
            endX = int(box[2])
            endY = int(box[3])
            center_x, center_y = int((startX + endX) / 2), int((startY + endY) / 2)
            # Draw rectangle
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            # Draw label
            cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            # Draw center point
            cv2.circle(frame, (center_x, center_y), 2, color, 2)

        return frame

    def process_video(self, video_name):
        ObjectTracker = Tracker(60, 15)
        ObjectRuler = RulerManager()

        start = time.time()
        self.processing_video.append(video_name)
        self.queued_video.remove(video_name)
        video = cv2.VideoCapture(f"videos/{video_name}")
        size = (720, 360)

        # Use temporary filename
        re_without_ext = r"(.*)\.(.*)"
        video_name_without_ext = re.match(re_without_ext, video_name).group(1)
        temp_filename = f"videos/output/{video_name_without_ext}.mp4"
        target_fps = 15
        out = cv2.VideoWriter(temp_filename, cv2.VideoWriter_fourcc(*'mp4v'), target_fps, size)
        current_frame = 0
        skip_rate_to_read = 5

        while True:
            current_frame += 1
            ret, frame = video.read()
            if not ret:
                break
            if current_frame % skip_rate_to_read != 0:
                continue

            processed_frame = self.process_frame(frame, ObjectTracker, ObjectRuler)
            out.write(processed_frame)

        video.release()
        out.release()
        self.processed_video.append(video_name)
        self.processing_video.remove(video_name)

        print(f"Processing time: {time.time() - start}")
        time.sleep(0.5)
        self.move_processed_video(video_name)
        print(f"Video {video_name} processed")
        self.worker_list.remove(threading.current_thread())

    def move_processed_video(self, video_name):
        try:
            os.rename(f"videos/{video_name}", f"videos/processed/{video_name}")
        except:
            print(f"Error moving video {video_name}")

    def run_worker_queue(self):
        if len(self.workers_queue) > 0:
            if len(self.worker_list) < self.worker_limit:
                self.worker_list.append(self.workers_queue.pop(0))
                self.worker = self.worker_list[-1]
                self.worker.start()
            else:
                time.sleep(1)
                self.run_worker_queue()

        # Clear worker that is stopped
        for worker in self.worker_list:
            if not worker.is_alive():
                self.worker_list.remove(worker)

            

    def start_job(self):
        # check if there is any video to process
        self.check_video_dir()
        print(f"Videos to process: {self.to_process_video}")
        print(f"Videos queued: {self.queued_video}")
        print(f"Videos processing: {self.processing_video}")
        print(f"Videos processed: {self.processed_video}")

        # check if there is any video to process
        while len(self.to_process_video) > 0:
            video_name = self.to_process_video.pop(0)
            self.process_video_thread(video_name)

        time.sleep(5)
        # Start processing videos
        self.run_worker_queue()
        self.start_job()

    def process_video_thread(self, video_name):
        print(f"Scheduling video {video_name} to process")
        self.queued_video.append(video_name)
        video_process = threading.Thread(target=self.process_video, args=(video_name,))
        self.workers_queue.append(video_process)
        print ("----------------------")
        print (f"Workers queue: {len(self.workers_queue)}")
        print (f"Workers list: {len(self.worker_list)}")