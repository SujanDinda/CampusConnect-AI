from flask import Flask

from app.config import Config

from app.extensions import (
    db,
    migrate,
    jwt,
    cors
)

from app.auth import auth_bp

# Load authentication routes
import app.auth.routes


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize extensions

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    jwt.init_app(app)

    cors.init_app(app)

    # Register Blueprints

    app.register_blueprint(
        auth_bp
    )

    @app.route("/")
    def home():

        return {
            "status": "success",
            "message": "CampusConnect AI Backend is Running 🚀",
            "version": "1.0.0"
        }

    return app