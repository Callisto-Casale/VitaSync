from flask import Blueprint

from app.services.network import scan_network

network_bp = Blueprint("network", __name__)


@network_bp.route("/scan", methods=["GET"])
def scan():
    if scan_network() == 1:
        return {"status": "succes"}
    else:
        return {"status": "failed"}
