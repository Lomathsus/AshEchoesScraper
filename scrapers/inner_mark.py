import json
import os

from mwclient import Site
from utils import translate_inner_mark

wiki = Site("wiki.biligame.com/bjhl", path="/")

DOWNLOAD_FILE_PATH = "../data/inner_marks"

# dir_path = "../data/marks"
# dir_name = os.path.dirname(dir_path)
#
# if not os.path.exists(dir_name):
#     os.makedirs(dir_name, exist_ok=True)


def download_inner_mark_json(inner_mark):
    page = wiki.pages[inner_mark]
    print(inner_mark)
    lines = page.text().split("\n")

    dictionary = {}

    for line in lines:
        if "=" in line:
            parts = line[1:].split("=", 1)  # specify max split
            key, value = parts[0], parts[1] if len(parts) > 1 else ""
            dictionary[key] = value.strip()

    new_dict = translate_inner_mark(dictionary)

    file_name = new_dict["name"]

    # 定义文件路径
    file_path = f"{DOWNLOAD_FILE_PATH}/{file_name}.json"

    # 检查目录是否存在，不存在则创建
    dir_name = os.path.dirname(file_path)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(new_dict, json_file, ensure_ascii=False, indent=4)
    # inner_mark = wiki.pages["记忆烙痕/双重引力"]
    # print(inner_mark.text())
    # for image in inner_mark.images():
    #     print(image.name)


def get_inner_mark_list():
    inner_marks = wiki.categories["记忆烙痕"]
    return [inner_mark.name for inner_mark in inner_marks]


def download_inner_marks():
    marker_list = get_inner_mark_list()
    list(map(download_inner_mark_json, marker_list))


download_inner_marks()
# download_inner_mark_json("记忆烙痕/如在镜中")
