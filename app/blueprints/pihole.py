import subprocess

from flask import Blueprint, jsonify

from app.services.pihole_service import get_pihole_stats

pihole_bp = Blueprint("pihole", __name__)


@pihole_bp.route("/stats", methods=["GET"])
def pihole_stats():
    return jsonify(get_pihole_stats())


@pihole_bp.route("/status", methods=["GET"])
def get_pihole_status():
    try:
        result = subprocess.run(["pihole", "status"], capture_output=True, text=True)
        status = (
            "enabled"
            if "Active" in result.stdout or "enabled" in result.stdout.lower()
            else "disabled"
        )
        return jsonify({"status": status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pihole_bp.route("/enable", methods=["POST"])
def enable_pihole():
    result = subprocess.run(["pihole", "enable"], capture_output=True, text=True)
    return jsonify({"status": "enabled" if result.returncode == 0 else "failed"})


@pihole_bp.route("/disable", methods=["POST"])
def disable_pihole():
    result = subprocess.run(["pihole", "disable"], capture_output=True, text=True)
    return jsonify({"status": "disabled" if result.returncode == 0 else "failed"})
