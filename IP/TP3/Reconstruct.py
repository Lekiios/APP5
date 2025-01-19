"""
Image Processing TP3
LACZKOWSKI Lorenzo
LE BOT Maxime
"""

import cv2
import os
from functions import ransac, extract_from_inliers, reconstruct_fresco, read_files, precision, \
    filter_by_euclidean_distance

os.environ["XDG_SESSION_TYPE"] = "xcb"

if __name__ == "__main__":
    image_path = "Michelangelo/Michelangelo_ThecreationofAdam_1707x775.jpg"
    fragments_dir = "Michelangelo/frag_eroded/"

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Erreur : Impossible de charger l'image globale.")
        exit()

    # Load fragments
    fragment_files = sorted([f for f in os.listdir(fragments_dir) if f.endswith(".png")])
    fragments = {i + 1: cv2.imread(os.path.join(fragments_dir, f)) for i, f in enumerate(fragment_files)}
    for index, fragment in fragments.items():
        if fragment is None:
            print(f"Erreur : Impossible de charger le fragment {index}.")
            exit()

    solutions = {}
    sift = cv2.SIFT_create()
    kp_image, desc_image = sift.detectAndCompute(image, None)

    for index, fragment in fragments.items():
        fragment_gray = cv2.cvtColor(fragment, cv2.COLOR_BGR2GRAY)
        kp_fragment, desc_fragment = sift.detectAndCompute(fragment_gray, None)
        bf = cv2.BFMatcher(cv2.NORM_L2)
        matches = bf.knnMatch(desc_fragment, desc_image, k=2)
        matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

        # Exercice 4================================================================================
        # matches = filter_by_euclidean_distance(matches, kp_fragment, kp_image, epsilon=10.0)
        # ===========================================================================================

        if len(matches) < 3:
            print(f"Erreur : Pas assez de correspondances pour le fragment {index}.")
            continue

        model, inliers = ransac(matches, kp_fragment, kp_image, threshold=4.0, iterations=5000)

        if model is not None:
            x, y, theta, _ = extract_from_inliers(inliers, kp_fragment, kp_image)
            solutions[index] = (x, y, theta)

    # Reconstruction
    base_image = cv2.imread(image_path)
    fresco = reconstruct_fresco(fragments, solutions, base_image)
    cv2.imshow("Fresque reconstruite", fresco)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save results
    with open("results.txt", "w") as file:
        for index, (x, y, theta) in solutions.items():
            file.write(f"{index} {x:.0f} {y:.0f} {theta:.3f}\n")
    print("Results saved in 'results.txt'")

    # compute precision
    fragments, solution = read_files("Michelangelo/fragments.txt", "results.txt")

    # Process precision (you can adjust tolerance with delta x / y / r)
    precision = precision(fragments, solution, delta_x=1, delta_y=1, delta_r=1)
    print(f'Precision of reconstruction: {precision:.3f}')
