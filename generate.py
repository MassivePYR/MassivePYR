#!/usr/bin/env python3
"""
GitHub Snake Animation Generator
Generates an animated SVG of a snake eating contribution dots.
Usage: python generate.py [--output snake.svg] [--theme dark|light] [--cols 53] [--rows 7]
"""

import argparse
import random
import math
from collections import deque

CELL = 12
GAP = 2
STEP = CELL + GAP

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "empty": "#161b22",
        "cells": ["#0e4429", "#006d32", "#26a641", "#39d353"],
        "snake_head": "#f78166",
        "snake_body": "#ff7b72",
        "snake_outline": "#da3633",
        "eye": "#0d1117",
    },
    "light": {
        "bg": "#ffffff",
        "empty": "#ebedf0",
        "cells": ["#9be9a8", "#40c463", "#30a14e", "#216e39"],
        "snake_head": "#cf222e",
        "snake_body": "#ff8182",
        "snake_outline": "#82071e",
        "eye": "#ffffff",
    },
}


def make_grid(cols, rows, density=0.65):
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if random.random() < density:
                row.append(random.randint(1, 4))
            else:
                row.append(0)
        grid.append(row)
    return grid


def bfs_path(grid, start, rows, cols):
    """BFS that visits every non-zero cell, returns ordered list of (r,c)."""
    visited = set()
    path = [start]
    visited.add(start)
    queue = deque([start])

    targets = {(r, c) for r in range(rows) for c in range(cols) if grid[r][c] > 0}
    targets.discard(start)

    while targets:
        found = False
        current = path[-1]
        # BFS to nearest unvisited target
        bfs_q = deque([(current, [current])])
        seen = {current}
        while bfs_q:
            pos, trail = bfs_q.popleft()
            if pos in targets:
                for step in trail[1:]:
                    path.append(step)
                    visited.add(step)
                targets.discard(pos)
                found = True
                break
            r, c = pos
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) not in seen:
                    seen.add((nr,nc))
                    bfs_q.append(((nr,nc), trail+[(nr,nc)]))
        if not found:
            break

    return path


def cell_cx(c): return GAP + c * STEP + CELL // 2
def cell_cy(r): return GAP + r * STEP + CELL // 2


def round_rect(x, y, w, h, r, **attrs):
    attr_str = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}" {attr_str}/>'


def generate_svg(cols, rows, theme_name, output):
    theme = THEMES[theme_name]
    grid = make_grid(cols, rows)

    # Find a starting cell with a contribution
    starts = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] > 0]
    if not starts:
        starts = [(0, 0)]
    start = random.choice(starts)

    path = bfs_path(grid, start, rows, cols)

    W = GAP + cols * STEP
    H = GAP + rows * STEP
    SNAKE_LEN = 5   # visible body segments behind head
    FRAME_MS = 80   # ms per step
    total_frames = len(path)
    total_dur = total_frames * FRAME_MS / 1000  # seconds

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    lines.append(f'  <rect width="{W}" height="{H}" rx="4" fill="{theme["bg"]}"/>')

    # --- Static grid cells ---
    lines.append('  <g id="grid">')
    for r in range(rows):
        for c in range(cols):
            v = grid[r][c]
            x = GAP + c * STEP
            y = GAP + r * STEP
            color = theme["cells"][v-1] if v > 0 else theme["empty"]
            lines.append(f'    {round_rect(x, y, CELL, CELL, 2, fill=color, id=f"c{r}_{c}")}')
    lines.append('  </g>')

    # --- SMIL animation: hide cells as snake eats them ---
    lines.append('  <g id="eaten">')
    for idx, (r, c) in enumerate(path):
        t_start = idx * FRAME_MS / 1000
        lines.append(f'    <!-- eat {r},{c} at t={t_start:.2f}s -->')
        lines.append(f'    {round_rect(GAP+c*STEP, GAP+r*STEP, CELL, CELL, 2, fill=theme["bg"])}')
        # We use animate to make it appear at the right time
        lines[-1] = lines[-1].replace('/>', f' opacity="0"><animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="{FRAME_MS/1000:.3f}s" begin="{t_start:.3f}s" fill="freeze"/></rect>')
    lines.append('  </g>')

    # --- Snake body segments (animated along path) ---
    lines.append('  <g id="snake">')

    def make_keyTimes(n_path, offset, total):
        """Build keyTimes string for a segment offset steps behind head."""
        times = []
        for i in range(total):
            src = max(0, i - offset)
            t = src / (total - 1) if total > 1 else 0
            times.append(f"{t:.4f}")
        return ";".join(times)

    def make_values_xy(path, offset, axis):
        vals = []
        for i in range(len(path)):
            src = max(0, i - offset)
            r, c = path[src]
            vals.append(str(cell_cy(r) if axis == 'y' else cell_cx(c)))
        return ";".join(vals)

    # Body segments (back to front, head last)
    for seg in range(SNAKE_LEN, 0, -1):
        cx0 = cell_cx(path[0][1])
        cy0 = cell_cy(path[0][0])
        radius = CELL // 2 - 1
        color = theme["snake_head"] if seg == 1 else theme["snake_body"]
        if seg == 1:
            color = theme["snake_head"]
            r2 = radius
        else:
            fade = 1 - (seg - 1) / SNAKE_LEN
            r2 = max(3, int(radius * (0.6 + 0.4 * fade)))

        cx_vals = make_values_xy(path, seg - 1, 'x')
        cy_vals = make_values_xy(path, seg - 1, 'y')
        n = len(path)
        kt = ";".join([f"{i/(n-1):.4f}" for i in range(n)]) if n > 1 else "0;1"

        lines.append(f'    <circle cx="{cx0}" cy="{cy0}" r="{r2}" fill="{color}" stroke="{theme["snake_outline"]}" stroke-width="0.5">')
        lines.append(f'      <animate attributeName="cx" values="{cx_vals}" keyTimes="{kt}" dur="{total_dur:.3f}s" repeatCount="indefinite"/>')
        lines.append(f'      <animate attributeName="cy" values="{cy_vals}" keyTimes="{kt}" dur="{total_dur:.3f}s" repeatCount="indefinite"/>')
        lines.append(f'    </circle>')

    # Eye on head
    cx0 = cell_cx(path[0][1])
    cy0 = cell_cy(path[0][0])
    cx_vals = make_values_xy(path, 0, 'x')
    cy_vals_eye = ";".join([str(cell_cy(path[i][0]) - 2) for i in range(len(path))])
    cx_vals_eye = ";".join([str(cell_cx(path[i][1]) + 2) for i in range(len(path))])
    kt = ";".join([f"{i/(len(path)-1):.4f}" for i in range(len(path))]) if len(path) > 1 else "0;1"

    lines.append(f'    <circle cx="{cx0+2}" cy="{cy0-2}" r="1.5" fill="{theme["eye"]}">')
    lines.append(f'      <animate attributeName="cx" values="{cx_vals_eye}" keyTimes="{kt}" dur="{total_dur:.3f}s" repeatCount="indefinite"/>')
    lines.append(f'      <animate attributeName="cy" values="{cy_vals_eye}" keyTimes="{kt}" dur="{total_dur:.3f}s" repeatCount="indefinite"/>')
    lines.append(f'    </circle>')

    lines.append('  </g>')
    lines.append('</svg>')

    svg = "\n".join(lines)
    with open(output, "w") as f:
        f.write(svg)
    print(f"Generated: {output}  ({W}x{H}px, {len(path)} steps, {total_dur:.1f}s loop)")


def main():
    parser = argparse.ArgumentParser(description="GitHub Snake Animation Generator")
    parser.add_argument("--output", default="snake.svg", help="Output SVG file")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark")
    parser.add_argument("--cols", type=int, default=53, help="Grid columns (weeks)")
    parser.add_argument("--rows", type=int, default=7, help="Grid rows (days)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    generate_svg(args.cols, args.rows, args.theme, args.output)


if __name__ == "__main__":
    main()
