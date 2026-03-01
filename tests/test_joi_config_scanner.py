import pytest
import os
import tempfile
import json
import yaml
from joi_config_scanner import extract_models_info

class TestExtractModelsInfo:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Sample JSON configuration
        self.json_config = {
            "models": [
                {"name": "model1", "version": "v1"},
                {"name": "model2", "version": "v2"}
            ]
        }
        # Sample YAML configuration
        self.yaml_config_no_models = """
        no_models_here: true
        """

        self.json_config_no_models = {
            "no_models_here": True
        }
        self.yaml_config = """
        models:
          - name: model1
            version: v1
          - name: model2
            version: v2
        """

    def test_extract_models_info_from_json(self):
        global temp_json_file_path
        temp_json_file_path = ''
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w+', delete=False) as temp_json_file:
            json.dump(self.json_config, temp_json_file)
            temp_json_file_path = temp_json_file.name
            temp_json_file.seek(0)
            models_info = extract_models_info(temp_json_file.name)
            expected_info = [
                {"name": "model1", "version": "v1"},
                {"name": "model2", "version": "v2"}
            ]
            assert models_info == expected_info

    @pytest.fixture(autouse=True)
    def teardown_method(self, request):
        global temp_json_file_path, temp_yaml_file_path
        temp_json_file_path = ''
        temp_yaml_file_path = ''
        if temp_json_file_path and os.path.exists(temp_json_file_path):
            os.remove(temp_json_file_path)
        if temp_yaml_file_path and os.path.exists(temp_yaml_file_path):
            os.remove(temp_yaml_file_path)

    def test_extract_models_info_with_temp_json_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, 'config.json')
            with open(config_path, 'w') as config_file:
                json.dump(self.json_config, config_file)
            models_info = extract_models_info(config_path)
            expected_info = [
                {"name": "model1", "version": "v1"},
                {"name": "model2", "version": "v2"}
            ]
            assert models_info == expected_info

    def test_extract_models_info_from_yaml(self):
        global temp_yaml_file_path
        temp_yaml_file_path = ''
        with tempfile.NamedTemporaryFile(suffix='.yaml', mode='w+', delete=False) as temp_yaml_file:
            temp_yaml_file.write(self.yaml_config_no_models)
            temp_yaml_file.seek(0)
            temp_yaml_file_path = temp_yaml_file.name
            models_info = extract_models_info(temp_yaml_file.name)
            expected_info = []
            assert models_info == expected_info

    def test_extract_models_info_from_json_no_models(self):
        global temp_json_file_path
        temp_json_file_path = ''
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w+', delete=False) as temp_json_file:
            json.dump(self.json_config_no_models, temp_json_file)
            temp_json_file.seek(0)
            temp_json_file_path = temp_json_file.name
            models_info = extract_models_info(temp_json_file.name)
            expected_info = []
            assert models_info == expected_info
        global temp_yaml_file_path
        temp_yaml_file_path = ''
        with tempfile.NamedTemporaryFile(suffix='.yaml', mode='w+', delete=False) as temp_yaml_file:
            temp_yaml_file.write(self.yaml_config)
            temp_yaml_file.seek(0)
            temp_yaml_file_path = temp_yaml_file.name
            models_info = extract_models_info(temp_yaml_file.name)
            expected_info = [
                {"name": "model1", "version": "v1"},
                {"name": "model2", "version": "v2"}
            ]
            assert models_info == expected_info


