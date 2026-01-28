#!/usr/bin/env python3
"""Generate a TikZ diagram for the A2^4 Magic-Star layer.

Outputs: latex/magic_star_a2_4.tex
"""
from __future__ import annotations

import json
from math import cos, sin, pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT / 'artifacts' / 'a2_4_decomposition.json').read_text())
    a2_sets = data['a2_4_solution']
    hits = data['alignment_with_27_orbits']['a2_orbit_hits']

    # Layout positions for four hexagons
    centers = [(-4.0, 3.0), (4.0, 3.0), (-4.0, -3.0), (4.0, -3.0)]
    radius = 1.2

    tikz = []
    tikz.append(r"\begin{figure}[ht]")
    tikz.append(r"\centering")
    tikz.append(r"\begin{tikzpicture}[scale=0.95]")

    for idx, (cx, cy) in enumerate(centers):
        roots = a2_sets[idx]
        # six vertices on hexagon
        coords = []
        for k in range(6):
            ang = pi/3 * k + pi/6
            x = cx + radius * cos(ang)
            y = cy + radius * sin(ang)
            coords.append((x, y))

        # draw hexagon
        tikz.append(rf"\draw[thick] {tuple(coords[0])} -- {tuple(coords[1])} -- {tuple(coords[2])} -- {tuple(coords[3])} -- {tuple(coords[4])} -- {tuple(coords[5])} -- cycle;")

        # label vertices
        for k, (x, y) in enumerate(coords):
            label = roots[k]
            tikz.append(rf"\node[font=\scriptsize] at ({x:.2f},{y:.2f}) {{{label}}};")

        # title
        tikz.append(rf"\node[font=\small\bfseries] at ({cx:.2f},{cy+1.9:.2f}) {{A2\#{idx+1}}};")

        # orbit-hit annotation
        hit = hits[idx]
        hit_str = ', '.join([f"o{k}:{v}" for k, v in hit.items()]) if hit else 'none'
        tikz.append(rf"\node[font=\tiny] at ({cx:.2f},{cy-1.8:.2f}) {{27-orbit hits: {hit_str}}};")

    tikz.append(r"\end{tikzpicture}")
    tikz.append(r"\caption{A2$^4$ layer inside E8 (one explicit orthogonal 4-tuple). Numbers are E8 root indices in the standard ordering. The A2 hexagons are global: their roots split across multiple 27-orbits.}")
    tikz.append(r"\end{figure}")

    out_path = ROOT / 'latex' / 'magic_star_a2_4.tex'
    out_path.write_text('\n'.join(tikz) + '\n', encoding='utf-8')
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
