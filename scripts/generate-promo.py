#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thyme Grove Theme — promo tiles (440x280 + 1400x560), all English.

Colours are read from manifest.json. Five palette blocks sit on a shelf across
the full width; each canvas keeps its own geometry and font scale, with bounds
assertions so overflow fails loudly at generation time.
"""
import json
import os
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

OUT_DIR = "store-assets/promo"


def save_png(img, path, tries=5):
    """PIL intermittently raises OSError [Errno 22] on this non-ASCII project path.

    Observed on Windows: the very same save() succeeds on one run and fails on the
    next, so retry a few times instead of crashing the whole generation.
    """
    last = None
    for i in range(tries):
        try:
            img.save(path)
            return
        except OSError as exc:            # pragma: no cover - environment specific
            last = exc
            time.sleep(0.35 * (i + 1))
    raise last


def rgb(vals):
    return tuple(vals)


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def bg_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, h - 1)))
    return img


def draw_chip(d, x, y, h, label, f, fill, txt, pad=18):
    w = text_w(d, label, f) + pad * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill)
    d.text((x + pad, y + (h - f.size) // 2 - 3), label, font=f, fill=txt)
    return w


def compose(size, geom, colors, props):
    W, H = size
    M = geom["margin"]
    RIGHT = W - M

    img = bg_gradient(size, rgb(colors["ntp_background"]), rgb(colors["button_background"]))
    d = ImageDraw.Draw(img)

    ink = rgb(colors["ntp_text"])
    sub = lerp(ink, rgb(colors["ntp_background"]), 0.34)
    chip_bg = rgb(colors["ntp_header"])
    cta_bg = rgb(colors["frame"])
    cta_txt = rgb(colors["tab_text"])

    # palette strip: one long band across the full width, split into segments
    # (user request 2026-10-20: long strips instead of a tile grid, so the
    #  composition no longer leaves the left side empty)
    # big palette blocks spread across the full width (user request 2026-10-20:
    # larger, blocky, distributed — not crowded on the right). Five distinct
    # colours ordered pale -> deep, sitting on a shelf under the text column.
    block_colors = [rgb(colors["ntp_background"]), rgb(colors["button_background_secondary"]),
                    rgb(colors["frame"]), rgb(props["ntp_button_background"]),
                    rgb(colors["ntp_link"])]
    n = len(block_colors)
    row_y, row_h, bgap = geom["row_y"], geom["row_h"], geom["row_gap"]
    bw = (RIGHT - M - bgap * (n - 1)) / n
    radius = min(bw, row_h) * 0.22
    assert bw > row_h * 0.8, "blocks should read as blocks, not thin strips"
    assert row_y + row_h <= H - 14, "block row too close to the canvas bottom"
    assert row_y >= geom["cta_y"] + geom["cta_h"] + 8, "block row overlaps the CTA"

    # a very soft shadow keeps the palest blocks readable against a same-hue
    # background without drawing an outline
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    x = M
    for _ in block_colors:
        sd.rounded_rectangle([x, row_y + 5, x + bw, row_y + row_h + 5],
                             radius=radius, fill=ink + (28,))
        x += bw + bgap
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))
    img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
    d = ImageDraw.Draw(img)

    x = M
    for col in block_colors:
        d.rounded_rectangle([x, row_y, x + bw, row_y + row_h], radius=radius, fill=col)
        x += bw + bgap
    assert x - bgap <= RIGHT + 0.5, "palette blocks overflow the right margin"

    lsize = geom["logo"]
    logo = Image.open("logo/logo.png").convert("RGBA").resize((lsize, lsize), Image.LANCZOS)
    img.paste(logo, (M, geom["logo_y"]), logo)

    f_title, f_sub = font(geom["title_size"], True), font(geom["sub_size"])
    tx = M + (lsize + geom["logo_gap"] if geom["title_beside_logo"] else 0)
    ty = geom["title_y"] if geom["title_beside_logo"] else geom["logo_y"] + lsize + geom["logo_gap"]
    d.text((tx, ty), geom["title"], font=f_title, fill=ink)
    sub_y = ty + geom["title_size"] + geom["title_sub_gap"]
    d.text((tx if geom["title_beside_logo"] else M, sub_y), geom["subtitle"], font=f_sub, fill=sub)
    assert geom["title_sub_gap"] >= 8, "title/subtitle gap too tight"

    f_chip = font(geom["chip_size"])
    cx, cy = (tx if geom["title_beside_logo"] else M), sub_y + geom["sub_size"] + geom["chip_gap"]
    for label in geom["chips"]:
        w = draw_chip(d, cx, cy, geom["chip_h"], label, f_chip, chip_bg, ink)
        cx += w + geom["chip_gap_x"]
    assert cx - geom["chip_gap_x"] <= RIGHT, "chip row overflows the right margin"

    f_cta = font(geom["cta_size"], True)
    btn_w, btn_h = geom["cta_w"], geom["cta_h"]
    btn_x = (RIGHT - btn_w) if geom.get("cta_right") else M
    btn_y = geom["cta_y"] if geom["cta_beside"] else cy + geom["chip_h"] + geom["cta_gap"]
    d.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=btn_h // 2, fill=cta_bg)
    tw = text_w(d, geom["cta"], f_cta)
    d.text((btn_x + (btn_w - tw) // 2, btn_y + (btn_h - f_cta.size) // 2 - 3),
           geom["cta"], font=f_cta, fill=cta_txt)
    assert btn_y + btn_h <= H - 12, "CTA button too close to the canvas bottom"
    assert btn_x + btn_w <= RIGHT, "CTA button overflows the right margin"
    return img, {"btn": (btn_x, btn_y, btn_w, btn_h),
                 "blocks": (M, row_y, RIGHT - M, row_h)}


LARGE = {
    "margin": 70,
    "logo": 104, "logo_y": 82, "logo_gap": 26, "title_beside_logo": True,
    "title": "Thyme Grove", "title_size": 58, "title_y": 98,
    "title_sub_gap": 14, "subtitle": "An herbal olive Chrome theme", "sub_size": 21,
    "chips": ["Solid colors", "Olive palette", "Easy on the eyes"],
    "chip_size": 15, "chip_h": 34, "chip_gap": 34, "chip_gap_x": 12,
    "cta": "Try It Now", "cta_size": 20, "cta_w": 210, "cta_h": 54,
    "cta_y": 225, "cta_beside": True, "cta_right": True,
    "row_y": 330, "row_h": 170, "row_gap": 18,
}

SMALL = {
    "margin": 28,
    "logo": 46, "logo_y": 22, "logo_gap": 10, "title_beside_logo": False,
    "title": "Thyme Grove", "title_size": 26, "title_y": 0,
    "title_sub_gap": 8, "subtitle": "An herbal olive Chrome theme", "sub_size": 12,
    "chips": ["Solid colors", "Olive palette"],
    "chip_size": 10, "chip_h": 22, "chip_gap": 12, "chip_gap_x": 8,
    "cta": "Try It Now", "cta_size": 13, "cta_w": 118, "cta_h": 36,
    "cta_y": 136, "cta_gap": 16, "cta_beside": True, "cta_right": True,
    "row_y": 224, "row_h": 40, "row_gap": 7,
}


def main():
    with open("manifest.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        c = data["theme"]["colors"]
        p = data["theme"]["properties"]
    os.makedirs(OUT_DIR, exist_ok=True)
    for size, geom in (((1400, 560), LARGE), ((440, 280), SMALL)):
        img, boxes = compose(size, geom, c, p)
        out = "%s/%dx%d.png" % (OUT_DIR, size[0], size[1])
        save_png(img, out)
        print("saved:", out, img.size, img.mode, "cta:", boxes["btn"], "blocks:", boxes["blocks"])


if __name__ == "__main__":
    main()
