profession_dict = {
    "铁御": "bulwark",
    "轻卫": "vanguard",
    "尖锋": "striker",
    "筑术师": "ranger",
    "护佑者": "support",
    "战术家": "tactician",
    "游徒": "skirmisher",
}

profession_category_dict = {"方块": "square", "三角": "triangle", "菱形": "diamond"}

stat_dict = {
    "体质": "vitality",
    "防御": "defence",
    "攻击": "attack",
    "专精": "mastery",
    "终端": "terminal",
}

training_dict = {
    **stat_dict,
    **{
        "攻击速度": "attack_speed",
        "治愈力": "healing",
        "格挡强度": "block",
        "减伤": "basic_damage_reduction",
    },
}

rang_dict = {"近": "melee"}

element_dict = {
    "炎": "fire",
    "水": "water",
    "雷": "lighting",
    "霜": "ice",
    "风": "wind",
    "蚀": "corrosion",
    "物理": "physical",
}

elemental_reaction_dict = {"爆燃": "explosion"}

enemy_dict = {
    "一般单位": "common",
    "精英单位": "elite",
    "首领单位": "boss",
    "地面单位": "ground",
    "空中单位": "air",
    "原生单位": "native",
    "异种单位": "alien",
    "人形单位": "humanoid",
    "机械单位": "mechanical",
    "屏障保护": "shield",
}
