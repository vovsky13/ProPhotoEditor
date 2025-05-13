import streamlit as st
from PIL import Image
from config import Config
from utils import create_grid
from processing import process_image
from presets import save_preset, load_preset

Config.ensure_directories()

def main():
    st.set_page_config(page_title="Pro Photo Editor", layout="wide")
    st.title("📸 Pro Photo Editor")

    uploaded_files = st.file_uploader("Загрузите фото", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    with st.sidebar:
        st.header("Настройки")
        template_choice = st.selectbox("Шаблон документа", list(Config.TEMPLATES_MM.keys()))
        dpi_choice = st.selectbox("Качество (DPI)", Config.DPI_VALUES, index=2)
        model_choice = st.selectbox("AI Модель", list(Config.AI_MODELS.keys()))

        brightness = st.slider("Яркость", 0.5, 2.0, 1.0, 0.1)
        contrast = st.slider("Контраст", 0.5, 2.0, 1.0, 0.1)
        saturation = st.slider("Насыщенность", 0.0, 2.0, 1.0, 0.1)
        gamma = st.slider("Гамма", 0.5, 2.0, 1.0, 0.1)

        preset_name = st.text_input("Название пресета")
        if st.button("💾 Сохранить пресет"):
            settings = {
                "template": template_choice,
                "dpi": dpi_choice,
                "model": model_choice,
                "brightness": brightness,
                "contrast": contrast,
                "saturation": saturation,
                "gamma": gamma,
            }
            save_preset(preset_name, settings)
            st.success(f"Пресет '{preset_name}' сохранён!")

    for uploaded_file in uploaded_files:
        with st.expander(f"Обработка: {uploaded_file.name}", expanded=True):
            original_image = Image.open(uploaded_file)
            st.image(original_image, caption="Исходное изображение", use_column_width=True)

            if st.checkbox("Показать сетку"):
                grid_color = st.color_picker("Цвет сетки", "#FF0000")
                grid_image = create_grid(original_image.copy(), grid_color)
                st.image(grid_image, caption="Сетка", use_column_width=True)

            if st.button(f"🚀 Обработать {uploaded_file.name}"):
                template_mm = Config.TEMPLATES_MM[template_choice]
                processed_img = process_image(original_image, template_mm, dpi_choice, model_choice, brightness, contrast, saturation, gamma)
                st.image(processed_img, caption="Результат", use_column_width=True)

if name == "__main__":
    main()