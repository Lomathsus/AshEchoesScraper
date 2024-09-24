import json
import os

from mwclient import Site
from utils import translate_memory_trace

wiki = Site("wiki.biligame.com/bjhl", path="/")

DOWNLOAD_FILE_PATH = "../data/memory_traces"


def download_memory_trace_json(memory_trace):
    page = wiki.pages[memory_trace]
    print(memory_trace)
    lines = page.text().split("\n")

    dictionary = {}

    for line in lines:
        if "=" in line:
            parts = line[1:].split("=", 1)  # specify max split
            key, value = parts[0], parts[1] if len(parts) > 1 else ""
            dictionary[key] = value.strip()

    new_dict = translate_memory_trace(dictionary)

    file_name = new_dict["name"]

    # 定义文件路径
    file_path = f"{DOWNLOAD_FILE_PATH}/{file_name}.json"

    # 检查目录是否存在，不存在则创建
    dir_name = os.path.dirname(file_path)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(new_dict, json_file, ensure_ascii=False, indent=4)


def get_memory_trace_list():
    memory_traces = wiki.categories["记忆烙痕"]
    return [memory_trace.name for memory_trace in memory_traces]


def download_memory_traces():
    marker_list = get_memory_trace_list()
    list(map(download_memory_trace_json, marker_list))


# download_memory_traces()
