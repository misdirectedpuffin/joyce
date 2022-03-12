"""Healthcheck blueprints"""
from random import randint
from flask import Blueprint, jsonify

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/random", methods=["GET"])
def random():
    """Return a random integer."""
    return jsonify(random_integer=randint(1, 100), success=True)