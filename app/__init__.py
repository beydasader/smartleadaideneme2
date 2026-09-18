from flask import Flask, jsonify
from flask_cors import CORS

from config import configurations
from app.database import init_db
from app.routes import pages, api


def create_app(config_name="development"):

    app = Flask(
        __name__,
        template_folder="templates"
    )

    app.config.from_object(
        configurations[config_name]
    )

    CORS(
        app,
        origins=app.config["CORS_ORIGINS"]
    )

    with app.app_context():
        init_db(app)

    app.register_blueprint(pages)

    app.register_blueprint(
        api,
        url_prefix="/api"
    )

    @app.route("/health")
    def health():

        return jsonify({
            "basari": True,
            "durum": "aktif"
        })

    return app