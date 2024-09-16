import cv2
import numpy as np

# Read fragments.txt file and parse the information
fragments = []
with open('./assets/fragments.txt', 'r') as file:
    for line in file:
        i, x, y, r = map(float, line.split())
        fragments.append((i, x, y, r))

# Load the original fresco image
fresco_rgb = cv2.imread('./assets/Michelangelo_ThecreationofAdam_1707x775.jpg', cv2.IMREAD_UNCHANGED)
f_height, f_width = fresco_rgb.shape[:2]
fresco = cv2.cvtColor(fresco_rgb, cv2.COLOR_RGB2RGBA)
alpha_data = np.ones((f_height, f_width), dtype=np.uint8) * 255
cv2.mixChannels((alpha_data,), (fresco,), (0,3,))



# Create a canvas to work on
OFFSET = 20
canvas = np.zeros((f_height + 2*OFFSET, f_width + 2*OFFSET, 4), dtype=np.uint8)
c_height, c_width = canvas.shape[:2]
canvas[:,:,3] = np.ones((c_height, c_width), dtype=np.uint8) * 255


# Place the fresco image on the canvas
canvas[OFFSET:f_height + OFFSET, OFFSET:f_width + OFFSET] = fresco

for i,x,y,r in fragments:
    fragment = cv2.imread(f'./assets/frag_eroded/frag_eroded_{int(i)}.png', cv2.IMREAD_UNCHANGED)
    ht, wd = fragment.shape[:2]

    # extract alpha channel as mask and base bgr images
    bgr = canvas[:, :, 0:3]
    mask = canvas[:, :, 3]
    bgr2 = fragment[:, :, 0:3]
    mask2 = fragment[:, :, 3]



    x1 = int(x) - wd // 2 + OFFSET
    y1 = int(y) - ht // 2 + OFFSET
    x2 = x1 + wd
    y2 = y1 + ht

    bgr2_new = bgr.copy()
    bgr2_new[y1:y2, x1:x2] = bgr2

    mask_new = np.zeros((c_height, c_width), dtype=np.uint8)
    mask_new[y1:y2, x1:x2] = mask2

    # combine the two masks
    # either multiply or use bitwise_and
    mask_combined = cv2.multiply(mask, mask_new)
    mask_combined = cv2.cvtColor(mask_combined, cv2.COLOR_GRAY2BGR)

    result = np.where(mask_combined == 255, bgr2_new, bgr)

    # Display the fragment and the corresponding region in the fresco image
    # cv2.imshow('fragment', fragment)
    # cv2.imshow('fresco region', fresque[y1:y2, x1:x2])
    # cv2.waitKey(0)

    # fresque[y1:y2, x1:x2] = fragment


cv2.imshow('canvas', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()