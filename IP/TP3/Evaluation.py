"""
Image Processing TP3
LACZKOWSKI Lorenzo
LE BOT Maxime
"""

import cv2
import os
from functions import evaluate_all

os.environ["XDG_SESSION_TYPE"] = "xcb"

if __name__ == "__main__":
    image_path = "Michelangelo/Michelangelo_ThecreationofAdam_1707x775.jpg"

    # Choose the fragment for evaluation
    fragment_path = "Michelangelo/frag_eroded/frag_eroded_1.png"

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    fragment = cv2.imread(fragment_path, cv2.IMREAD_GRAYSCALE)

    if image is None or fragment is None:
        print("Error : Cannot load images.")
    else:
        evaluate_all(image, fragment)
