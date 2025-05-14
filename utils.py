from PIL import Image, ImageEnhance, ImageOps, ImageDraw
import numpy as np

def mm_to_pixels(mm: float, dpi: int) -> int:
    return int(mm * dpi / 25.4)

def apply_color_calibration(img, brightness, contrast, saturation, gamma):
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)

    img = img.point(lambda p: 255 * ((p / 255) ** (1 / gamma)))
    return img

def apply_filter(image, filter_type):
    if filter_type == "Сепия":
        sepia = np.array(image.convert("RGB"))
        tr = [0.393, 0.769, 0.189]
        tg = [0.349, 0.686, 0.168]
        tb = [0.272, 0.534, 0.131]

        r = sepia[:, :, 0] * tr[0] + sepia[:, :, 1] * tr[1] + sepia[:, :, 2] * tr[2]
        g = sepia[:, :, 0] * tg[0] + sepia[:, :, 1] * tg[1] + sepia[:, :, 2] * tg[2]
        b = sepia[:, :, 0] * tb[0] + sepia[:, :, 1] * tb[1] + sepia[:, :, 2] * tb[2]

        sepia = np.stack([r, g, b], axis=2)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        return Image.fromarray(sepia)

    elif filter_type == "Чёрно-белый":
        return image.convert("L").convert("RGB")

    elif filter_type == "Инверсия":
        return ImageOps.invert(image.convert("RGB"))

    return image

def create_grid(image, color="#FF0000"):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for x in range(0, width, 100):
        draw.line([(x, 0), (x, height)], fill=color)

    for y in range(0, height, 100):
        draw.line([(0, y), (width, y)], fill=color)

    return image

def validate_image(image: Image.Image) -> bool:
    return isinstance(image, Image.Image) and image.mode in ["RGB", "RGBA", "L"]

def format_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"
