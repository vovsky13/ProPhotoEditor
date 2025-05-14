from rembg import remove
import cv2
import numpy as np
from skimage import exposure

def remove_background(img: Image.Image) -> Image.Image:
    """Удаление фона с помощью нейросети U-2-Net"""
    return remove(img)

def replace_background(
    img: Image.Image, 
    background: Image.Image, 
    border_pixels: int = 5,
    blur_radius: int = 3
) -> Image.Image:
    """
    Замена фона с обработкой границ
    """
    # Создаем маску без фона
    mask = remove(img.convert('RGB')).convert('L')
    
    # Обработка границ
    mask_np = np.array(mask)
    mask_np = cv2.dilate(mask_np, np.ones((border_pixels, border_pixels), np.uint8))
    mask_np = cv2.GaussianBlur(mask_np, (blur_radius*2+1, blur_radius*2+1), 0)
    
    # Наложение на новый фон
    background = background.resize(img.size)
    composite = Image.composite(img, background, Image.fromarray(mask_np))
    
    return composite

def apply_advanced_filters(
    img: Image.Image,
    filter_type: str = 'clarendon',
    intensity: float = 1.0
) -> Image.Image:
    """
    Применение пресет-фильтров в стиле Instagram
    Доступные фильтры: clarendon, gingham, moon, lark, juno
    """
    filters = {
        'clarendon': lambda x: exposure.adjust_gamma(x, 0.9),
        'gingham': lambda x: cv2.applyColorMap(x, cv2.COLORMAP_PINK),
        'moon': lambda x: cv2.cvtColor(x, cv2.COLOR_RGB2GRAY),
        'lark': lambda x: exposure.adjust_sigmoid(x, gain=5),
        'juno': lambda x: cv2.addWeighted(x, 0.8, np.full(x.shape, [50, 30, 180], dtype=np.uint8), 0.2, 0)
    }
    
    img_np = np.array(img.convert('RGB'))
    filtered = filters[filter_type](img_np)
    blended = cv2.addWeighted(img_np, 1-intensity, filtered, intensity, 0)
    
    return Image.fromarray(blended)