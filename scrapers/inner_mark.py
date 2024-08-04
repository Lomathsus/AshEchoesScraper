import os

from mwclient import Site

wiki = Site("wiki.biligame.com/bjhl", path="/")

# dir_path = "../data/marks"
# dir_name = os.path.dirname(dir_path)
#
# if not os.path.exists(dir_name):
#     os.makedirs(dir_name, exist_ok=True)


def get_inner_mark_list():
    inner_marks = wiki.categories["记忆烙痕"]
    return [inner_mark for inner_mark in inner_marks]


def download_inner_mark_json():
    inner_mark = wiki.pages["记忆烙痕/双重引力"]
    print(inner_mark.text())
    # for image in inner_mark.images():
    #     print(image.name)


download_inner_mark_json()

# def download_inner_marks():
#     inner_mark_list = get_inner_mark_list()
#     list(map(download_inner_mark_json, inner_mark_list))
#

# def download_thumbnail():
#     page = wiki.pages["记忆烙痕图鉴"]
#     images = page.images()
#     for image in images:
#         print(image.page_title, image.imageinfo["url"])
#
#
# def download_inner_mark_json():
#     page = wiki.pages["记忆烙痕/因果历然"]
#     print(page.text())
#
#
# download_thumbnail()
