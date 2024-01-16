from flask import Flask
from routes import create_routes
import threading
import time
app = Flask(__name__)
from job.ProcessVideo import VideoProcessor
# Carrega as rotas do arquivo routes.py
create_routes(app)


def process_videos():
    print ("Process videos thread started")
    # Cria uma instância do VideoProcessor e inicia o job
    video_processor = VideoProcessor()
    video_processor.start_job()


schedule_thread = threading.Thread(target=process_videos)
schedule_thread.setName("Process Videos")
schedule_thread.start()

# Inicia o servidor
if __name__ == '__main__':
    app.run()
