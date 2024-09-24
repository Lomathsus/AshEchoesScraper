import json
import os

from mwclient import Site
from tqdm import tqdm

from utils import translate_skill

wiki = Site("wiki.biligame.com/bjhl", path="/")

DOWNLOAD_FILE_PATH = "../data/skills"


def download_memory_trace_json(skill):
    page = wiki.pages[skill]
    print(skill)
    lines = page.text().split("\n")

    dictionary = {}

    for line in lines:
        if "=" in line:
            parts = line[1:].split("=", 1)  # specify max split
            key, value = parts[0], parts[1] if len(parts) > 1 else ""
            dictionary[key] = value.strip()

    new_dict = translate_skill(dictionary)

    file_name = new_dict["name"]

    # 定义文件路径
    file_path = f"{DOWNLOAD_FILE_PATH}/{file_name}.json"

    # 检查目录是否存在，不存在则创建
    dir_name = os.path.dirname(file_path)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(new_dict, json_file, ensure_ascii=False, indent=4)


def get_skill_list():
    skills = wiki.categories["刻印技能"]
    return [skill.name for skill in skills]


def download_skills():
    skill_list = get_skill_list()
    for skill in tqdm(skill_list, disable=not len(skill_list)):
        download_memory_trace_json(skill)


download_skills()
# download_memory_trace_json("刻印技能/监督刻印·额外攻击")
