import json
from pathlib import Path
from config import Config

def save_preset(name, settings):
    preset_path = Config.PRESET_PATH / f"{name}.json"
    with open(preset_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

def load_preset(name):
    preset_path = Config.PRESET_PATH / f"{name}.json"
    if preset_path.exists():
        with open(preset_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def get_available_presets():
    return [p.stem for p in Config.PRESET_PATH.glob("*.json")]

def delete_preset(name):
    preset_path = Config.PRESET_PATH / f"{name}.json"
    if preset_path.exists():
        preset_path.unlink()
