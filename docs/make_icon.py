# -*- coding: utf-8 -*-
"""生成工具箱图标：账簿纸 + 红边线 + 一个「审」字。输出多尺寸 ico。"""
from PIL import Image, ImageDraw, ImageFont

PAPER = (247, 243, 235)
INK = (23, 21, 15)
RED = (166, 43, 31)
LINE = (228, 220, 204)

S = 1024
img = Image.new("RGB", (S, S), PAPER)
d = ImageDraw.Draw(img)

# 账簿横格线
for y in range(int(S * 0.12), S, int(S * 0.14)):
    d.line([(0, y), (S, y)], fill=LINE, width=max(2, S // 400))

# 左侧红边线
d.line([(int(S * 0.16), 0), (int(S * 0.16), S)], fill=RED, width=max(4, S // 170))

# 「审」字
font = None
for path in (r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"):
    try:
        font = ImageFont.truetype(path, int(S * 0.50))
        break
    except Exception:  # noqa: BLE001
        continue
if font is None:
    raise SystemExit("没有可用中文字体")

text = "审"
box = d.textbbox((0, 0), text, font=font)
w, h = box[2] - box[0], box[3] - box[1]
cx = (S * 0.16 + S) / 2
d.text((cx - w / 2 - box[0], (S - h) / 2 - box[1]), text, font=font, fill=INK)

img.save("icon_1024.png")
img.resize((256, 256), Image.LANCZOS).save(
    "app.ico", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("app.ico written")
