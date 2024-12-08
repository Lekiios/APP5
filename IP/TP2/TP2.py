import cv2
import numpy as np

# Loading image
image_filename = "images/four.png"
image = cv2.imread(image_filename, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError("Couldn't find the loaded image.")

blurred = cv2.GaussianBlur(image, (5, 5), 1)

# Sobel gradient
grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
magnitude = cv2.magnitude(grad_x, grad_y)

# Defining thresholds
t = 0.4
threshold = t * magnitude.max()
contour_pixels = np.where(magnitude > threshold)

# Accumulator init
rows, cols = image.shape
r_min, r_max, delta_r = 5, int(np.sqrt(rows**2 + cols**2)), 1
accumulator = np.zeros((rows, cols, r_max - r_min + 1))

# Accumulator voting and filling
for y, x in zip(*contour_pixels):
    for r_idx, rad in enumerate(range(r_min, r_max + 1, delta_r)):
        weight = magnitude[y, x] / (2 * np.pi * rad)
        for theta in range(0, 360, 2):
            theta_rad = np.deg2rad(theta)
            r = int(y - rad * np.sin(theta_rad))
            c = int(x - rad * np.cos(theta_rad))
            if 0 <= r < rows and 0 <= c < cols:
                accumulator[r, c, r_idx] += weight

# Accumulator's local maximum search
def is_local_max(acc, i, j, k):
    local_region = acc[max(i - 1, 0):i + 2, max(j - 1, 0):j + 2, max(k - 1, 0):k + 2]
    return acc[i, j, k] == local_region.max()

candidates = []
for r in range(accumulator.shape[0]):
    for c in range(accumulator.shape[1]):
        for rad in range(accumulator.shape[2]):
            if is_local_max(accumulator, r, c, rad):
                candidates.append((accumulator[r, c, rad], r, c, rad + r_min))

# Filter by DESC votes
candidates.sort(reverse=True, key=lambda x: x[0])
top_circles = candidates[:10]

# Output
output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
for _, r, c, rad in top_circles:
    cv2.circle(output_image, (c, r), rad, (0, 255, 0), 2)

# Display
cv2.imshow("Detected circles", output_image)
cv2.waitKey(0)
