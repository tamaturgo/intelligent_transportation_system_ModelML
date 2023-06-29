options = {
    'STREAM_RESOLUTION': '480p',
} 
SOURCE = 'https://www.youtube.com/watch?v=UaVeLK0kslQ'

OUTPUT_CAPTION = 'Output Frame'
LOGGING = False
path_to_save = "C:\\Users\\dioge\\Documents\\GitHub\\tcc\\frames\\"
classesFile = "C:\\Users\\dioge\\Documents\\GitHub\\tcc\\trained_models\\class.names"


model_path = 'C:\\Users\\dioge\\Documents\\GitHub\\tcc\\trained_models\\yolov8_datav3.pt'
confThreshold = 0.49  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 416  # 416     # Width of network's input image
inpHeight = 416  # 416     # Height of network's input image

color_palette = [
    (0, 0, 255),
    (0, 128, 255),
    (0, 0, 128),
    (0, 255, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 0, 0),
    (128, 0, 0),
    (128, 0, 128),
    (255, 0, 255),
]