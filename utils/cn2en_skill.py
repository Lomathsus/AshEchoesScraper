base_dict = {
    "技能名称": "name",
    "稀有度": "rarity",
    "职业": "profession",
    "类型": "profession_type",
    "技能词条": "skill_entry",
    "技能描述": "skill_description",
    "技能图标": "skill_icon",
    "来源": "source",
    "点亮所需技能点": "skill_point_requirement",
    "元素": "element",
    "属性": "skill_attribute",
    "敌人类型": "enemy_type",
    "生效模式": "activation_mode",
    "增伤乘区": "damage_enhance",
    "减伤乘区": "damage_reduce",
    "目标减益乘区": "debuff",
    "属性乘区": "element_enhance",
    "特殊机制": "special_mechanism",
}


def translate_skill(origin_dict):
    translated_dict = {}

    for key, value in origin_dict.items():
        english_attribute = base_dict.get(key, key)
        translated_dict[english_attribute] = (
            value if not english_attribute == "profession" else value.split("、")
        )
    return translated_dict


__all__ = ["translate_skill"]
