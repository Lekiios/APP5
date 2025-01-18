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
