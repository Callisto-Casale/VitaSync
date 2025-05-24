import subprocess

from flask import Blueprint, render_template
from flask import jsonify
from app.services.system_service import get_temperature, get_system_uptime, get_cpu_usage, get_ram_usage, get_disk_usage, get_network_info
from app.blueprints.pihole import get_pihole_status

health_bp = Blueprint("health", __name__)


@health_bp.route("/status")
def status():
    return jsonify({"status": "OK"})


@health_bp.route("/info")
def info():
    return jsonify({
        "temperature": get_temperature(),
        "system_uptime": get_system_uptime(),
        "cpu_usage": get_cpu_usage(),
        "ram_usage": get_ram_usage(),
        "disk_usage": get_disk_usage(),
        "network_info": get_network_info()
    })


@health_bp.route("/pihole")
def pihole_stats():
    return get_pihole_status()
