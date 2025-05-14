class Config:
    # Логирование
    LOG_FILE = "pro_editor.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Производительность
    MAX_HISTORY_STEPS = 20
    GPU_ACCELERATION = True
    THREAD_WORKERS = 4
    
    # Интерфейс
    CUSTOM_CSS = """
    <style>
        .stButton>button { transition: all 0.3s ease; }
        .stButton>button:hover { transform: scale(1.05); }
        .stDownloadButton>button { background: linear-gradient(45deg, #4CAF50, #45a049); }
    </style>
    """
    
    # AI
    AI_MODELS_DIR = "./models"
    DEFAULT_SEG_MODEL = "u2net_human_seg"