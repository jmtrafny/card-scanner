# ocr_utils.py
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re

def extract_card_name(image_path, crop_coords):
    try:
        with Image.open(image_path) as img:
            cropped = img.crop(crop_coords)
            gray = cropped.convert("L")
            enhanced = gray.filter(ImageFilter.SHARPEN)
            return pytesseract.image_to_string(enhanced, config="--psm 7").strip()
    except Exception as e:
        print(f"OCR failed for {image_path}: {e}")
        return None

def sanitize_card_name(name):
    if not name:
        return "UnknownCard"
    name = name.strip()
    # Remove anything that isn't alphanumeric, dash, or space
    name = re.sub(r"[^\w\s-]", "", name)
    # Replace spaces with underscores
    name = re.sub(r"\s+", "_", name)
    return name
