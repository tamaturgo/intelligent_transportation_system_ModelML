
import os
import cv2
import numpy as np
import pandas as pd
import threading
import time
from CONST import CLASSES, COLORS
from Tracker import Tracker
import re
from moviepy.editor import VideoFileClip

worker = None
workers_queue = []

processed_video = []
processing_video = []
to_process_video = []

ObjectTracker = Tracker(60, 15)

def check_video_dir():
    if not os.path.exists("videos"):
        os.makedirs("videos")
    if not os.path.exists("videos/processed"):
        os.makedirs("videos/processed")
    
    # check if there is any video to process
    for file in os.listdir("videos"):
        if file not in processed_video and file not in processing_video and file not in to_process_video:
            regex_file_with_ext = r"(.*)\.(.*)"
            if re.match(regex_file_with_ext, file):
                to_process_video.append(file)
                print(f"Added {file} to process list")
    
def process_video_thread(video_name):
    print(f"Processing {video_name}")
    processing_video.append(video_name)
    # load video
    if not os.path.exists(f"videos/{video_name}"):
        print(f"Video {video_name} not found")
        return    
    video_process = threading.Thread(target=process_video_function, args=(video_name,))
    workers_queue.append(video_process)

def process_video_function(video_name):
    global worker
    start = time.time()
    video = cv2.VideoCapture(f"videos/{video_name}")
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)

     # Use temporary filename
    re_withou_ext = r"(.*)\.(.*)"
    video_name_without_ext = re.match(re_withou_ext, video_name).group(1)
    temp_filename = f"videos/output/{video_name_without_ext}.mp4"
    target_fps = 15
    out = cv2.VideoWriter(temp_filename, cv2.VideoWriter_fourcc(*'mp4v'), target_fps, size)
    current_frame = 0
    skip_rate_to_read = 3

    while video.isOpened():
        current_frame += 1
        ret, frame = video.read()
        if not ret:
            break
        if current_frame % skip_rate_to_read != 0:
            continue
        
        (classes_id, object_ids, boxes) = ObjectTracker.update(frame)
        print ("Detected: ", len(boxes))
        for (classid, objid, box) in zip(classes_id, object_ids, boxes):
            classes_id = int(classid)
            color = COLORS[classes_id % len(COLORS)]
            label = "{}:{}".format(CLASSES[classes_id], objid)

            startX = int(box[0])
            startY = int(box[1])
            endX = int(box[2])
            endY = int(box[3])
            center_x = int((startX + endX) / 2)
            center_y = int((startY + endY) / 2)

            # Draw rectangle
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            # Draw label
            cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            # Draw center point
            cv2.circle(frame, (center_x, center_y), 2, color, 2)
        
        out.write(frame)
    video.release()
    out.release()
    processed_video.append(video_name)
    processing_video.remove(video_name)

    #move_processed_video(video_name)
    print (f"Processing time: {time.time() - start}")
    time.sleep(0.5)
    move_processed_video(video_name)
    worker = None

    
def move_processed_video(video_name):
    os.rename(f"videos/{video_name}", f"videos/processed/{video_name}")

def run_worker_queue():
    global worker
    print(f"\n\nCurrent worker: {worker}")
    if len(workers_queue) > 0:
        if worker is None or not worker.is_alive():
            worker = workers_queue.pop(0)
            worker.start()
            run_worker_queue()
        else:
            time.sleep(1)
            run_worker_queue()


def StartJob():
    global worker
    # check if there is any video to process
    check_video_dir()
    print (f"Videos to process: {to_process_video}")
    print (f"Videos processing: {processing_video}")
    print (f"Videos processed: {processed_video}")

    # check if there is any video to process
    while len(to_process_video) > 0:
        process_video_thread(to_process_video.pop(0))

            
    time.sleep(15)
    # Start processing videos
    run_worker_queue()
    StartJob()