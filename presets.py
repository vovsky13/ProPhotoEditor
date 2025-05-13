import json
from config import Config

def save_preset(name, settings):
    path = Config.PRESET_PATH / f"{name}.json"
    with open(path, "w") as f:
        json.dump(settings, f, indent=4)

def load_preset(name):
    path = Config.PRESET_PATH / f"{name}.json"
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return None