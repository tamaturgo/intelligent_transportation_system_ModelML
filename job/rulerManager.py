import numpy as np
import cv2
import os
import time
from services.RuleService import RuleService
from services.AreaService import AreaService

enum_rule_type = {
    "speed" : 0,
    "not_allowed" : 1,
    "cross_area_to_area" : 2,
    "time_limit" : 3,
}


class TimeLimitRule:
    def __init__(self, poligono, value):
        self.value = value
        self.observed_area = poligono
        self.object_current_time = {}
        self.observed_objects = []
        print ("Time limit rule created" , self.value, self.observed_area )

    def update(self, frame, object_ids, boxes):
        for (object_id, box) in zip(object_ids, boxes):
            if object_id in self.observed_objects:
                if self.check_collision(box, self.observed_area):
                        frame = self.draw_timer(frame, box=box, object_id=object_id)
                        self.check_time(object_id)
            else:
                if self.check_collision(box, self.observed_area):
                    print ("Object", object_id, "entered area", self.observed_area)
                    self.check_time(object_id)
                    frame = self.draw_timer(frame, box=box, object_id=object_id)
                    self.observed_objects.append(object_id)

        return frame
    
    def check_collision(self, box, area):
        start_x = int(box[0])
        start_y = int(box[1])
        end_x = int(box[2])
        end_y = int(box[3])
        x_values = [int(ponto['x']) for ponto in area]
        y_values = [int(ponto['y']) for ponto in area]

        np_x_values = np.array(x_values, np.int32)
        np_y_values = np.array(y_values, np.int32)
        np_areas = np.array([np_x_values, np_y_values]).T
        center_x, center_y = int((start_x + end_x) / 2), int((start_y + end_y) / 2)
        if cv2.pointPolygonTest(np_areas, (center_x, center_y), False) >= 0:
            return True
        return False

    def check_time(self, object_id):
        # Se o objeto não está sendo observado, começa a observar
        if object_id not in self.object_current_time:
            print ("Start time limit for object", object_id)
            self.object_current_time[object_id] = time.time()
            return False
        # Se o objeto está sendo observado, verifica se o tempo limite foi atingido
        else:
            if time.time() - self.object_current_time[object_id] > self.value:
                self.alert_event(object_id)
                return True
            else:
                print ("Time limit not reached for object", object_id, "time:", time.time() - self.object_current_time[object_id])
                return False
    def alert_event(self, object_id):
        print(f"Time limit reached for object {object_id}")
    
    def draw_timer(self, frame, box, object_id):
        start_x = int(box[0])
        start_y = int(box[1])
        end_x = int(box[2])
        end_y = int(box[3])
        
        center_x, center_y = int((start_x + end_x) / 2), int((start_y + end_y) / 2)
        cv2.putText(frame, str(self.value -  int(time.time() - self.object_current_time[object_id])), (center_x, center_y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        
        return frame
    
            

class RulerManager:
    def __init__(self) -> None:
        self.rule_service = RuleService()
        self.area_service = AreaService()
        self.area_info = []
        self.rule_dict = {}
        self.initiate_area_info()
        self.time_rulers = []
        self.initiate_time_rulers(self.rule_dict)

    def initiate_area_info(self):
        areas = self.area_service.get_all_areas()
        for area in areas:
            self.area_info.append(self.area_service.get_area_info(area['id']))
        for area in self.area_info:
            self.rule_dict[area['id']] = area['rules']

    def initiate_time_rulers(self, rule_dict):
        for area_id in rule_dict:
            for rule in rule_dict[area_id]:
                if rule['type'] == "3":
                    get_area_polygon = lambda area_id: [ponto for ponto in self.area_info if ponto['id'] == area_id][0]['points']
                    self.time_rulers.append(
                        {
                            "area_id": area_id,
                            "rule": TimeLimitRule(get_area_polygon(area_id), rule['value']) 
                        }
                    )

    def update(self, frame, object_ids, boxes):
        # Draw areas
        for area in self.area_info:
            x_values = [int(ponto['x']) for ponto in area['points']]
            y_values = [int(ponto['y']) for ponto in area['points']]
            np_x_values = np.array(x_values, np.int32)
            np_y_values = np.array(y_values, np.int32)
            np_areas = np.array([np_x_values, np_y_values]).T
            cv2.polylines(frame, [np_areas], True, (0, 0, 190), 2)

        for ruler in self.time_rulers:
            frame = ruler['rule'].update(frame, object_ids, boxes)
        return frame
        
        