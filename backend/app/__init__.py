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

from app.models.token_blocklist import TokenBlocklist


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


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):

    jti = jwt_payload["jti"]

    token = TokenBlocklist.query.filter_by(
        jti=jti
    ).first()

    return token is not None