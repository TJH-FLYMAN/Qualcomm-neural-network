import os
from PIL import Image

def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size

def analyze(path):
    image_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    size_count = {}
    for image_file in image_files:
        image_path = os.path.join(path, image_file)
        size = get_image_size(image_path)
        if size in size_count:
            size_count[size] += 1
        else:
            size_count[size] = 1  
    return size_count

path = "/home/tjh/demo/demo_model_apa/line_od/quantilize_used_image_3in1"
size_count = analyze(path)


for size, count in size_count.items():
    print(f"图像宽高:{size[0],size[1]}- 数量: {count}")
