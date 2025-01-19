"""
Image Processing TP3
LACZKOWSKI Lorenzo
LE BOT Maxime
APP 5 IIM
"""

import cv2
import os
import numpy as np
import math
from functions import ransac, extract_from_inliers, reconstruct_fresco, adjust_gamma, alpha_blend

os.environ["XDG_SESSION_TYPE"] = "xcb"

if __name__ == "__main__":
    # Chemin des fragments et de l'image globale
    image_path = "Michelangelo/Michelangelo_ThecreationofAdam_1707x775.jpg"

    # Choose the fragment for evaluation
    fragment_path = "Michelangelo/frag_eroded/frag_eroded_4.png"

    # Charger l'image globale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    fragment = cv2.imread(fragment_path)
    fragment_gray = cv2.cvtColor(fragment, cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher(cv2.NORM_L2)

    kp_image, desc_image = sift.detectAndCompute(image, None)
    kp_fragment, desc_fragment = sift.detectAndCompute(fragment_gray, None)

    matches = bf.knnMatch(desc_fragment, desc_image, k=2)
    matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

    matched_img = cv2.drawMatches(
        fragment, kp_fragment,
        image, kp_image,
        matches[:50], None, flags=2
    )
    cv2.imshow(f"Good Matches", matched_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(matches) < 3:
        print(f"not enough matches for {fragment_path}")
        exit()

    model, inliers = ransac(matches, kp_fragment, kp_image, threshold=5.0, iterations=1000)

    if model is not None:
        x, y, theta, _ = extract_from_inliers(inliers, kp_fragment, kp_image)
        print(f"Fragment {fragment_path} : x={x:.0f}, y={y:.0f}, theta={theta:.0f}°")

    fresco = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    fresco = adjust_gamma(fresco, 5)

    rows, cols = fragment.shape[:2]
    center = (cols // 2, rows // 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, -theta, 1)
    rotation_matrix[0, 2] = x
    rotation_matrix[1, 2] = y

    transformed_fragment = cv2.warpAffine(fragment, rotation_matrix, (fresco.shape[1], fresco.shape[0]))

    mask = transformed_fragment > 0
    fresco[mask] = transformed_fragment[mask]

    cv2.imshow("Fresque reconstruite", fresco)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
