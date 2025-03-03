import os
import sys

from flask import Blueprint, jsonify

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from config import Config  # noqa: E402

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/key")
def key():
    return jsonify({"apiKey": Config.OPEN_WEATHER_KEY})
