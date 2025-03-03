import subprocess

from flask import Blueprint, redirect

github_bp = Blueprint("github", __name__)


@github_bp.route("/reload", methods=["POST", "GET"])
def github_reload():
    subprocess.run(["git", "pull"])
    return redirect("/")
