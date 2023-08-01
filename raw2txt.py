import os
import struct

# 定义输入文件夹路径和输出文件夹路径
input_folder = '/home/tjh/QNN/output/Result_99'
output_folder = '/home/tjh/QNN/output/Result_99'

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    if filename.endswith('.raw'):
        # 构建输入文件的完整路径
        input_path = os.path.join(input_folder, filename)
        
        # 构建输出文件的完整路径
        output_filename = os.path.splitext(filename)[0] + '.txt'
        output_path = os.path.join(output_folder, output_filename)

        # 打开 raw 文件以进行读取
        with open(input_path, 'rb') as file:
            # 读取 raw 数据
            raw_data = file.read()

        # 创建一个空列表来存储浮点数值
        float_data = []

        # 将 raw 数据按照浮点数格式解析并添加到列表中
        index = 0
        while index < len(raw_data):
            value = struct.unpack('f', raw_data[index:index+4])[0]
            float_data.append(value)
            index += 4

        # 将浮点数写入文本文件
        with open(output_path, 'w') as file:
            for value in float_data:
                file.write(str(value) + '\n')
