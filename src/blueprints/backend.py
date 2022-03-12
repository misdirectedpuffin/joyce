"""Healthcheck blueprints"""
from random import randint
from flask import Blueprint, jsonify

bp = Blueprint("backend", __name__, url_prefix="/backend")

@bp.route("/random", methods=["GET"])
def random():
    """Return a random integer."""
    return jsonify(random_integer=randint(1, 100), success=True)