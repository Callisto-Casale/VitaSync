from flask import Blueprint, jsonify

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
