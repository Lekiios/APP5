from functions import detect_circles, detect_circles_with_gradient_angle
import cv2

# four.png --------------------------------------------------------------------------------------------------------
four = cv2.imread("images/four.png", cv2.IMREAD_GRAYSCALE)
if four is None:
    raise FileNotFoundError("Couldn't find the loaded image.")

# Whit n=15 the algorithm detects 4 circles right, with n=4 it only detects 3 circles.
detect_circles(four, 4)

# coins.png -----------------------------------------------------------------------------------------------------------
# coins = cv2.imread("images/coins.png", cv2.IMREAD_GRAYSCALE)
# if coins is None:
#     raise FileNotFoundError("Couldn't find the loaded image.")
#
# detect_circles(coins, 2, edges_threshold=0.

# coins2.png -----------------------------------------------------------------------------------------------------------
# coins2 = cv2.imread("images/coins2.jpg", cv2.IMREAD_GRAYSCALE)
# if coins2 is None:
#     raise FileNotFoundError("Couldn't find the loaded image.")
#
# detect_circles_with_gradient_angle(coins2, 8, edges_threshold=0.4, blur_kernel=(5, 5))

# fourn.png -----------------------------------------------------------------------------------------------------------
# fourn = cv2.imread("images/fourn.png", cv2.IMREAD_GRAYSCALE)
# if fourn is None:
#     raise FileNotFoundError("Couldn't find the loaded image.")
#
# detect_circles(fourn, 4)

# MoonCoin.png -------------------------------------------------------------------------------------------------------
# moon_coins = cv2.imread("images/MoonCoin.png", cv2.IMREAD_GRAYSCALE)
# if moon_coins is None:
#     raise FileNotFoundError("Couldn't find the loaded image.")
#
# detect_circles(moon_coins, 4, edges_threshold=0.4, blur_kernel=(5, 5))
