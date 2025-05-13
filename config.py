from pathlib import Path

class Config:
    TEMPLATES_MM = {
        "A4": (210, 297),
        "Passport": (88, 125),
        "Square": (100, 100)
    }
    
    DPI_VALUES = [150, 300, 600]
    AI_MODELS = ["U2Net", "DeepLabV3"]
    PRESET_PATH = Path(__file__).parent / "presets"

    @classmethod
    def ensure_directories(cls):
        cls.PRESET_PATH.mkdir(parents=True, exist_ok=True)