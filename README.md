# Qualcomm-neural-network
script 
#get_image_wh.py
用于统计path中所有图像的宽高数据以及数量

#png2raw
将path中的所有图像转换为raw格式，并保存在save_path路径中，同时save_path会自动生成 raw_list.txt文件
txt文件包含所有raw图像路径

#raw2txt
将raw数据转换为txt文件，此处的raw数据/txt文件为网络特征。需后处理转换为边界框坐标

#UYVY2RGB
将UYVY格式的图像转换为RGB格式，按照422存储格式取YUV值，根据公式计算RGB像素

#calcualteRGBdiff
两张不同尺寸的RGB图像，计算在像素、直方图、SSIM等不同角度的差异值
