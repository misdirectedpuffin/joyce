"""Healthcheck unit tests"""
import pytest


@pytest.mark.parametrize(
    "method,uri,status",
    [
        ("get", "/healthcheck/", 200),
        ("get", "/healthcheck/db", 200),
        ("get", "/healthcheck/redis", 200),
    ],
)
def test_status_codes(method, uri, status, client):
    """It tests it returns the expected status codes."""
    assert getattr(client, method)(uri).status_code == status


@pytest.mark.parametrize(
    "method,uri,content",
    [
        ("get", "/healthcheck/", "application/json"),
        ("get", "/healthcheck/db", "application/json"),
        ("get", "/healthcheck/redis", "application/json"),
    ],
)
def test_content_types(method, uri, content, client):
    """It tests it returns the expected content type."""
    assert getattr(client, method)(uri).content_type == content
