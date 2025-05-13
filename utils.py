from PIL import Image, ImageEnhance

def mm_to_pixels(mm: float, dpi: int) -> int:
    return int(mm * dpi / 25.4)

def apply_color_calibration(img, brightness, contrast, saturation, gamma):
    # Яркость
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)
    
    # Контраст
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    
    # Насыщенность
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)
    
    # Гамма-коррекция
    img = img.point(lambda p: p ** gamma)
    
    return img

def create_grid(image, color="#FF0000"):
    from PIL import ImageDraw
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # Вертикальные линии
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=color)
    
    # Горизонтальные линии
    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill=color)
    
    return image