# routes.py
from flask import jsonify, request
from flask_cors import CORS
from services.ImageService import ImageService
from services.VideoService import VideoService
from services.AreaService import AreaService


ImageService = ImageService()
VideoService = VideoService()
AreaService = AreaService()


def create_routes(app):

    CORS(app)

    @app.route('/image', methods=['POST', 'GET'])
    def image():
        if request.method == 'POST':
            if request.content_type.startswith("multipart/form-data") == False:
                return jsonify({"error": "O tipo de conteúdo da requisição deve ser multipart/form-data."})
            if 'image' not in request.files:
                return jsonify({"error": "O arquivo não está presente na requisição."})
            image = request.files['image']
            if image.filename == '':
                return jsonify({"error": "O nome do arquivo está vazio."})
            if not image:
                return jsonify({"error": "O arquivo é inválido."})
            image_id = ImageService.save_image(image)
            return jsonify({'msg': 'image received!', 'id': image_id})
        elif request.method == 'GET':
            return ImageService.get_last_image()
        else:
            return jsonify({"error": "Método não permitido."}), 405

    @app.route('/video', methods=['POST'])
    def video():

        if request.method == 'POST':
            if request.content_type.startswith("multipart/form-data") == False:
                return jsonify({"error": "O tipo de conteúdo da requisição deve ser multipart/form-data."})
            if 'video' not in request.files:
                return jsonify({"error": "O arquivo não está presente na requisição."})
            video = request.files['video']
            if video.filename == '':
                return jsonify({"error": "O nome do arquivo está vazio."})
            if not video:
                return jsonify({"error": "O arquivo é inválido."})
            video_id = VideoService.save_video(
                nome=video.filename, video=video)
            return jsonify({'msg': 'video received!', 'id': video_id})

    @app.route('/video/process', methods=['GET'])
    def video_process():
        if request.method == 'GET':
            return VideoService.get_last_video()

    @app.route('/video/to/process', methods=['GET'])
    def video_to_process():
        if request.method == 'GET':
            return jsonify(VideoService.get_videos_at_folder())

    @app.route('/area', methods=['POST', 'GET'])
    def area():
        if request.method == 'POST':
            polygon = request.get_json()['polygon']
            AreaService.add_area(polygon)
            return jsonify({'msg': 'area received!'})
        elif request.method == 'GET':
            return jsonify(AreaService.get_all_areas())

    @app.route('/area/<id>/info', methods=['GET'])
    def area_info(id):
        if request.method == 'GET':
            print(AreaService.get_area_info(id))
            return jsonify(AreaService.get_area_info(id))

    @app.route('/area/<id>', methods=['DELETE'])
    def area_delete(id):
        if request.method == 'DELETE':
            return jsonify(AreaService.delete_area(id))

    @app.route('/rules', methods=['POST'])
    def rules():
        return jsonify({'msg': 'rules received!'})
