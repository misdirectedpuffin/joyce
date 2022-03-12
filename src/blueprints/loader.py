"""Healthcheck blueprints"""
from flask import Blueprint, jsonify

from cache import redis_client
from loader import write, load_rows

import requests

bp = Blueprint("loader", __name__, url_prefix="/db")


@bp.route("/load", methods=["GET"])
def load():
    """load dara."""
    # r = requests.get('http://backend.dagster/backend/random', verify=False)
    rows = load_rows("/usr/src/app/test.csv")
    write(rows)
    return jsonify(resp='yes')