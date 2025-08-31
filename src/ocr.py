import cv2
import numpy as np
import pytesseract

from PIL import Image
from secrets import PYTESSERACT_PATH # from your local file

# This path is from your installed Tesseract executable
pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH

def preprocess_image(image_path: str):
    """
    Loads image, grayscales, and binarizes with Otsu.
    Returns the thresholded image (np array) suitable for OCR.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Can not open the image {image_path}")

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, threshold = cv2.threshold(gray, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save copies
    cv2.imwrite('gray_img.jpg', gray)
    cv2.imwrite('threshold_img.jpg', threshold)

    return threshold


def extract_text(image_array: np.ndarray, lang: str):
    """
    Run OCR with Tesseract on a preprocessed image
    lang: selected language
    """
    # Convert np array to PIL image
    pil_img = Image.fromarray(image_array)
    return pytesseract.image_to_string(pil_img, lang=lang)
