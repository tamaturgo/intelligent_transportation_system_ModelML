options = {
    'STREAM_RESOLUTION': '1080p',  # stream resolution
} 
OUTPUT_CAPTION = 'Output Frame'
LOGGING = False

classesFile = "models/classes.names"
model_path = 'models/best_1280_px_color.pt'
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.81  # Non-maximum suppression threshold
inpWidth = 1280  # 416     # Width of network's input image
inpHeight = 720  # 416     # Height of network's input image
skip_rate = 5  # 2

outputResolution = (640, 360)

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