import config

from app import app
from flask import (
    jsonify,
    request,
    send_from_directory
)
from werkzeug.utils import secure_filename


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

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({"status": "Success"}), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
