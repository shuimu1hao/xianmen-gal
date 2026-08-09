#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按指定顺序生成画廊 HTML（不按文件名排序）。
用法：python3 make_gallery_ordered.py <输出html> <名字,逗号分隔> <图片路径...>"""
import base64, sys

def main():
    html_path = sys.argv[1]
    names = sys.argv[2].split(",") if len(sys.argv) > 2 else []
    imgs = sys.argv[3:]
    cards = ""
    for i, img in enumerate(imgs):
        nm = names[i] if i < len(names) else img.split("/")[-1].replace(".png", "")
        with open(img, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        cards += (f'<div class="card"><img src="data:image/png;base64,{b64}">'
                  f'<div class="nm">{nm}</div></div>\n')
    html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>立绘画廊</title>
<style>
body {{ margin:0; padding:24px; background:#12101e; color:#eee; font-family:sans-serif; }}
.grid {{ display:flex; flex-wrap:wrap; justify-content:center; gap:20px; }}
.card {{ background:#1e1a30; border-radius:12px; padding:12px; text-align:center; }}
.card img {{ height:480px; border-radius:8px; display:block; }}
.nm {{ margin-top:10px; color:#ffd878; font-weight:bold; }}
</style></head><body>
<div class="grid">{cards}</div>
</body></html>'''
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("gallery:", html_path, len(cards), "bytes,", len(imgs), "images")

if __name__ == "__main__":
    main()
