from PIL import Image, ImageEnhance, ImageDraw

def mm_to_pixels(mm: float, dpi: int) -> int:
    return int(mm * dpi / 25.4)

def apply_color_calibration(img, brightness, contrast, saturation, gamma):
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)
    img = img.point(lambda p: 255 * ((p / 255) ** gamma))
    return img

def create_grid(image, color="#FF0000"):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=color)
    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill=color)
    return image