import logging
import streamlit as st
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from typing import Optional, Tuple
from rembg import remove

# Custom modules
from utils import (
    validate_image,
    mm_to_pixels,
    format_size,
    create_grid,
    apply_color_filters,
    apply_color_calibration,
    remove_background,
    replace_background,
    apply_advanced_filters,
    adjust_mask_parameters
)
from exceptions import InvalidImageError, ProcessingError
from config import Config
from presets import save_preset, load_preset, get_available_presets

# Configure logging
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format=Config.LOG_FORMAT
)

# Cache AI models for better performance
@st.cache_resource
def load_ai_models():
    return {
        'u2net': new_session("u2net"),
        'human_seg': new_session("u2net_human_seg")
    }

def main():
    st.set_page_config(
        page_title="Pro Photo Editor",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Session state initialization
    session_defaults = {
        'image': None,
        'processed_image': None,
        'mask': None,
        'history': [],
        'current_step': -1
    }
    for key, value in session_defaults.items():
        st.session_state.setdefault(key, value)

    # UI Configuration
    st.markdown(Config.CUSTOM_CSS, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🌄 Загрузка изображения")
        uploaded_file = st.file_uploader(
            "Перетащите файл или кликните для выбора",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=False,
            key="file_uploader"
        )
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                validate_image(image, min_size=(256, 256))
                st.session_state.image = image
                st.session_state.processed_image = image.copy()
                st.success("Изображение успешно загружено!")
            except Exception as e:
                st.error(f"Ошибка загрузки: {str(e)}")
                logging.exception("Image upload error")

        st.divider()
        st.header("⚙️ Глобальные настройки")
        Config.DEBUG = st.checkbox("Режим отладки", value=Config.DEBUG)
        dpi = st.slider("Разрешение печати (DPI)", 72, 1200, 300)
        show_histogram = st.checkbox("Показать гистограмму")
        watermark = st.text_input("Водяной знак")

    # Main tabs
    tab_names = ["🌈 Коррекция", "🌀 Фон", "🎭 Фильтры", "⏳ История", "💾 Экспорт"]
    tabs = st.tabs(tab_names)

    with tabs[0]:  # Correction tab
        if st.session_state.image:
            col1, col2, col3 = st.columns([1, 0.2, 1])
            
            with col1:
                st.subheader("Оригинал")
                st.image(st.session_state.image, use_column_width=True)
                if show_histogram:
                    display_histogram(st.session_state.image)

            with col3:
                st.subheader("Коррекция цвета")
                
                correction_type = st.radio(
                    "Тип коррекции",
                    ["Авто", "Ручная", "Пресет"],
                    horizontal=True
                )

                if correction_type == "Ручная":
                    temperature = st.slider("Температура (K)", 1000, 40000, 6500)
                    tint = st.slider("Оттенок", -100, 100, 0)
                    exposure = st.slider("Экспозиция", -1.0, 1.0, 0.0, 0.1)
                    gamma = st.slider("Гамма", 0.1, 4.0, 1.0, 0.1)

                elif correction_type == "Пресет":
                    presets = get_available_presets()
                    selected_preset = st.selectbox("Выберите пресет", presets)
                    if st.button("Загрузить пресет"):
                        preset_config = load_preset(selected_preset)
                        # Apply preset logic

                apply_correction = st.button("Применить коррекцию")
                
                if apply_correction:
                    try:
                        processed = apply_color_calibration(
                            st.session_state.image,
                            temperature=temperature,
                            tint=tint
                        )
                        update_image_state(processed)
                    except Exception as e:
                        handle_error(e)

                st.subheader("Результат")
                if st.session_state.processed_image:
                    st.image(st.session_state.processed_image, use_column_width=True)
                    if show_histogram:
                        display_histogram(st.session_state.processed_image)

    with tabs[1]:  # Background tab
        if st.session_state.image:
            bg_col1, bg_col2 = st.columns([1, 1])
            
            with bg_col1:
                st.subheader("Удаление фона")
                bg_model = st.selectbox(
                    "Модель сегментации",
                    ["Общая (u2net)", "Портреты (human_seg)"]
                )
                
                if st.button("Создать маску"):
                    try:
                        mask = remove_background(
                            st.session_state.image,
                            session=load_ai_models()[bg_model.split("(")[1][:-1]]
                        )
                        st.session_state.mask = mask
                        st.success("Маска создана!")
                    except Exception as e:
                        handle_error(e)

                if st.session_state.mask:
                    st.image(st.session_state.mask, use_column_width=True)
                    
                    st.subheader("Точная настройка")
                    erosion = st.slider("Эрозия", 0, 50, 0)
                    dilation = st.slider("Дилатация", 0, 50, 0)
                    feather = st.slider("Размытие границ", 0, 50, 5)
                    
                    st.session_state.mask = adjust_mask_parameters(
                        st.session_state.mask,
                        erosion=erosion,
                        dilation=dilation,
                        feather=feather
                    )

            with bg_col2:
                st.subheader("Замена фона")
                new_bg = st.file_uploader(
                    "Выберите фон",
                    type=["png", "jpg", "jpeg", "webp"]
                )
                
                if new_bg and st.session_state.mask:
                    background = Image.open(new_bg).convert("RGB")
                    blend_level = st.slider("Смешивание", 0.0, 1.0, 1.0)
                    
                    try:
                        replaced = replace_background(
                            st.session_state.processed_image,
                            background,
                            mask=st.session_state.mask,
                            blend=blend_level
                        )
                        update_image_state(replaced)
                        st.image(replaced, use_column_width=True)
                    except Exception as e:
                        handle_error(e)

    # Other tabs implementation...
    
def update_image_state(new_image: Image.Image):
    """Update image history for undo/redo functionality"""
    if len(st.session_state.history) >= Config.MAX_HISTORY_STEPS:
        st.session_state.history.pop(0)
    st.session_state.history.append(st.session_state.processed_image)
    st.session_state.processed_image = new_image
    st.session_state.current_step += 1

def display_histogram(img: Image.Image):
    """Display RGB histogram using Plotly"""
    import plotly.express as px
    hist_r = np.histogram(np.array(img)[:, :, 0], bins=256, range=(0, 255))[0]
    hist_g = np.histogram(np.array(img)[:, :, 1], bins=256, range=(0, 255))[0]
    hist_b = np.histogram(np.array(img)[:, :, 2], bins=256, range=(0, 255))[0]
    
    fig = px.line(
        title="RGB Histogram",
        labels={'value': 'Count', 'index': 'Intensity'}
    )
    fig.add_scatter(y=hist_r, line=dict(color='red'), name='Red')
    fig.add_scatter(y=hist_g, line=dict(color='green'), name='Green')
    fig.add_scatter(y=hist_b, line=dict(color='blue'), name='Blue')
    st.plotly_chart(fig, use_container_width=True)

def handle_error(e: Exception):
    """Universal error handler"""
    error_msg = f"Ошибка: {str(e)}"
    st.error(error_msg)
    logging.error(error_msg, exc_info=True)
    if Config.DEBUG:
        st.exception(e)

if __name__ == "__main__":
    main()