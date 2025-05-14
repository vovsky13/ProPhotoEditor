"""
Professional Document Photo Editor Application

Features:
- Batch image processing with AI-powered background removal
- Customizable document templates and export settings
- Preset management system
- Real-time adjustments with preview
"""

import streamlit as st
from PIL import Image
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
import time

from config import Config
from utils import create_grid, validate_image, format_size
from processing import process_image
from presets import save_preset, load_preset, get_available_presets
from exceptions import InvalidImageError, ProcessingError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(Config.LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

Config.ensure_directories()

def handle_image_processing(uploaded_file, settings: Dict) -> Optional[Image.Image]:
    """Process and display image with given settings"""
    try:
        with st.spinner(f"Обработка {uploaded_file.name}..."):
            start_time = time.time()
            
            # Validate and load image
            original_image = Image.open(uploaded_file).convert("RGB")
            validate_image(original_image)
            
            # Processing
            processed_img = process_image(
                image=original_image,
                template_mm=Config.TEMPLATES_MM[settings["template"]],
                dpi=settings["dpi"],
                model_name=settings["model"],
                bg_color=settings["background_color"],
                brightness=settings["brightness"],
                contrast=settings["contrast"],
                saturation=settings["saturation"],
                gamma=settings["gamma"]
            )
            
            # Log performance
            processing_time = time.time() - start_time
            logger.info(f"Processed {uploaded_file.name} ({original_image.size}) in {processing_time:.2f}s")
            
            return processed_img

    except InvalidImageError as e:
        logger.error(f"Invalid image error: {str(e)}")
        st.error(f"Ошибка валидации изображения: {str(e)}")
    except ProcessingError as e:
        logger.error(f"Processing error: {str(e)}")
        st.error(f"Ошибка обработки изображения: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        st.error("Непредвиденная ошибка при обработке.")
    return None

def create_sidebar() -> Dict:
    """Create sidebar controls and return settings dictionary"""
    st.sidebar.header("⚙️ Настройки обработки")
    
    # Preset management
    presets = get_available_presets()
    selected_preset = st.sidebar.selectbox("Загрузить пресет", ["Custom"] + presets)
    
    # Initialize settings with defaults
    settings = {
        "template": Config.DEFAULT_TEMPLATE,
        "dpi": Config.DEFAULT_DPI,
        "model": Config.DEFAULT_MODEL,
        "background_color": Config.DEFAULT_BG_COLOR,
        "brightness": Config.DEFAULT_BRIGHTNESS,
        "contrast": Config.DEFAULT_CONTRAST,
        "saturation": Config.DEFAULT_SATURATION,
        "gamma": Config.DEFAULT_GAMMA,
    }

    # Load preset
    if selected_preset != "Custom":
        preset_settings = load_preset(selected_preset)
        if preset_settings:
            settings.update(preset_settings)
            st.sidebar.success(f"Пресет '{selected_preset}' загружен")
        else:
            st.sidebar.error("Ошибка загрузки пресета")

    # Template settings
    settings["template"] = st.sidebar.selectbox(
        "Формат документа",
        options=list(Config.TEMPLATES_MM.keys()),
        index=list(Config.TEMPLATES_MM.keys()).index(settings["template"])
    )

    # Quality settings
    col1, col2 = st.sidebar.columns(2)
    with col1:
        settings["dpi"] = st.selectbox(
            "Разрешение (DPI)",
            options=Config.DPI_VALUES,
            index=Config.DPI_VALUES.index(settings["dpi"])
        )
    with col2:
        settings["model"] = st.selectbox(
            "AI Модель",
            options=Config.AI_MODELS,
            index=Config.AI_MODELS.index(settings["model"])
        )

    # Color adjustments
    st.sidebar.subheader("🎨 Коррекция цвета")
    settings["background_color"] = st.sidebar.color_picker(
        "Цвет фона",
        value=settings["background_color"]
    )
    
    settings["brightness"] = st.sidebar.slider(
        "Яркость",
        min_value=0.5, max_value=2.0,
        value=settings["brightness"], step=0.1
    )
    settings["contrast"] = st.sidebar.slider(
        "Контраст",
        min_value=0.5, max_value=2.0,
        value=settings["contrast"], step=0.1
    )
    settings["saturation"] = st.sidebar.slider(
        "Насыщенность",
        min_value=0.0, max_value=2.0,
        value=settings["saturation"], step=0.1
    )
    settings["gamma"] = st.sidebar.slider(
        "Гамма-коррекция",
        min_value=0.5, max_value=2.0,
        value=settings["gamma"], step=0.1
    )

    # Preset saving
    st.sidebar.subheader("💾 Сохранение пресета")
    preset_name = st.sidebar.text_input("Название пресета")
    if st.sidebar.button("Сохранить текущие настройки"):
        if preset_name and preset_name != "Custom":
            try:
                save_preset(preset_name, settings)
                st.sidebar.success(f"Пресет '{preset_name}' сохранён")
            except Exception as e:
                st.sidebar.error(f"Ошибка сохранения: {str(e)}")
        else:
            st.sidebar.error("Введите корректное имя пресета")

    return settings

def main():
    """Основная функция приложения"""
    st.set_page_config(
        page_title="📸 Pro Редактор Фото на Документы",
        page_icon="📷",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Заголовок приложения
    st.title("📸 Pro Редактор Фото на Документы")
    st.markdown("""
        **Профессиональная обработка фотографий для документов**  
        Загрузите фото и настройте параметры обработки
    """)
    
    # Загрузка файлов
    uploaded_files = st.file_uploader(
        "ПЕРЕТАЩИТЕ ФОТО СЮДА",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Максимальное количество файлов: 10"
    )
    
    # Лимит файлов
    if uploaded_files and len(uploaded_files) > 10:
        st.error("Максимальное количество файлов: 10")
        uploaded_files = uploaded_files[:10]

    # Получение настроек
    processing_settings = create_sidebar()
    
    # Обработка
    if uploaded_files:
        if st.button("🚀 Начать обработку", type="primary"):
            st.subheader(f"🖼 Обработка {len(uploaded_files)} изображений")
            progress_bar = st.progress(0)
            success_count = 0
            
            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    with st.container():
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            original_image = Image.open(uploaded_file).convert("RGB")
                            st.image(original_image, 
                                   caption=f"Исходное: {uploaded_file.name}",
                                   use_column_width=True)
                            
                            if st.checkbox("Показать сетку", key=f"grid_{i}"):
                                grid_image = create_grid(original_image.copy())
                                st.image(grid_image, 
                                       caption="Сетка выравнивания",
                                       use_column_width=True)

                        with col2:
                            processed_img = handle_image_processing(uploaded_file, processing_settings)
                            if processed_img:
                                st.image(processed_img, 
                                       caption="Результат обработки",
                                       use_column_width=True)
                                
                                # Кнопка скачивания
                                img_bytes = processed_img.tobytes()
                                st.download_button(
                                    label="⬇️ Скачать результат",
                                    data=img_bytes,
                                    file_name=f"processed_{uploaded_file.name}",
                                    mime="image/jpeg",
                                    key=f"download_{i}"
                                )
                                success_count += 1

                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                except Exception as e:
                    logger.error(f"Ошибка обработки {uploaded_file.name}: {str(e)}")
                    st.error(f"Ошибка обработки {uploaded_file.name}: {str(e)}")

            # Итоговое сообщение
            if success_count > 0:
                st.success(f"✅ Успешно обработано {success_count}/{len(uploaded_files)} изображений")
                st.balloons()
            else:
                st.error("⚠️ Обработка не удалась для всех файлов")

if __name__ == "__main__":
    main()
