from PIL import Image, ImageDraw
from typing import Tuple

def create_grid(image: Image.Image) -> Image.Image:
    """
    Создает сетку на изображении для выравнивания.
    """
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Размер ячейки сетки
    cell_size = 50

    # Рисуем вертикальные линии
    for x in range(0, width, cell_size):
        draw.line([(x, 0), (x, height)], fill="gray", width=1)

    # Рисуем горизонтальные линии
    for y in range(0, height, cell_size):
        draw.line([(0, y), (width, y)], fill="gray", width=1)

    return image

def validate_image(image: Image.Image) -> None:
    """
    Проверяет, является ли изображение корректным.
    """
    if image.mode not in ("RGB", "RGBA"):
        raise ValueError("Изображение должно быть в формате RGB или RGBA")

def format_size(size: int) -> str:
    """
    Форматирует размер файла в читаемый вид.
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"