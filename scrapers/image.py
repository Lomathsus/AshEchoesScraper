import os

from mwclient import Site

wiki = Site("wiki.biligame.com/bjhl", path="/")


DOWNLOAD_FILE_BASE_PATH = "../data/images"

images = wiki.allimages()
for image in images:
    file_name = image.name[3:]
    file = wiki.images[file_name]

    file_path = ""
    formatted_filename = ""
    if not file_name.endswith(".mp3"):
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

        # 检查目录是否存在，不存在则创建
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # 检查文件是否存在，存在则跳过下载
        if not os.path.exists(file_path):
            with open(file_path, "wb") as img:
                file.download(img)
