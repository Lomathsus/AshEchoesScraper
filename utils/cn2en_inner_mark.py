import re

base_dict = {
    "烙痕名称": "name",
    "品质": "rarity",
    "烙痕属性": "attribute",
    "画师": "illustrator",
    "准线技能": "mark_skill",
    "技能": "skill",
    "实装日期": "implemented_at",
    "获取途径": "acquisition",
    "烙痕介绍": "description",
    # "特质LV1": "{{颜色烙痕蓝高维同调}}处，获取{{颜色烙痕蓝防御}}到达10次时，可获得{{颜色烙痕蓝攻击}}{{颜色烙痕黄20}}点<br>本烙痕完成一次{{颜色烙痕蓝记忆强化}}，有{{颜色烙痕黄30%}}几率获得40点{{颜色烙痕蓝专精}}",
    # "特质LV2": "{{颜色烙痕蓝高维同调}}处，获取{{颜色烙痕蓝防御}}到达10次时，可获得{{颜色烙痕蓝攻击}}{{颜色烙痕黄25}}点<br>本烙痕完成一次{{颜色烙痕蓝记忆强化}}，有{{颜色烙痕黄50%}}几率获得40点{{颜色烙痕蓝专精}}",
    # "特质LV3": "{{颜色烙痕蓝高维同调}}处，获取{{颜色烙痕蓝防御}}到达10次时，可获得{{颜色烙痕蓝攻击}}{{颜色烙痕黄30}}点<br>本烙痕完成一次{{颜色烙痕蓝记忆强化}}，有{{颜色烙痕黄60%}}几率获得40点{{颜色烙痕蓝专精}}",
    # "特质LV4": "{{颜色烙痕蓝高维同调}}处，获取{{颜色烙痕蓝防御}}到达10次时，可获得{{颜色烙痕蓝攻击}}{{颜色烙痕黄40}}点<br>本烙痕完成一次{{颜色烙痕蓝记忆强化}}，有{{颜色烙痕黄60%}}几率获得40点{{颜色烙痕蓝专精}}",
    # "特质LV5": "{{颜色烙痕蓝高维同调}}处，获取{{颜色烙痕蓝防御}}到达10次时，可获得{{颜色烙痕蓝攻击}}{{颜色烙痕黄40}}点<br>本烙痕完成一次{{颜色烙痕蓝记忆强化}}，有{{颜色烙痕黄70%}}几率获得40点{{颜色烙痕蓝专精}}",
    # "特质LV6": "{{颜色烙痕蓝高维同调}}处，获取{{颜色烙痕蓝防御}}到达10次时，可获得{{颜色烙痕蓝攻击}}{{颜色烙痕黄50}}点<br>本烙痕完成一次{{颜色烙痕蓝记忆强化}}，有{{颜色烙痕黄75%}}几率获得40点{{颜色烙痕蓝专精}}<br>在首个{{颜色烙痕蓝烙痕唤醒点}}，可直接解锁{{颜色烙痕黄核心技能的2级}}",
    # "II-A-1": "技能点+50",
    # "II-A-2": "防御+10~20",
    # "II-B-1": "攻击+5~15",
    # "II-B-2": "专精+30",
    # "IV-A-1": "攻击+10~20",
    # "IV-A-2": "技能点+40",
    # "IV-B-1": "技能点+40",
    # "IV-B-2": "专精+10~20",
    # "烙痕立绘1": "",
    # "烙痕立绘2": "",
}

attribute_dict = {
    "体质": "health",
    "防御": "defence",
    "攻击": "attack",
    "专精": "mastery",
    "终端": "terminal",
}

attribute_pairs = []


def translate_base_attribute(match, item, target):
    global attribute_pairs
    key, value = item
    attribute_level = match.group(1).lower() if match.group(1) else None

    if not attribute_level:
        attributes = value.split(",")
        for attr in attributes:
            attribute_pairs.append(attribute_dict[attr])
    else:
        target.setdefault("base_attribute", {})
        target["base_attribute"].setdefault("level", {})
        target["base_attribute"]["level"][attribute_level] = dict(
            zip(attribute_pairs, value.split(","))
        )


def translate_crossing_attribute(match, item, target):
    key, value = item
    attribute_num = match.group(1)

    target.setdefault("crossing_attribute", {})
    target["crossing_attribute"].setdefault(attribute_num, {})

    if match.group(2) == "解锁等级":
        attribute_type = "unlock_level"
        target["crossing_attribute"][attribute_num][attribute_type] = value
    elif match.group(2):
        target["crossing_attribute"][attribute_num].setdefault("level", {})
        target["crossing_attribute"][attribute_num]["level"][
            match.group(2).lower()
        ] = value
    else:
        attribute_type = "name"
        target["crossing_attribute"][attribute_num][attribute_type] = value


def translate_content(match, item, target):
    content_dict = {
        "名称": "name",
        "类型": "type",
        "条件": "condition",
        "简介": "description",
        "内容": "content",
    }
    key, value = item

    content_num = match.group(1)
    content_attr = content_dict[match.group(2)]
    target.setdefault("content", {})
    target["content"].setdefault(content_num, {})

    target["content"][content_num][content_attr] = value


def translate_trait(match, item, target):
    key, value = item
    level = match.group(1).lower()
    target.setdefault("trait", {})
    target["trait"][level] = value


def translate_inner_mark(origin_dict):
    translated_dict = {}

    for key, value in origin_dict.items():
        item = [key, value]
        if match := re.match(r"^属性(\d+)(解锁等级|LV\d*)?", key):
            translate_crossing_attribute(match, item, translated_dict)
        elif match := re.match(r"^基础属性([Ll][Vv]\d+)?", key):
            translate_base_attribute(match, item, translated_dict)
        elif match := re.match(r"^内容解锁(\d+)(名称|类型|条件|简介|内容)", key):
            translate_content(match, item, translated_dict)
        elif match := re.match(r"^特质([Ll][Vv]\d+)", key):
            translate_trait(match, item, translated_dict)
        elif english_attribute := base_dict.get(key, key):
            translated_dict[english_attribute] = value
    return translated_dict


__all__ = ["translate_inner_mark"]
