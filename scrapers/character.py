import json
import os
from typing import TextIO

from mwclient import Site
from tqdm import tqdm

from utils import translate_character


wiki = Site("wiki.biligame.com/bjhl", path="/")

DOWNLOAD_FILE_PATH = "../data/characters"


def download_character_json(character):
    page = wiki.pages[character]
    print(character)
    lines = page.text().split("\n")

    dictionary = {}

    for line in lines:
        if "=" in line:
            parts = line[1:].split("=", 1)  # specify max split
            key, value = parts[0], parts[1] if len(parts) > 1 else ""
            dictionary[key] = value.strip()

    new_dict = translate_character(dictionary)

    file_name = new_dict["name"]

    # 定义文件路径
    file_path = f"{DOWNLOAD_FILE_PATH}/{file_name}.json"

    # 检查目录是否存在，不存在则创建
    dir_name = os.path.dirname(file_path)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(new_dict, json_file, ensure_ascii=False, indent=4)


def get_character_list():
    characters = wiki.categories["同调者"]
    return [character.name for character in characters]


def download_characters():
    character_list = get_character_list()
    for character in tqdm(character_list, disable=not len(character_list)):
        download_character_json(character)  # 不需要返回值


# download_characters()
# download_character_json("同调者/龙晴")
