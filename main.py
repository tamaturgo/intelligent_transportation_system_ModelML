import json
import cv2
import tkinter as tk
from CONST import *
from vidgear.gears import CamGear
from Tracker import Tracker
from controllers import *
import customtkinter
from PIL import ImageTk, Image
from GUI.MenuFrame import MenuFrame
from GUI.ImageFrame import ImageFrame
from GUI.SecundaryMenuFrame import SecundaryMenuFrame
from GUI.BottomMenu import BottomMenu
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')


def exit(self):
    cv2.destroyAllWindows()
    self.window.destroy()
    self.video_capture.release()


class IntelligentTransportationSystem:
    def __init__(self, window, source):
        self.window = window
        self.window.title("Intelligent Transportation System")
        self.window.resizable(False, False)
        self.window.geometry("1280x720")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.current_frame = None
        if (source != 'stream'):
            self.video_capture = cv2.VideoCapture(
                './datasets/videos/batecarro.mp4')
            self.stream = None
        else:
            self.stream = CamGear(source='https://www.youtube.com/watch?v=ByED80IKdIU',
                                  stream_mode=True,
                                  logging=LOGGING, **options).start()
            self.video_capture = None

        self.tracker = Tracker(threshold=90, age_threshold=15)
        self.skip_rate = 5
        self.frame_count = 0
        self.source = source
        self.action_context = {
            "action": None,
            "payload": None
        }
        with open('context.json', 'w') as outfile:
            json.dump(self.action_context, outfile)
        self.draw_gui()
        self.update_frame()

    def draw_gui(self):
        self.menu_frame = MenuFrame(self.window, width=380, height=720)
        self.menu_frame.grid(row=0, column=0, padx=10,
                             pady=10, rowspan=2, sticky="NSEW")

        self.image_frame = ImageFrame(self.window, fg_color="black")
        self.image_frame.grid(row=0, column=1)

        self.secundary_menu_frame = SecundaryMenuFrame(self.window)
        self.secundary_menu_frame.grid(
            row=0, column=2, padx=10, pady=10, rowspan=2, sticky="NSEW")

        self.bottom_frame = BottomMenu(self.window)
        self.bottom_frame.grid(row=1, column=1, padx=10,
                               pady=10, sticky="NSEW")

        self.canvas = self.image_frame.canvas

    def update_frame(self):
        # Update context read the last action
        with open('context.json', 'r') as f:
            context = json.load(f)
            self.action_context["action"] = context["action"]
            self.action_context["payload"] = context["payload"]
            

        self.frame_count += 1
        if (self.source == 'stream'):
            frame = self.stream.read()
        else:
            _, frame = self.video_capture.read()

        if self.frame_count % self.skip_rate != 0:
            self.window.after(15, self.update_frame)
            return

        frame = cv2.resize(frame, outputResolution)

        (classes_id, object_ids, boxes) = self.tracker.update(frame)
        for (classid, objid, box) in zip(classes_id, object_ids, boxes):
            classes_id = int(classid)
            color = COLORS[classes_id % len(COLORS)]
            label = "%s:%d" % (CLASSES[classes_id], objid)
            frame = track_downtown(
                frame, frame, objid, box, label, color)

        self.current_frame = Image.fromarray(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(image=self.current_frame)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(15, self.update_frame)

        show_area_menu(self)



def clear_action_context(self):
    self.action_context["action"] = None
    self.action_context["payload"] = None
    with open('context.json', 'w') as outfile:
        json.dump(self.action_context, outfile)

def show_area_menu(self):
    if (self.action_context["action"] == "add area"):
        self.secundary_menu_frame.active_area_menu()
        self.action_context["action"] = None
        self.action_context["payload"] = None
        clear_action_context(self)
    elif (self.action_context["action"] == "cancel_area"):
        self.secundary_menu_frame.disable_area_menu()
        self.action_context["action"] = None
        self.action_context["payload"] = None


if __name__ == "__main__":
    root = customtkinter.CTk()
    app = IntelligentTransportationSystem(root, 'video')
    root.mainloop()
