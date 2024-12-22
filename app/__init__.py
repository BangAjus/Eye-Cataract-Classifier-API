from flask import Flask
from app.config import *
import os

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints/routes
    from app.routes import api
    app.register_blueprint(api, url_prefix='/api')

    return app
