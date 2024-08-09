import os
from tqdm import tqdm

from mwclient import Site

wiki = Site("wiki.biligame.com/bjhl", path="/")


DOWNLOAD_FILE_BASE_PATH = "../data/images"


def construct_file_path(file_name):
    # 将字符串分解为多个部分
    if " " in file_name:
        parts = file_name.split(" ")
        # 将最后一个部分作为文件名，其余部分作为路径格式化
        formatted_path = "/".join(parts[:-1]) + "/" + parts[-1]

        # 定义文件路径
        file_path = f"{DOWNLOAD_FILE_BASE_PATH}/{formatted_path}"

    else:
        formatted_filename = file_name
        # 定义文件路径
        file_path = f"{DOWNLOAD_FILE_BASE_PATH}/{formatted_filename}"
    return file_path


def image_check():
    images = wiki.allimages()
    image_list = []
    print("Image Checking...")
    for image in images:
        file_name = image.name[3:]
        if not file_name.endswith(".mp3"):
            file_path = construct_file_path(file_name)
            # 检查文件是否存在，存在则跳过下载
            if not os.path.exists(file_path):
                image_list.append(image)
    print("Image Checking Complete")
    return image_list


def image_save(image):
    file_name = image.name[3:]
    file = wiki.images[file_name]

    file_path = construct_file_path(file_name)
    dir_name = os.path.dirname(file_path)

    # 检查目录是否存在，不存在则创建
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "wb") as img:
        file.download(img)


def image_download():
    image_list = image_check()
    for image in tqdm(image_list, disable=not len(image_list)):
        tqdm.set_postfix(image.name[3:])
        image_save(image)


image_download()
