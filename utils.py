from PIL import Image, ImageEnhance, ImageDraw
from typing import Tuple

def validate_image(img: Image.Image, min_size: Tuple[int, int] = (100, 100)) -> None:
    if img.width < min_size[0] or img.height < min_size[1]:
        raise ValueError(f"Изображение слишком маленькое. Минимальный размер: {min_size}")

def mm_to_pixels(mm: float, dpi: int) -> int:
    return int(mm * dpi / 25.4)

def format_size(size: Tuple[int, int]) -> str:
    return f"{size[0]} x {size[1]} px"

def create_grid(image: Image.Image, color: str = "#FF0000", spacing: int = 100) -> Image.Image:
    draw = ImageDraw.Draw(image)
    width, height = image.size

    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=color)

    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=color)

    return image

def apply_color_filters(
    img: Image.Image,
    brightness: float = 1.0,
    contrast: float = 1.0,
    saturation: float = 1.0,
    gamma: float = 1.0,
) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)

    if gamma != 1.0:
        inv_gamma = 1.0 / gamma
        table = [int(((i / 255.0) ** inv_gamma) * 255) for i in range(256)]
        img = img.point(table)

    return img
