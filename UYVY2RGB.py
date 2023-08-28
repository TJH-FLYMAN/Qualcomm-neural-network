import cv2
import numpy as np
import argparse
def uyvy2rgb(uyvy_data,width,height):
    expected_size = width * height * 2
    if len(uyvy_data) != expected_size:
        print("UYVY文件大小与指定的图像尺寸不匹配!")
        exit()
    uyvy_buffer = np.frombuffer(uyvy_data, dtype=np.uint8)
    rgb_data = np.zeros((height, width, 3), dtype=np.uint8)
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

            rgb_data[i][j] = [r1, g1, b1]
            rgb_data[i][j + 1] = [r2, g2, b2]
    return rgb_data
def RGB_norm_nsp(rgb_data):
    height,width,_ = rgb_data.shape
    normlzR = [30.999, 1.111, 30.321 ]
    normlzG = [40.888, 1.222 ,40.432 ]
    normlzB = [50.777, 1.333, 50.654 ]
    for i in range(height):
        for j in range(width):
            rgb_data[i][j][0] = max(0, min(255, int(  (rgb_data[i][j][0]-normlzR[0]) * normlzR[1] + normlzR[2]  )))
            rgb_data[i][j][1] = max(0, min(255, int(  (rgb_data[i][j][1]-normlzG[0]) * normlzG[1] + normlzG[2] )))
            rgb_data[i][j][2] = max(0, min(255, int(  (rgb_data[i][j][2]-normlzB[0]) * normlzB[1] + normlzB[2] )))
    return rgb_data

def RGB_norm_cpu(rgb_data):
    height,width,_ = rgb_data.shape
    normlzR = [ 126.999, 1.111, 3.321 ]
    normlzG = [ 126.888, 1.222, 4.432 ]
    normlzB = [ 126.777, 1.333, 5.654 ]
    for i in range(height):
        for j in range(width):
            rgb_data[i][j][0] = max(0, min(255, int(  (rgb_data[i][j][0]-normlzR[0]) * normlzR[1] + normlzR[2]  )))
            rgb_data[i][j][1] = max(0, min(255, int(  (rgb_data[i][j][1]-normlzG[0]) * normlzG[1] + normlzG[2] )))
            rgb_data[i][j][2] = max(0, min(255, int(  (rgb_data[i][j][2]-normlzB[0]) * normlzB[1] + normlzB[2] )))
    return rgb_data

def args_parse():
    parser = argparse.ArgumentParser(description = 'uyvy2rgb and normrgb')
    parser.add_argument("-i", "--input_path", default='', help='uyvy data path')
    parser.add_argument("-w", "--width", default=1920, help='width data')
    parser.add_argument("-t", "--height", default=1020, help='height data')
    parser.add_argument('-o', '--mode', default=12, help='two different treatments')
    return parser.parse_args()

if __name__ == "__main__":
    args = args_parse()
    uyvy_file = args.input_path
    width = args.width
    height = args.height
    if uyvy_file:
        uyvy_file = uyvy_file
    else:
        uyvy_file = "/home/tjh/test_c++/img1.uyvy"
    with open(uyvy_file, "rb") as file:
        uyvy_data = file.read()
    last_slash_pos = uyvy_file.rfind('/') 
    result = uyvy_file[:last_slash_pos + 1]
    mode = args.mode
    rgb_data = uyvy2rgb(uyvy_data,width,height)
    rgb_image = cv2.cvtColor(rgb_data.copy(), cv2.COLOR_RGB2BGR)
    cv2.imwrite(result + "img1.ppm", rgb_image)
    if mode == 1:
        rgb_data = RGB_norm_cpu(rgb_data)
        cv2.imwrite(result + "img1" + "_cpu.ppm", cv2.cvtColor(rgb_data, cv2.COLOR_RGB2BGR))
    elif mode == 2:
        rgb_data = RGB_norm_nsp(rgb_data)
        cv2.imwrite(result + "img1" + "_nsp.ppm", cv2.cvtColor(rgb_data, cv2.COLOR_RGB2BGR))
    else:
        nsp_data = rgb_data.copy()
        rgb_data = RGB_norm_cpu(rgb_data)
        cv2.imwrite(result + "img1" + "_cpu.ppm", cv2.cvtColor(rgb_data, cv2.COLOR_RGB2BGR))
        rgb_data = RGB_norm_nsp(nsp_data)
        cv2.imwrite(result + "img1" + "_nsp.ppm", cv2.cvtColor(rgb_data, cv2.COLOR_RGB2BGR))
    print("success")


