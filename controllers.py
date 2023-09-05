import cv2
from CONST import *
import numpy as np
import time
from alert_maker import write_alert
from moviepy.editor import VideoFileClip

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

    # North america video
    central_area = [(200, 590), (1000, 515), (1300, 655), (350, 800)]  # 1920x1080
    central_area = [(int(x / 2), int(y / 2)) for x, y in central_area]
     
    not_stop_area = [
        [(56, 40), (317, 172), (591, 150), (600, 170), (363, 195), (500, 247), (960, 200), (960, 150), (460, 15)], # Pedestrian area 1
        central_area, # Intersection center
        [(690,330), (960, 290), (960, 490), (730, 380)],
        [(1, 415), (0,540), (320, 540), (274, 475), (200, 415), (119, 410)],
        [(1, 120), (115, 270),(0,300)]
    ]

    # Vehicle at central area stopped for more than 30 seconds
    if objid in vehicle_at_central_area:
        contact = cv2.pointPolygonTest(np.array(central_area, np.int32), (center_x, center_y), False)
        contact_any = []
        for area in not_stop_area:
            contact_local = cv2.pointPolygonTest(np.array(area, np.int32), (center_x, center_y), False)
            contact_any.append(contact_local)
        contact = max(contact_any)
        elepsed_time = time.time() - vehicle_at_central_area[objid]
        print("Elapsed time: ", elepsed_time)

        if contact >= 0:
            vehicle_at_central_area_time[objid] = elepsed_time
        cv2.putText(frame, 'E.T: %.2f' % vehicle_at_central_area_time[objid], (
            startX, startY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

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
                height, width, layers = last_frames[0].shape
                size = (width, height)
                out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
                for i in range(len(last_frames)):
                    out.write(last_frames[i])
                out.release()

                # Converter o vídeo para o formato H.264 (MP4) usando o moviepy
                video_clip = VideoFileClip(video_name)
                video_clip.write_videofile(video_name.replace(".mp4", "_converted.mp4"), codec="libx264")


                f.write('### VIDEO: %s\n' % video_name)
                f.write('### FIM DO ALERTA\n\n')
                f.close()

    contact = cv2.pointPolygonTest(np.array(central_area, np.int32), (center_x, center_y), False)
    contact_any = []
    for area in not_stop_area:
        print("Area: ", area)
        cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 0, 190), 2)
        contact_local = cv2.pointPolygonTest(np.array(area, np.int32), (center_x, center_y), False)
        contact_any.append(contact_local)
    
    contact = max(contact_any)
    print("Contact: ", contact)
    if contact >= 0:
        if objid not in vehicle_at_central_area:
            vehicle_at_central_area[objid] = time.time()

    # Draw a bounding box.
    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
    cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    # Draw a center point
    cv2.circle(frame, (center_x, center_y), 2, color, 2)


    # Zip frames and save as video
    if len(last_frames) > 200:
        last_frames = last_frames[-200:]
        height, width, layers = last_frames[0].shape
        size = (width, height)
        

    return frame
