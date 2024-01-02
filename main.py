from flask import Flask
from routes import create_routes
import threading
import time
app = Flask(__name__)

# Carrega as rotas do arquivo routes.py
create_routes(app)

# Job temporário para processar os vídeos
timer = 0
time_interval = 10


def process_videos():
    print("Processando vídeos...")

# Função para agendar o job a cada 10 segundos
def schedule_job():
    global timer
    while True:
        if timer == time_interval:
            process_videos()
            timer = 0
        else:
            timer += 1
            time.sleep(1)


# Inicia um job temporizado a cada 10 segundos em uma thread
schedule_thread = threading.Thread(target=schedule_job)
schedule_thread.start()

# Inicia o servidor
if __name__ == '__main__':

    # Inicia o servidor
    app.run(debug=True)
