#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仙门物语 素材生成 v2：全身立绘 + 场景加群众 + CG 加性暗示。
10 张：portraits_full(4) + scenes 重绘(2) + cg 重绘(4)。"""
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

# ---------- 1. 角色全身立绘（full body） ----------
FULLS = [
    ("hero_full",
     "anime style 2D game character full body standing portrait, "
     "handsome well-built teenage boy full view head to toe, black hair, bright cheerful eyes, "
     "green cotton wuxia robe, standing pose, shy playful smile, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 5001),
    ("shifu_full",
     "anime style 2D game character full body standing portrait, "
     "mature elegant beauty full view head to toe, long white hair single ponytail, crimson red eyes, "
     "large breasts, thin translucent white silk robe flowing, standing pose, cold noble expression, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 5002),
    ("shijie_full",
     "anime style 2D game character full body standing portrait, "
     "mature lively beauty full view head to toe, long loose red hair, bright crimson eyes, "
     "large breasts, skimpy red swimsuit-like wuxia outfit, standing pose, playful teasing smile, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 5003),
    ("shimei_full",
     "anime style 2D game character full body standing portrait, "
     "cute little girl full view head to toe, grey hair twin tails, big dark purple eyes, "
     "small flat chest, simple blue robes, standing pose, sweet innocent smile, " + FACE +
     "clean soft background, game CG illustration, high quality, masterpiece", 5004),
]

# ---------- 2. 场景重绘：加群众 ----------
SCENES = [
    ("market",
     "anime style game background scenery, lively ancient chinese market street, "
     "crowds of people shopping and chatting, stalls and lanterns, bustling market activity, "
     "warm daylight, game CG background, high quality", 5005),
    ("battle",
     "anime style game background scenery, battlefield at the sect gate, "
     "many soldiers and cultivators fighting in the background, red flames, broken swords, demon mist, "
     "dramatic night battle scene, game CG background, high quality", 5006),
]

# ---------- 3. 特殊 CG 重绘：加性暗示（艺术性、含蓄） ----------
SENSUAL = "sensual suggestive atmosphere, thin wet translucent fabric clinging to skin, flushed cheeks, half-lidded alluring eyes, intimate mood, tasteful artistic"
CGS = [
    ("cg_spring",
     "anime style game CG illustration, red-haired beauty in thin wet bathrobe "
     "in a hot spring at night, leaning close to a boy, " + SENSUAL + ", steam and moonlight, " + FACE,
     5007),
    ("cg_poison",
     "anime style game CG illustration, white-haired beauty kneeling under a tree "
     "in moonlight, thin white robe slipping off shoulder, " + SENSUAL + ", distressed yet alluring, " + FACE,
     5008),
    ("cg_ending1",
     "anime style game CG illustration, white-haired beauty in translucent white robe and "
     "handsome boy embracing closely under blooming peach trees, " + SENSUAL + ", spring sunshine, "
     "happy ending, " + FACE,
     5009),
    ("cg_ending2",
     "anime style game CG illustration, red-haired beauty in red wedding dress and "
     "handsome boy embracing in a sea of red lotus flowers, " + SENSUAL + ", joyful wedding night, " + FACE,
     5010),
]

all_jobs = [(os.path.join(BASE, "portraits"), n, p, s) for n, p, s in FULLS] + \
           [(os.path.join(BASE, "scenes"), n, p, s) for n, p, s in SCENES] + \
           [(os.path.join(BASE, "cg"), n, p, s) for n, p, s in CGS]

total = len(all_jobs)
for i, (outdir, n, p, s) in enumerate(all_jobs):
    print(f"[{i+1}/{total}] 生成 {n} ...", flush=True)
    print("  " + gen(outdir, n, p, s), flush=True)
    if i < total - 1:
        time.sleep(8)
print("ALL DONE", flush=True)
