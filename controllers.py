import cv2
from CONST import *
import numpy as np
import time
from alert_maker import write_alert
from moviepy.editor import VideoFileClip
import threading

# Auxiliar variables DOWN TOWN
vehicle_at_central_area = {}
vehicle_at_central_area_time = {}
alerted_ids = []
last_frames = []

def track_downtown(frame, frame_without_draw, objid, box, label, color):
    startX = int(box[0])
    startY = int(box[1])
    endX = int(box[2])
    endY = int(box[3])
    center_x = int((startX + endX) / 2)
    center_y = int((startY + endY) / 2)
    global last_frames 
    last_frames.append(frame_without_draw)

    not_stop_area = [
        [(690,330), (960, 290), (960, 490), (730, 380)],
    ]

    # Vehicle at central area stopped for more than 30 seconds
    if objid in vehicle_at_central_area:
        contact_any = []
        for area in not_stop_area:
            contact_local = cv2.pointPolygonTest(np.array(area, np.int32), (center_x, center_y), False)
            contact_any.append(contact_local)
        contact = max(contact_any)
        elepsed_time = time.time() - vehicle_at_central_area[objid]

        if contact >= 0:
            vehicle_at_central_area_time[objid] = elepsed_time
        # Alerta de tempo
        if elepsed_time > 15 and objid not in alerted_ids:
            alerted_ids.append(objid)
            with open('alerta.txt', 'a') as f:
                hash_para_imagem = str(hash(frame.tostring()))
                #cv2.imwrite('alerta/%s.jpg' % hash_para_imagem, frame_without_draw)
                f.write("### ALERTA DE TEMPO\n")
                f.write('### VEICULO %d ESTA A MAIS DE 15 SEGUNDOS EM LOCAL PROIBIDO\n' % objid)
                f.write('### TEMPO: %.2f\n' % elepsed_time)
                f.write('### DATA: %s\n' % time.strftime("%d/%m/%Y %H:%M:%S"))
                # Salva o video
                video_name = 'alerta/%s.mp4' % hash_para_imagem
                height, width, _ = last_frames[0].shape
                size = (width, height)

                def thread_function():
                    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
                    for i in range(len(last_frames)):
                        out.write(last_frames[i])
                    out.release()
                    
                    video_clip = VideoFileClip(video_name)
                    video_clip.write_videofile(video_name.replace(".mp4", "_converted.mp4"), codec="libx264")
                    video_clip.close()
                x = threading.Thread(target=thread_function)
                x.start()
                f.write('### VIDEO: %s\n' % video_name)
                f.write('### FIM DO ALERTA\n\n')
                f.close()

    contact_any = []
    for area in not_stop_area:
        cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 0, 190), 2)
        contact_local = cv2.pointPolygonTest(np.array(area, np.int32), (center_x, center_y), False)
        contact_any.append(contact_local)
    
    contact = max(contact_any)
    if objid not in vehicle_at_central_area and contact >= 0:
        vehicle_at_central_area[objid] = time.time()

    # Draw a bounding box.
    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
    cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    # Draw a center point
    cv2.circle(frame, (center_x, center_y), 2, color, 2)
        
    return frame
