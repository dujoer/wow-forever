# -*- coding: utf-8 -*-
import io, os

BASE = r"G:/ai/game/wow_forever"

# 每个文件: 列表 of (old, new)
REPL = {
    "classes-and-gear.md": [
        ("寻路 Pathfinding", "寻路（Pathfinding）"),
        ("集中火力 Focused Fire", "集中火力（Focused Fire）"),
        ("强化复活宠物 Improved Revive Pet", "强化复活宠物（Improved Revive Pet）"),
        ("神恩 Benediction", "祈福（Benediction）"),
        ("信念 Conviction", "定罪（Conviction）"),
        ("命令圣印 Seal of Command", "命令圣印（Seal of Command）"),
        ("咒逐 Malediction", "邪咒（Malediction）"),
        ("瘟疫 Pandemic", "恶疾（Pandemic）"),
        ("强化腐蚀术 Improved Corruption", "强化腐蚀术（Improved Corruption）"),
        ("灵魂收割 Soul Harvest", "灵魂收割（Soul Harvest）"),
        ("强化冰霜箭 Improved Frostbolt", "强化寒冰箭（Improved Frostbolt）"),
        ("冰碎片 Ice Shards", "碎冰（Ice Shards）"),
        ("刺骨冰寒 Piercing Ice", "穿刺之寒（Piercing Ice）"),
        ("雷霆打击 Thundering Strikes", "雷鸣打击（Thundering Strikes）"),
        ("强化幽魂之狼 Improved Ghost Wolf", "强化幽魂之狼（Improved Ghost Wolf）"),
        ("精神敏捷 Mental Dexterity", "精神敏捷（Mental Dexterity）"),
        ("萨满专注 Shamanistic Focus", "萨满专注（Shamanistic Focus）"),
        ("凶猛 Ferocity", "凶猛（Ferocity）"),
        ("野性迅捷 Feral Swiftness", "野性迅捷（Feral Swiftness）"),
        ("厚皮 Thick Hide", "厚皮（Thick Hide）"),
        ("锐利之爪 Sharpened Claws", "锐利之爪（Sharpened Claws）"),
        ("强化邪恶攻击 Improved Sinister Strike", "强化邪恶攻击（Improved Sinister Strike）"),
        ("强化剔骨 Improved Eviscerate", "强化剔骨（Improved Eviscerate）"),
        ("精准 Precision", "精准（Precision）"),
        ("刺穿伤口 Puncturing Wounds", "穿刺之伤（Puncturing Wounds）"),
        ("魔杖专精 Wand Specialization", "魔杖专精（Wand Specialization）"),
        ("精神分流 Spirit Tap", "精神分流（Spirit Tap）"),
        ("双生戒律 Twin Disciplines", "双生戒律（Twin Disciplines）"),
        ("强化真言术盾 Improved Power Word: Shield", "强化真言术：盾（Improved Power Word: Shield）"),
        ("残酷 Cruelty", "残酷（Cruelty）"),
        ("无羁狂怒 Unbridled Wrath", "无拘狂怒（Unbridled Wrath）"),
        ("刺耳怒吼 Piercing Howl", "刺耳怒吼（Piercing Howl）"),
        ("沿 Retribution 主干", "沿**惩戒系**主干"),
        ("沿 Frost 主干", "沿**冰霜系**主干"),
        ("43 点 Protection + 8 点 Retribution", "43 点**防护系** + 8 点**惩戒系**"),
        ("狮心头盔 Lionheart Helm", "狮心头盔（Lionheart Helm）"),
        ("剑师护手 Edgemaster's Handguards", "剑师护手（Edgemaster's Handguards）"),
        ("野性之皮 Hide of the Wild", "野性之皮（Hide of the Wild）"),
        ("西部荒野法杖 Staff of Westfall", "西部荒野法杖（Staff of Westfall）"),
        ("完美符文 Rune of Perfection", "完美符文（Rune of Perfection）"),
        ("狼人杀手护符 Worgenbane Talisman", "狼人杀手护符（Worgenbane Talisman）"),
        ("石猪剑 X'caliboar", "石猪剑（X'caliboar）"),
        ('毁灭"烧尽"', '毁灭"炼狱"'),
        ('> ⚠️ **中文天赋名为暂译**——国服客户端未上线，官方中文名未公布，请以括号内英文原名为准。',
         '> ⚠️ **天赋/技能名以国服（Beta 汉化）中文名为准，英文仅作括号参考**；最终以游戏内 tooltip 为准，Beta 数值仍可能调整。'),
    ],
    "intel-digest.md": [
        ("Unbridled Wrath 不再给双手武器双倍怒气", "**无拘狂怒**不再给双手武器双倍怒气"),
        ("毁灭系转向真火法：烧尽 Incinerate 为 30 级后终极", "毁灭系转向真火法：**炼狱 Incinerate** 为 30 级后终极"),
        ("烧尽 / 灾厄浩劫", "燃尽 / 灾厄浩劫"),
        ("烧尽/灾厄浩劫/炼狱 Incinerate", "燃尽/灾厄浩劫/炼狱 Incinerate"),
        ('"瘟疫/恶疾 Pandemic', '"恶疾 Pandemic'),
        ("| 瘟疫暴击伤害 |", "| 恶疾暴击伤害 |"),
        ("warlock.md 以英文为主（咒逐 Malediction / 瘟疫 Pandemic 等）",
         "**warlock.md 已校准为国服客户端中文名**（邪咒 / 恶疾 / 疲惫诅咒 / 怨毒 / 强化吸取 / 灵魂收割 等，英文仅作括号参考）"),
        (",warlock.md 待校准为中文", ""),
    ],
    "timeline.md": [
        ("痛苦系新增裂伤 Wrack 与瘟疫 Pandemic", "痛苦系新增裂伤 Wrack 与恶疾 Pandemic"),
        ("瘟疫/恶疾(+暴击伤害)", "恶疾(+暴击伤害)"),
        ("新增 3 天赋（Lingering Rage / Furious Precision / Gore Drinker）",
         "新增 3 天赋（余怒 Lingering Rage / 狂怒精准 Furious Precision / 嗜血者 Gore Drinker，暂译）"),
        ("移除 Improved Cleave 与 Boundless Rage", "移除 强化顺劈斩（Improved Cleave）与无尽怒气（Boundless Rage）"),
        ("Iron Will 入第 1 行、Toughness 移除", "钢铁意志（Iron Will）入第 1 行、坚韧（Toughness）移除"),
        ("Furious Precision 提供", "狂怒精准 提供"),
    ],
    "hunter.md": [
        ("狙击射击 Sniper Shot", "狙击射击（Sniper Shot）"),
        ("龙脊之刺 Wyvern Sting / 猎杀本能 Killer Instinct", "龙脊之刺（Wyvern Sting）/ 猎杀本能（Killer Instinct）"),
        ("独来独往 Lone Wolf", "独来独往（Lone Wolf）"),
    ],
    "leveling-and-gold.md": [
        ("Legacy「Talented」（5 级）", "Legacy「天赋异禀 Talented」（5 级）"),
        ("Legacy「Well Rested」优先拉满", "Legacy「休息充足 Well Rested」优先拉满"),
        ("Legacy「Thrill of Adventure」（5 级）", "Legacy「冒险快感 Thrill of Adventure」（5 级）"),
        ("Legacy 天赋 **Gourmand** 只延长食物 buff 时长", "Legacy 天赋 **美食家 Gourmand** 只延长食物 buff 时长"),
        ("**Permanence** 把营地增益从 1 小时拉到 1.5 小时", "**持久 Permanence** 把营地增益从 1 小时拉到 1.5 小时"),
        ("Legacy「Frequent Flier」（1 级）", "Legacy「常旅客 Frequent Flier」（1 级）"),
    ],
    "warlock.md": [
        # Conflagrate 在 Forever 国服译名为 燃尽（见 warlock 第72行定义）；原文宏内误写作 烧尽，统一校正
        ("烧尽", "燃尽"),
    ],
}

summary = []
for fn, pairs in REPL.items():
    path = os.path.join(BASE, fn)
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    total = 0
    report = []
    for old, new in pairs:
        cnt = text.count(old)
        if cnt:
            text = text.replace(old, new)
            total += cnt
        report.append((old[:24], cnt))
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
    summary.append((fn, total, report))

for fn, total, report in summary:
    print("=== %s : %d replacements ===" % (fn, total))
    for o, c in report:
        flag = "" if c else "  <-- ZERO"
        print("   [%2d] %-24s%s" % (c, o, flag))
