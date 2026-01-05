from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "static" / "images" / "aged_cheese.png"
CANVAS_SIZE = 512


def gradient_background(size: int) -> Image.Image:
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg)
    top = (10, 13, 36)
    bottom = (24, 28, 60)
    for y in range(size):
        ratio = y / (size - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3))
        draw.line([(0, y), (size, y)], fill=color + (255,))
    return bg


def cheese_layer(size: int) -> Image.Image:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    base_rect = (120, 250, 420, 430)
    draw.rounded_rectangle(base_rect, radius=90, fill=(255, 208, 104, 255))
    wedge = [(120, 260), (420, 260), (320, 130)]
    draw.polygon(wedge, fill=(255, 222, 148, 255))

    holes = [
        (190, 330, 26),
        (250, 380, 20),
        (330, 320, 30),
        (360, 380, 18),
        (250, 290, 14),
    ]
    for cx, cy, r in holes:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(238, 176, 80, 255))
        inset = max(r - 6, 4)
        draw.ellipse((cx - inset, cy - inset, cx + inset, cy + inset), fill=(255, 226, 160, 255))

    return layer


def shadow_layer(size: int) -> Image.Image:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse((150, 410, 360, 470), fill=(0, 0, 0, 120))
    return layer.filter(ImageFilter.GaussianBlur(18))


def highlight_layer(size: int) -> Image.Image:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.arc((80, 100, 480, 520), start=210, end=260, width=18, fill=(255, 255, 255, 96))
    draw.arc((120, 160, 420, 460), start=210, end=260, width=10, fill=(255, 255, 255, 80))
    return layer


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    background = gradient_background(CANVAS_SIZE)
    cheese = cheese_layer(CANVAS_SIZE)
    shadow = shadow_layer(CANVAS_SIZE)
    highlight = highlight_layer(CANVAS_SIZE)

    combined = Image.alpha_composite(background, shadow)
    combined = Image.alpha_composite(combined, cheese)
    combined = Image.alpha_composite(combined, highlight)

    final_img = combined.resize((360, 360), Image.LANCZOS)
    final_img.save(OUTPUT_PATH, "PNG")
    print(f"Saved aged cheese illustration to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
