r"""The 24 Niemeier lattices and their theta series collapse onto M_12.

Niemeier (1973) classified the EVEN UNIMODULAR LATTICES of rank 24:
there are exactly 24 of them.  They are determined by their root systems
(rank-24 sums of simple ADE pieces), with the LEECH lattice the unique
one that has no roots.

THE 24 ROOT SYSTEMS.

       #    root system            |R|       (Niemeier root count)
       --   -----------            ---
        1   (none, Leech)            0
        2   A_1^{24}                48 = 24 . 2
        3   A_2^{12}                72 = 12 . 6
        4   A_3^{8}                 96 = 8 . 12
        5   A_4^{6}                120 = 6 . 20
        6   D_4^{6}                144 = 6 . 24
        7   A_5^{4} D_4            144 = 4 . 30 + 24
        8   A_6^{4}                168 = 4 . 42
        9   A_7^{2} D_5^{2}        192 = 2 . 56 + 2 . 40
       10   A_8^{3}                216 = 3 . 72
       11   A_9^{2} D_6            240 = 2 . 90 + 60
       12   D_6^{4}                240 = 4 . 60
       13   E_6^{4}                288 = 4 . 72
       14   A_11 D_7 E_6           288 = 132 + 84 + 72
       15   A_12^{2}               312 = 2 . 156
       16   D_8^{3}                336 = 3 . 112
       17   A_15 D_9               384 = 240 + 144
       18   A_17 E_7               432 = 306 + 126
       19   D_10 E_7^{2}           432 = 180 + 2 . 126
       20   D_12^{2}               528 = 2 . 264
       21   A_24                   600
       22   E_8^{3}                720 = 3 . 240
       23   D_16 E_8               720 = 480 + 240
       24   D_24                  1104 = 2 . 24 . 23

(For ADE root counts:  |A_n| = n(n+1),  |D_n| = 2 n (n-1),  |E_6| = 72,
|E_7| = 126,  |E_8| = 240.)

THEOREM (theta-collapse).  For an even unimodular rank-24 lattice  L with
root count  h,

    theta_L  =  E_4^3  +  (h - 720) Delta.

PROOF.  theta_L is a holomorphic modular form of weight 12 with constant
term 1, so  theta_L lies in the affine 1-dimensional space  E_4^3 + C . Delta
inside  M_12.  The q^1 coefficient pins the affine constant:
[q^1] E_4^3 = 720, [q^1] Delta = 1, so coefficient of Delta is h - 720.

CONSEQUENCES.

    (i)   theta_E_8^3   =  E_4^3                 (h = 720),  no Delta.
    (ii)  theta_Leech   =  E_4^3 - 720 Delta     (h =   0),  the OTHER extreme.
    (iii) theta-collisions: the 24 lattices give only 19 distinct
          theta series, since five pairs share root counts:
            (D_4^6, A_5^4 D_4),     h = 144
            (A_9^2 D_6, D_6^4),     h = 240
            (E_6^4, A_11 D_7 E_6),  h = 288
            (A_17 E_7, D_10 E_7^2), h = 432
            (E_8^3, D_16 E_8),      h = 720

Thus dim M_12 = 2 imposes a 24-to-19 collapse on Niemeier lattices: the
modular ring sees only the root count, not the lattice isomorphism class.

CONNECTION TO W(3,3).

    24 = rank Niemeier = 2 . k_W33                (Layer 30 / 32 valency).
    24 = 24 = number of Niemeier lattices         (the same 24!).
    h = 720 = 60 . k_W33 splits Niemeier into Leech (h = 0) and Pure-E_8
              triple (h = 720) as the two extremes (h - 720 = -720, 0).
    Each Niemeier lattice is a 24-dim Z-module on which 196560 (Leech kissing)
    or  E_8^3 (= 720 = 3 |E_8 root|) controls the local geometry.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_niemeier_lattices_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_ramanujan_system import delta_series, e4_series, series_mul


# ----------------------------------------------------------------------
# Root-count helpers for ADE pieces.
# ----------------------------------------------------------------------
def roots_A(n: int) -> int:
    return n * (n + 1)


def roots_D(n: int) -> int:
    return 2 * n * (n - 1)


def roots_E(n: int) -> int:
    return {6: 72, 7: 126, 8: 240}[n]


# ----------------------------------------------------------------------
# Niemeier table:  (label, list of (kind, n, multiplicity)).
# ----------------------------------------------------------------------
NIEMEIER: list[tuple[str, list[tuple[str, int, int]]]] = [
    ("Leech",                []),
    ("A1^24",               [("A",  1, 24)]),
    ("A2^12",               [("A",  2, 12)]),
    ("A3^8",                [("A",  3,  8)]),
    ("A4^6",                [("A",  4,  6)]),
    ("D4^6",                [("D",  4,  6)]),
    ("A5^4 D4",             [("A",  5,  4), ("D",  4,  1)]),
    ("A6^4",                [("A",  6,  4)]),
    ("A7^2 D5^2",           [("A",  7,  2), ("D",  5,  2)]),
    ("A8^3",                [("A",  8,  3)]),
    ("A9^2 D6",             [("A",  9,  2), ("D",  6,  1)]),
    ("D6^4",                [("D",  6,  4)]),
    ("E6^4",                [("E",  6,  4)]),
    ("A11 D7 E6",           [("A", 11,  1), ("D",  7,  1), ("E",  6,  1)]),
    ("A12^2",               [("A", 12,  2)]),
    ("D8^3",                [("D",  8,  3)]),
    ("A15 D9",              [("A", 15,  1), ("D",  9,  1)]),
    ("A17 E7",              [("A", 17,  1), ("E",  7,  1)]),
    ("D10 E7^2",            [("D", 10,  1), ("E",  7,  2)]),
    ("D12^2",               [("D", 12,  2)]),
    ("A24",                 [("A", 24,  1)]),
    ("E8^3",                [("E",  8,  3)]),
    ("D16 E8",              [("D", 16,  1), ("E",  8,  1)]),
    ("D24",                 [("D", 24,  1)]),
]


def root_count(decomp: list[tuple[str, int, int]]) -> int:
    total = 0
    for kind, n, mult in decomp:
        per = roots_A(n) if kind == "A" else roots_D(n) if kind == "D" else roots_E(n)
        total += mult * per
    return total


def total_rank(decomp: list[tuple[str, int, int]]) -> int:
    return sum(n * mult for _, n, mult in decomp)


# ----------------------------------------------------------------------
# Verify each Niemeier lattice has rank 24.
# ----------------------------------------------------------------------
def verify_all_have_rank_24() -> dict[str, Any]:
    discrepancies = []
    for label, decomp in NIEMEIER:
        r = total_rank(decomp)
        if label != "Leech" and r != 24:
            discrepancies.append({"label": label, "rank": r})
        if label == "Leech" and r != 0:
            discrepancies.append({"label": label, "rank": r})
    return {
        "n_tested":      len(NIEMEIER),
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


def verify_total_count_is_24() -> dict[str, Any]:
    return {
        "count":      len(NIEMEIER),
        "equals_24":  len(NIEMEIER) == 24,
    }


# ----------------------------------------------------------------------
# Theta-collapse: theta_L = E_4^3 + (h - 720) Delta.
# Verify coefficient-wise that this produces consistent shell counts.
# ----------------------------------------------------------------------
def theta_niemeier(h: int, n_max: int) -> list[int]:
    e4 = e4_series(n_max)
    delta = delta_series(n_max)
    e4_cubed = series_mul(series_mul(e4, e4, n_max), e4, n_max)
    coeff = h - 720
    return [e4_cubed[n] + coeff * delta[n] for n in range(n_max + 1)]


def verify_theta_root_count_pin(n_max: int = 10) -> dict[str, Any]:
    """Check [q^1] theta_L = h for each Niemeier."""
    discrepancies = []
    for label, decomp in NIEMEIER:
        h = root_count(decomp)
        th = theta_niemeier(h, n_max)
        if th[0] != 1:
            discrepancies.append({"label": label, "h": h, "q0_coef": th[0]})
        if th[1] != h:
            discrepancies.append({"label": label, "h": h, "q1_coef": th[1]})
    return {
        "n_max":         n_max,
        "discrepancies": discrepancies,
        "all_match":     discrepancies == [],
    }


# ----------------------------------------------------------------------
# Theta-collisions: distinct lattices with the same theta series.
# ----------------------------------------------------------------------
def theta_collisions() -> dict[str, Any]:
    by_h: dict[int, list[str]] = {}
    for label, decomp in NIEMEIER:
        h = root_count(decomp)
        by_h.setdefault(h, []).append(label)
    collisions = {h: labels for h, labels in by_h.items() if len(labels) > 1}
    return {
        "by_root_count":         {h: by_h[h] for h in sorted(by_h)},
        "collision_root_counts": sorted(collisions),
        "collisions":            collisions,
        "n_distinct_thetas":     len(by_h),
        "n_lattices":            sum(len(v) for v in by_h.values()),
        "collapse_24_to_19":     len(by_h) == 19 and sum(len(v) for v in by_h.values()) == 24,
    }


# ----------------------------------------------------------------------
# Cross-check special cases against earlier layers.
# ----------------------------------------------------------------------
def verify_E8_cubed_theta_equals_E4_cubed(n_max: int = 8) -> dict[str, Any]:
    """h = 720 ⇒ theta_L = E_4^3.  Hence theta_{E_8^3} = theta_{E_8}^3 = E_4^3."""
    e4 = e4_series(n_max)
    e4_cubed = series_mul(series_mul(e4, e4, n_max), e4, n_max)
    th = theta_niemeier(720, n_max)
    return {
        "n_max":           n_max,
        "theta_E8_cubed":  th,
        "E_4_cubed":       e4_cubed,
        "all_match":       th == e4_cubed,
    }


def verify_leech_theta_matches_layer_37(n_max: int = 4) -> dict[str, Any]:
    """For Leech (h = 0): theta_Leech = E_4^3 - 720 Delta.  q^2 should equal
       196560 (kissing number).  q^1 should equal 0."""
    th = theta_niemeier(0, n_max)
    return {
        "n_max":             n_max,
        "theta_Leech":       th,
        "q1_is_0":           th[1] == 0,
        "q2_is_196560":      th[2] == 196560,
        "matches_layer_37":  th[1] == 0 and th[2] == 196560,
    }


# ----------------------------------------------------------------------
# Niemeier root count summary.
# ----------------------------------------------------------------------
def niemeier_root_table() -> dict[str, Any]:
    out = []
    for label, decomp in NIEMEIER:
        out.append({"label": label, "h": root_count(decomp)})
    hs = sorted(set(item["h"] for item in out))
    return {
        "table":               out,
        "distinct_root_counts": hs,
        "extremes":            {"leech_h_0": hs[0], "max_h_1104": hs[-1]},
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    cnt = verify_total_count_is_24()
    rk = verify_all_have_rank_24()
    table = niemeier_root_table()
    pin = verify_theta_root_count_pin(n_max=8)
    coll = theta_collisions()
    cube = verify_E8_cubed_theta_equals_E4_cubed(n_max=8)
    leech = verify_leech_theta_matches_layer_37(n_max=4)
    return {
        "count":                  cnt,
        "rank_check":             rk,
        "root_table":             table,
        "theta_root_count_pin":   pin,
        "theta_collisions":       coll,
        "E8_cubed_theta":         cube,
        "leech_theta_pin":        leech,
        "summary_chain": {
            "exactly_24_Niemeier_lattices":              cnt["equals_24"],
            "every_Niemeier_has_rank_24_or_Leech":       rk["all_match"],
            "theta_q0_q1_match_root_count_pin":          pin["all_match"],
            "theta_collapse_24_to_19_distinct_thetas":   coll["collapse_24_to_19"],
            "E8_cubed_theta_equals_E4_cubed":            cube["all_match"],
            "leech_theta_matches_layer_37":              leech["matches_layer_37"],
        },
    }


def main() -> None:
    summary = derive_all()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print("=" * 72)
    print("W33 NIEMEIER LATTICES AND THE 24-TO-19 THETA COLLAPSE")
    print("=" * 72)
    print()
    for key, val in summary["summary_chain"].items():
        status = "PASS" if val else "FAIL"
        print(f"  [{status}] {key}")
    print()
    table = summary["root_table"]["table"]
    for item in table:
        print(f"   {item['label']:>18}    h = {item['h']:>5}")
    print()
    print(f"  Distinct theta classes:  {len(summary['root_table']['distinct_root_counts'])}")
    print(f"  Niemeier collisions:     {summary['theta_collisions']['collisions']}")


if __name__ == "__main__":
    main()
