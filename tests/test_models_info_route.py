import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch

# Assuming the Flask app is defined in a module named app
from app import app as flask_app


def test_models_info_route(monkeypatch):
    # Mock data to return from extract_models_info
    mock_data = {
        "models": [
            {"name": "Model A", "version": "1.0"},
            {"name": "Model B", "version": "2.0"}
        ]
    }

    # Mock function to replace extract_models_info
    def mock_extract_models_info():
        return mock_data

    # Use monkeypatch to replace extract_models_info with mock function
    monkeypatch.setattr('app.extract_models_info', mock_extract_models_info)

    # Create a test client for the Flask app
    client: FlaskClient = flask_app.test_client()

    # Send GET request to /models_info
    response = client.get('/models_info')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response data matches the mock data
    assert response.get_json() == mock_data
