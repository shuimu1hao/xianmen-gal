#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仙门物语 素材生成：Pollinations.ai 串行+重试+验证。
19 张：portraits(4) + scenes(6) + cg(9)。"""
import io, os, sys, time, urllib.parse, urllib.request
from PIL import Image

BASE = os.path.expanduser("~/hermes11/xianmen-gal/assets")
for d in ("portraits", "scenes", "cg"):
    os.makedirs(os.path.join(BASE, d), exist_ok=True)

FACE = "detailed beautiful face, large sparkling eyes, sharp facial features, delicate skin, "

def gen(outdir, name, prompt, seed):  # 调用 Pollinations 生成立绘并保存outdir, name, prompt, seed):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) +
           f"?width=1024&height=1536&model=flux&nologo=true&seed={seed}")
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=240) as r:
                data = r.read()
            im = Image.open(io.BytesIO(data))
            im.load()
            with open(os.path.join(outdir, name + ".png"), "wb") as f:
                f.write(data)
            return f"{name}: OK {im.size} {len(data)}B"
        except Exception as e:
            if attempt < 3:
                print(f"  {name} fail({e}) 等15s重试...", flush=True)
                time.sleep(15)
            else:
                return f"{name}: FAIL {e}"
    return f"{name}: FAIL"

# ---------- 角色立绘（半身像 chest-up） ----------
ROLES = [
    # 主角 陆亘满（清秀少年）
    ("hero",
     "anime style 2D game character portrait, chest-up bust shot, "
     "handsome well-built teenage boy, black hair, bright cheerful eyes, "
     "green cotton wuxia robe, shy playful smile, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 2001),
    # 师傅 白霜华（白发红瞳单马尾 巨乳 白纱）
    ("shifu",
     "anime style 2D game character portrait, chest-up bust shot, "
     "mature elegant beauty, long white hair single ponytail, crimson red eyes, "
     "large breasts, thin translucent white silk robe, cold noble expression, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 2002),
    # 师姐 严吟烽（红发 巨乳 火系清凉衣）
    ("shijie",
     "anime style 2D game character portrait, chest-up bust shot, "
     "mature lively beauty, long loose red hair, bright crimson eyes, "
     "large breasts, skimpy red swimsuit-like wuxia outfit, playful teasing smile, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 2003),
    # 师妹 陆倩瑶（灰发双马尾 可爱小姑娘）
    ("shimei",
     "anime style 2D game character portrait, chest-up bust shot, "
     "cute little girl, grey hair twin tails, big dark purple eyes, "
     "small flat chest, simple blue robes, sweet innocent smile, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 2004),
]

# ---------- 场景立绘 ----------
SCENES = [
    ("gate", "anime style game background scenery, misty mountain gate of a xianxia sect, "
             "ancient stone archway with stairs leading up, clouds and pine trees, soft morning light, "
             "game CG background, high quality", 3001),
    ("cave", "anime style game background scenery, ice crystal cave interior, "
             "frost curtains, medicine furnace, meditation cushion, cold blue atmosphere, "
             "game CG background, high quality", 3002),
    ("spring", "anime style game background scenery, moonlit hot spring at night, "
               "steaming water, full moon, pine trees silhouette, warm lantern light, "
               "game CG background, high quality", 3003),
    ("market", "anime style game background scenery, lively ancient chinese market street, "
               "stalls and lanterns, crowd, warm daylight, "
               "game CG background, high quality", 3004),
    ("demon", "anime style game background scenery, dark demon army approaching a mountain sect, "
              "black clouds, torches, mountain gate silhouette, ominous red glow, "
              "game CG background, high quality", 3005),
    ("battle", "anime style game background scenery, battlefield at the sect gate, "
               "red flames, broken swords, demon mist, dramatic night, "
               "game CG background, high quality", 3006),
]

# ---------- 剧情 CG ----------
CGS = [
    ("cg_gate_meet", "anime style game CG illustration, white-haired beauty in white robe "
                     "standing under a mountain gate looking back, misty stairs, first meeting scene, " + FACE,
     4001),
    ("cg_guihua", "anime style game CG illustration, cute grey-haired twin-tail girl holding "
                  "a paper-wrapped osmanthus cake under moonlight, shy smile, " + FACE,
     4002),
    ("cg_spring", "anime style game CG illustration, red-haired beauty in thin wet bathrobe "
                  "in a hot spring at night looking back playfully, steam and moonlight, " + FACE,
     4003),
    ("cg_poison", "anime style game CG illustration, white-haired beauty kneeling under a tree "
                  "in moonlight, thin white robe, feverish blush, distressed expression, " + FACE,
     4004),
    ("cg_purple", "anime style game CG illustration, cute grey-haired girl standing in moonlight "
                  "looking at her hands, fingertips faintly purple, mysterious mood, " + FACE,
     4005),
    ("cg_demon_lord", "anime style game CG illustration, cute grey-haired girl walking out "
                      "of demon army, twin tails, purple glowing eyes, dark magic aura, "
                      "menacing yet beautiful, " + FACE,
     4006),
    ("cg_ending1", "anime style game CG illustration, white-haired beauty in white robe and "
                   "handsome boy standing together under blooming peach trees, spring sunshine, "
                   "happy ending, " + FACE,
     4007),
    ("cg_ending2", "anime style game CG illustration, red-haired beauty in red wedding dress "
                   "and handsome boy in a sea of red lotus flowers, joyful wedding, " + FACE,
     4008),
    ("cg_ending3", "anime style game CG illustration, cute grey-haired girl sitting by a bed "
                   "holding a bowl of porridge, chains shadow behind, dark cave with glowing pearls, "
                   "sweet yet creepy atmosphere, " + FACE,
     4009),
]

all_jobs = [(os.path.join(BASE, "portraits"), n, p, s) for n, p, s in ROLES] + \
           [(os.path.join(BASE, "scenes"), n, p, s) for n, p, s in SCENES] + \
           [(os.path.join(BASE, "cg"), n, p, s) for n, p, s in CGS]

total = len(all_jobs)
for i, (outdir, n, p, s) in enumerate(all_jobs):
    print(f"[{i+1}/{total}] 生成 {n} ...", flush=True)
    print("  " + gen(outdir, n, p, s), flush=True)
    if i < total - 1:
        time.sleep(8)
print("ALL DONE", flush=True)
