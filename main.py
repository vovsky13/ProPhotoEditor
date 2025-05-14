def main():
import logging
import streamlit as st
from PIL import Image
from io import BytesIO
from utils import (
    validate_image,
    mm_to_pixels,
    format_size,
    create_grid,
    apply_color_filters,
    apply_color_calibration
)
from exceptions import InvalidImageError, ProcessingError
from config import Config

# Настройка логирования
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    st.set_page_config(page_title="Pro Photo Editor", layout="wide")
    st.title("🎨 Pro Photo Editor")
    
    # Инициализация сессионных переменных
    if "image" not in st.session_state:
        st.session_state.image = None
    if "processed_image" not in st.session_state:
        st.session_state.processed_image = None

    # Сайдбар для загрузки и базовых настроек
    with st.sidebar:
        st.header("⚙️ Настройки")
        uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                validate_image(image)
                st.session_state.image = image
                st.success("Изображение загружено!")
            except InvalidImageError as e:
                st.error(str(e))
            except Exception as e:
                logging.error(f"Ошибка загрузки: {str(e)}")
                st.error("Неподдерживаемый формат файла")

        st.divider()
        dpi = st.slider("DPI для печати", 72, 600, 300)
        show_grid = st.checkbox("Показать сетку")
        grid_spacing = st.slider("Шаг сетки (мм)", 1, 100, 10) if show_grid else 10

    # Основные вкладки
    tab1, tab2, tab3 = st.tabs(["📷 Коррекция", "🎚️ Фильтры", "💾 Экспорт"])

    with tab1:
        if st.session_state.image:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Оригинал")
                st.image(st.session_state.image, use_column_width=True)

            with col2:
                st.subheader("Калибровка цвета")
                temperature = st.slider("Температура (K)", 1000, 40000, 6500)
                tint = st.slider("Оттенок", -100, 100, 0)
                
                if st.button("Применить калибровку"):
                    try:
                        processed = apply_color_calibration(
                            st.session_state.image,
                            temperature=temperature,
                            tint=tint
                        )
                        if show_grid:
                            processed = create_grid(processed, spacing=mm_to_pixels(grid_spacing, dpi))
                        st.session_state.processed_image = processed
                    except ProcessingError as e:
                        st.error(str(e))
                        logging.error(f"Ошибка калибровки: {str(e)}")

                if st.session_state.processed_image:
                    st.subheader("Результат")
                    st.image(st.session_state.processed_image, use_column_width=True)

    with tab2:
        if st.session_state.image:
            brightness = st.slider("Яркость", 0.0, 2.0, 1.0, 0.1)
            contrast = st.slider("Контраст", 0.0, 2.0, 1.0, 0.1)
            saturation = st.slider("Насыщенность", 0.0, 2.0, 1.0, 0.1)
            gamma = st.slider("Гамма", 0.1, 3.0, 1.0, 0.1)

            if st.button("Применить фильтры"):
                try:
                    processed = apply_color_filters(
                        st.session_state.image,
                        brightness=brightness,
                        contrast=contrast,
                        saturation=saturation,
                        gamma=gamma
                    )
                    if show_grid:
                        processed = create_grid(processed, spacing=mm_to_pixels(grid_spacing, dpi))
                    st.session_state.processed_image = processed
                except ProcessingError as e:
                    st.error(str(e))
                    logging.error(f"Ошибка фильтров: {str(e)}")

    with tab3:
        if st.session_state.processed_image:
            # Информация о размере
            size_info = format_size(st.session_state.processed_image.size)
            st.metric("Размер изображения", size_info)
            
            # Пресеты
            preset_name = st.text_input("Название пресета")
            if st.button("Сохранить пресет"):
                save_preset(preset_name, {
                    'temperature': temperature,
                    'tint': tint,
                    'brightness': brightness,
                    'contrast': contrast
                })
                st.success("Пресет сохранен!")

            # Экспорт
            buf = BytesIO()
            st.session_state.processed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Скачать изображение",
                data=byte_im,
                file_name="processed_image.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
 tab4, tab5 = st.tabs(["🌀 Фон", "🎭 Пресет-фильтры"])

    with tab4:
        if st.session_state.image:
            col1, col2, col3 = st.columns([1,1,1])
            
            with col1:
                st.subheader("Оригинал")
                st.image(st.session_state.image, use_column_width=True)
                
            with col2:
                if st.button("Удалить фон"):
                    try:
                        bg_removed = remove_background(st.session_state.image)
                        st.session_state.processed_image = bg_removed
                    except Exception as e:
                        st.error(f"Ошибка удаления фона: {str(e)}")
                        
                new_bg = st.file_uploader("Загрузите новый фон", type=["jpg", "png"])
                border_size = st.slider("Сглаживание границ", 1, 20, 5)
                blend_level = st.slider("Смешивание с фоном", 0.0, 1.0, 1.0)
                
            with col3:
                if st.session_state.processed_image and new_bg:
                    background_img = Image.open(new_bg)
                    replaced = replace_background(
                        st.session_state.processed_image,
                        background_img,
                        border_pixels=border_size,
                        blur_radius=int(blend_level*10)
                    st.image(replaced, use_column_width=True)

    with tab5:
        if st.session_state.image:
            preset = st.selectbox("Выберите фильтр", 
                ['clarendon', 'gingham', 'moon', 'lark', 'juno'])
            intensity = st.slider("Интенсивность", 0.0, 1.0, 0.8)
            
            preview = apply_advanced_filters(
                st.session_state.image, 
                filter_type=preset,
                intensity=intensity)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(st.session_state.image, caption="Оригинал")
            with col2:
                st.image(preview, caption=f"Фильтр: {preset}")