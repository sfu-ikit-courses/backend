from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .user import user
    from .math import math

    app.register_blueprint(user)
    app.register_blueprint(math)

    return app
