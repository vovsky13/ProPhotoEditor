from PIL import Image, ImageDraw, ImageEnhance
import numpy as np

def mm_to_pixels(mm, dpi):
    return int((mm / 25.4) * dpi)

def apply_color_calibration(img, brightness, contrast, saturation, gamma):
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)
    gamma_lut = [255 * (i / 255) ** (1.0 / gamma) for i in range(256)]
    return img.point(gamma_lut)

def create_grid(image, color, spacing=50):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=color, width=1)

    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=color, width=1)

    return image