import re

from constant.dict import stat_dict

base_dict = {
    "烙痕名称": "name",
    "品质": "rarity",
    "烙痕属性": "type",
    "画师": "artist",
    "准线技能": "awaking_skill",
    "技能": "nexus_skills",
    "实装日期": "implemented_at",
    "获取途径": "acquisitions",
    "烙痕介绍": "description",
}


stat_pairs = []


def translate_basic_stats(match, item, target):
    global stat_pairs
    key, value = item
    stats_level = match.group(1).lower() if match.group(1) else None

    if not stats_level:
        if value:
            attributes = value.split(",")
            for attr in attributes:
                stat_pairs.append(stat_dict[attr])

    else:
        basic_stats = target.setdefault("basic_stats", {})

        if stat_pairs:
            if value:
                basic_stats[stats_level] = dict(zip(stat_pairs, value.split(",")))
            else:
                basic_stats[stats_level] = {}


def translate_nexus_stats(match, item, target):
    key, value = item
    attribute_num = match.group(1)

    target.setdefault("nexus_stats", {})
    target["nexus_stats"].setdefault(attribute_num, {})

    if match.group(2) == "解锁等级":
        attribute_type = "unlock_level"
        target["nexus_stats"][attribute_num][attribute_type] = value
    elif match.group(2):
        target["nexus_stats"][attribute_num].setdefault("level", {})
        target["nexus_stats"][attribute_num]["level"][match.group(2).lower()] = value
    else:
        attribute_type = "name"
        target["nexus_stats"][attribute_num][attribute_type] = value


def translate_content(match, item, target):
    content_dict = {
        "名称": "name",
        "类型": "type",
        "条件": "condition",
        "简介": "description",
        "内容": "detail",
    }
    key, value = item

    content_num = match.group(1)
    content_attr = content_dict[match.group(2)]
    target.setdefault("content", {})
    target["content"].setdefault(content_num, {})

    target["content"][content_num][content_attr] = value


def translate_nexus_effect(match, item, target):
    key, value = item
    level = match.group(1).lower()
    target.setdefault("nexus_effect", {})
    target["nexus_effect"][level] = value


def translate_illustration(match, item, target):
    key, value = item
    num = match.group(1)
    target.setdefault("illustration", {})
    target["illustration"][num] = value


def translate_trace_awaking(match, item, target):
    key, value = item
    awaking_stage = 2 if match.group(1) == "II" else 4
    awaking_option = 0 if match.group(2) == "A" else 1
    target.setdefault("trace_awaking", {})
    target["trace_awaking"].setdefault(awaking_stage, [[], []])
    target["trace_awaking"][awaking_stage][awaking_option].append(value)


def translate_memory_trace(origin_dict):
    translated_dict = {}

    for key, value in origin_dict.items():
        item = [key, value]
        if match := re.match(r"^属性(\d+)(解锁等级|LV\d*)?", key):
            translate_nexus_stats(match, item, translated_dict)
        elif match := re.match(r"^基础属性([Ll][Vv]\d+)?", key):
            translate_basic_stats(match, item, translated_dict)
        elif match := re.match(r"^内容解锁(\d+)(名称|类型|条件|简介|内容)", key):
            translate_content(match, item, translated_dict)
        elif match := re.match(r"^特质([Ll][Vv]\d+)", key):
            translate_nexus_effect(match, item, translated_dict)
        elif match := re.match(r"^烙痕立绘(\d+)", key):
            translate_illustration(match, item, translated_dict)
        elif match := re.match(r"^(II|IV)-([AB])-(\d+)", key):
            translate_trace_awaking(match, item, translated_dict)

        elif english_attribute := base_dict.get(key, key):
            valid_attributes = {"acquisitions", "nexus_skills"}

            if english_attribute in valid_attributes:
                translated_dict[english_attribute] = value.split(",")
            elif english_attribute == "type":
                translated_dict[english_attribute] = stat_dict[value]
            else:
                translated_dict[english_attribute] = value

    return translated_dict


__all__ = ["translate_memory_trace"]
