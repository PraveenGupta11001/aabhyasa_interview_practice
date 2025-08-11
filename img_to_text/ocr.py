import pytesseract
import cv2
import numpy as np
from PIL import Image

# img_path = '/home/praveen/Desktop/My-Projects/interview_p/imgs/inputs/image copy 2.png'

def extract_text_strong(image_path):
    # Read in OpenCV
    img = cv2.imread(image_path)

    # 1) Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2) Scale up aggressively (3x)
    scale_factor = 3
    gray = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # 3) Sharpen edges
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    gray = cv2.filter2D(gray, -1, kernel)

    # 4) Adaptive threshold (smaller block size for thin fonts)
    thresh = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 15, 8)

    # 5) Morphological close (connect broken letters)
    kernel_morph = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_morph)

    # 6) OCR with UI-friendly config
    config = r'--oem 3 --psm 11'  # sparse text, LSTM engine
    text = pytesseract.image_to_string(morph, config=config)

    return text
