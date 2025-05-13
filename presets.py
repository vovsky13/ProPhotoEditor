import os
import json
from pathvalidate import sanitize_filename
from config import Config

def save_preset(preset_name, settings):
    try:
        os.makedirs(Config.PRESET_PATH, exist_ok=True)
        safe_name = sanitize_filename(preset_name)
        filepath = os.path.join(Config.PRESET_PATH, f"{safe_name}.json")
        
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=2)
        return True
    except Exception as e:
        print(f"Preset save error: {str(e)}")
        return False

def load_preset(preset_name):
    try:
        safe_name = sanitize_filename(preset_name)
        filepath = os.path.join(Config.PRESET_PATH, f"{safe_name}.json")
        
        if not os.path.exists(filepath):
            return None
            
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Preset load error: {str(e)}")
        return None

def delete_preset(preset_name):
    try:
        safe_name = sanitize_filename(preset_name)
        filepath = os.path.join(Config.PRESET_PATH, f"{safe_name}.json")
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Preset delete error: {str(e)}")
        return False

def list_presets():
    try:
        return [f[:-5] for f in os.listdir(Config.PRESET_PATH) 
               if f.endswith(".json")]
    except FileNotFoundError:
        return []