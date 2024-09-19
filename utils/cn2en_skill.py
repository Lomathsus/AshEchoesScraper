from constant import (
    profession_dict,
    profession_type_dict,
    element_dict,
    enemy_dict,
    damage_increase_dict,
    stats_increase_dict,
)

base_dict = {
    "技能名称": "name",
    "稀有度": "rarity",
    "职业": "profession",
    "类型": "profession_type",
    "技能词条": "skill_tag",
    "技能描述": "skill_description",
    "技能图标": "skill_icon",
    "来源": "source",
    "点亮所需技能点": "point_requirement",
    "元素": "element",
    "属性": "skill_attribute",
    "敌人类型": "enemy_type",
    "生效模式": "activation_mode",
    "增伤乘区": "damage_increase",
    "减伤乘区": "damage_reduction",
    "目标减益乘区": "target_debuff",
    "属性乘区": "stat_increase",
    "特殊机制": "special_mechanism",
}


def translate_skill(origin_dict):
    translated_dict = {}

    for key, value in origin_dict.items():
        english_attribute = base_dict.get(key, key)

        if english_attribute == "profession":
            parts = value.split("、")
            translated_dict[english_attribute] = (
                [profession_dict[part] for part in parts]
                if not parts[0] == "所有同调者"
                else "all"
            )
        elif english_attribute == "profession_type":
            parts = value.split("、")
            translated_dict[english_attribute] = [
                profession_type_dict[part] for part in parts
            ]
        elif english_attribute == "element":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [element_dict[part] for part in parts] if not parts[0] == "" else []
            )
        elif english_attribute == "point_requirement":
            parts = value.split("/")
            translated_dict[english_attribute] = (
                [int(part) for part in parts] if not parts[0] == "" else []
            )
        elif english_attribute == "enemy_type":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [enemy_dict[part] for part in parts] if not parts[0] == "" else []
            )
        elif english_attribute == "damage_increase":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [damage_increase_dict[part] for part in parts]
                if not parts[0] == ""
                else []
            )
        elif english_attribute == "stat_increase":
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [stats_increase_dict[part] for part in parts]
                if not parts[0] == ""
                else []
            )
        elif english_attribute in [
            "skill_tag",
            "activation_mode",
            "special_mechanism",
            "target_debuff",
        ]:
            parts = value.split(",")
            translated_dict[english_attribute] = (
                [part for part in parts] if not parts[0] == "" else []
            )
        else:
            translated_dict[english_attribute] = value
    return translated_dict


__all__ = ["translate_skill"]
