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
        if value:
            attributes = value.split(",")
            for attr in attributes:
                attribute_pairs.append(attribute_dict[attr])

    else:
        target.setdefault("base_attribute", {})
        target["base_attribute"].setdefault("level", {})

        if attribute_pairs:
            if value:
                target["base_attribute"]["level"][attribute_level] = dict(
                    zip(attribute_pairs, value.split(","))
                )
            else:
                target["base_attribute"]["level"][attribute_level] = {}


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


def translate_illustration(match, item, target):
    key, value = item
    num = match.group(1)
    target.setdefault("illustration", {})
    target["illustration"][num] = value


def translate_mark_wakeup(match, item, target):
    key, value = item
    wakeup_stage = 2 if match.group(1) == "II" else 4
    wakeup_option = 0 if match.group(2) == "A" else 1
    target.setdefault("mark_wakeup", {})
    target["mark_wakeup"].setdefault(wakeup_stage, [[], []])
    target["mark_wakeup"][wakeup_stage][wakeup_option].append(value)


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
        elif match := re.match(r"^烙痕立绘(\d+)", key):
            translate_illustration(match, item, translated_dict)
        elif match := re.match(r"^(II|IV)-(A|B)-(\d+)", key):
            translate_mark_wakeup(match, item, translated_dict)

        elif english_attribute := base_dict.get(key, key):
            valid_attributes = {"acquisition", "expression", "tag"}

            if english_attribute in valid_attributes:
                translated_dict[english_attribute] = value.split(",")
            else:
                translated_dict[english_attribute] = value

    return translated_dict


__all__ = ["translate_inner_mark"]
