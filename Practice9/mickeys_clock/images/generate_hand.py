"""
Run this once to generate the mickey_hand.png asset.
Requires Pillow: pip install Pillow
"""
from PIL import Image, ImageDraw
import math

W, H = 80, 220

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

glove_cx, glove_cy = W // 2, 52
glove_r = 34

draw.ellipse(
    [glove_cx - glove_r, glove_cy - glove_r,
     glove_cx + glove_r, glove_cy + glove_r],
    fill=(255, 255, 255, 255),
    outline=(30, 30, 30, 255),
    width=3,
)

for angle_deg, bump_r in [(-35, 20), (0, 22), (35, 20)]:
    a = math.radians(angle_deg - 90)
    bx = glove_cx + int((glove_r - 4) * math.cos(a))
    by = glove_cy + int((glove_r - 4) * math.sin(a))
    draw.ellipse(
        [bx - bump_r, by - bump_r, bx + bump_r, by + bump_r],
        fill=(255, 255, 255, 255),
        outline=(30, 30, 30, 255),
        width=2,
    )

thumb_angle = math.radians(30 - 90)
tx = glove_cx + int((glove_r - 2) * math.cos(thumb_angle))
ty = glove_cy + int((glove_r - 2) * math.sin(thumb_angle))
draw.ellipse([tx - 14, ty - 10, tx + 14, ty + 10],
             fill=(255, 255, 255, 255), outline=(30, 30, 30, 255), width=2)

draw.line(
    [(glove_cx - glove_r + 8, glove_cy + 6),
     (glove_cx + glove_r - 8, glove_cy + 6)],
    fill=(180, 180, 180, 200), width=2,
)

arm_top    = glove_cy + glove_r - 8   
arm_bottom = H - 2
arm_left   = W // 2 - 12
arm_right  = W // 2 + 12

draw.rectangle(
    [arm_left, arm_top, arm_right, arm_bottom],
    fill=(255, 165, 0, 255),
    outline=(180, 100, 0, 255),
    width=2,
)

cuff_h = 22
draw.rectangle(
    [arm_left - 4, arm_bottom - cuff_h,
     arm_right + 4, arm_bottom],
    fill=(220, 60, 60, 255),
    outline=(160, 30, 30, 255),
    width=2,
)

img.save("mickey_hand.png")
print("mickey_hand.png saved  (80 × 220 px, RGBA)")