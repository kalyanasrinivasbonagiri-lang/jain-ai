import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from jain_ai.app_factory import create_app


def test_home_route_get():
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_missing_route_returns_404_not_500():
    app = create_app()
    client = app.test_client()
    response = client.get("/does-not-exist")
    assert response.status_code == 404


def test_favicon_route_is_available():
    app = create_app()
    client = app.test_client()
    response = client.get("/favicon.ico")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/static/favicon.svg")
