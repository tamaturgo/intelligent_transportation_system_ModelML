# routes.py
from flask import jsonify, request, Flask
from flask_cors import CORS
from services.ImageService import ImageService
from services.VideoService import VideoService
from services.AreaService import AreaService
from services.RuleService import RuleService


ImageService = ImageService()
VideoService = VideoService()
AreaService = AreaService()
RuleService = RuleService()

MULTIPART_FORM_DATA = "multipart/form-data"

def create_routes(app: Flask):
    CORS(app)
    app.route('/image', methods=['POST', 'GET'])(image)
    app.route('/video', methods=['POST'])(video)
    app.route('/video/process', methods=['GET'])(video_process)
    app.route('/video/to/process', methods=['GET'])(video_to_process)
    app.route('/area', methods=['POST', 'GET'])(area)
    app.route('/area/<id>/info', methods=['GET'])(area_info)
    app.route('/area/<id>', methods=['DELETE'])(area_delete)
    app.route('/rule', methods=['POST'])(rules)
    app.route('/rule', methods=['GET'])(rules_get)
    app.route('/rule/<id>', methods=['DELETE'])(rule_delete)
    app.route('/rule/associate', methods=['POST'])(associate_rule)
    app.route('/rule/desassociate', methods=['POST'])(desassociate_rule)
    
def image():
    if request.method == 'POST':
        if request.content_type.startswith(MULTIPART_FORM_DATA) == False:
            return jsonify({"error": "O tipo de conteúdo da requisição deve ser" + MULTIPART_FORM_DATA + "."})
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

def video():
    if request.method == 'POST':
        if request.content_type.startswith(MULTIPART_FORM_DATA) == False:
            return jsonify({"error": "O tipo de conteúdo da requisição deve ser multipart/form-data."})
        if 'video' not in request.files:
            return jsonify({"error": "O arquivo não está presente na requisição."})
        video = request.files['video']
        if video.filename == '':
            return jsonify({"error": "O nome do arquivo está vazio."})
        if not video:
            return jsonify({"error": "O arquivo é inválido."})
        video_id = VideoService.save_video(nome=video.filename, video=video)
        return jsonify({'msg': 'video received!', 'id': video_id})

def video_process():
    if request.method == 'GET':
        return VideoService.get_last_video()

def video_to_process():
    if request.method == 'GET':
        return jsonify(VideoService.get_videos_at_folder())

def area():
    if request.method == 'POST':
        polygon = request.get_json()['polygon']
        AreaService.add_area(polygon)
        return jsonify({'msg': 'area received!'})
    elif request.method == 'GET':
        return jsonify(AreaService.get_all_areas())

def area_info(id):
    if request.method == 'GET':
        print(AreaService.get_area_info(id))
        return jsonify(AreaService.get_area_info(id))

def area_delete(id):
    if request.method == 'DELETE':
        return jsonify(AreaService.delete_area(id))

def rules():
    if request.method == 'POST':
        if request.content_type.startswith(MULTIPART_FORM_DATA) == False:
            return jsonify({"error": "O tipo de conteúdo da requisição deve ser multipart/form-data."})
        rule_type = request.form['type']
        value = request.form['value']
        aux_value = request.form['aux_value']
        if aux_value:
            RuleService.add_rule(rule_type, value, aux_value)
        else:
            RuleService.add_rule(rule_type, value)
        return jsonify({'msg': 'rule received!'})
    return jsonify({"error": "Método não permitido."}), 405

def rules_get():
    if request.method == 'GET':
        return jsonify(RuleService.get_all_rules())

def rule_delete(id):
    if request.method == 'DELETE':
        return jsonify(RuleService.remove_rule_cascade(id))

def associate_rule():
    if request.method == 'POST':
        rule_id = request.get_json()['rule_id']
        area_id = request.get_json()['area_id']
        return jsonify(RuleService.associate_rule(rule_id, area_id))
    
def desassociate_rule():
    if request.method == 'POST':
        rule_id = request.get_json()['rule_id']
        area_id = request.get_json()['area_id']
        return jsonify(RuleService.desassociate_rule(rule_id, area_id))