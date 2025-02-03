"""
LACZKOWSKI Lorenzo
LE BOT Maxime
APP5 IIM
"""

import numpy as np
import os
import cv2

fresco_path = './assets/Michelangelo_ThecreationofAdam_1707x775.jpg'
fragments_dir = 'assets/frag_eroded/'
fragments_txt_path = 'assets/fragments.txt'
fragments_s_txt_path = 'assets/fragments_s.txt'

# Open files and put data in map and set
def read_data():
    fragments = []
    with open(fragments_txt_path, 'r') as file:
        for line in file:
            i, x, y, r = map(float, line.split())
            fragments.append((int(i), int(x), int(y), float(r)))

    with open(fragments_s_txt_path, 'r') as f_s:
        invalid_fragments = set(map(int, f_s.readlines()))

    return fragments, invalid_fragments

# Rotate a frag with desired angle
def rotate(frag, r):
    # Get frag center
    h, w = frag.shape[:2]
    center = (w // 2, h // 2)
    # Create rotation matrix
    m = cv2.getRotationMatrix2D(center, r, 1.0)
    # Rotate fragment
    fragment = cv2.warpAffine(frag, m, (w, h))
    return fragment

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

    return new_frag

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([
        ((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)])
    return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))

# ====================== MAIN ===========================

# Get original fresco size
fresco_rgb = cv2.imread(fresco_path, cv2.IMREAD_UNCHANGED)
f_height, f_width = fresco_rgb.shape[:2]

# Add alpha channel to the original fresco
b_channel, g_channel, r_channel = cv2.split(fresco_rgb) # Extract BGR channel
alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 # Create alpha channel the size of others
fresco = cv2.merge((b_channel, g_channel, r_channel, alpha_channel)) # Recreate the image with 4 channels

# Make it brighter for a better result
fresco = adjust_gamma(fresco, 5)

# Get data from txt files
fragments_data, invalid_fragments = read_data()
# Loop over data to process each fragments
for index, pos_x, pos_y, r in fragments_data:

    # Skip invalid fragments
    if index in invalid_fragments:
        continue

    # Load fragment image (with IMREAD_UNCHANGED to keep alpha channel)
    fragment_path = os.path.join(fragments_dir, f'frag_eroded_{index}.png')
    fragment = cv2.imread(fragment_path, cv2.IMREAD_UNCHANGED)

    if fragment is None:
        print(f"Fragment {index} could not be loaded.")
        continue

    # Rotate fragment if angle != 0
    if r != 0:
        fragment = rotate(fragment, r)

    # Process position of fragment from center
    h, w = fragment.shape[:2]
    x1 = pos_x - w // 2
    y1 = pos_y - h // 2
    x2 = x1 + w
    y2 = y1 + h

    # crop fragment if going out of the original fresco
    if x1 < 0:
        fragment = fragment[:,abs(x1):w]
        x1 = 0

    if y1 < 0:
        fragment = fragment[abs(y1):h,:]
        y1 = 0

    if x2 > f_width:
        fragment = fragment[:,0:w-(x2-f_width)]
        x2 = f_width

    if y2 > f_height:
        fragment = fragment[0:h-(y2-f_height),:]
        y2 = f_height

    # Blend fragment with fresco
    fragment = alpha_blend(fresco, fragment, (x1, x2, y1, y2))

    # Write fragment onto original fresco
    # (not useful as references are passed threw the alpha blend,
    # the fragment are already on the final fresco, but it helps to understand the program)
    fresco[y1:y2, x1:x2] = fragment

cv2.imshow("fresco", fresco)
cv2.imwrite("reconstructed_fresco.png", fresco)
cv2.waitKey(0)
