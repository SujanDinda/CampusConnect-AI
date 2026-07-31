from flask import jsonify


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):

        return jsonify({
            "success": False,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):

        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):

        return jsonify({
            "success": False,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):

        return jsonify({
            "success": False,
            "message": "Internal Server Error"
        }), 500