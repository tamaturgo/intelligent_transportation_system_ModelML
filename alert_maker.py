import os
import sys
import time
import cv2 as cv

def write_alert(frame_history, message):
    """Save a frame with a message"""
    alert_path = os.path.join(os.getcwd(), 'alerta')
    if not os.path.exists(alert_path):
        os.mkdir(alert_path)
    
    # Get last alert id
    last_alert_id = 0
    for file in os.listdir(alert_path):
        if file.endswith('.jpg'):
            file_id = int(file.split('.')[0])
            if file_id > last_alert_id:
                last_alert_id = file_id
    
    # Add 1 to last alert id
    last_alert_id += 1

    # Create a id directory
    alert_id_path = os.path.join(alert_path, str(last_alert_id))
    os.mkdir(alert_id_path)
    # Save the frame history
    for i, frame in enumerate(frame_history):
        cv.imwrite(os.path.join(alert_id_path, f'{i}.jpg'), frame)
    # Save the message
    with open(os.path.join(alert_id_path, 'message.txt'), 'w') as f:
        f.write(message)
