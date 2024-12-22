from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from app.config import *
from app.utils import *

# Create a blueprint for the API
api = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint: Upload Image
@api.route('/predict', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({
                        "status":{
                            "code":400,
                            "message":"error, no file part!"
                        }
                        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status":{
                            "code":400,
                            "message":"error, no selected file!"
                        }}), 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        result = cataract_prediction(file_path)

        return jsonify({
                        "status" : {
                            "code":201,
                            "message":"Success uploading the image!"
                        },
                                        
                        "data":result
                    }), 200

    return jsonify({"error": "Invalid file type"}), 400

# Endpoint: Fetch Uploaded Image
@api.route('/uploads/<filename>', methods=['GET'])
def fetch_image(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({"status":{
                            "code":404,
                            "message":"File not found!"
                        }}), 404

# Endpoint: List Uploaded Images
@api.route('/uploads', methods=['GET'])
def list_images():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"status":{
                            "code":200,
                            "message":"success!"
                        },

                    "data":files
                    }), 200
