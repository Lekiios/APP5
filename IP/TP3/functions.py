import cv2
import time
import numpy as np


# Function to evaluate a detector + descriptor
def evaluate_detector(detector, matcher, image, fragment):
    try:
        # Detect keypoints and descriptors
        start_time = time.time()
        kp_image, desc_image = detector.detectAndCompute(image, None)
        kp_fragment, desc_fragment = detector.detectAndCompute(fragment, None)
        detection_time = (time.time() - start_time) * 1000

        # Check descriptors
        if desc_image is None or desc_fragment is None:
            return {
                "num_keypoints_image": len(kp_image) if kp_image else 0,
                "num_keypoints_fragment": len(kp_fragment) if kp_fragment else 0,
                "num_matches": 0,
                "num_good_matches": 0,
                "detection_time": detection_time,
                "matching_time": 0,
                "keypoints_image": kp_image or [],
                "keypoints_fragment": kp_fragment or [],
                "matches": [],
                "good_matches": []
            }

        # Find matches using knnMatch
        start_time = time.time()
        matches = matcher.knnMatch(desc_fragment, desc_image, k=2)
        matching_time = (time.time() - start_time) * 1000

        # Distance ratio filtering
        good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

        # Flatten matches list for drawing all matches
        all_matches = [m for m, _ in matches]

        return {
            "num_keypoints_image": len(kp_image),
            "num_keypoints_fragment": len(kp_fragment),
            "num_matches": len(all_matches),
            "num_good_matches": len(good_matches),
            "detection_time": detection_time,
            "matching_time": matching_time,
            "keypoints_image": kp_image,
            "keypoints_fragment": kp_fragment,
            "matches": all_matches,
            "good_matches": good_matches,
        }
    except Exception as e:
        print(f"Error in evaluate_detector: {e}")
        return None


# Evaluation with SIFT
def evaluate_sift(image, fragment):
    sift = cv2.SIFT_create()
    bf = cv2.BFMatcher(cv2.NORM_L2)
    return evaluate_detector(sift, bf, image, fragment)


# Evaluation with ORB
def evaluate_orb(image, fragment):
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    return evaluate_detector(orb, bf, image, fragment)


# Main function to evaluate SIFT and ORB and display good matches
# all matches are available in the results dict
def evaluate_all(image, fragment):
    results = {
        "SIFT": evaluate_sift(image, fragment),
        "ORB": evaluate_orb(image, fragment)
    }

    for method_name, res in results.items():
        if res is None:
            print(f"{method_name}: Evaluation failed.")
            continue

        print(f"{method_name}:\n"
              f"  - Num keypoints image: {res['num_keypoints_image']}\n"
              f"  - Num keypoints fragment: {res['num_keypoints_fragment']}\n"
              f"  - Num matches: {res['num_matches']}\n"
              f"  - Num good matches: {res['num_good_matches']}\n"
              f"  - Detection time: {res['detection_time']:.2f}ms\n"
              f"  - Matching time: {res['matching_time']:.2f}ms\n")

        # Draw and display all matches
        matched_img = cv2.drawMatches(
            fragment, res["keypoints_fragment"],
            image, res["keypoints_image"],
            res["good_matches"][:50], None, flags=2
        )
        cv2.imshow(f"Good Matches with {method_name}", matched_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return results


def ransac(matches, kp_fragment, kp_image, threshold=5.0, iterations=1000):
    best_inliers = []
    best_model = None

    if len(matches) < 3:
        print("Erreur : Pas assez de correspondances pour exécuter RANSAC.")
        return None, []

    for _ in range(iterations):
        # Random part
        sample = np.random.choice(matches, 3, replace=True)
        src_points = np.float32([kp_fragment[m.queryIdx].pt for m in sample]).reshape(-1, 1, 2)
        dst_points = np.float32([kp_image[m.trainIdx].pt for m in sample]).reshape(-1, 1, 2)

        model, _ = cv2.estimateAffine2D(src_points, dst_points)

        if model is None:
            continue

        # inliers
        src_all = np.float32([kp_fragment[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_all = np.float32([kp_image[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        projected = cv2.transform(src_all, model)
        errors = np.linalg.norm(projected - dst_all, axis=2).flatten()

        inliers = [m for i, m in enumerate(matches) if errors[i] < threshold]

        # Update if better
        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_model = model

    return best_model, best_inliers


def extract_from_inliers(inliers, kp_fragment, kp_image):
    src_points = np.float32([kp_fragment[m.queryIdx].pt for m in inliers]).reshape(-1, 1, 2)
    dst_points = np.float32([kp_image[m.trainIdx].pt for m in inliers]).reshape(-1, 1, 2)

    model, _ = cv2.estimateAffine2D(src_points, dst_points)

    # Extract parameters x, y, θ
    if model is not None:
        theta = np.arctan2(model[1, 0], model[0, 0])  # Rotation
        x, y = model[0, 2], model[1, 2]  # Translation
        return x, y, np.degrees(theta), model
    return None, None, None, None

def filter_by_euclidean_distance(matches, kp_fragment, kp_image, epsilon=5.0):
    filtered_matches = []

    for i in range(len(matches)):
        is_valid = True
        m1 = matches[i]

        # Coordonnées du premier point
        p1_frag = np.array(kp_fragment[m1.queryIdx].pt)
        p1_image = np.array(kp_image[m1.trainIdx].pt)

        # Comparer avec tous les autres points
        for j in range(i + 1, len(matches)):
            m2 = matches[j]

            # Coordonnées du deuxième point
            p2_frag = np.array(kp_fragment[m2.queryIdx].pt)
            p2_image = np.array(kp_image[m2.trainIdx].pt)

            # Calculer les distances euclidiennes
            d_frag = np.linalg.norm(p1_frag - p2_frag)
            d_image = np.linalg.norm(p1_image - p2_image)

            # Vérifier si les distances sont cohérentes
            if abs(d_frag - d_image) > epsilon:
                is_valid = False
                break

        if is_valid:
            filtered_matches.append(m1)

    return filtered_matches

def reconstruct_fresco(fragments, solutions, base_image):
    fresco = adjust_gamma(base_image,5.0)

    for index, (x, y, theta) in solutions.items():
        if x is None or y is None or theta is None:
            print(f"Fragment {index} : Transformation invalid, ignored.")
            continue

        fragment = fragments[index]
        rows, cols = fragment.shape[:2]
        center = (cols // 2, rows // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, -theta, 1)
        rotation_matrix[0, 2] = x
        rotation_matrix[1, 2] = y

        transformed_fragment = cv2.warpAffine(fragment, rotation_matrix, (fresco.shape[1], fresco.shape[0]))
        mask = transformed_fragment > 0
        fresco[mask] = transformed_fragment[mask]

    return fresco

# Read files
def read_files(fragments_path, solution_path):
    # Read fragments real position (use map to index correctly with any solution order)
    fragments = {}
    with open(fragments_path, 'r') as f:
        for line in f:
            index, x, y, angle = map(float, line.split())
            fragments[int(index)] = ( x, y, angle)

    # Read solution
    solution = {}
    with open(solution_path, 'r') as f:
        for line in f:
            index, x, y, angle = map(float, line.split())
            solution[int(index)] = ( x, y, angle)

    return fragments, solution

# Evaluate precision of solution file
def precision(fragments, solution, delta_x=1, delta_y=1, delta_r=1):
    total = len(fragments)
    found = 0

    for index, (x_sol, y_sol, r_sol) in solution.items():
        if index in fragments:
            x, y, r = fragments[index]

            # If solution within the tolerance add to precision
            if abs(x_sol - x) <= delta_x and abs(y_sol - y) <= delta_y and abs(r_sol - r) <= delta_r:
                found += 1

    # Give precision between 0% - 100% (0.0 - 1.0)
    if found <= 0:
        return 0
    return found / total

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)])
    return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))

def alpha_blend(background, overlay, pos):
    x1, x2, y1, y2 = pos

    # Get de ROI from background
    new_frag = background[y1:y2, x1:x2]

    # normalize alpha channels to 0-1 (not useful in our case because we do not have partial transparency)
    alpha_background = new_frag[:,:,3] / 255
    alpha_overlay = overlay[:,:,3] / 255.0

    # See: https://en.wikipedia.org/wiki/Alpha_compositing
    # a is Overlay & b is Background
    # For each channel use Ca*ALPHA_a + Cb*ALPHA_b*(1-ALPHA_a)
    for channel in range(0, 3):
        new_frag[:,:,channel] = (
                overlay[:,:,channel] * alpha_overlay + new_frag[:,:,channel] * alpha_background * (1 - alpha_overlay))

    # adjust alpha and denormalize back to 0-255
    new_frag[:,:,3] = (1 - (1 - alpha_overlay) * (1 - alpha_background)) * 255