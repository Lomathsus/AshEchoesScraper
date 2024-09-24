import re
from constant.dict import profession_dict, element_dict, stat_dict, training_dict

base_dict = {
    "姓名": "name",
    "英文名": "en_name",
    "日文名": "jp_name",
    "职业": "profession",
    "元素": "element",
    "星级": "rarity",
    "TAG": "tags",
    "国配声优": "cn_cv",
    "日配声优": "jp_cv",
    "原型来源": "prototype",
    "实装日期": "implemented_at",
    "获取途径": "acquisitions",
    "音乐名称": "music_name",
    "表情名称": "expressions",
    "漫巡初始技能": "engraving_skills",
    "特性强化": "character_enhancement",
}


mastery_bonus_dict = {
    "治愈": "healing",
    "增伤": "damage_bonus",
    "格挡": "block",
}


combat_dict = {
    "暴击率": "critical_rate",
    "普通攻击TAG": "attack_tags",
    "射程": "attack_range",
    "射程具体数值": "range_value",
    "攻击速度": "attack_speed",
    "普通攻击描述": "attack_description",
    "基础减伤": "basic_damage_reduction",
    "战术移动距离": "reposition_distance",
    "战术移动指令冷却": "reposition_cooldown",
}

skill_dict = {
    "名称": "name",
    "类型": "type",
    "TAG": "tags",
    "指令冷却类型": "cooldown_type",
    "指令冷却数值": "cooldown",
    "每场次数": "availability",
    "施放条件": "cast_condition",
    "增益持续": "cast_duration",
    "-描述-": "level",
}

report_dict = {
    "出生世界": "birth_world",
    "档案姓名": "document_name",
    "曾用名": "alias_name",
    "性别": "gender",
    "身高": "height",
    "生日": "birthday",
    "所属势力": "faction",
    "原生世界": "teleported_from",
    "出生地": "birthplace",
    "现居地": "address",
    "基础报告简介": "brief_report",
}

seed_data = {
    "异化核心": "name",
    "初始异化相性指数": "init_compatibility",
    "稳定异化相性指数": "stable_compatibility_1",
    "稳定异化相性指数2": "stable_compatibility_2",
    "稳定异化相性指数3": "stable_compatibility_3",
    "细胞同步率指数": "cell_synchronisation_rate",
    "测定机构": "inspection_agency",
    "异化核心相关数据备注": "comment",
}


# 攻击属性
def translate_combat_stats(match, item, target):
    key, value = item
    attack_attribute = combat_dict[match.group()]
    target.setdefault("combat_stats", {})

    target["combat_stats"][attack_attribute] = (
        value if not attack_attribute == "attack_tags" else value.split(",")
    )


# (位阶)(属性)加成
def translate_basic_stat(match, item, target):
    key, value = item
    level = match.group(1).lower()
    attribute = stat_dict[match.group(2)]
    target.setdefault("basic_stats", {}).setdefault(level, {}).setdefault(attribute, {})
    target["basic_stats"][level][attribute] = value


# (位阶)作为队长时蚀刻初始属性-(属性)
def translate_captain_attribute(match, item, target):
    key, value = item
    level = match.group(1).lower()
    attribute = stat_dict[match.group(3)]
    target.setdefault("engraving_stats", {}).setdefault(level, {})
    target["engraving_stats"][level][attribute] = value


# 专精影响分支
def translate_mastery_bonus(match, item, target):
    key, value = item
    attribute = mastery_bonus_dict[match.group(2)]
    target.setdefault("mastery_bonus", {})[attribute] = value


# 技能
def translate_combat_skill(match, item, target):
    key, value = item

    target.setdefault("combat_skill", {})

    skill_type = "combat_skill" if match.group(1) == "技能" else "seed_skill"
    skill_number = int(match.group(2)) if match.group(1) == "技能" else 0
    skill_code = "seed" if skill_type == "seed_skill" else skill_number

    target["combat_skill"].setdefault(skill_code, {})

    en_skill_attribute = skill_dict[match.group(3)]
    skill_level = match.group(4).lower() if match.group(4) else ""

    if en_skill_attribute != "level":
        target["combat_skill"][skill_code][en_skill_attribute] = (
            value if not en_skill_attribute == "tags" else value.split(",")
        )
    else:
        target["combat_skill"][skill_code].setdefault("level", {})

        # Split the value into "{{..}}" structures and other text
        values = re.split(r"(\{\{.*?\}\})", value)

        # Initialize an empty dictionary for "{{..}}" structures
        values_dict = {}

        # Initialize an index counter
        index_counter = 0

        # Initialize an empty description string
        description = ""

        # Go through each split value
        for v in values:
            # If it starts with "{{", increment index_counter and add it to the dictionary with a unique key
            if v.startswith("{{"):
                index_counter += 1

                # Insert text directly into description
                description += f"{{value_{index_counter}}}"

                # Extract only the part of the value after the last "|"
                match_result = re.findall(r"\|.*\|(.*)\}\}", v)
                if match_result:  # Check if the list is not empty
                    extracted_value = match_result[0]
                    # If the extracted value can be converted to an int, do so. If not, keep it as is.
                    try:
                        converted_value = int(extracted_value)
                    except ValueError:
                        converted_value = extracted_value

                    values_dict[f"value_{index_counter}"] = converted_value
            else:
                description += v

        # Store the description with placeholders and "{{..}}" structures separately
        target["combat_skill"][skill_code]["description"] = description
        target["combat_skill"][skill_code]["level"][skill_level] = values_dict


# 装备
def translate_equipment(match, item, target):
    key, value = item
    attribute_name = ""
    if match.group(2) == "名称":
        attribute_name = "name"
    if match.group(2) == "描述":
        attribute_name = "description"
    if match.group(2) == "详情":
        attribute_name = "detail"
    target.setdefault("equipment", {})
    target["equipment"][attribute_name] = value


# 记忆镌相
def translate_collection(match, item, target):
    key, value = item
    attribute_name = int(match.group(2))
    target.setdefault("collection", {})
    target["collection"][attribute_name] = value


# 记忆档案
def translate_document(match, item, target):
    key, value = item
    documents = target.setdefault("documents", [])
    doc_type_dict = {"名称": "title", "内容": "content"}
    doc_sequence = int(match.group(1)) - 1
    doc_type = doc_type_dict[match.group(2)]

    if key in ["", "无"] or value in ["", "无"]:
        return
    else:
        try:
            target_item = documents[doc_sequence]
        except IndexError:
            # 插入一个新的字典，如果doc_sequence超出了列表的长度
            documents.insert(doc_sequence, {doc_type: value})
        else:
            target_item.update({doc_type: value})


# 特性
def translate_trait(match, item, target):
    key, value = item
    trait = target.setdefault("trait", {})
    trait.setdefault("description", {})

    if match.group(2) == "名称":
        trait["name"] = value
    else:
        attribute_name = match.group(3).lower()
        trait["description"][attribute_name] = value


training_attribute_name = ""


# 训练
def translate_training(match, item, target):
    key, value = item
    step_num = f"phase_{int(match.group(4))}"
    target.setdefault("training", {}).setdefault(step_num, {})
    global training_attribute_name

    if match.group(5) == "属性":
        if value:
            base_training_attribute_name = training_dict[value[2:]]
            count = 1
            training_attribute_name = base_training_attribute_name
            while training_attribute_name in target["training"][step_num]:
                training_attribute_name = (
                    base_training_attribute_name + "_" + str(count)
                )
                count += 1
            target["training"][step_num].setdefault(training_attribute_name, "")
    else:
        if value:
            # The training_attribute_name will be the one from the previous call
            target["training"][step_num][training_attribute_name] = value
        else:
            target["training"][step_num] = {}


# 穹顶技能
def translate_dome_skill(match, item, target):
    key, value = item
    dom_skill = target.setdefault("dome_skill", {})
    if not match.group(3):
        dom_skill.setdefault("1", {})
        if match.group(4) == "名称":
            dom_skill["1"]["name"] = value
        else:
            dom_skill["1"]["description"] = value
    else:
        dom_skill.setdefault(match.group(3), {})
        if match.group(4) == "名称":
            dom_skill[match.group(3)]["name"] = value
        else:
            dom_skill[match.group(3)]["description"] = value


# 报告
def translate_report(match, item, target):
    key, value = item
    target.setdefault("report", {})
    attribute_name = report_dict[key]
    target["report"][attribute_name] = value


# 异核报告
def translate_seed_data(match, item, target):
    key, value = item
    target.setdefault("seed_report", {})
    attribute_name = seed_data[key]
    target["seed_report"][attribute_name] = value


def translate_character(origin_dict):
    translated_dict = {}
    skill_regs = "|".join(re.escape(key) for key in skill_dict)
    combat_regs = "|".join(r"\b" + re.escape(key) + r"\b" for key in combat_dict)
    report_regs = "|".join(r"\b" + re.escape(key) + r"\b" for key in report_dict)
    seed_data_regs = "|".join(r"\b" + re.escape(key) + r"\b" for key in seed_data)

    for key, value in origin_dict.items():
        item = [key, value]
        if match := re.match(r"(S\d+)(体质|专精|攻击)(加成)", key):
            translate_basic_stat(match, item, translated_dict)
        elif match := re.match(combat_regs, key):
            translate_combat_stats(match, item, translated_dict)
        elif match := re.match(r"(S\d+)(作为队长时蚀刻初始属性-)(.+)", key):
            translate_captain_attribute(match, item, translated_dict)
        elif match := re.match(r"(技能|异核)(\d+)?(" + skill_regs + ")(.*)", key):
            translate_combat_skill(match, item, translated_dict)
        elif match := re.match(r"(专精影响分支-)(.+)", key):
            translate_mastery_bonus(match, item, translated_dict)
        elif match := re.match(r"记忆档案(\d+)-(内容|名称)", key):
            translate_document(match, item, translated_dict)
        elif match := re.match(r"(装备-)(.+)", key):
            translate_equipment(match, item, translated_dict)
        elif match := re.match(r"(记忆镌相)(.+)", key):
            translate_collection(match, item, translated_dict)
        elif match := re.match(r"(特性)(名称|-描述)(.+)?", key):
            translate_trait(match, item, translated_dict)
        elif match := re.match(r"(项目)(\d+)(阶段)(\d+)(属性|数值)", key):
            translate_training(match, item, translated_dict)
        elif match := re.match(r"(穹顶)(技能)(\d+)?(名称|描述)", key):
            translate_dome_skill(match, item, translated_dict)
        elif match := re.match(report_regs, key):
            translate_report(match, item, translated_dict)
        elif match := re.match(seed_data_regs, key):
            translate_seed_data(match, item, translated_dict)

        elif english_attribute := base_dict.get(key, key):
            valid_attributes = {
                "tags",
                "engraving_skills",
                "acquisitions",
                "expressions",
            }

            if english_attribute in valid_attributes:
                translated_dict[english_attribute] = value.split(",")
            elif english_attribute == "profession":
                translated_dict[english_attribute] = profession_dict[value]
            elif english_attribute == "element":
                translated_dict[english_attribute] = element_dict[value]
            else:
                translated_dict[english_attribute] = value
    return translated_dict


__all__ = ["translate_character"]
