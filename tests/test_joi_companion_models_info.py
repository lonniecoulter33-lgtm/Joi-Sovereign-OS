import os
import json
import tempfile
import unittest
from flask import Flask
from flask.testing import FlaskClient

# Assume the app and route are defined in joi_companion
from joi_companion import create_app

class TestModelsInfoEndpoint(unittest.TestCase):
    def setUp(self):
        """Set up a temporary directory and Flask test client"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app()
        self.client: FlaskClient = self.app.test_client()

    def tearDown(self):
        """Clean up the temporary directory"""
        self.temp_dir.cleanup()

    def test_models_info_endpoint(self):
        """Test the /models_info endpoint with a temporary directory"""
        response = self.client.get(f'/models_info?dir={self.temp_dir.name}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected_data = self.get_expected_models_info()
        self.assertEqual(data, expected_data)

    def get_expected_models_info(self):
        """Generate expected models info from the temp directory"""
        # This function should return the expected JSON data structure
        # based on the contents of the temporary directory
        return {
            "models": []  # Example structure, adjust according to actual expected data
        }

if __name__ == '__main__':
    unittest.main()
