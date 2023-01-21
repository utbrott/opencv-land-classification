import cv2
import numpy as np
from PIL import Image, ImageTk

mask_colors = {
    "green": (87, 120, 4),
    "gray": (70, 63, 63),
}

default_masks = {
    "green_l": (36, 25, 25),
    "green_h": (86, 255, 255),
    "brown_l": (74, 74, 74),
    "brown_h": (255, 255, 255),
    "gray_l": (0, 10, 100),
    "gray_h": (180, 30, 255),
    "white_l": (0, 0, 168),
    "white_h": (172, 111, 255),
}


def load_image(path, with_scale=False, target_scale=(0, 0)):
    image = cv2.imread(path)

    if with_scale:
        image = scale_image(image, target_scale)

    return image_for_gui(image)


def image_for_gui(image):
    blue, green, red = cv2.split(image)
    image = cv2.merge((red, green, blue))

    # Make image
    img = Image.fromarray(image)
    return ImageTk.PhotoImage(img)


def scale_image(image, target):
    input = image.shape[:2]

    scaled_dims = (
        int(input[0] * (target[0] / input[0])),
        int(input[1] * (target[1] / input[1])),
    )

    return cv2.resize(image.copy(), scaled_dims, interpolation=cv2.INTER_AREA)


def actual_area(image, image_params):
    width, height = image.shape[:2]
    pixels, distance = image_params

    a_width = width / pixels * distance
    a_height = height / pixels * distance
    sq_m_km = 1_000_000  # square m in square km

    return round((a_width * a_height) / sq_m_km, 2)


def adaptive_histogram(image):
    lab_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2LAB)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab_image[:, :, 0] = clahe.apply(lab_image[:, :, 0])

    return cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)


def create_mask(image, low_threshold, high_threshold):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, low_threshold, high_threshold)

    return mask


def mask_image(image, mask, color=(255, 255, 255)):
    image = np.zeros(image.copy().shape, np.uint8)

    image[mask > 0] = color

    return image


def in_mask(image, area, mask):
    width, height = image.shape[:2]

    img_pixels = width * height
    mask_pixels = cv2.countNonZero(mask)

    mask_percent = mask_pixels / img_pixels
    in_mask = area * mask_percent

    return int(mask_percent * 100), round(in_mask, 2)


def process_image(
    image,
    green_mask=(default_masks["green_l"], default_masks["green_h"]),
    brown_mask=(default_masks["brown_l"], default_masks["brown_h"]),
    gray_mask=(default_masks["gray_l"], default_masks["gray_h"]),
    white_mask=(default_masks["white_l"], default_masks["white_h"])
):
    enhanced_image = adaptive_histogram(image)

    green_m = create_mask(enhanced_image, green_mask[0], green_mask[1])
    brown_m = create_mask(enhanced_image, brown_mask[0], brown_mask[1])
    gray_m = create_mask(enhanced_image, gray_mask[0], gray_mask[1])
    white_m = create_mask(enhanced_image, white_mask[0], white_mask[1])

    greens_mask = green_m + brown_m
    buildings_mask = gray_m + white_m

    greens = mask_image(enhanced_image, greens_mask, mask_colors["green"])
    buildings = mask_image(enhanced_image, buildings_mask, mask_colors["gray"])

    return greens, buildings
