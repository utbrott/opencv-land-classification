import cv2
import numpy as np
from PIL import Image, ImageTk

mask_colors = {
    "green": (87, 120, 4),
    "gray": (70, 63, 63),
}

mask_green_l = (36, 25, 25)
mask_green_u = (86, 255, 255)
mask_brown_l = (74, 74, 74)
mask_brown_u = (180, 255, 255)
mask_gray_l = (0, 10, 100)
mask_gray_u = (179, 30, 255)
mask_white_l = (0, 0, 168)
mask_white_u = (172, 111, 255)


def load_image(path, with_scale=False, target_scale=(0, 0)):
    image = cv2.imread(path)

    if with_scale:
        image = scale_image(image, target_scale)

    return image


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


def clahe(image):
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


def process_image(image):
    enhanced_image = clahe(image)

    green_m = create_mask(enhanced_image, mask_green_l, mask_green_u)
    brown_m = create_mask(enhanced_image, mask_brown_l, mask_brown_u)
    gray_m = create_mask(enhanced_image, mask_gray_l, mask_gray_u)
    white_m = create_mask(enhanced_image, mask_white_l, mask_white_u)

    greens_mask = green_m + brown_m
    builds_mask = gray_m + white_m

    greens = mask_image(enhanced_image, greens_mask, mask_colors["green"])
    builds = mask_image(enhanced_image, builds_mask, mask_colors["gray"])

    processing_out = greens + builds

    return processing_out


def classification_data(image, image_params):
    area = actual_area(image, image_params)
    enhanced_image = clahe(image)

    green_m = create_mask(enhanced_image, mask_green_l, mask_green_u)
    brown_m = create_mask(enhanced_image, mask_brown_l, mask_brown_u)
    gray_m = create_mask(enhanced_image, mask_gray_l, mask_gray_u)
    white_m = create_mask(enhanced_image, mask_white_l, mask_white_u)

    greens_mask = green_m + brown_m
    builds_mask = gray_m - white_m

    _, greens_area = in_mask(enhanced_image, area, greens_mask)
    _, builds_area = in_mask(enhanced_image, area, builds_mask)
    others = round(area - (greens_area + builds_area), 2)

    if others < 0:
        others = 0.00

    return area, greens_area, builds_area, others
