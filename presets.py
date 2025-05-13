import os
import json
from config import Config

def save_preset(preset_name, settings):
    filepath = os.path.join(Config.PRESET_PATH, f"{preset_name}.json")
    with open(filepath, "w") as file:
        json.dump(settings, file)

def load_preset(preset_name):
    filepath = os.path.join(Config.PRESET_PATH, f"{preset_name}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return None

def delete_preset(preset_name):
    filepath = os.path.join(Config.PRESET_PATH, f"{preset_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)