import json
from pathlib import Path

config_dir = Path.cwd() /".config" 
config_file = config_dir / "config.json"

def load_config():
    if config_file.exists():
        with open(config_file, "r") as f:
            return json.load(f)
    return None

def save_config(config_data):
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)

def get_api_key():
    with open(config_file, 'r') as f:
        data = json.load(f)
        return data["api"]["key"]

def get_city_name():
    with open(config_file, 'r') as f:
        data = json.load(f)
        return data["defaults"]["location"]
    
def config_file_location():
    return config_file