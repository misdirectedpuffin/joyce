"""Healthcheck blueprints"""
from flask import Blueprint, jsonify

from cache import redis_client
# from models.model import add_and_query

import requests

bp = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")


@bp.route("/", methods=["GET"])
def healthcheck():
    """ALB healthcheck."""
    # r = requests.get('http://backend.dagster/backend/random', verify=False)
    return jsonify(resp='yes')

@bp.route("/ok", methods=["GET"])
def ok():
    """ALB healthcheck."""
    return '', 200

# @bp.route("/db", methods=["GET"])
# def dbcheck():
#     """Postgres check."""
    users = add_and_query()
#     data = [{"username": user.username, "email": user.email} for user in users]
#     return jsonify(data)


# @bp.route("/redis", methods=["GET"])
# def redis_check():
#     """Ping the redis instance."""
#     client = redis_client()
#     client.set_obj("foo", {"thing": "bar"})
#     response = client.get_obj("foo")
#     return jsonify({"data": response})
