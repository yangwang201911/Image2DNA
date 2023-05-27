import os
from PIL import Image
import numpy as np
import argparse

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='Convert RGB values of all pixels in a JPEG image to letters')
parser.add_argument('path', help='Path to the JPEG file or directory')
args = parser.parse_args()

def convert_dna_list_to_jpeg(file_path):
    # 解析文件名中的图像宽度和高度
    file_name = os.path.basename(file_path)
    saved_path = os.path.dirname(file_path)
    image_name, size_str = file_name[:-4].split("#")
    width, height = size_str.split("x")
    width = int(width)
    height = int(height)
    
    # 读取文件内容并将字母转换为RGB
    with open(file_path, 'r') as f:
        content = f.read()
        rgb_list = convert_letters_to_rgb(content)

    print("JPEG file size: {} x {} and Pixle size: {}".format(width, height, len(rgb_list) / 3))
    # 检查数据列表的长度是否正确
    assert len(rgb_list) == width * height * 3, "数据列表长度错误" 
    # 创建PIL图片对象并设置像素值
    rgb_array = np.array(rgb_list, dtype=np.uint8).reshape(height, width, 3)
    img = Image.fromarray(rgb_array)
    img = img.resize((width, height))
    print("R: {}\tG: {}\tB: {}\n".format(rgb_list[0], rgb_list[1], rgb_list[2]))
    
    # 将图片保存为JPEG格式
    print(f"Will save to file: {saved_path}/Convertd_{image_name}.jpg")
    img.save(f"{saved_path}/Convertd_{image_name}.jpg", 'JPEG')



def convert_letters_to_rgb(ret):
    rgb = []
    for i in range(0, len(ret), 4):
        c1, c2, c3, c4 = ret[i], ret[i+1], ret[i+2], ret[i+3]
        binary_str = ''
        if c1 == 'A':
            binary_str += '00'
        elif c1 == 'T':
            binary_str += '01'
        elif c1 == 'G':
            binary_str += '10'
        else:
            binary_str += '11'

        if c2 == 'A':
            binary_str += '00'
        elif c2 == 'T':
            binary_str += '01'
        elif c2 == 'G':
            binary_str += '10'
        else:
            binary_str += '11'

        if c3 == 'A':
            binary_str += '00'
        elif c3 == 'T':
            binary_str += '01'
        elif c3 == 'G':
            binary_str += '10'
        else:
            binary_str += '11'

        if c4 == 'A':
            binary_str += '00'
        elif c4 == 'T':
            binary_str += '01'
        elif c4 == 'G':
            binary_str += '10'
        else:
            binary_str += '11'
        rgb.append(int(binary_str, 2))
    return rgb

def convert_rgb_to_letters(rgb):
    ret = ''
    first = True
    for value in rgb:
        binary_str = format(value, '08b')
        for i in range(0, 8, 2):
            if binary_str[i:i+2] == '00':
                ret += 'A'
            elif binary_str[i:i+2] == '01':
                ret += 'T'
            elif binary_str[i:i+2] == '10':
                ret += 'G'
            else:
                ret += 'C'
    return ret

# 处理单个JPEG文件
def convert_jpeg_to_dna_list(file_path):
    # 检查文件是否存在且为普通文件
    if not os.path.isfile(file_path):
        print(f'{file_path} is not a file')
        return

    # 检查文件扩展名是否为JPEG
    if not file_path.lower().endswith('.jpg') and not file_path.lower().endswith('.jpeg'):
        print(f'{file_path} is not a JPEG file')
        return

    # 打开JPEG文件
    with Image.open(file_path) as im:
        # 将图像转换为numpy数组
        arr = np.array(im)

        # 遍历每个像素并访问其RGB值
        ret = ''
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                pixel = arr[i, j]
                ret += convert_rgb_to_letters(pixel)
                if i == 0 and j == 0:
                    print(f"Orignal RGB: {pixel}")
                    print(f"DNA sequence: {ret}")
                    convert_ret = convert_letters_to_rgb(ret)
                    print("Decoded RGB: {}".format(convert_ret))
        # 将处理后的字符串写入txt文件
        width, height = im.size
        txt_file_path = os.path.splitext(file_path)[0] + f'#{width}x{height}' +'.txt'
        print("JPEG file: {} x {} and Pixle size: {}".format(arr.shape[0], arr.shape[1], len(ret) / 12))
        with open(txt_file_path, 'w') as f:
            f.write(ret)

# 处理目录下的所有JPEG文件
def process_directory(dir_path):
    # 遍历目录下的所有文件和子目录
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # 检查文件扩展名是否为JPEG
            if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
                file_path = os.path.join(root, file)
                print("Processing the JPEG file {}...".format(file_path))
                convert_jpeg_to_dna_list(file_path)
                print("Processing the JPEG file wihtin {}...Done".format(dir_path))
            # 检查文件扩展名是否为txt
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                print("Processing the DNA sequence file wihtin {}...".format(file_path))
                convert_dna_list_to_jpeg(file_path)
                print("Processing the DNA sequence file wihtin {}...Done".format(file_path))

def main():
    # 判断路径是文件还是目录，并调用相应的处理函数
    if os.path.isfile(args.path):
        convert_jpeg_to_dna_list(args.path)
    elif os.path.isdir(args.path):
        process_directory(args.path)
    else:
        print(f'{args.path} is not a file or directory')

if __name__ == '__main__':
    main()