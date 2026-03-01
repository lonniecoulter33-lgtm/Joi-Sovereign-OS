import os
import json
try:
    import yaml
    yaml_available = True
except ImportError:
    yaml_available = False


def get_config_file_paths(directory):
    """Scan the given directory and return a list of paths to config files."""
    config_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.json', '.yaml', '.yml')):
                config_files.append(os.path.join(root, file))
    return config_files


def parse_config_file(file_path):
    """Parse the config file based on its extension."""
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif yaml_available and file_path.endswith(('.yaml', '.yml')):
            return yaml.safe_load(file)
        else:
            raise ValueError("Unsupported config file format: " + file_path)




def extract_models_info(dir_path):
    """Extract model information from the parsed config data."""
    models_info = []
    try:
        config_file_paths = get_config_file_paths(dir_path)
    except Exception as e:
        return []
    for file_path in config_file_paths:
        try:
            config_data = parse_config_file(file_path)
        except Exception as e:
            continue
        if 'models' in config_data:
            models_info.extend(config_data['models'])
    return models_info
