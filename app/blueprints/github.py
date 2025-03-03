import subprocess

from flask import Blueprint, jsonify, request

from app.config import Config

github_bp = Blueprint("github", __name__)


@github_bp.route("/reload", methods=["POST"])
def github_reload():
    data = request.get_json()
    received_token = data.get("auth_token")

    # Validate authentication token
    if received_token != Config.AUTH_RELOAD_TOKEN:
        return jsonify({"error": "Invalid authentication token"}), 403

    subprocess.run(["git", "pull"], check=True)

    subprocess.Popen(["sudo", "systemctl", "restart", "gunicorn"])

    return jsonify({"message": "Code updated and Gunicorn restarted"}), 200
