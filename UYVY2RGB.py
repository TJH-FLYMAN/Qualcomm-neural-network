import cv2
import numpy as np
uyvy_file = "/home/tjh/8650_platform/apps/qnx_ap/AMSS/multimedia/fadas/fadas/tst/app_nsp/uyvy/img1.uyvy"
width = 1920
height = 1020

with open(uyvy_file, "rb") as file:
    uyvy_data = file.read()

expected_size = width * height * 2
if len(uyvy_data) != expected_size:
    print("UYVY文件大小与指定的图像尺寸不匹配！")
    exit()
pixel_count = width * height 
uyvy_buffer = np.frombuffer(uyvy_data, dtype=np.uint8)
rgb_buffer = np.zeros((height, width, 3), dtype=np.uint8)
for i in range(height):
    for j in range(0, width, 2):
        uy = uyvy_buffer[i * width * 2 + j * 2]
        y0 = uyvy_buffer[i * width * 2 + j * 2 + 1]
        vy = uyvy_buffer[i * width * 2 + j * 2 + 2]
        y1 = uyvy_buffer[i * width * 2 + j * 2 + 3]

        u = uy - 128
        v = vy - 128

        r1 = max(0, min(255, int(y0 + 1.402 * v)))
        g1 = max(0, min(255, int(y0 - 0.344136 * u - 0.714136 * v)))
        b1 = max(0, min(255, int(y0 + 1.772 * u)))

        r2 = max(0, min(255, int(y1 + 1.402 * v)))
        g2 = max(0, min(255, int(y1 - 0.344136 * u - 0.714136 * v)))
        b2 = max(0, min(255, int(y1 + 1.772 * u)))

        rgb_buffer[i][j] = [r1, g1, b1]
        rgb_buffer[i][j + 1] = [r2, g2, b2]

if __name__ == "__main__":
    rgb_image = cv2.cvtColor(rgb_buffer, cv2.COLOR_RGB2BGR)

    rgb_image = cv2.cvtColor(rgb_buffer.reshape(height, width, 3), cv2.COLOR_RGB2BGR)

    cv2.imshow("RGB Image", rgb_image)
    cv2.imwrite('/home/tjh/fsdownload/img1.ppm',rgb_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



