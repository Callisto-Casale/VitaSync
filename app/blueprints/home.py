import subprocess

from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():

    result = subprocess.run(["pihole", "status"], capture_output=True, text=True)
    is_enabled = "enabled" in result.stdout.lower()

    return render_template("index.html", is_enabled=is_enabled)
