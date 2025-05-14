from PIL import Image, ImageEnhance, ImageFilter

def mm_to_pixels(mm: float, dpi: int) -> int:
    return int(mm * dpi / 25.4)

def apply_color_calibration(img, brightness, contrast, saturation, gamma):
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)

    img = img.point(lambda p: 255 * (p / 255) ** gamma)
    return img

def apply_filter(image, filter_name):
    if filter_name == "Сепия":
        sepia_image = Image.new("RGB", image.size)
        pixels = image.convert("RGB").load()
        for y in range(image.height):
            for x in range(image.width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                sepia_image.putpixel((x, y), (min(tr, 255), min(tg, 255), min(tb, 255)))
        return sepia_image
    elif filter_name == "Черно-белый":
        return image.convert("L").convert("RGB")
    elif filter_name == "Холодный":
        r, g, b = image.split()
        b = b.point(lambda i: min(255, i + 30))
        return Image.merge("RGB", (r, g, b))
    elif filter_name == "Тёплый":
        r, g, b = image.split()
        r = r.point(lambda i: min(255, i + 30))
        return Image.merge("RGB", (r, g, b))
    else:
        return image

def create_grid(image, color="#FF0000"):
    from PIL import ImageDraw
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=color)
    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill=color)
    return image
