from flask import Flask

from app.blueprints.github import github_bp
from app.blueprints.home import home_bp
from app.blueprints.ingredients import ingredients_bp
from app.blueprints.meals import meals_bp
from app.blueprints.network import network_bp
from app.blueprints.pihole import pihole_bp
from app.blueprints.system import system_bp
from app.blueprints.weather import weather_bp
from app.blueprints.health import health_bp
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(github_bp, url_prefix="/github")
    app.register_blueprint(pihole_bp, url_prefix="/pihole")
    app.register_blueprint(system_bp, url_prefix="/api")
    app.register_blueprint(network_bp, url_prefix="/network")
    app.register_blueprint(weather_bp, url_prefix="/weather")
    app.register_blueprint(meals_bp, url_prefix="/meals")
    app.register_blueprint(ingredients_bp, url_prefix="/ingredients")
    app.register_blueprint(health_bp, url_prefix="/health")

    app.register_blueprint(home_bp)

    return app
