#!/usr/bin/env python3
"""
Top Languages SVG Card Generator
Generates an animated SVG card showing programming language statistics.
Usage: python3 languages.py [--output langs.svg] [--theme dark|light] [--style bar|donut|compact]
"""

import argparse
import math
import json

# GitHub's official language color palette (subset)
LANG_COLORS = {
    "Python":        "#3572A5",
    "JavaScript":    "#f1e05a",
    "TypeScript":    "#3178c6",
    "Rust":          "#dea584",
    "Go":            "#00ADD8",
    "C":             "#555555",
    "C++":           "#f34b7d",
    "C#":            "#178600",
    "Java":          "#b07219",
    "Kotlin":        "#A97BFF",
    "Swift":         "#F05138",
    "Ruby":          "#701516",
    "PHP":           "#4F5D95",
    "Shell":         "#89e051",
    "HTML":          "#e34c26",
    "CSS":           "#563d7c",
    "Dart":          "#00B4AB",
    "Elixir":        "#6e4a7e",
    "Haskell":       "#5e5086",
    "Lua":           "#000080",
    "R":             "#198CE7",
    "Scala":         "#c22d40",
    "Zig":           "#ec915c",
    "Vue":           "#41b883",
    "Svelte":        "#ff3e00",
    "YAML":          "#cb171e",
    "Markdown":      "#083fa1",
}

THEMES = {
    "dark": {
        "bg":          "#0d1117",
        "border":      "#30363d",
        "title":       "#e6edf3",
        "text":        "#8b949e",
        "subtext":     "#6e7681",
        "bar_bg":      "#21262d",
        "percent":     "#e6edf3",
        "donut_hole":  "#0d1117",
    },
    "light": {
        "bg":          "#ffffff",
        "border":      "#d0d7de",
        "title":       "#1f2328",
        "text":        "#656d76",
        "subtext":     "#adbac7",
        "bar_bg":      "#eaeef2",
        "percent":     "#1f2328",
        "donut_hole":  "#ffffff",
    },
}

DEFAULT_LANGS = [
    ("Python",     42.3),
    ("TypeScript", 23.1),
    ("Rust",       14.7),
    ("Go",          9.2),
    ("Shell",       6.4),
    ("C++",         4.3),
]


def lang_color(name):
    return LANG_COLORS.get(name, "#8b949e")


def ease_out(t):
    return 1 - (1 - t) ** 3


# ──────────────────────────────────────────────
# BAR STYLE
# ──────────────────────────────────────────────

def generate_bar(langs, theme_name, output, title):
    t = THEMES[theme_name]
    CARD_W   = 340
    PAD      = 20
    TITLE_H  = 32
    ROW_H    = 46
    CARD_H   = TITLE_H + len(langs) * ROW_H + PAD

    BAR_W    = CARD_W - PAD * 2
    BAR_H    = 8
    DOT_R    = 5
    ANIM_DUR = 0.9  # seconds

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">')

    # Card background + border
    lines.append(f'  <rect width="{CARD_W}" height="{CARD_H}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1"/>')

    # Title
    lines.append(f'  <text x="{PAD}" y="22" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="14" font-weight="600" fill="{t["title"]}">{title}</text>')
    lines.append(f'  <line x1="{PAD}" y1="30" x2="{CARD_W - PAD}" y2="30" stroke="{t["border"]}" stroke-width="0.5"/>')

    for i, (name, pct) in enumerate(langs):
        y_top   = TITLE_H + i * ROW_H + 8
        bar_y   = y_top + 18
        color   = lang_color(name)
        bar_fill = int(BAR_W * pct / 100)
        delay   = i * 0.12

        # Language dot
        lines.append(f'  <circle cx="{PAD + DOT_R}" cy="{y_top + 6}" r="{DOT_R}" fill="{color}"/>')

        # Language name
        lines.append(f'  <text x="{PAD + DOT_R * 2 + 6}" y="{y_top + 10}" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="12" fill="{t["text"]}">{name}</text>')

        # Percentage text (right-aligned)
        lines.append(f'  <text x="{CARD_W - PAD}" y="{y_top + 10}" text-anchor="end" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="11" fill="{t["percent"]}">{pct:.1f}%</text>')

        # Bar background
        lines.append(f'  <rect x="{PAD}" y="{bar_y}" width="{BAR_W}" height="{BAR_H}" rx="{BAR_H//2}" fill="{t["bar_bg"]}"/>')

        # Animated bar fill
        lines.append(f'  <rect x="{PAD}" y="{bar_y}" width="0" height="{BAR_H}" rx="{BAR_H//2}" fill="{color}" opacity="0.9">')
        lines.append(f'    <animate attributeName="width" from="0" to="{bar_fill}" dur="{ANIM_DUR}s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>')
        lines.append(f'    <animate attributeName="opacity" from="0" to="0.9" dur="{ANIM_DUR * 0.4:.2f}s" begin="{delay:.2f}s" fill="freeze"/>')
        lines.append(f'  </rect>')

    lines.append('</svg>')

    with open(output, "w") as f:
        f.write("\n".join(lines))
    print(f"Generated (bar): {output}  {CARD_W}x{CARD_H}px")


# ──────────────────────────────────────────────
# DONUT STYLE
# ──────────────────────────────────────────────

def arc_path(cx, cy, r, start_deg, end_deg):
    """SVG arc path string for a slice."""
    def to_rad(d): return d * math.pi / 180
    sx = cx + r * math.cos(to_rad(start_deg))
    sy = cy + r * math.sin(to_rad(start_deg))
    ex = cx + r * math.cos(to_rad(end_deg))
    ey = cy + r * math.sin(to_rad(end_deg))
    large = 1 if (end_deg - start_deg) > 180 else 0
    return f"M {cx} {cy} L {sx:.3f} {sy:.3f} A {r} {r} 0 {large} 1 {ex:.3f} {ey:.3f} Z"


def generate_donut(langs, theme_name, output, title):
    t = THEMES[theme_name]
    CARD_W   = 400
    CARD_H   = 220
    PAD      = 20

    CX = 110
    CY = CARD_H // 2
    R_OUT = 80
    R_IN  = 52
    ANIM_DUR = 1.1

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">')
    lines.append(f'  <rect width="{CARD_W}" height="{CARD_H}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1"/>')

    # Title
    lines.append(f'  <text x="{PAD}" y="22" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="14" font-weight="600" fill="{t["title"]}">{title}</text>')
    lines.append(f'  <line x1="{PAD}" y1="30" x2="{CARD_W - PAD}" y2="30" stroke="{t["border"]}" stroke-width="0.5"/>')

    total = sum(p for _, p in langs)
    angle = -90.0  # start at top

    # Donut slices
    lines.append('  <g id="slices">')
    for i, (name, pct) in enumerate(langs):
        sweep = 360 * pct / total
        end   = angle + sweep
        color = lang_color(name)

        # Full donut slice (pie minus hole)
        path = arc_path(CX, CY, R_OUT, angle, end)
        delay = i * 0.09

        # Clip from inner circle: use two paths (outer arc, inner arc)
        # Build proper donut arc
        def to_rad(d): return d * math.pi / 180
        sx_o = CX + R_OUT * math.cos(to_rad(angle))
        sy_o = CY + R_OUT * math.sin(to_rad(angle))
        ex_o = CX + R_OUT * math.cos(to_rad(end))
        ey_o = CY + R_OUT * math.sin(to_rad(end))
        sx_i = CX + R_IN  * math.cos(to_rad(end))
        sy_i = CY + R_IN  * math.sin(to_rad(end))
        ex_i = CX + R_IN  * math.cos(to_rad(angle))
        ey_i = CY + R_IN  * math.sin(to_rad(angle))
        large = 1 if sweep > 180 else 0

        donut = (
            f"M {sx_o:.3f} {sy_o:.3f} "
            f"A {R_OUT} {R_OUT} 0 {large} 1 {ex_o:.3f} {ey_o:.3f} "
            f"L {sx_i:.3f} {sy_i:.3f} "
            f"A {R_IN} {R_IN} 0 {large} 0 {ex_i:.3f} {ey_i:.3f} Z"
        )
        lines.append(f'    <path d="{donut}" fill="{color}" opacity="0">')
        lines.append(f'      <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay:.2f}s" fill="freeze"/>')
        lines.append(f'    </path>')

        angle = end
    lines.append('  </g>')

    # Hole
    lines.append(f'  <circle cx="{CX}" cy="{CY}" r="{R_IN - 1}" fill="{t["donut_hole"]}"/>')

    # Centre label
    lines.append(f'  <text x="{CX}" y="{CY - 6}" text-anchor="middle" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="11" fill="{t["text"]}">Most</text>')
    lines.append(f'  <text x="{CX}" y="{CY + 10}" text-anchor="middle" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="11" fill="{t["text"]}">Used</text>')

    # Legend (right side)
    LX = CX + R_OUT + 24
    LY_START = CY - (len(langs) * 22) // 2 + 8
    for i, (name, pct) in enumerate(langs):
        color = lang_color(name)
        ly = LY_START + i * 26
        lines.append(f'  <rect x="{LX}" y="{ly - 8}" width="10" height="10" rx="2" fill="{color}"/>')
        lines.append(f'  <text x="{LX + 14}" y="{ly}" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="12" fill="{t["text"]}">{name}</text>')
        lines.append(f'  <text x="{CARD_W - PAD}" y="{ly}" text-anchor="end" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="11" fill="{t["subtext"]}">{pct:.1f}%</text>')

    lines.append('</svg>')

    with open(output, "w") as f:
        f.write("\n".join(lines))
    print(f"Generated (donut): {output}  {CARD_W}x{CARD_H}px")


# ──────────────────────────────────────────────
# COMPACT STYLE  (two columns)
# ──────────────────────────────────────────────

def generate_compact(langs, theme_name, output, title):
    t = THEMES[theme_name]
    COLS     = 2
    PAD      = 16
    CARD_W   = 340
    ITEM_H   = 28
    TITLE_H  = 36
    rows     = math.ceil(len(langs) / COLS)
    CARD_H   = TITLE_H + rows * ITEM_H + PAD
    COL_W    = (CARD_W - PAD * 2) // COLS
    DOT_R    = 5

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}">')
    lines.append(f'  <rect width="{CARD_W}" height="{CARD_H}" rx="8" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1"/>')
    lines.append(f'  <text x="{PAD}" y="22" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="14" font-weight="600" fill="{t["title"]}">{title}</text>')
    lines.append(f'  <line x1="{PAD}" y1="30" x2="{CARD_W - PAD}" y2="30" stroke="{t["border"]}" stroke-width="0.5"/>')

    for i, (name, pct) in enumerate(langs):
        col = i % COLS
        row = i // COLS
        x   = PAD + col * COL_W
        y   = TITLE_H + row * ITEM_H + 10
        color = lang_color(name)

        lines.append(f'  <circle cx="{x + DOT_R}" cy="{y}" r="{DOT_R}" fill="{color}"/>')
        lines.append(f'  <text x="{x + DOT_R * 2 + 6}" y="{y + 4}" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="12" fill="{t["text"]}">{name}</text>')
        lines.append(f'  <text x="{x + COL_W - 4}" y="{y + 4}" text-anchor="end" font-family="Segoe UI,Ubuntu,Sans-Serif" font-size="11" fill="{t["subtext"]}">{pct:.1f}%</text>')

    # Animated bottom progress strip
    total = sum(p for _, p in langs)
    strip_y = CARD_H - 8
    strip_h = 5
    lines.append(f'  <rect x="{PAD}" y="{strip_y}" width="{CARD_W - PAD*2}" height="{strip_h}" rx="2" fill="{t["bar_bg"]}"/>')
    x_off = 0
    for i, (name, pct) in enumerate(langs):
        seg_w = (CARD_W - PAD * 2) * pct / total
        color = lang_color(name)
        delay = 0.4 + i * 0.07
        lines.append(f'  <rect x="{PAD + x_off:.2f}" y="{strip_y}" width="0" height="{strip_h}" rx="0" fill="{color}">')
        lines.append(f'    <animate attributeName="width" from="0" to="{seg_w:.2f}" dur="0.7s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>')
        lines.append(f'  </rect>')
        x_off += seg_w

    lines.append('</svg>')

    with open(output, "w") as f:
        f.write("\n".join(lines))
    print(f"Generated (compact): {output}  {CARD_W}x{CARD_H}px")


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def parse_langs(raw):
    """Parse 'Python:42,JS:30' or load from JSON file."""
    if raw.endswith(".json"):
        with open(raw) as f:
            data = json.load(f)
        return [(item["name"], float(item["pct"])) for item in data]
    pairs = []
    for part in raw.split(","):
        name, pct = part.rsplit(":", 1)
        pairs.append((name.strip(), float(pct)))
    total = sum(p for _, p in pairs)
    if abs(total - 100) > 0.5:
        pairs = [(n, p * 100 / total) for n, p in pairs]
    return pairs


def main():
    parser = argparse.ArgumentParser(description="Top Languages SVG Card Generator")
    parser.add_argument("--output", default="langs.svg")
    parser.add_argument("--theme",  choices=["dark","light"], default="dark")
    parser.add_argument("--style",  choices=["bar","donut","compact"], default="bar")
    parser.add_argument("--title",  default="Most Used Languages")
    parser.add_argument("--langs",  default=None,
                        help='Comma-separated "Name:pct" pairs or path to JSON file. '
                             'Example: "Python:42,TypeScript:30,Rust:28"')
    args = parser.parse_args()

    langs = parse_langs(args.langs) if args.langs else DEFAULT_LANGS

    if args.style == "bar":
        generate_bar(langs, args.theme, args.output, args.title)
    elif args.style == "donut":
        generate_donut(langs, args.theme, args.output, args.title)
    else:
        generate_compact(langs, args.theme, args.output, args.title)


if __name__ == "__main__":
    main()
