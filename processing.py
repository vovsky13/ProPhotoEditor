from PIL import ImageOps
from utils import mm_to_pixels, apply_color_calibration
from ai_models import remove_background

def process_image(image, template_mm, dpi, model_type, brightness, contrast, saturation, gamma):
    processed_img = remove_background(image, model_type)
    processed_img = apply_color_calibration(processed_img, brightness, contrast, saturation, gamma)

    target_size = (mm_to_pixels(template_mm[0], dpi), mm_to_pixels(template_mm[1], dpi))
    processed_img = ImageOps.fit(processed_img.convert("RGB"), target_size, method=Image.Resampling.LANCZOS)

    return processed_img