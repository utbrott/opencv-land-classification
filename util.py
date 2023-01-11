import cv2
import numpy as np


def scale_image(image, target):
    input = image.shape[:2]

    scaled_dims = (
        int(input[0] * (target[0] / input[0])),
        int(input[1] * (target[1] / input[1]))
    )

    return cv2.resize(
        image.copy(),
        scaled_dims,
        interpolation=cv2.INTER_AREA
    )


def actual_area(image, distance, pixels):
    input = image.shape[:2]

    a_width = (input[0] / pixels * distance)
    a_height = (input[1] / pixels * distance)
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
    input = image.shape[:2]

    img_pixels = input[0] * input[1]
    mask_pixels = cv2.countNonZero(mask)

    mask_percent = mask_pixels / img_pixels
    in_mask = area * mask_percent

    return int(mask_percent * 100), round(in_mask, 2)
