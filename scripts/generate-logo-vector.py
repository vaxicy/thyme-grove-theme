#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thyme Grove Theme — vector logo candidates (SVG rendered by headless Chromium).

Same quality bar as the latest themes: gradient fills, a soft drop shadow and
highlight streaks on every mark, consistent 24–232 safe box.

Playwright screenshots each SVG cell with omit_background=True (true
transparency); PIL only composes the contact sheets, the inline strip and the
official logo/logo.png exported from SELECTED.

Colours come from manifest.json. Change SELECTED and re-run; never hand-copy PNGs.
"""
import json
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))                      # relative paths only (non-ASCII path safety)

SIZE = 128
CELL = 512
PREVIEW = 256
SELECTED = "01"
CAND_DIR = Path("logo/candidates")
LOGO_OUT = Path("logo/logo.png")

with open("manifest.json", "r", encoding="utf-8") as f:
    _m = json.load(f)
_C, _P = _m["theme"]["colors"], _m["theme"]["properties"]


def hx(vals):
    return "#%02X%02X%02X" % tuple(vals)


SAGE = hx(_C["frame"])                             # #B2BD7E
PALE = hx(_C["ntp_background"])                    # #D9D28B
OLIVE = hx(_P["ntp_button_background"])            # #8E9162
MOSS = hx(_C["ntp_link"])                          # #4A5741
INK = hx(_C["ntp_text"])                           # #2F3A28

SHADOW = """
  <filter id="ds" x="-35%%" y="-35%%" width="170%%" height="170%%">
    <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="%s" flood-opacity=".20"/>
  </filter>""" % MOSS


def svg_open(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 256 256">%s%s</svg>' % (CELL, CELL, defs, body))


def bezier(p0, p1, p2, p3, t):
    mt = 1 - t
    return (mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0],
            mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1])


def tangent_deg(p0, p1, p2, p3, t):
    mt = 1 - t
    dx = 3 * mt * mt * (p1[0] - p0[0]) + 6 * mt * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * mt * mt * (p1[1] - p0[1]) + 6 * mt * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    return math.degrees(math.atan2(dy, dx))


def leaflet(x, y, angle, length, fill, vein=None, width_k=0.34):
    w = length * width_k
    d = ('M0 0 C %.1f %.1f %.1f %.1f %.1f 0 C %.1f %.1f %.1f %.1f 0 0 Z'
         % (length * 0.34, -w, length * 0.78, -w * 0.95, length,
            length * 0.78, w * 0.95, length * 0.34, w))
    out = '<g transform="translate(%.2f %.2f) rotate(%.2f)"><path d="%s" fill="%s"/>' % (
        x, y, angle, d, fill)
    if vein:
        out += ('<path d="M%.1f 0 H%.1f" stroke="%s" stroke-opacity=".30" stroke-width="%.2f" '
                'stroke-linecap="round" fill="none"/>' % (
                    length * 0.10, length * 0.86, vein, max(1.4, length * 0.05)))
    return out + '</g>'


def sprig(p0, p1, p2, p3, pairs=6, leaf_len=34, decay=0.45, spread=58, fill="", vein=None):
    out = []
    for i in range(pairs):
        t = 0.16 + 0.74 * i / (pairs - 1)
        x, y = bezier(p0, p1, p2, p3, t)
        ang = tangent_deg(p0, p1, p2, p3, t)
        length = leaf_len * (1 - decay * i / (pairs - 1))
        for side in (1, -1):
            out.append(leaflet(x, y, ang + side * spread, length, fill, vein))
    return "".join(out)


def stem(p0, p1, p2, p3, width=6.0, color=MOSS):
    return ('<path d="M%.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" stroke="%s" stroke-width="%.1f" '
            'stroke-linecap="round" fill="none"/>'
            % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], color, width))


STEM = ((128, 226), (120, 176), (136, 118), (150, 52))

# ------------------------------------------------------------------ candidates
SVG_01 = svg_open("""
<defs>
  <linearGradient id="lf1" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="%s"/>
    <stop offset="0.55" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  %s
  %s
</g>
<path d="M128 226 q6 -18 20 -26" stroke="%s" stroke-width="5" stroke-linecap="round" fill="none"/>
""" % (MOSS, OLIVE, SAGE, SHADOW,
       stem(*STEM, width=7, color=MOSS),
       sprig(*STEM, pairs=6, leaf_len=40, fill="url(#lf1)", vein=MOSS),
       SAGE))

SVG_02 = svg_open("""
<defs>
  <linearGradient id="lf2" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="%s"/>
    <stop offset="0.5" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <g transform="rotate(26 128 140)">
    %s
    %s
  </g>
  <g transform="rotate(-26 128 140)">
    %s
    %s
  </g>
</g>
""" % (MOSS, OLIVE, SAGE, SHADOW,
       stem((128, 218), (118, 154), (134, 74), (128, 60), width=7, color=MOSS),
       sprig((128, 218), (118, 154), (134, 74), (128, 60), pairs=5, leaf_len=34,
             fill="url(#lf2)", vein=MOSS),
       stem((128, 218), (138, 154), (122, 74), (128, 60), width=7, color=MOSS),
       sprig((128, 218), (138, 154), (122, 74), (128, 60), pairs=5, leaf_len=34,
             fill="url(#lf2)", vein=MOSS)))

SVG_03 = svg_open("""
<defs>
  <linearGradient id="gp3" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  <path d="M40 162 Q128 92 216 162" fill="none" stroke="%s" stroke-width="10" stroke-linecap="round" stroke-opacity=".55"/>
  <path d="M50 188 Q128 126 206 188" fill="none" stroke="%s" stroke-width="16" stroke-linecap="round"/>
  <path d="M60 214 Q128 156 196 214" fill="none" stroke="url(#gp3)" stroke-width="21" stroke-linecap="round"/>
</g>
<circle cx="128" cy="76" r="15" fill="%s"/>
<path d="M128 90 V62" stroke="%s" stroke-width="6" stroke-linecap="round"/>
""" % (SAGE, MOSS, SHADOW, SAGE, OLIVE, OLIVE, MOSS))

SVG_04 = svg_open("""
<defs>
  <linearGradient id="tl4" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="0.55" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<rect x="34" y="34" width="188" height="188" rx="54" fill="url(#tl4)" filter="url(#ds)"/>
<g transform="rotate(-32 128 132)">
  <path d="M128 56 C170 88 170 168 128 208 C86 168 86 88 128 56 Z" fill="%s" fill-opacity=".92"/>
  <path d="M128 74 V190" stroke="%s" stroke-opacity=".45" stroke-width="5" stroke-linecap="round"/>
  <g stroke="%s" stroke-opacity=".35" stroke-width="4" stroke-linecap="round" fill="none">
    <path d="M128 100 C116 106 108 116 104 126"/>
    <path d="M128 100 C140 106 148 116 152 126"/>
    <path d="M128 130 C114 136 106 146 102 156"/>
    <path d="M128 130 C142 136 150 146 154 156"/>
  </g>
</g>
<ellipse cx="92" cy="88" rx="38" ry="24" fill="#FFFFFF" opacity=".16" transform="rotate(-24 92 88)"/>
""" % (SAGE, OLIVE, MOSS, SHADOW, PALE, MOSS, MOSS))

SVG_05 = svg_open("""
<defs>
  <linearGradient id="bd5" x1="0" y1="0" x2="0.8" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  <linearGradient id="lf5" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
</defs>
<circle cx="128" cy="128" r="102" fill="url(#bd5)"/>
<circle cx="128" cy="128" r="102" fill="none" stroke="%s" stroke-opacity=".20" stroke-width="4"/>
<g transform="translate(128 136) scale(0.66) translate(-128 -140)">
  %s
  %s
</g>
""" % (MOSS, INK, PALE, SAGE, PALE,
       stem((128, 224), (118, 168), (136, 104), (148, 48), width=8, color=PALE),
       sprig((128, 224), (118, 168), (136, 104), (148, 48), pairs=5, leaf_len=38,
             fill="url(#lf5)", vein=None)))

SVG_06 = svg_open("""
<defs>
  <linearGradient id="fl6" x1="0" y1="0" x2="0.7" y2="1">
    <stop offset="0" stop-color="%s"/>
    <stop offset="1" stop-color="%s"/>
  </linearGradient>
  %s
</defs>
<g filter="url(#ds)">
  %s
  <g fill="url(#fl6)">
    <circle cx="128" cy="86" r="17"/>
    <circle cx="104" cy="104" r="14"/>
    <circle cx="152" cy="104" r="14"/>
    <circle cx="116" cy="126" r="12"/>
    <circle cx="142" cy="126" r="12"/>
  </g>
</g>
<circle cx="128" cy="86" r="7" fill="%s"/>
<circle cx="104" cy="104" r="5.5" fill="%s"/>
<circle cx="152" cy="104" r="5.5" fill="%s"/>
%s
""" % (SAGE, OLIVE, SHADOW,
       stem((128, 226), (120, 190), (134, 150), (128, 120), width=7, color=MOSS),
       PALE, PALE, PALE,
       sprig((128, 226), (120, 190), (134, 150), (128, 120), pairs=3, leaf_len=30,
             fill=OLIVE, vein=None)))

CANDIDATES = [
    ("01", "thyme-sprig", "Thyme sprig with paired leaves — most literal", SVG_01),
    ("02", "thyme-pair", "Two crossed sprigs — herbal mark, good balance", SVG_02),
    ("03", "grove-arcs", "Grove canopy arcs — abstract, calm", SVG_03),
    ("04", "leaf-tile", "Leaf on a gradient tile — strongest at 32px", SVG_04),
    ("05", "sprig-badge", "Pale sprig in a moss badge — bold silhouette", SVG_05),
    ("06", "thyme-flower", "Thyme flower cluster — softest, most botanical", SVG_06),
]


def font(size, bold=False):
    for name in (("segoeuib.ttf", "seguisb.ttf") if bold else ("segoeui.ttf", "segoeuisl.ttf")):
        p = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def render_cells():
    cells = "".join('<div id="cell%s" style="width:%dpx;height:%dpx">%s</div>' % (num, CELL, CELL, svg)
                    for num, _n, _d, svg in CANDIDATES)
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            'html,body{margin:0;padding:0;background:transparent}'
            '#grid{display:flex;flex-wrap:wrap;width:%dpx}div[id^=cell]{display:block}'
            '</style></head><body><div id="grid">%s</div></body></html>' % (CELL * 3, cells))
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:
            b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": CELL * 3, "height": CELL * 2})
        pg.set_content(html)
        for num, name, _d, _svg in CANDIDATES:
            path = CAND_DIR / ("%s-%s.png" % (num, name))
            pg.locator("#cell" + num).screenshot(path=str(path), omit_background=True)
            img = Image.open(path).convert("RGBA").resize((PREVIEW, PREVIEW), Image.LANCZOS)
            img.save(path)
            bbox = img.split()[3].getbbox()
            assert bbox, "candidate %s rendered empty" % name
            assert bbox[0] > 6 and bbox[1] > 6 and bbox[2] < PREVIEW - 6 and bbox[3] < PREVIEW - 6, \
                "candidate %s touches the canvas edge: %s" % (name, bbox)
            out[num] = img
            print("candidate %s %s -> alpha bbox %s" % (num, name, bbox))
        b.close()
    return out


def contact_sheet(rendered, bg, txt, sub, path, title):
    cols, rows = 3, 2
    cw, ch = 384, 374
    gap, margin = 28, 40
    W = margin * 2 + cols * cw + (cols - 1) * gap
    H = margin * 2 + 34 + rows * ch + (rows - 1) * gap
    sheet = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(sheet)
    f_title, f_name, f_desc, f_file = font(24, True), font(21, True), font(15), font(14)
    d.text((margin, margin), title, font=f_title, fill=txt)
    y0 = margin + 34
    for i, (num, name, desc, _svg) in enumerate(CANDIDATES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = y0 + r * (ch + gap)
        big = rendered[num].resize((220, 220), Image.LANCZOS)
        sheet.paste(big, (x + (cw - 220) // 2, y + 14), big)
        d.text((x + 18, y + 250), "%s · %s" % (num, name), font=f_name, fill=txt)
        d.text((x + 18, y + 280), desc, font=f_desc, fill=sub)
        thumb = rendered[num].resize((32, 32), Image.LANCZOS)
        sheet.paste(thumb, (x + 18, y + 330), thumb)
        d.text((x + 60, y + 339), "%s.png  256x256" % name, font=f_file, fill=sub)
        assert y + 300 <= y + 322, "text block collides with the thumbnail row"
    sheet.save(path)
    print("saved:", path, sheet.size)


def inline_strip(rendered, path):
    n, cell, gap, margin = len(CANDIDATES), 108, 22, 30
    W = margin * 2 + n * cell + (n - 1) * gap
    H = margin * 2 + cell + 30
    strip = Image.new("RGB", (W, H), (243, 240, 218))
    d = ImageDraw.Draw(strip)
    f = font(15, True)
    for i, (num, _n, _d, _s) in enumerate(CANDIDATES):
        x = margin + i * (cell + gap)
        img = rendered[num].resize((cell, cell), Image.LANCZOS)
        strip.paste(img, (x, margin), img)
        d.text((x + cell // 2 - 8, margin + cell + 8), num, font=f, fill=(47, 58, 40))
    strip.save(path)
    print("saved:", path, strip.size)


def main():
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rendered = render_cells()
    contact_sheet(rendered, (243, 240, 218), (47, 58, 40), (120, 126, 96),
                  CAND_DIR / "contact-light.png", "Thyme Grove — vector logo candidates (light)")
    contact_sheet(rendered, (44, 52, 38), (217, 210, 139), (150, 162, 116),
                  CAND_DIR / "contact-dark.png", "Thyme Grove — vector logo candidates (dark)")
    inline_strip(rendered, CAND_DIR / "inline-strip.png")
    sel = [c for c in CANDIDATES if c[0] == SELECTED][0]
    icon = rendered[sel[0]].resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(LOGO_OUT)
    print("official icon from SELECTED=%s (%s):" % (sel[0], sel[1]), LOGO_OUT, icon.size)


if __name__ == "__main__":
    main()
