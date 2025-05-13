import os

class Config:
    TEMPLATES_MM = {
        "Паспорт РФ (35x45 мм)": (35, 45),
        "Виза США (50x50 мм)": (50, 50),
        "Водительские права (35x45 мм)": (35, 45),
    }
    DPI_VALUES = [96, 150, 300, 600]
    SUPPORTED_FORMATS = ["PNG", "JPEG", "PDF"]
    AI_MODELS = {
        "Базовая": "u2net",
        "Высокая точность": "u2netp",
        "Человеки": "u2net_human_seg"
    }
    PRESET_PATH = "assets/presets"

    @staticmethod
    def ensure_directories():
        os.makedirs(Config.PRESET_PATH, exist_ok=True)