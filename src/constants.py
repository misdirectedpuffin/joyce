"""Application constants"""

import os

DATABASE_CONFIG = {
    "development": {
        "username": os.environ.get("POSTGRES_USER", "postgres"),
        "password": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "host": os.environ.get("POSTGRES_HOST", "pgdb"),
        "port": os.environ.get("POSTGRES_PORT", 5432),
        "db": os.environ.get("POSTGRES_DB", "postgres"),
    },
    "testing": {
        "username": "postgres",
        "password": "postgres",
        "host": "postgres",
        "port": 5432,
        "db": "testing",
    },
}

REDIS_CONFIG = {
    "development": {
        "host": os.environ.get("REDIS_HOST", "redis"),
        "port": os.environ.get("REDIS_PORT", 6379),
        "db": os.environ.get("REDIS_DB", 0),
    },
    "testing": {
        "host": os.environ.get("REDIS_HOST", "redis"),
        "port": os.environ.get("REDIS_PORT", 6379),
        "db": os.environ.get("REDIS_DB", 0),
    },
}
