import streamlit as st
from PIL import Image
from config import Config
from utils import create_grid
from processing import process_image, export_to_pdf
from presets import save_preset

Config.ensure_directories()

def main():
    st.set_page_config(page_title="📸 Pro Фото на Документы", layout="wide")
    st.title("📸 Pro Фото на Документы")

    uploaded_files = st.file_uploader("Загрузите фото", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    with st.sidebar:
        st.header("Настройки")
        template_choice = st.selectbox("Формат", list(Config.TEMPLATES_MM.keys()))
        dpi_choice = st.selectbox("Качество (DPI)", Config.DPI_VALUES, index=2)
        model_choice = st.selectbox("AI Модель", Config.AI_MODELS)
        background_color = st.color_picker("Фон после удаления", "#FFFFFF")

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
                "background_color": background_color,
                "brightness": brightness,
                "contrast": contrast,
                "saturation": saturation,
                "gamma": gamma,
            }
            save_preset(preset_name, settings)
            st.success(f"Пресет '{preset_name}' сохранён!")

    if uploaded_files:
        processed_images = []
        for uploaded_file in uploaded_files:
            with st.expander(f"Обработка: {uploaded_file.name}", expanded=True):
                original_image = Image.open(uploaded_file).convert("RGB")
                st.image(original_image, caption="Исходное изображение", use_column_width=True)

                if st.checkbox("Показать сетку", key=uploaded_file.name):
                    grid_image = create_grid(original_image.copy())
                    st.image(grid_image, caption="Сетка", use_column_width=True)

                if st.button(f"🚀 Обработать {uploaded_file.name}"):
                    template_mm = Config.TEMPLATES_MM[template_choice]
                    processed_img = process_image(
                        original_image,
                        template_mm,
                        dpi_choice,
                        model_choice,
                        background_color,
                        brightness,
                        contrast,
                        saturation,
                        gamma
                    )
                    st.image(processed_img, caption="Результат", use_column_width=True)
                    processed_images.append(processed_img)

        if processed_images:
            if st.button("📄 Экспортировать PDF 10x15"):
                pdf_path = export_to_pdf(processed_images)
                st.success("PDF успешно создан!")
                st.download_button("⬇️ Скачать PDF", data=open(pdf_path, "rb"), file_name="document_photos.pdf")

if __name__ == "__main__":
    main()