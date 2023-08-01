import os
import argparse
import torch
import numpy as np
import mmcv



def create_raw(image_path, platform,save_path):
    size_divisor = 32
    img = mmcv.imread(image_path)
    img_scale = (288,384)
    img, _ = mmcv.imrescale(img, img_scale, return_scale=True)
    img = mmcv.impad_to_multiple(img, size_divisor, pad_val=((114.0, 114.0, 114.0)))

    img = torch.Tensor(img).unsqueeze_(dim=0)
    if platform == "onnx":
        img = img.permute((0, 1, 2, 3))
    elif platform == "torch":
        img = img.permute((0, 3, 1, 2))
    else:
        raise ValueError(f"platform {platform} error, only in 'onnx' or 'torch'." )
    img = img.numpy().astype(np.float32)
    print(f"img type {img.dtype}")
    print(img.shape)
    raw_path = os.path.splitext(image_path)[0] + ".raw"
    last_slash_index = raw_path.rfind("/")
    filename = raw_path[last_slash_index + 1:]
    path = os.path.join(save_path,filename)
    img.tofile(path)

def write_image_paths_to_txt(data_path, txt_file):
    with open(txt_file, 'w') as f:
        for root, dirs, files in os.walk(data_path):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png','.raw')):
                    image_path = os.path.join(root, file)
                    f.write(image_path + '\n')


def args_parse():
    parser = argparse.ArgumentParser(description = 'YoloX raw image')
    parser.add_argument("-i", "--path", default='', help='Input data path')
    parser.add_argument('-p', '--platform', default='onnx', help='model train platform')
    parser.add_argument('-s', '--savepath',default= '', help="path to save raw image")
    return parser.parse_args()

if __name__ == "__main__":
    args = args_parse()
    data_path = args.path
    platform = args.platform
    save_path = args.savepath
    print(data_path,platform,save_path)
    image_paths = os.listdir(data_path)
    for path in image_paths:
        if path.split('.')[-1] not in ["jpg", "png"]:
            continue
        image_path = os.path.join(data_path, path)
        create_raw(image_path, platform,save_path)
    txt_file = os.path.join(save_path,'raw_list.txt')
    if not os.path.exists(txt_file):
         open(txt_file, 'w').close()
    write_image_paths_to_txt(save_path,txt_file=txt_file)
#  python png2raw.py -i .... -p ..... -s ....
