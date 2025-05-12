# ocr_utils.py
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def extract_card_name(image_path, crop_coords):
    try:
        with Image.open(image_path) as img:
            cropped = img.crop(crop_coords)

            if HAS_CV2:
                # Convert PIL image to OpenCV format
                open_cv_image = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

                # Resize for better OCR accuracy
                scaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

                # Apply adaptive thresholding
                thresh = cv2.adaptiveThreshold(
                    scaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )

                text = pytesseract.image_to_string(
                    thresh,
                    config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
                )
                return text.strip()
            else:
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
