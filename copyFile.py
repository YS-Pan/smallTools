"""
This script recursively copies files and directories from a source directory 
to a destination directory, excluding directories that end with '.aedtresults'.
The script maintains the directory structure and updates the modification 
times of the copied directories to match the source directories.
"""

import os
import shutil

def copy_files(src_dir, dst_dir):
    try:
        # 遍历源目录中的所有文件和文件夹
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)

            # 检查是否是文件夹并且名称不以 ".aedtresults" 结尾
            if os.path.isdir(s) and not item.endswith('.aedtresults'):
                # 如果目标目录中不存在该文件夹，则创建它
                if not os.path.exists(d):
                    os.makedirs(d)
                print(f"Copying directory: {s}")
                # 递归复制文件和文件夹
                copy_files(s, d)

                # 获取源文件夹的修改时间，并设置目标文件夹的修改时间
                src_time = os.path.getmtime(s)
                os.utime(d, (src_time, src_time))
            elif os.path.isfile(s):
                # 如果是文件，则直接复制到目标目录
                shutil.copy2(s, d)
                print(f"Copied file: {s}")
    except Exception as e:
        print(f"An error occurred while copying files: {e}")


# 定义源目录和目标目录
src_dir = "H:\\"
dst_dir = r"\\DESKTOP-DERG5LD\download\backup\20240829  20190507 lenovo pHDD"

copy_files(src_dir, dst_dir)
