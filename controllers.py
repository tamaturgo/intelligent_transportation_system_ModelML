import cv2
from CONST import *
import numpy as np
import time


# Auxiliar variables DOWN TOWN
vehicle_at_central_area = {}
vehicle_at_central_area_time = {}


# Auxiliar variables DJALMA
vehicle_at_centro_1 = {}
vehicle_at_centro_1_time = {}

vehicle_at_centro_2 = {}
vehicle_at_centro_2_time = {}

vehicle_at_bairro_1 = {}
vehicle_at_bairro_1_time = {}

vehicle_at_bairro_2 = {}
vehicle_at_bairro_2_time = {}

vehicle_at_crosswalk = {}
vehicle_at_crosswalk_time = {}


def track_downtown(frame, frame_without_draw, objid, box, label, color):
    startX = int(box[0])
    startY = int(box[1])
    endX = int(box[2])
    endY = int(box[3])
    center_x = int((startX + endX) / 2)
    center_y = int((startY + endY) / 2)

    # North america video
    central_area = [(200, 590), (1000, 515),
                    (1300, 655), (350, 800)]  # 1920x1080
    central_area = [(int(x / 2), int(y / 2)) for x, y in central_area]

    pista_1 = [(120, 320), (380, 320), (620, 480), (250, 520)]  # 1920x1080
    pista_1 = [(int(x / 2), int(y / 2)) for x, y in pista_1]

    # Vehicle at central area stoped for more than 30 seconds
    if objid in vehicle_at_central_area:
        contact = cv2.pointPolygonTest(
            np.array(central_area, np.int32), (center_x, center_y), False)
        elepsed_time = time.time() - vehicle_at_central_area[objid]
        print("Elepsed time: ", elepsed_time)

        if contact >= 0:
            vehicle_at_central_area_time[objid] = elepsed_time

        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, startY - 15), color, -1)
        cv2.putText(frame, label, (startX, startY - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(frame, 'E.T: %.2f' % vehicle_at_central_area_time[objid], (
            startX, startY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        # Alerta de tempo
        if elepsed_time > 30:
            with open('alerta.txt', 'a') as f:
                hash_para_imagem = str(hash(frame.tostring()))
                cv2.imwrite('alerta/%s.jpg' %
                            hash_para_imagem, frame_without_draw)
                f.write("### ALERTA DE TEMPO\n")
                f.write(
                    '### VEICULO %d ESTA A MAIS DE 30 SEGUNDOS NA AREA CENTRAL\n' % objid)
                f.write('### TEMPO: %.2f\n' % elepsed_time)
                f.write('### DATA: %s\n' % time.strftime("%d/%m/%Y %H:%M:%S"))
                f.write('### IMAGEM: %s.jpg\n' % hash_para_imagem)
                f.write('###\n\n')

    for i, area in enumerate([central_area]):
        if i == 0:
            print(area)
            cv2.polylines(frame, [np.array(area, np.int32)],
                          True, (0, 0, 255), 2)
        else:
            cv2.polylines(frame, [np.array(area, np.int32)],
                          True, (255, 0, 0), 2)

    contact = cv2.pointPolygonTest(
        np.array(central_area, np.int32), (center_x, center_y), False)
    if contact >= 0:
        if objid not in vehicle_at_central_area:
            vehicle_at_central_area[objid] = time.time()

    # TODO: Verificar se o veiculo esta na calçada
    # TODO: Verificar se o veiculo esta na faixa de pedestre
    # TODO: Verificar se o veiculo esta na parado na pista 1 e se há veículos andando na pista 1
    # TODO: Verificar velocidade do veiculo
    return frame


def track_djalma(frame, frame_without_draw, objid, box, label, color):
    startX = int(box[0])
    startY = int(box[1])
    endX = int(box[2])
    endY = int(box[3])
    center_x = int((startX + endX) / 2)
    center_y = int((startY + endY) / 2)

    crosswalk = [(180, 270), (440, 250), (767, 242),
                 (775, 280), (414, 280), (125, 290)]

    pista_centro_1 = [(208, 260), (447, 160), (590, 150),
                      (444, 242)]  # 1920x1080
    pista_centro_2 = [(130, 290), (383, 282), (29, 507), (29, 330)]

    pista_bairro_1 = [(484, 246), (770, 240), (750, 145), (612, 150)]
    pista_bairro_2 = [(426, 285), (781, 280), (851, 534), (88, 532)]

    # Draw the areas
    for i, area in enumerate([crosswalk, pista_centro_1, pista_centro_2, pista_bairro_1, pista_bairro_2]):
        if i == 0:
            print(area)
            cv2.polylines(frame, [np.array(area, np.int32)],
                          True, (0, 0, 255), 2)
        else:
            cv2.polylines(frame, [np.array(area, np.int32)],
                          True, (255, 255, 0), 2)
            
    # Check if vehicle is in crosswalk
    contact = cv2.pointPolygonTest(
        np.array(crosswalk, np.int32), (center_x, center_y), False)
    if contact >= 0:
        if objid not in vehicle_at_crosswalk:
            vehicle_at_crosswalk[objid] = time.time()
        
        elepsed_time = time.time() - vehicle_at_crosswalk[objid]
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, startY - 15), color, -1)
        cv2.putText(frame, label, (startX, startY - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(frame, 'E.T: %.2f' % elepsed_time, (
            startX, startY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        

    # Check if vehicle is in pista centro 1
    contact = cv2.pointPolygonTest(
        np.array(pista_centro_1, np.int32), (center_x, center_y), False)
    if contact >= 0:
        if objid not in vehicle_at_bairro_1:
            vehicle_at_centro_1[objid] = time.time()
        
    # Check if vehicle is in pista centro 2
    contact = cv2.pointPolygonTest(
        np.array(pista_centro_2, np.int32), (center_x, center_y), False)
    if contact >= 0:
        if objid not in vehicle_at_bairro_2:
            vehicle_at_centro_2[objid] = time.time()
        
        elepsed_time = time.time() - vehicle_at_centro_2[objid]
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, startY - 15), color, -1)
        cv2.putText(frame, label, (startX, startY - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(frame, 'E.T: %.2f' % elepsed_time, (
            startX, startY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    # Check if vehicle is in pista bairro 1
    contact = cv2.pointPolygonTest(
        np.array(pista_bairro_1, np.int32), (center_x, center_y), False)
    if contact >= 0:
        if objid not in vehicle_at_centro_1:
            vehicle_at_bairro_1[objid] = time.time()

    # Check if vehicle is in pista bairro 2
    contact = cv2.pointPolygonTest(
        np.array(pista_bairro_2, np.int32), (center_x, center_y), False)
    if contact >= 0:
        if objid not in vehicle_at_centro_2:
            vehicle_at_bairro_1[objid] = time.time()

    # Draw the box
    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
    cv2.rectangle(frame, (startX, startY), (endX, startY - 15), color, -1)
    cv2.putText(frame, label, (startX, startY - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    
    # Print IDs that passed at centro 1 or centro 2 and are in bairro 1 or bairro 2
    if objid in vehicle_at_centro_1 and objid in vehicle_at_bairro_1:
        print("ID %d passou no centro 1 e esta no bairro 1" % objid)
    if objid in vehicle_at_centro_2 and objid in vehicle_at_bairro_2:
        print("ID %d passou no centro 2 e esta no bairro 2" % objid)
    if objid in vehicle_at_centro_1 and objid in vehicle_at_bairro_2:
        print("ID %d passou no centro 1 e esta no bairro 2" % objid)
    if objid in vehicle_at_centro_2 and objid in vehicle_at_bairro_1:
        print("ID %d passou no centro 2 e esta no bairro 1" % objid)
        
    # Print IDs that passed at bairro 1 or bairro 2 and are in centro 1 or centro 2
    if objid in vehicle_at_bairro_1 and objid in vehicle_at_centro_1:
        print("ID %d passou no bairro 1 e esta no centro 1" % objid)
    if objid in vehicle_at_bairro_2 and objid in vehicle_at_centro_2:
        print("ID %d passou no bairro 2 e esta no centro 2" % objid)
    if objid in vehicle_at_bairro_1 and objid in vehicle_at_centro_2:
        print("ID %d passou no bairro 1 e esta no centro 2" % objid)
    if objid in vehicle_at_bairro_2 and objid in vehicle_at_centro_1:
        print("ID %d passou no bairro 2 e esta no centro 1" % objid)
        
    return frame
