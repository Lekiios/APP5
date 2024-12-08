from functions import detect_circles
import cv2

# four.png --------------------------------------------------------------------------------------------------------
four = cv2.imread("images/four.png", cv2.IMREAD_GRAYSCALE)
if four is None:
    raise FileNotFoundError("Couldn't find the loaded image.")

detect_circles(four, 4)
