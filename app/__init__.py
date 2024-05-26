import os

from flask import Flask
from flask_compress import Compress
from flask_wtf import CSRFProtect

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

csrf = CSRFProtect()
compress = Compress()


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    config.init_app(app)

    # Set up extensions
    csrf.init_app(app)
    compress.init_app(app)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .scanner import scanner_bp
    app.register_blueprint(scanner_bp, url_prefix='/scanner')

    from .ocr import ocr_bp
    app.register_blueprint(ocr_bp, url_prefix='/ocr')

    return app