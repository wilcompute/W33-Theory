#!/usr/bin/env python3
"""
Render the exceptional tower as a standalone SVG figure (docs/w33_exceptional_
tower.svg) -- the visual thesis of the session, with no external dependency
(graphviz is not required). A vertical ladder q=3 (bottom) -> Monster (top), the
E6/E7/E8 trio side by side, a dashed Standard-Model branch, and the three threads
(omega, G2, U4(2)) drawn as a side rail.

Verifies the emitted SVG is well-formed and contains every rung.
"""
from __future__ import annotations

import json
from pathlib import Path

# (label, substrate integer)  -- bottom to top
SPINE = [
    ("q = 3  (one trit: triangle + tetrahedron)", "q=3, mu=4"),
    ("{3,n} genus / register tower", "{7,8,9,10,12} = {Phi6,2^3,q^2,Phi4,k}"),
    ("vertex-figure selection; gap = K12 = ternary Golay / M12", "n-6 | k=12"),
    ("Witting body  (Eisenstein, q=3)", "240 = E8 roots, 2160 = bus, 40 = W(3,3)"),
    ("__TRIO__", ""),  # E6 / E7 / E8 placed specially
    ("complex Leech  (Eisenstein 12 = k),  Aut 6.Suz", "12 = k,  24 = f"),
    ("Co0 = 2.Co1  (real Leech)", "24 = f"),
    ("Monster  M = Aut(V-natural)", "c = 24 = f  (holographic boundary)"),
]
TRIO = [
    ("E6", "Hessian 27 = trinification", "27 = q+f"),
    ("E7", "Klein quartic, 28 bitangents", "56 = v+k+mu"),
    ("E8", "120 icosians = 2I = 600-cell", "240 = 2*120"),
]
THREADS = [
    "omega (Eisenstein order-3 weld)",
    "G2 = Aut(O), keyed by Phi6=7",
    "U4(2) = PSp(4,3) = 25920",
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def emit_svg():
    W, H = 980, 760
    bx, bw, bh, gap = 70, 540, 52, 18
    n = len(SPINE)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'font-family="Helvetica,Arial,sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#0d1117"/>',
        f'<text x="{W//2}" y="28" fill="#d4af37" font-size="20" font-weight="bold" '
        f'text-anchor="middle">W(3,3) exceptional tower: q=3 -&gt; Monster</text>',
    ]
    # bottom (q=3) at large y, top (Monster) at small y
    y0 = H - bh - 30
    ys = []
    for i in range(n):
        y = y0 - i * (bh + gap)
        ys.append(y)
        label, integer = SPINE[i]
        if label == "__TRIO__":
            tw = (bw - 2 * 12) // 3
            for j, (nm, desc, ig) in enumerate(TRIO):
                x = bx + j * (tw + 12)
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{tw}" height="{bh}" rx="8" '
                    f'fill="#1b2838" stroke="#5fa8d3"/>'
                )
                parts.append(
                    f'<text x="{x+tw//2}" y="{y+20}" fill="#9fd3ff" '
                    f'font-size="14" font-weight="bold" text-anchor="middle">'
                    f"{esc(nm)}</text>"
                )
                parts.append(
                    f'<text x="{x+tw//2}" y="{y+36}" fill="#cfe6ff" '
                    f'font-size="9" text-anchor="middle">{esc(desc)}</text>'
                )
                parts.append(
                    f'<text x="{x+tw//2}" y="{y+48}" fill="#7fae7f" '
                    f'font-size="9" text-anchor="middle">{esc(ig)}</text>'
                )
            continue
        parts.append(
            f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="8" '
            f'fill="#161b22" stroke="#8b949e"/>'
        )
        parts.append(
            f'<text x="{bx+14}" y="{y+22}" fill="#e6edf3" font-size="14">'
            f"{esc(label)}</text>"
        )
        parts.append(
            f'<text x="{bx+14}" y="{y+40}" fill="#7fae7f" font-size="11">'
            f"{esc(integer)}</text>"
        )
    # arrows up the spine
    cx = bx + bw // 2
    for i in range(n - 1):
        parts.append(
            f'<line x1="{cx}" y1="{ys[i]}" x2="{cx}" y2="{ys[i+1]+bh}" '
            f'stroke="#d4af37" stroke-width="2" marker-end="url(#a)"/>'
        )
    # SM dashed branch off the trio (level 4)
    trio_y = ys[4]
    smx = bx + bw + 30
    parts.append(
        f'<rect x="{smx}" y="{trio_y-4}" width="320" height="44" rx="8" '
        f'fill="#161b22" stroke="#aa6" stroke-dasharray="5,3"/>'
    )
    parts.append(
        f'<text x="{smx+12}" y="{trio_y+16}" fill="#d9d98a" font-size="13">'
        f"Standard Model (break)</text>"
    )
    parts.append(
        f'<text x="{smx+12}" y="{trio_y+33}" fill="#7fae7f" font-size="11">'
        f"dim SM = 8+3+1 = 12 = k</text>"
    )
    parts.append(
        f'<line x1="{bx+bw}" y1="{trio_y+bh//2}" x2="{smx}" y2="{trio_y+16}" '
        f'stroke="#aa6" stroke-width="1.5" stroke-dasharray="5,3"/>'
    )
    # thread side-rail
    parts.append(
        f'<text x="20" y="{H-8}" fill="#8b949e" font-size="10">threads: '
        f'{esc("  |  ".join(THREADS))}</text>'
    )
    # arrowhead marker
    parts.insert(
        1,
        '<defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" '
        'refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#d4af37"/>'
        "</marker></defs>",
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    out = {}
    svg = emit_svg()
    path = Path("docs") / "w33_exceptional_tower.svg"
    path.write_text(svg, encoding="utf-8")
    print(f"wrote {path} ({len(svg)} bytes, {len(svg.splitlines())} lines)")

    # well-formedness + completeness checks
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert svg.count("<rect") >= len(SPINE) + len(TRIO)
    for label, _ in SPINE:
        if label != "__TRIO__":
            assert esc(label) in svg
    for nm, _, _ in TRIO:
        assert f">{nm}</text>" in svg
    assert "Monster" in svg and "q = 3" in svg and "Standard Model" in svg
    print("  SVG well-formed; all rungs present (q=3 bottom, Monster top, SM branch)")

    out["svg_file"] = str(path)
    out["bytes"] = len(svg)
    out["rungs"] = [s[0] for s in SPINE if s[0] != "__TRIO__"] + [t[0] for t in TRIO]
    out["threads"] = THREADS
    out["summary"] = (
        "rendered the exceptional tower as a standalone SVG "
        "(docs/w33_exceptional_tower.svg), no graphviz needed: a vertical ladder "
        "q=3 (bottom) -> Monster (top) with the E6/E7/E8 trio side by side, a "
        "dashed Standard-Model branch (dim 12=k), and the three threads (omega, "
        "G2=Aut(O), U4(2)) as a side rail. Well-formedness and all-rungs-present "
        "verified."
    )
    out["sources"] = [
        "self-contained SVG render of the tower (graphviz not required); "
        "structure from w33_exceptional_tower_synthesis.py / "
        "docs/w33_exceptional_tower.dot."
    ]
    with open("data/w33_tower_figure_svg.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_tower_figure_svg.json")


if __name__ == "__main__":
    main()
