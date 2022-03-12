"""Unit test fixtures"""

import pytest
from flask import Flask

from bootstrap import create_app
from extensions import db


@pytest.fixture
def client():
    """Create a test client."""
    instance = Flask("test")
    instance.testing = True

    app = create_app(instance, "testing")

    with app.test_client() as test_client:
        with app.app_context() as ctx:
            ctx.push()
            db.create_all()
            db.session.commit()
        yield test_client
    db.session.remove()
    db.drop_all()
