import config
import os
from flask import Flask
from flask_cors import CORS
import uuid

from PIL import Image

from flask import (
    jsonify,
    request,
    send_from_directory
)

from model import (
    store_image,
    list_data,
    init_data,
    load_pca
)

if os.environ.get('INIT', False):
    init_data()
else:
    load_pca()

app = Flask(__name__)
#app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_SIZE
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, support_credentials=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True,host='0.0.0.0',port=port)

def allowed_file(filename):
    extension = filename.rsplit('.', 1)[1].lower() 
    return '.' in filename and extension in config.ALLOWED_EXTENSIONS, extension

@app.route("/ping")
def hello():
    return jsonify({"ping": "pong"})

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

    image_name = request.form.get("name", "Unknown")
    id = str(uuid.uuid4())
    image_file = id + "." + extension
    img_file = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
    file.save(img_file)

    store_image(img_file, image_file, image_name, id)
    return jsonify({"status": "Success"}), 201

@app.route('/analyzes')
def analyzes():
    return jsonify(list_data())

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
