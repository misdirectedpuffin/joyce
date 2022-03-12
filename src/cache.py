"""Wrapper for redis.StrictRedis"""
import os
import pickle

from redis import StrictRedis

from constants import REDIS_CONFIG
from util import Singleton


class RedisClient(metaclass=Singleton):
    """RedisClient wrapper"""

    def __init__(self, host="redis", port=6379, db=0, password=None):
        self.client = StrictRedis(
            host=host, port=port, db=db, password=password
        )

    def ping(self):
        """Ping redis."""
        return self.client.ping()

    def get(self, key):
        """Get the value of a key"""
        return self.client.get(key)

    def get_obj(self, key):
        """Get and unpickle a python object"""
        pickled_obj = self.client.get(key)
        if pickled_obj is None:
            return None

        retval = pickle.loads(pickled_obj)
        return retval

    def setnx(self, key, val):
        """Set a value if it doesn't exist at a given key"""
        return self.client.setnx(key, val)

    def set_obj(self, key, obj, timeout_secs=None):
        """Pickle and set an object."""
        pickled_obj = pickle.dumps(obj)
        self.client.set(key, pickled_obj, ex=timeout_secs)


def redis_client():
    """Configure redis client, given an environment."""
    return RedisClient(**REDIS_CONFIG[os.getenv("FLASK_ENV", "development")])
