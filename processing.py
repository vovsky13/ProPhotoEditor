from PIL import Image, ImageOps
from utils import mm_to_pixels, apply_color_calibration
from ai_models import remove_background
import tempfile

def process_image(image, template_mm, dpi, model_type, background_color, brightness, contrast, saturation, gamma):
    image = remove_background(image, model_type, background_color)
    image = apply_color_calibration(image, brightness, contrast, saturation, gamma)
    size = (mm_to_pixels(template_mm[0], dpi), mm_to_pixels(template_mm[1], dpi))
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS)

def export_to_pdf(images, dpi=300, layout=(2, 3)):
    photo_w, photo_h = mm_to_pixels(35, dpi), mm_to_pixels(45, dpi)
    page_w, page_h = mm_to_pixels(100, dpi), mm_to_pixels(150, dpi)
    page = Image.new("RGB", (page_w, page_h), "white")
    x_margin = (page_w - layout[0] * photo_w) // 2
    y_margin = (page_h - layout[1] * photo_h) // 2

    for i, img in enumerate(images[: layout[0] * layout[1]]):
        resized = img.resize((photo_w, photo_h))
        x = x_margin + (i % layout[0]) * photo_w
        y = y_margin + (i // layout[0]) * photo_h
        page.paste(resized, (x, y))

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    page.save(temp_file.name, "PDF", resolution=dpi)
    return temp_file.name