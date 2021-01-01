import config
import os
from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_SIZE

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True,host='0.0.0.0',port=port)
