<p align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/thyme-grove-theme/main/logo/logo.png" width="128" alt="Thyme Grove Theme logo">
</p>

<h1 align="center">Thyme Grove Theme</h1>

<p align="center">
  An earthy olive-green Chrome theme in four herbal tones — soft sage chrome over a pale thyme page.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/manifest-v3-b2bd7e" alt="Manifest V3">
  <img src="https://img.shields.io/badge/version-1.0.0-c7da8c" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/chrome-light-b2bd7e" alt="Light chrome">
  <img src="https://img.shields.io/badge/license-non--commercial-4a5741" alt="Non-commercial license">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/thyme-grove-theme/main/store-assets/promo/1400x560.png" alt="Thyme Grove Theme promo" width="700">
</p>

## Overview

Thyme Grove pairs a sage frame with a pale olive toolbar, then opens onto a soft thyme New Tab Page with an olive Google logo that matches the palette. Deep olive ink keeps every tab, bookmark and toolbar icon readable on the light chrome, links take a deeper moss tone, and a single-row shortcut layout keeps the New Tab Page clean.

The palette is deliberately earthy: nothing is bright, nothing is cold, and every tone reads like a herb or a leaf. Contrast comes from deep ink rather than from a dark frame.

## Design Concept

The source palette is four steps of one olive hue — khaki, sage, olive and moss. The theme keeps all four, then lightens the page to a pastel thyme tone so the New Tab Page feels soft rather than heavy, and adds a single deep olive ink for text.

| Color | Hex | RGB | Role |
|---|---|---|---|
| Thyme Pastel | `#E8F0D0` | 232, 240, 208 | New Tab background (pastel take on the palette lightest) |
| Sage | `#C6D095` | 198, 208, 149 | Toolbar |
| Olive | `#B2BD7E` | 178, 189, 126 | Frame / New Tab header / buttons |
| Fern | `#8E9162` | 142, 145, 98 | New Tab buttons |
| Khaki | `#D9D28B` | 217, 210, 139 | Palette lightest (source) |
| Moss | `#6A795D` | 106, 121, 93 | Palette deepest (source) |
| Deep Olive Ink | `#2F3A28` | 47, 58, 40 | Tab, bookmark and New Tab text |
| Moss Link | `#4A5741` | 74, 87, 65 | New Tab links |

## Features

- Pure color, no wallpaper — fast and distraction-free
- Herbal olive palette: sage, olive, moss and thyme in one family
- Light chrome with deep olive ink — readable without a dark frame
- Tab text, bookmark text and toolbar icons all share the same ink
- Single-row shortcut row and a color-matched Google logo for a clean New Tab Page
- No configuration needed — install and enjoy

## Screenshots

| Browser | Palette |
|:-:|:-:|
| <img src="https://raw.githubusercontent.com/vaxicy/thyme-grove-theme/main/store-assets/screenshots/en/screenshot-1-browser.png" width="420" alt="Thyme Grove New Tab"> | <img src="https://raw.githubusercontent.com/vaxicy/thyme-grove-theme/main/store-assets/screenshots/en/screenshot-2-palette.png" width="420" alt="Thyme Grove palette"> |

## Installation

### Load unpacked (development)

1. Download or clone this repository.
2. Open `chrome://extensions` in Chrome.
3. Enable **Developer mode** in the top right.
4. Click **Load unpacked** and select this folder (`thyme-grove-theme`).
5. The theme is active immediately.

### Package for the Chrome Web Store

```
chrome://extensions → Pack extension → select this folder → thyme-grove-theme.zip
```

Upload the resulting `.zip` to the [Chrome Web Store developer dashboard](https://chrome.google.com/webstore/devconsole).

## Store listing copy

Ready to paste into the store listing (also kept in `store-assets/store-description.txt`):

> Thyme Grove is an earthy olive-green Chrome theme: a sage frame, a pale olive toolbar, and a soft thyme New Tab Page with an olive Google logo that matches the palette. Deep olive ink keeps every tab, bookmark and toolbar icon readable on the light chrome. Solid colors only, no wallpaper — calm, herbal, and easy on the eyes.

## Project structure

| File | Purpose |
|---|---|
| `manifest.json` | Theme definition (single-file, inlined `theme` field) |
| `logo/logo.png` | 128×128 store icon (transparent background) |
| `store-assets/promo/440x280.png` | Small promo tile |
| `store-assets/promo/1400x560.png` | Marquee promo tile |
| `store-assets/screenshots/en/screenshot-1-browser.png` | Browser mockup screenshot (1280×800) |
| `store-assets/screenshots/en/screenshot-2-palette.png` | Palette introduction screenshot (1280×800) |
| `store-assets/store-description.txt` | Store listing description |
| `scripts/generate-logo-vector.py` | Render all SVG logo candidates with headless Chromium, build contact sheets, export `logo/logo.png` from `SELECTED` |
| `scripts/generate-screenshot-headless.py` | Regenerate the browser mockup via Playwright |
| `scripts/generate-screenshot-2-palette.py` | Regenerate the palette screenshot |
| `scripts/generate-promo.py` | Regenerate both promo tiles |
| `LICENSE` | Non-Commercial License (English / 中文) |

## Regenerating assets

Every asset is code-generated, so nothing here is hand-drawn or hand-copied:

```bash
py -3 scripts/generate-logo-vector.py         # candidates + contact sheets + logo/logo.png
py -3 scripts/generate-screenshot-headless.py # store screenshot 1 (browser mockup)
py -3 scripts/generate-screenshot-2-palette.py # store screenshot 2 (palette)
py -3 scripts/generate-promo.py               # promo 440x280 + 1400x560
```

To ship a different icon candidate, change `SELECTED` at the top of `generate-logo-vector.py` and re-run, then re-run the three asset scripts so the promo and screenshots pick up the new logo.

## License

Thyme Grove Theme is released under the Non-Commercial License. See `LICENSE` for full text (English / 中文).
