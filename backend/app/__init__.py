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

from app.profile import profile_bp

import app.profile.routes

from app.skills import skills_bp

import app.skills.routes

from app.utils.error_handlers import (
    register_error_handlers
)

from app.jobs import jobs_bp
import app.jobs.routes

import app.resumes.routes
from app.resumes import resume_bp


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

    app.register_blueprint(
        profile_bp
    )

    app.register_blueprint(
        skills_bp
    )

    app.register_blueprint(
        jobs_bp
    )

    app.register_blueprint(
        resume_bp,
        url_prefix="/api/v1/resumes"
    )

    register_error_handlers(app)


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