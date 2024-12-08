import cv2
import numpy as np
from scipy.ndimage import maximum_filter

# Loading image -------------------------------------------------------------------------------------------------------
image_path = "images/four.png"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    raise FileNotFoundError("Couldn't find the loaded image.")

cv2.imshow("Original - GrayScale", image)
cv2.waitKey(0)
cv2.destroyWindow("Original - GrayScale")

# Blurring ------------------------------------------------------------------------------------------------------------
blur_kernel = (3, 3)
blurred = cv2.GaussianBlur(image, blur_kernel, 0)

cv2.imshow("Blurred", blurred)
cv2.waitKey(0)
cv2.destroyWindow("Blurred")

# Sobel gradient ------------------------------------------------------------------------------------------------------
grad_x = cv2.Sobel(image, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
grad_y = cv2.Sobel(image, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

# Combine the gradients (from opencv documentation) but magnitude seems more efficient
# abs_grad_x = cv2.convertScaleAbs(grad_x)
# abs_grad_y = cv2.convertScaleAbs(grad_y)
#
# magnitude = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

# Magnitude of the gradient -------------------------------------------------------------------------------------------
magnitude = cv2.magnitude(grad_x, grad_y)
magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)


cv2.imshow("Magnitude", magnitude)
cv2.waitKey(0)
cv2.destroyWindow("Magnitude")

# Extracting the edges ------------------------------------------------------------------------------------------------
t = 0.6 # % of maximum value in magnitude
threshold = t * magnitude.max()
edges = np.where(magnitude >= threshold, 255, 0).astype(np.uint8)

cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyWindow("Edges")

# Accumulator init ----------------------------------------------------------------------------------------------------
rows, cols = image.shape

# Parameters
r_min, r_max, delta_r = 1, rows, 2
c_min, c_max, delta_c = 1, cols, 2
rad_min, rad_max, delta_rad = 5, int(np.sqrt(2) * ((rows+cols)/2)), 1

acc = np.zeros(((r_max - r_min) // delta_r + 1,
                (c_max - c_min) // delta_c + 1,
                (rad_max - rad_min) // delta_rad + 1), dtype=np.float64)

# Accumulator voting and filling --------------------------------------------------------------------------------------
indices = np.argwhere(edges > 0)  # Get the indices of the non-null pixels in edges

for y, x in indices:
    for i, r in enumerate(range(r_min, r_max + 1, delta_r)):
        for j, c in enumerate(range(c_min, c_max + 1, delta_c)):
            rad = int(np.sqrt((x - c) ** 2 + (y - r) ** 2))
            if rad_min <= rad <= rad_max:
                k = (rad - rad_min) // delta_rad
                perimeter = 2 * np.pi * rad
                if perimeter > 0:  # Avoid division by zero
                    # use the magnitude as a weight with perimeter to normalize circles with different sizes
                    acc[i, j, k] += magnitude[y, x] / perimeter

# Accumulator's local maximum search ----------------------------------------------------------------------------------
local_max = maximum_filter(acc, size=3)  # Thanks scipy <3
maxima = (acc == local_max) & (acc > 0)

# Retrieve results ----------------------------------------------------------------------------------------------------
N = 5
indices = np.argpartition(acc.flatten(), -N)[-N:]
indices = np.unravel_index(indices, acc.shape)

# indices -> (i, j, k) -> (r, c, rad)
circles = []
for i, j, k in zip(*indices):
    r = r_min + i * delta_r
    c = c_min + j * delta_c
    rad = rad_min + k * delta_rad
    circles.append((r, c, rad))

# Draw detected circles onto the original image
output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
for r, c, rad in circles:
    cv2.circle(output, (int(c), int(r)), int(rad), (0, 0, 255), 1)
    cv2.drawMarker(output, (int(c), int(r)), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=2)

cv2.imshow("Detected Circles", output)
cv2.waitKey(0)
cv2.destroyAllWindows()