import cv2
import numpy as np
from scipy.ndimage import maximum_filter

def detect_circles(image, n, blur_kernel=(3, 3), edges_threshold=0.5, delta_r=2, delta_c=2, delta_rad=1,
                   display_steps=False):
    """
    :param image: Grayscale image
    :param n: number of circles to detect
    :param blur_kernel: blurring kernel for the Gaussian filter
    :param edges_threshold: percentage of the maximum value in the magnitude to threshold the edges
    :param delta_r: accumulator's steps in the rows
    :param delta_c: accumulator's steps in the columns
    :param delta_rad: accumulator's steps in the radius
    :param display_steps: boolean to display all the intermediate steps
    :return:
    """
    start_time = cv2.getTickCount()

    # Blurring ------------------------------------------------------------------------------------------------------------
    blurred = cv2.GaussianBlur(image, blur_kernel, 0)

    if display_steps:
        cv2.imshow("Blurred", blurred)
        cv2.waitKey(0)
        cv2.destroyWindow("Blurred")

    # Sobel gradient ------------------------------------------------------------------------------------------------------
    grad_x = cv2.Sobel(image, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(image, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

    # Magnitude of the gradient -------------------------------------------------------------------------------------------
    magnitude = cv2.magnitude(grad_x, grad_y)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    if display_steps:
        cv2.imshow("Magnitude", magnitude)
        cv2.waitKey(0)
        cv2.destroyWindow("Magnitude")

    # Extracting the edges ------------------------------------------------------------------------------------------------
    threshold = edges_threshold * magnitude.max()
    edges = np.where(magnitude >= threshold, 255, 0).astype(np.uint8)

    if display_steps:
        cv2.imshow("Edges", edges)
        cv2.waitKey(0)
        cv2.destroyWindow("Edges")

    # Accumulator init ----------------------------------------------------------------------------------------------------
    rows, cols = image.shape

    # Parameters
    r_min, r_max = 1, rows
    c_min, c_max = 1, cols
    rad_min, rad_max = 5, int(np.sqrt(2) * ((rows + cols) / 2))

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
    indices = np.argpartition(acc.flatten(), -n)[-n:]
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

    end_time = cv2.getTickCount()
    time_taken = (end_time - start_time) / cv2.getTickFrequency()

    print(f"Time elapsed: {time_taken} seconds")

    cv2.imshow("Detected Circles", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
