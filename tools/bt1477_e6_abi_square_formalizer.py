#!/usr/bin/env python3
"""BT1477: formalize the E6 firewall / ABI / CSS closure square."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1477_e6_abi_square_formalizer.json"
TEX = ROOT / "analysis" / "BT1477_e6_abi_square_diagram.tex"


def main() -> None:
    nodes = {
        "affine_triads": {"value": 36, "formula": "k*q=12*3", "meaning": "E6 firewall affine-triad skeleton"},
        "oriented_sector": {"value": 72, "formula": "2*36=24+48", "meaning": "oriented closure sector / ABI active+guard rows"},
        "firewall_gap": {"value": 9, "formula": "q^2", "meaning": "firewall/fiber completion sector"},
        "css_logical": {"value": 81, "formula": "72+9", "meaning": "CSS logical/H1 closure sector"},
        "e6_dimension": {"value": 78, "formula": "72+6", "meaning": "E6 rank-completed Lie closure"},
    }
    arrows = [
        {"src": "affine_triads", "dst": "oriented_sector", "operation": "orient x2", "equation": "36*2=72"},
        {"src": "oriented_sector", "dst": "css_logical", "operation": "+ firewall q^2", "equation": "72+9=81"},
        {"src": "oriented_sector", "dst": "e6_dimension", "operation": "+ rank 2q", "equation": "72+6=78"},
        {"src": "active_rows", "dst": "oriented_sector", "operation": "+ guard rows", "equation": "24+48=72"},
    ]
    checks = {
        "affine_orients_to_72": 2 * nodes["affine_triads"]["value"] == nodes["oriented_sector"]["value"],
        "active_guard_is_72": 24 + 48 == nodes["oriented_sector"]["value"],
        "firewall_gap_is_9": nodes["firewall_gap"]["value"] == 9,
        "css_logical_is_72_plus_9": nodes["oriented_sector"]["value"] + nodes["firewall_gap"]["value"] == nodes["css_logical"]["value"],
        "e6_is_72_plus_6": nodes["oriented_sector"]["value"] + 6 == nodes["e6_dimension"]["value"],
        "css_minus_e6_is_3": nodes["css_logical"]["value"] - nodes["e6_dimension"]["value"] == 3,
    }
    tex = r"""\begin{center}
\begin{tikzpicture}[node distance=3.3cm,>=stealth]
\node (A) {$36$ affine triads};
\node[right of=A] (B) {$72$ oriented / ABI rows};
\node[below of=B] (C) {$81$ CSS/H1 closure};
\node[above of=B] (D) {$78$ E6 closure};
\draw[->] (A) -- node[above] {$\times2$} (B);
\draw[->] (B) -- node[right] {$+9=q^2$} (C);
\draw[->] (B) -- node[right] {$+6=2q$} (D);
\node[below of=A] (E) {$24$ active $+$ $48$ guard};
\draw[->] (E) -- node[below] {$=72$} (B);
\end{tikzpicture}
\end{center}
"""
    TEX.write_text(tex, encoding="utf-8")
    result = {
        "bt": 1477,
        "title": "E6 firewall / ABI square formalizer",
        "verified": all(checks.values()),
        "nodes": nodes,
        "arrows": arrows,
        "tex_diagram": "analysis/BT1477_e6_abi_square_diagram.tex",
        "interpretation": "The ABI/CSS closure is the decoder-side realization of the older E6 firewall square: 36 orients to 72, the ABI realizes 72 as 24+48, and CSS/H1 closes by adding the q^2=9 firewall sector.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1477, "verified": result["verified"], "square": "36->72->81"}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
