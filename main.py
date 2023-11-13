import cv2
from CONST import LOGGING, options, outputResolution, COLORS, CLASSES
from vidgear.gears import CamGear
from Tracker import Tracker
import asyncio
import websockets
import base64
from controllers import track_downtown

stream = CamGear(
    source='https://www.youtube.com/watch?v=E8LsKcVpL5A',
    stream_mode=True,
    logging=LOGGING, **options
).start()

tracker = Tracker(threshold=90, age_threshold=15)
websocket_connections = set()  # Usando um conjunto para armazenar várias conexões WebSocket
websocket_queue = asyncio.Queue()

async def process_frame(frame):
    (classes_id, object_ids, boxes) = tracker.update(frame)
    for (classid, objid, box) in zip(classes_id, object_ids, boxes):
        classes_id = int(classid)
        color = COLORS[1]
        label = f"{CLASSES[classes_id]}:{objid}"
        frame = track_downtown(frame, frame, objid, box, label, color)
    _, buffer = cv2.imencode(".jpg", frame)
    image_data = base64.b64encode(buffer).decode('utf-8')
    return image_data

async def send_image(websocket, _):
    frame_count = 0
    skip_rate = 5
    try:
        while True:
            frame_count += 1
            frame = stream.read()
            if frame_count % skip_rate == 0:
                frame = cv2.resize(frame, outputResolution)
                image_data = await process_frame(frame)
                try:
                    await websocket.send(image_data)
                except websockets.exceptions.ConnectionClosed:
                    print("Cliente desconectado")
                    # Remover a conexão se estiver fechada
                    websocket_connections.remove(websocket)
                    break
    except Exception as e:
        print(e)

async def handle_websocket_message(websocket, path):
    websocket_connections.add(websocket)  # Adicionar a nova conexão ao conjunto
    await websocket_queue.put(websocket)
    try:
        while True:
            message = await websocket.recv()
            print(f"Recebeu a mensagem do WebSocket: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Cliente desconectado")
        # Remover a conexão se estiver fechada
        websocket_connections.remove(websocket)
    

async def main(loop):
    start_server = websockets.serve(handle_websocket_message, "localhost", 8765)
    await asyncio.gather(start_server)

    while True:
        # Esperar por novas conexões
        websocket = await websocket_queue.get()
        
        # Iniciar a tarefa para enviar imagens
        asyncio.create_task(send_image(websocket, loop))

# Obter o loop de eventos principal
event_loop = asyncio.get_event_loop()

# Iniciar o loop de eventos principal
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
