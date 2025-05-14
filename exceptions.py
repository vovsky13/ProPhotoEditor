class InvalidImageError(Exception):
    """Вызывается при невалидном изображении."""
    def __init__(self, message: str = "Некорректное изображение"):
        super().__init__(message)

class ProcessingError(Exception):
    """Вызывается при ошибках обработки."""
    def __init__(self, message: str = "Ошибка обработки"):
        super().__init__(message)