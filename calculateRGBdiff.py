import math
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as compareSSIM

def calculate_pixel_difference(image1, image2):
    width, height ,_= image2.shape
    total_diff = 0
    num_pixels = width * height

    for y in range(height):
        for x in range(width):
            r1, g1, b1 = image1[x, y]
            r2, g2, b2 = image2[x, y]
            r1, g1, b1 = int(r1) ,int(g1) ,int(b1)
            r2, g2, b2 = int(r2) ,int(g2) ,int(b2)
            diff = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
            total_diff += diff

    average_diff = total_diff / num_pixels
    return average_diff


def calculate_histogram_ssim_difference(image1, image2):
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    hist1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray_image2], [0], None, [256], [0, 256])

    hist1 = cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    hist2 = cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

    diff_value = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)

    (_, diff) = compareSSIM(gray_image1, gray_image2, full=True)
    diff = (diff * 255).astype("uint8")

    return diff_value,diff.mean()

if __name__ == "__main__":
    image1 = cv2.imread('/home/tjh/fsdownload/img1.ppm')
    image2 = cv2.imread('/home/tjh/fsdownload/nsp/tmp_img1_cc_nrm.ppm')
    image3 = cv2.imread('/home/tjh/fsdownload/nsp/tmp_img1_cc_nrm2.ppm')
    image1=cv2.resize(image1,(1280,680))
    diff12 = calculate_pixel_difference(image1,image2)
    diff13 = calculate_pixel_difference(image1,image3)
    diff_value12,diff_value12_ = calculate_histogram_ssim_difference(image1, image2)
    diff_value13,diff_value13_ = calculate_histogram_ssim_difference(image1, image3)
    print("像素差异值:", diff12, diff13)
    print("直方图差异值:", diff_value12, diff_value13)
    print("ssim差异值:", diff_value12_,diff_value13_)


