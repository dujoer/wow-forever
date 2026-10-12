# -*- coding: utf-8 -*-
import io, os
BASE = r"G:/ai/game/wow_forever"

REPL = {
    "intel-digest.md": [
        ("**烧尽 Incinerate**", "**炼狱 Incinerate**"),
        ("瘟疫/恶疾 Pandemic", "恶疾 Pandemic"),
        ("，warlock.md 待校准为中文", ""),
    ],
    "leveling-and-gold.md": [
        ("Gourmand", "美食家 Gourmand"),
        ("Permanence", "持久 Permanence"),
    ],
}

for fn, pairs in REPL.items():
    path = os.path.join(BASE, fn)
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    for old, new in pairs:
        cnt = text.count(old)
        text = text.replace(old, new)
        print("%s : %-40s -> %d" % (fn, old[:38], cnt))
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)
print("done")
