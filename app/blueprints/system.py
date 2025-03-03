from flask import Blueprint, jsonify, request

from app.config import Config
from app.services.system_service import (
    get_cpu_usage,
    get_disk_usage,
    get_network_info,
    get_ram_usage,
    get_system_uptime,
    get_temperature,
)

system_bp = Blueprint("system", __name__)


@system_bp.route("/temp")
def api_temp():
    return jsonify({"temperature": get_temperature()})


@system_bp.route("/cpu")
def api_cpu():
    return jsonify({"cpu_usage": get_cpu_usage()})


@system_bp.route("/ram")
def api_ram():
    return jsonify({"ram_usage": get_ram_usage()})


@system_bp.route("/disk")
def api_disk():
    return jsonify({"disk_usage": get_disk_usage()})


@system_bp.route("/uptime")
def api_system_uptime():
    return jsonify({"uptime": get_system_uptime()})


@system_bp.route("/network")
def api_network():
    return jsonify(get_network_info())


@system_bp.route("/process_env", methods=["POST"])
def process_env():
    data = request.get_json()

    # Validate request structure
    if not data or "auth_token" not in data or "env_data" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    auth_token = data["auth_token"]
    env_data = data["env_data"]

    # Authenticate the request
    if auth_token != Config.AUTH_SHIP_ENV_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        # Convert the dictionary into a .env format
        env_lines = [f"{key}={value}" for key, value in env_data.items()]
        env_content = "\n".join(env_lines)

        # Write the new environment variables to the .env file
        with open(".env", "w") as env_file:
            env_file.write(env_content)

        return jsonify({"message": "Environment variables updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
