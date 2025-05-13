import json
from config import Config

def save_preset(name, data):
    preset_path = Config.PRESET_PATH / f"{name}.json"
    with open(preset_path, "w") as f:
        json.dump(data, f)

def load_preset(name):
    preset_path = Config.PRESET_PATH / f"{name}.json"
    with open(preset_path, "r") as f:
        return json.load(f)
