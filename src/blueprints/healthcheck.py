"""Healthcheck blueprints"""
from flask import Blueprint, jsonify

bp = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")


@bp.route("/", methods=["GET"])
def healthcheck():
    """ALB healthcheck."""
    return jsonify(resp='yes')

@bp.route("/ok", methods=["GET"])
def ok():
    """ALB healthcheck."""
    return '', 200

