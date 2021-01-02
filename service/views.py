import config
import uuid

from PIL import Image

from app import app
from flask import (
    jsonify,
    request,
    send_from_directory
)

from model import (
    store_data,
    query_image,
    list_data
)

@app.route("/ping")
def hello():
    return jsonify({"ping": "pong"})

def allowed_file(filename):
    extension = filename.rsplit('.', 1)[1].lower() 
    return '.' in filename and extension in config.ALLOWED_EXTENSIONS, extension
           

@app.route('/analyze_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "no file provided"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "no file provided"}), 400

    type_allowed, extension = allowed_file(file.filename)
    if  not file or not type_allowed:
        return jsonify({"error": "disallowed file extension"}), 400
    
    image = Image.frombytes("RGB", (299, 299), file)
    prediction, pca = query_image(image)

    filename = uuid.uuid4() + "." + extension
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"status": "Success"}), 201

@app.route('/analyzes')
def analyzes():
    return jsonify(list_data())

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
