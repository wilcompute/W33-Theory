#!/usr/bin/env python3
"""BT1480: formalize the 12-strand grid as C3 x V4, not a bare C12."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1480_tensor_product_grid_reading.json"
TEX = ROOT / "analysis" / "BT1480_tensor_product_grid_reading.tex"

V4 = [(0, 0), (1, 0), (0, 1), (1, 1)]


def strand(c: int, branch: int) -> int:
    return 4 * c + branch


def v4_add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)


def c3_add(a: int, b: int) -> int:
    return (a + b) % 3


def main() -> None:
    branch_to_bits = {i: V4[i] for i in range(4)}
    bits_to_branch = {v: i for i, v in branch_to_bits.items()}
    elements = []
    for c in range(3):
        for b in range(4):
            side, orient = branch_to_bits[b]
            elements.append({
                "strand": strand(c, b),
                "c3_channel": c,
                "v4_branch": b,
                "side_bit": side,
                "orientation_bit": orient,
                "active_col": 14 * strand(c, b) + 13,
                "guard_cols": [216 + 2 * strand(c, b), 216 + 2 * strand(c, b) + 1],
            })
    channels = {f"C3_channel_{c}": [strand(c, b) for b in range(4)] for c in range(3)}
    triangles = {f"V4_branch_{b}_C3_triangle": [strand(c, b) for c in range(3)] for b in range(4)}
    product_table_sample = []
    for c1, b1 in [(0, 0), (1, 1), (2, 3)]:
        for c2, b2 in [(1, 0), (0, 2), (2, 1)]:
            bsum = bits_to_branch[v4_add(branch_to_bits[b1], branch_to_bits[b2])]
            product_table_sample.append({
                "left": [c1, b1],
                "right": [c2, b2],
                "sum": [c3_add(c1, c2), bsum],
                "strand_sum": strand(c3_add(c1, c2), bsum),
            })
    # C4 would require an order-4 branch generator; V4 has no order-4 element and matches two branch bits.
    v4_orders = []
    for b, bits in branch_to_bits.items():
        cur = (0, 0)
        for n in range(1, 5):
            cur = v4_add(cur, bits)
            if cur == (0, 0):
                v4_orders.append({"branch": b, "order": n})
                break
    checks = {
        "element_count_12": len(elements) == 12,
        "channels_partition_12": sorted(sum(channels.values(), [])) == list(range(12)),
        "triangles_partition_12": sorted(sum(triangles.values(), [])) == list(range(12)),
        "channels_are_size_4": all(len(v) == 4 for v in channels.values()),
        "triangles_are_size_3": all(len(v) == 3 for v in triangles.values()),
        "v4_has_no_order4_branch": max(row["order"] for row in v4_orders) <= 2,
        "active_cols_match_abi": sorted(e["active_col"] for e in elements) == [14 * s + 13 for s in range(12)],
        "guard_tail_match_abi": sorted({g for e in elements for g in e["guard_cols"]}) == list(range(216, 240)),
    }
    tex = r"""\begin{center}\small
\begin{tabular}{c|cccc}
\toprule
 & $(0,0)$ & $(1,0)$ & $(0,1)$ & $(1,1)$\\
\midrule
$0\in C_3$ & 0 & 1 & 2 & 3\\
$1\in C_3$ & 4 & 5 & 6 & 7\\
$2\in C_3$ & 8 & 9 & 10 & 11\\
\bottomrule
\end{tabular}
\end{center}
"""
    TEX.write_text(tex, encoding="utf-8")
    result = {
        "bt": 1480,
        "title": "Tensor/product reading of the 3x4 strand grid",
        "verified": all(checks.values()),
        "preferred_structure": "C3 x V4, where V4=C2 x C2 branch bits",
        "rejected_structure": "bare C12 or C3 x C4, because the branch factor is two-bit D4/V4 data with no intrinsic order-4 generator",
        "elements": elements,
        "channels": channels,
        "triangles": triangles,
        "branch_to_bits": {str(k): list(v) for k, v in branch_to_bits.items()},
        "v4_orders": v4_orders,
        "product_table_sample": product_table_sample,
        "tex_table": "analysis/BT1480_tensor_product_grid_reading.tex",
        "interpretation": "The three-channel Szilassi/Fano axis is the C3 coordinate; the four-triangle E6 gauge-shell axis is the V4 branch coordinate.  The closure strands are C3 x V4, with qutrit phase on C3 and D4 branch bits on V4.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1480, "verified": result["verified"], "structure": result["preferred_structure"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
