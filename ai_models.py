from rembg import remove
from PIL import Image

def remove_background(image, model_type="u2net", bg_color="#FFFFFF"):
    fg = remove(image)
    bg = Image.new("RGBA", fg.size, bg_color)
    return Image.alpha_composite(bg, fg.convert("RGBA"))