"""
GIF to PNG Converter with Automatic White Border Removal

Description:
Converts all .gif files in the current directory to .png image sequences.
For each .gif file, it creates a new folder named after the .gif file (without the extension),
and stores the .png images in that folder. Additionally, it removes any white borders around
the non-white pixels in each frame, ensuring that the resulting .png images are cropped to the
smallest possible bounding box that contains all non-white pixels.

Features:
1. Switches the working directory to the script's location.
2. Reads all .gif files in the current directory.
3. Creates a new folder for each .gif file, named after the .gif file.
4. Converts each .gif file into a sequence of .png images, stored in the respective folder.
5. Crops each frame to remove white borders, keeping only the non-white pixel areas.
6. The resulting .png files are named sequentially (0.png, 1.png, etc.).
7. In each folder, creates a 'sample' subfolder containing a specified number of evenly
   distributed sample images from the sequence.

Usage:
- Place the script in the directory containing the .gif files.
- Run the script using Python.
- Adjust the `num_samples` and `start_frame` parameters as needed.

Parameters:
- num_samples (default=8): The number of sample images to save in the 'sample' subfolder.
- start_frame (default=5): The starting frame index for saving sample images.

Dependencies:
- Python (tested with version 3.10)
- Pillow library (PIL)

Author: Ys_Pan, GPT4o
Date: 2024/7/25

GitHub Repository: https://github.com/YS-Pan/smallTools
"""

import os
from PIL import Image, ImageDraw, ImageSequence

def get_nonwhite_bbox(frames):
    """ 获取所有帧非白色区域的最小边界框 """
    if not frames:
        return None, []

    min_x, min_y = frames[0].size[0], frames[0].size[1]
    max_x, max_y = 0, 0

    debug_frames = []  # 用于保存调试帧

    # 遍历所有帧
    for frame in frames:
        pixels = frame.load()  # 直接访问像素数据
        frame_min_x, frame_min_y = frame.width, frame.height
        frame_max_x, frame_max_y = 0, 0

        for y in range(frame.height):
            for x in range(frame.width):
                r, g, b, a = pixels[x, y]
                if not (r == 255 and g == 255 and b == 255 and a == 255):  # 非白色像素
                    frame_min_x = min(frame_min_x, x)
                    frame_max_x = max(frame_max_x, x)
                    frame_min_y = min(frame_min_y, y)
                    frame_max_y = max(frame_max_y, y)

        # 确保我们只在有非白色像素时才更新全局边界框
        if frame_min_x <= frame_max_x and frame_min_y <= frame_max_y:
            min_x = min(min_x, frame_min_x)
            max_x = max(max_x, frame_max_x)
            min_y = min(min_y, frame_min_y)
            max_y = max(max_y, frame_max_y)

        # 将当前帧添加到调试帧列表中（不画裁剪框）
        debug_frames.append(frame)

    # 防止没有找到非白色像素的情况
    if min_x > max_x or min_y > max_y:
        return None, debug_frames
    
    return (min_x, min_y, max_x, max_y), debug_frames

def crop_image(img, bbox):
    """ 根据最小边界框裁剪图像 """
    if bbox is None:
        return img
    min_x, min_y, max_x, max_y = bbox
    return img.crop((min_x, min_y, max_x + 1, max_y + 1))

def save_sample_images(folder_path, total_frames, num_samples=6, start_frame=0):
    sample_folder_path = os.path.join(folder_path, 'sample')
    if not os.path.exists(sample_folder_path):
        os.makedirs(sample_folder_path)
    
    # 计算均匀分布的帧索引
    step = max(1, (total_frames - start_frame) // num_samples)
    sample_indices = [start_frame + i * step for i in range(num_samples)]
    
    # 保存选择的样本图片
    for index in sample_indices:
        src_path = os.path.join(folder_path, f"{index}.png")
        dst_path = os.path.join(sample_folder_path, f"{index}.png")
        if os.path.exists(src_path):
            os.rename(src_path, dst_path)
        else:
            print(f"Frame {index} not found.")

def main(num_samples=6, start_frame=0):
    # 获取脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 切换到脚本所在的目录
    os.chdir(script_dir)
    
    # 获取当前目录下的所有文件
    files = os.listdir(script_dir)
    
    # 过滤出所有的 .gif 文件
    gif_files = [f for f in files if f.lower().endswith('.gif')]
    
    # 为每个 .gif 文件创建一个同名的文件夹，并将 .gif 文件转换为 PNG 图片序列
    for gif in gif_files:
        folder_name = os.path.splitext(gif)[0]
        folder_path = os.path.join(script_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # 打开 .gif 文件
        gif_path = os.path.join(script_dir, gif)
        with Image.open(gif_path) as img:
            # 预加载所有帧
            frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(img)]

            # 获取非白色区域的最小边界框
            bbox, debug_frames = get_nonwhite_bbox(frames)
            
            # 保存调试动画
            if debug_frames:
                debug_gif_path = os.path.join(folder_path, "debug.gif")
                debug_frames[0].save(debug_gif_path, save_all=True, append_images=debug_frames[1:], loop=0)

            frame_index = 0
            for frame in frames:
                cropped_img = crop_image(frame, bbox)
                frame_path = os.path.join(folder_path, f"{frame_index}.png")
                cropped_img.save(frame_path, format="PNG")
                frame_index += 1
        
        # 保存样本图片到 sample 文件夹
        save_sample_images(folder_path, frame_index, num_samples, start_frame)

if __name__ == "__main__":
    # 你可以在这里更改 num_samples 和 start_frame 的值
    main(num_samples=8, start_frame=5)
