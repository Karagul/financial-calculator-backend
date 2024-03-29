from flask import Flask
from flask_cors import CORS

from config import config


def create_app(config_name):
    """
    App factory for the creation of a Flask app.
    :param config_name: The key for the config setting to use
    :type config_name: str
    :return: A Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    CORS(app)

    from calculators.calculators import calculators
    app.register_blueprint(calculators)

    return app
