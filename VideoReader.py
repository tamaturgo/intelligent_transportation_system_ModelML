import cv2
from vidgear.gears import CamGear

class VideoReader:
    def __init__(self, source, output_resolution):
        self.stream = CamGear(source=source, stream_mode=True).start()
        self.output_resolution = output_resolution

    def read_frame(self):
        print("Reading frame")
        frame = self.stream.read()
        return cv2.resize(frame, self.output_resolution) if frame is not None else None

    def stop(self):
        self.stream.stop()