import cv2
import numpy as np

import util

image = cv2.imread("images/image_9.png")

# Get image real area (image, (pixels, dist))
area = util.actual_area(image, (163, 100))

# Enhance the image
enhanced = util.clahe(image)

# Get greenery/buildings area
green_m = util.create_mask(enhanced, (36, 25, 25), (86, 255, 255))
brown_m = util.create_mask(enhanced, (74, 74, 74), (255, 255, 255))
greens_mask = green_m + brown_m
greens = util.mask_image(enhanced, greens_mask, util.mask_colors["green"])

gray_m = util.create_mask(enhanced, (0, 10, 100), (180, 30, 255))
white_m = util.create_mask(enhanced, (0, 0, 168), (172, 111, 255))
buildings_mask = gray_m + white_m
buildings = util.mask_image(enhanced, buildings_mask, util.mask_colors["gray"])

greens_percent, greens_area = util.in_mask(enhanced, area, greens_mask)
buildings_percent, buildings_area = util.in_mask(enhanced, area, buildings_mask)

# Resize image for display (width, height)
target_size = (852, 480)
scaled_input = util.scale_image(image, target_size)

output = greens + buildings
scaled_output = util.scale_image(output, target_size)

cv2.imshow("Input + Output", np.vstack((scaled_input, scaled_output)))

# \u00b2 -> superscript 2
print(f"Area in image: {area}km\u00b2")
print(f"Greenery: {greens_percent}%, {greens_area}km\u00b2")
print(f"Buildings: {buildings_percent}%, {buildings_area}km\u00b2")

uncategorized_area = area - (greens_area + buildings_area)
print(f"Uncategorized: {uncategorized_area}km\u00b2")

cv2.waitKey(0)
cv2.destroyAllWindows()
