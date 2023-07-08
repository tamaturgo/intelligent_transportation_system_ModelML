options = {
    'STREAM_RESOLUTION': '1080p',  # stream resolution
} 
OUTPUT_CAPTION = 'Output Frame'
LOGGING = False

classesFile = "models/classes.names"
model_path = 'models\yolov8_small_datav4.pt'
confThreshold = 0.2  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 416  # 416     # Width of network's input image
inpHeight = 416  # 416     # Height of network's input image
skip_rate = 5

COLORS = [
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
CLASSES = open(classesFile).read().strip().split("\n")