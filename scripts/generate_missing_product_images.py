from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Callable, Dict, Tuple
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from product_catalog import PRODUCT_IMAGE_MAP, PRODUCT_THEMES  # noqa: E402

STATIC_ROOT = BASE_DIR / "static"
IMAGES_DIR = STATIC_ROOT / "images"
CANVAS = 512
OUTPUT_SIZE = 360
BG_RADIUS = 40
FONT = ImageFont.load_default()

RGBColor = Tuple[int, int, int]


def hex_to_rgb(value: str, default: str = "#91a7ff") -> RGBColor:
    value = value.lstrip("#")
    if len(value) not in {3, 6}:
        value = default.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i : i + 2], 16) for i in range(0, 6, 2))  # type: ignore[return-value]


def blend(color: RGBColor, other: RGBColor, ratio: float) -> RGBColor:
    return tuple(int(color[i] * (1 - ratio) + other[i] * ratio) for i in range(3))


def gradient_background(primary: RGBColor, secondary: RGBColor) -> Image.Image:
    bg = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    for y in range(CANVAS):
        ratio = y / (CANVAS - 1)
        color = blend(primary, secondary, ratio * 0.85)
        draw.line([(0, y), (CANVAS, y)], fill=color + (255,))
    overlay = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    ImageDraw.Draw(overlay).ellipse((60, 40, 360, 340), fill=(255, 255, 255, 30))
    return Image.alpha_composite(bg, overlay)


def draw_leaf_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((150, 130, 360, 360), fill=secondary)
    draw.ellipse((170, 150, 340, 340), fill=primary)
    draw.line((255, 140, 255, 350), fill=(255, 255, 255, 200), width=6)


def draw_round_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((160, 150, 360, 350), fill=primary)
    draw.ellipse((190, 180, 330, 320), fill=secondary)


def draw_banana_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.pieslice((120, 200, 400, 420), start=200, end=340, fill=primary, outline=secondary, width=10)


def draw_spiky_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rounded_rectangle((200, 160, 320, 360), radius=40, fill=primary)
    for i in range(6):
        draw.polygon(
            [
                (230 + i * 15, 150),
                (240 + i * 15, 100),
                (250 + i * 15, 150),
            ],
            fill=secondary,
        )


def draw_carton_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((190, 150, 330, 360), fill=primary)
    draw.polygon([(190, 150), (260, 90), (400, 90), (330, 150)], fill=secondary)


def draw_cup_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((190, 200, 330, 360), fill=primary)
    draw.arc((320, 230, 380, 330), start=300, end=60, fill=secondary, width=18)
    draw.rectangle((180, 360, 340, 390), fill=secondary)


def draw_block_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rounded_rectangle((190, 220, 360, 360), radius=30, fill=primary)
    draw.rounded_rectangle((220, 190, 330, 300), radius=20, fill=secondary)


def draw_triangle_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.polygon([(170, 350), (380, 350), (320, 180)], fill=primary)
    draw.polygon([(200, 330), (350, 330), (320, 210)], fill=secondary)


def draw_ring_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((170, 200, 360, 390), fill=primary)
    draw.ellipse((210, 240, 320, 350), fill=secondary)


def draw_crescent_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((160, 230, 360, 410), fill=primary)
    draw.ellipse((200, 210, 400, 390), fill=secondary)


def draw_cupcake_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((200, 300, 330, 400), fill=secondary)
    draw.polygon([(180, 300), (350, 300), (265, 200)], fill=primary)
    draw.ellipse((220, 180, 310, 270), fill=primary)


def draw_fish_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((170, 230, 360, 330), fill=primary)
    draw.polygon([(340, 230), (400, 280), (340, 330)], fill=secondary)
    draw.ellipse((210, 260, 230, 280), fill=(255, 255, 255, 200))


def draw_shrimp_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.arc((150, 180, 370, 400), start=180, end=20, width=30, fill=primary)
    draw.arc((170, 200, 390, 420), start=180, end=20, width=30, fill=secondary)


def draw_strip_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rounded_rectangle((200, 220, 340, 360), radius=40, fill=primary)
    draw.rounded_rectangle((220, 200, 360, 340), radius=40, fill=secondary)


def draw_bag_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.polygon([(200, 160), (360, 160), (340, 380), (220, 380)], fill=primary)
    draw.rectangle((220, 140, 340, 190), fill=secondary)


def draw_box_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((200, 200, 360, 380), fill=primary)
    draw.polygon([(200, 200), (280, 150), (440, 150), (360, 200)], fill=secondary)


def draw_bowl_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.chord((170, 220, 370, 420), start=200, end=-20, fill=primary)
    draw.rectangle((190, 360, 350, 390), fill=secondary)


def draw_bundle_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    for offset in range(-20, 25, 10):
        draw.rectangle((250 + offset, 200, 260 + offset, 360), fill=primary)
    draw.rectangle((220, 320, 320, 350), fill=secondary)


def draw_scoop_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.pieslice((200, 240, 360, 400), start=180, end=360, fill=primary)
    draw.rectangle((260, 330, 400, 360), fill=secondary)


def draw_corn_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((220, 170, 320, 350), fill=primary)
    draw.polygon([(200, 220), (260, 370), (150, 360)], fill=secondary)
    draw.polygon([(340, 220), (280, 370), (390, 360)], fill=secondary)


def draw_chips_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    for offset in range(0, 50, 20):
        draw.ellipse((210 - offset, 250 - offset, 330 - offset, 330 - offset), fill=primary)
    draw.ellipse((260, 260, 360, 340), fill=secondary)


def draw_cookies_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((190, 260, 310, 380), fill=primary)
    draw.ellipse((260, 220, 360, 320), fill=secondary)


def draw_pretzel_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.line([(220, 280), (320, 360), (260, 360), (340, 280)], fill=primary, width=30)
    draw.line([(220, 280), (320, 280)], fill=secondary, width=20)


def draw_jar_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((210, 200, 350, 360), fill=primary)
    draw.rectangle((210, 180, 350, 210), fill=secondary)
    draw.rectangle((240, 150, 320, 180), fill=secondary)


def draw_can_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((220, 170, 320, 360), fill=primary)
    draw.ellipse((220, 150, 320, 210), fill=secondary)
    draw.ellipse((220, 320, 320, 380), fill=secondary)


def draw_bottle_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((250, 130, 290, 360), fill=secondary)
    draw.rectangle((190, 200, 350, 360), fill=primary)
    draw.rectangle((230, 100, 310, 150), fill=secondary)


def draw_jug_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((210, 180, 360, 360), fill=primary)
    draw.arc((320, 210, 420, 310), start=300, end=60, fill=secondary, width=20)


def draw_tube_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((240, 150, 300, 360), fill=primary)
    draw.polygon([(240, 150), (300, 150), (320, 100), (220, 100)], fill=secondary)


def draw_roll_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((200, 220, 360, 360), fill=primary)
    draw.ellipse((200, 200, 260, 380), fill=secondary)
    draw.ellipse((300, 200, 360, 380), fill=secondary)


def draw_bulb_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((200, 160, 360, 360), fill=primary)
    draw.rectangle((240, 320, 320, 360), fill=secondary)


def draw_pod_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((190, 200, 360, 320), fill=primary)
    draw.ellipse((220, 220, 330, 310), fill=secondary)


def draw_spiral_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.arc((180, 200, 360, 380), start=90, end=420, width=24, fill=primary)
    draw.arc((210, 230, 330, 350), start=90, end=420, width=18, fill=secondary)


def draw_oval_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.ellipse((190, 220, 360, 360), fill=primary)
    draw.ellipse((230, 250, 320, 330), fill=secondary)


def draw_loaf_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rounded_rectangle((170, 240, 380, 360), radius=60, fill=primary)
    draw.rounded_rectangle((200, 260, 340, 340), radius=40, fill=secondary)


def draw_churn_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((210, 220, 360, 360), fill=primary)
    draw.rectangle((240, 180, 330, 220), fill=secondary)


def draw_tub_icon(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw.rectangle((190, 260, 360, 360), fill=primary)
    draw.rectangle((170, 240, 380, 280), fill=secondary)


def draw_default(draw: ImageDraw.ImageDraw, primary: RGBColor, secondary: RGBColor) -> None:
    draw_round_icon(draw, primary, secondary)


STYLE_FUNCTIONS: Dict[str, Callable[[ImageDraw.ImageDraw, RGBColor, RGBColor], None]] = {
    "leaf": draw_leaf_icon,
    "round": draw_round_icon,
    "banana": draw_banana_icon,
    "pineapple": draw_spiky_icon,
    "carton": draw_carton_icon,
    "cup": draw_cup_icon,
    "block": draw_block_icon,
    "triangle": draw_triangle_icon,
    "ring": draw_ring_icon,
    "crescent": draw_crescent_icon,
    "cupcake": draw_cupcake_icon,
    "fish": draw_fish_icon,
    "shrimp": draw_shrimp_icon,
    "strip": draw_strip_icon,
    "bag": draw_bag_icon,
    "box": draw_box_icon,
    "bowl": draw_bowl_icon,
    "bundle": draw_bundle_icon,
    "scoop": draw_scoop_icon,
    "corn": draw_corn_icon,
    "chips": draw_chips_icon,
    "cookies": draw_cookies_icon,
    "pretzel": draw_pretzel_icon,
    "jar": draw_jar_icon,
    "can": draw_can_icon,
    "bottle": draw_bottle_icon,
    "jug": draw_jug_icon,
    "tube": draw_tube_icon,
    "roll": draw_roll_icon,
    "bulb": draw_bulb_icon,
    "pod": draw_pod_icon,
    "spiral": draw_spiral_icon,
    "oval": draw_oval_icon,
    "loaf": draw_loaf_icon,
    "tub": draw_tub_icon,
    "triangle_block": draw_triangle_icon,
    "wedge": draw_triangle_icon,
}

SHAPE_STYLE_MAP = {
    "round_leaf": "leaf",
    "berry": "leaf",
    "tomato": "round",
    "leafy": "leaf",
    "carrot": "leaf",
    "pod": "pod",
    "coconut": "round",
    "banana": "banana",
    "pineapple": "pineapple",
    "watermelon": "round",
    "carton": "carton",
    "cup": "cup",
    "block": "block",
    "wedge": "triangle",
    "cube": "block",
    "eggs": "oval",
    "loaf": "loaf",
    "croissant": "crescent",
    "muffin": "cupcake",
    "spiral": "spiral",
    "bagel": "ring",
    "cupcake": "cupcake",
    "steak": "oval",
    "fish": "fish",
    "meat_cut": "oval",
    "salmon": "fish",
    "shrimp": "shrimp",
    "bacon": "strip",
    "bag": "bag",
    "box": "box",
    "bowl": "bowl",
    "bundle": "bundle",
    "scoop": "scoop",
    "corn": "corn",
    "chips": "chips",
    "bar": "block",
    "cookies": "cookies",
    "mix_bowl": "bowl",
    "tub": "tub",
    "pretzel": "pretzel",
    "jar": "jar",
    "juice_box": "box",
    "can": "can",
    "bottle": "bottle",
    "soap": "block",
    "jug": "jug",
    "tube": "tube",
    "roll": "roll",
    "garlic": "bulb",
    "bulb": "bulb",
    "chips": "chips",
    "bundle": "bundle",
    "spiral": "spiral",
    "egg": "oval",
}


def get_style(shape: str) -> str:
    return SHAPE_STYLE_MAP.get(shape, "round")


def render_shape(shape: str, primary: RGBColor, secondary: RGBColor) -> Image.Image:
    canvas = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    style = get_style(shape)
    STYLE_FUNCTIONS.get(style, draw_default)(draw, primary, secondary)
    return canvas


def label_overlay(name: str) -> Image.Image:
    overlay = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    text = name[:16]
    bbox = draw.textbbox((0, 0), text, font=FONT)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    padding = 12
    box = (80, CANVAS - 90, CANVAS - 80, CANVAS - 40)
    draw.rounded_rectangle(box, radius=20, fill=(0, 0, 0, 120))
    draw.text(
        ((box[0] + box[2] - text_w) / 2, box[1] + (box[3] - box[1] - text_h) / 2),
        text,
        fill=(255, 255, 255, 230),
        font=FONT,
    )
    return overlay


def generate_image(product_name: str, rel_path: str) -> None:
    theme = PRODUCT_THEMES.get(
        product_name,
        {"shape": "round", "primary": "#8e9aaf", "secondary": "#cbc0d3"},
    )
    primary = hex_to_rgb(theme["primary"])
    secondary = hex_to_rgb(theme["secondary"])
    background = gradient_background(primary, secondary)
    icon = render_shape(theme.get("shape", "round"), primary, secondary)
    combined = Image.alpha_composite(background, icon)
    combined = Image.alpha_composite(combined, label_overlay(product_name))
    shadow = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((140, 360, 380, 430), fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    combined = Image.alpha_composite(shadow, combined)
    final_img = combined.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.LANCZOS)
    target = STATIC_ROOT / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    final_img.save(target, "PNG")
    print(f"🎨 Generated {rel_path} for {product_name}")


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    targets: "OrderedDict[str, str]" = OrderedDict()
    for product, rel_path in PRODUCT_IMAGE_MAP.items():
        targets.setdefault(rel_path, product)

    generated = 0
    for rel_path, product in targets.items():
        target_path = STATIC_ROOT / rel_path
        if target_path.exists():
            continue
        generate_image(product, rel_path)
        generated += 1

    if generated == 0:
        print("✅ All product images already exist – nothing to do!")
    else:
        print(f"✅ Generated {generated} product illustrations!")


if __name__ == "__main__":
    main()
