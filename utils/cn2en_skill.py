from constant.dict import (
    profession_dict,
    profession_category_dict,
    element_dict,
    enemy_dict,
)
from constant.buff import damage_increase_dict, stats_increase_dict

base_dict = {
    "技能名称": "name",
    "稀有度": "rarity",
    "职业": "professions",
    "类型": "profession_types",
    "技能词条": "skill_tags",
    "技能描述": "skill_description",
    "技能图标": "skill_icon",
    "来源": "source",
    "点亮所需技能点": "point_requirement",
    "元素": "elements",
    "属性": "skill_stats",
    "敌人类型": "enemy_types",
    "生效模式": "activation_modes",
    "增伤乘区": "damage_increases",
    "减伤乘区": "damage_reduction",
    "目标减益乘区": "target_debuffs",
    "属性乘区": "stats_increases",
    "特殊机制": "special_mechanism",
}


def translate_skill(origin_dict):
    translated_dict = {}

    for key, value in origin_dict.items():
        english_attribute = base_dict.get(key, key)

        if english_attribute == "professions":
            parts = value.split("、")
            translated_dict[english_attribute] = (
                [profession_dict[part] for part in parts]
                if not parts[0] == "所有同调者"
                else "all"
            )
        elif english_attribute == "profession_types":
            parts = value.split("、")
            translated_dict[english_attribute] = [
                profession_category_dict[part] for part in parts
            ]
        elif english_attribute == "elements":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [element_dict[part] for part in parts] if not parts[0] == "" else []
            )
        elif english_attribute == "point_requirement":

            def is_convertible_to_int(val):
                try:
                    int(val)
                    return True
                except (ValueError, TypeError):
                    return False

            parts = value.split("/")
            translated_dict[english_attribute] = (
                [int(part) for part in parts] if is_convertible_to_int(parts[0]) else []
            )
        elif english_attribute == "enemy_types":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [enemy_dict[part] for part in parts] if not parts[0] == "" else []
            )
        elif english_attribute == "damage_increases":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [damage_increase_dict[part] for part in parts]
                if not parts[0] == ""
                else []
            )
        elif english_attribute == "stats_increases":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [stats_increase_dict[part] for part in parts]
                if not parts[0] == ""
                else []
            )
        elif english_attribute in [
            "skill_tags",
            "activation_modes",
            "special_mechanism",
            "target_debuffs",
        ]:
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [part for part in parts] if not parts[0] == "" else []
            )
        else:
            translated_dict[english_attribute] = value
    return translated_dict


__all__ = ["translate_skill"]
