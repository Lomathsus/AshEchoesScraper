import os

from mwclient import Site

wiki = Site("wiki.biligame.com/bjhl", path="/")
# result = wiki.allcategories()
# result = wiki.categories["同调者"]

# page = wiki.pages["同调者/莫红袖"]
# lines = page.text().split("\n")
# images = page.images()
#
# for page in images:
#     print(
#         page.name,
#         f'{page.imageinfo["width"]} x {page.imageinfo["height"]}',
#         page.imageinfo["url"],
#     )

# for image in wiki.allimages():
#     print(
#         image.name,
#         f'{image.imageinfo["width"]} x {image.imageinfo["height"]}',
#         image.imageinfo["url"],
#     )


def clean_filename(filename):
    # Replace ":" with "_"
    return filename.replace(":", "_")


#
# DOWNLOAD_FILE_PATH = "../data/images"
#
# currentImage = wiki.images["记忆烙痕 谎言之下 缩略图.png"]
# file_name = clean_filename(currentImage.name)
#
# # 定义文件路径
# file_path = f"{DOWNLOAD_FILE_PATH}/{file_name}"
#
# # 检查目录是否存在，不存在则创建
# dir_name = os.path.dirname(file_path)
#
# if not os.path.exists(dir_name):
#     os.makedirs(dir_name, exist_ok=True)
#
# with open(f"{DOWNLOAD_FILE_PATH}/{file_name}", "wb") as img:
#     currentImage.download(img)
#
#
# # # Get a page
# # page = wiki.pages["模块:同调者语音档案数据库"]
# #
# # # Print the text
# # print(page.text())
