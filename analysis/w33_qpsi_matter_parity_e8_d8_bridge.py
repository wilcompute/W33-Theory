#!/usr/bin/env python3
"""Qpsi matter parity extends to the canonical E8 D8/spinor involution.

Inputs already certified elsewhere in this repository:
  * E6 -> SO(10) x U(1)_psi on the 27:
        27 = 16_1 + 10_-2 + 1_4.
  * The exact Qpsi spectrum on the repository's 240 E8 root channels:
        g0_e6: 40*0 + 16*(-3) + 16*(+3)
        g0_a2:  6*0
        g1:    48*(+1) + 30*(-2) + 3*(+4)
        g2:    48*(-1) + 30*(+2) + 3*(-4).
  * The 45 E6 cubic triads have Qpsi patterns
        (-2,1,1) x40 and (-2,-2,4) x5.

This verifier extracts the mod-2 consequence and independently reconstructs
the standard 240-root E8 shell.  The Qpsi-even/odd root counts are 112/128.
A standard E8 order-two Cartan parity has exactly the same split: its 112 even
roots are the D8 roots +-e_i+-e_j and its 128 odd roots are the half-spinor
roots.  Adding the eight Cartan generators gives the involution branching
248 = 120 + 128.

The theorem is therefore representation-theoretic: the Z2 whose restriction
to an E6 fundamental is matter parity (odd on the 16, even on 10+1) extends to
the canonical E8 D8/spinor involution class.

Boundary: the Qpsi spectra are source-locked to the repository's existing
metadata pipeline.  This file does not regenerate the heavyweight E8 metadata
artifact that is intentionally absent from ordinary CI, and it does not claim
a coordinatewise equality between that archived basis and the standard D8
coordinates constructed below without an explicit Weyl map.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_qpsi_matter_parity_e8_d8_bridge.json"

# Certified source data from tools/toe_closed_form_selection_rules.py.
ROOT_QPSI = {
    "g0_e6": {0: 40, -3: 16, 3: 16},
    "g0_a2": {0: 6},
    "g1": {1: 48, -2: 30, 4: 3},
    "g2": {-1: 48, 2: 30, -4: 3},
}
# Certified by tests/test_toe_new_results.py.
CUBIC_PATTERNS = {
    (-2, 1, 1): {"count": 40, "firewall_forbidden": 8},
    (-2, -2, 4): {"count": 5, "firewall_forbidden": 1},
}
REP27 = {1: 16, -2: 10, 4: 1}


def roots_e8():
    roots = []
    for i, j in itertools.combinations(range(8), 2):
        for a in (1, -1):
            for b in (1, -1):
                v = [F(0)] * 8
                v[i], v[j] = F(a), F(b)
                roots.append(tuple(v))
    for s in itertools.product((1, -1), repeat=8):
        if sum(x < 0 for x in s) % 2 == 0:
            roots.append(tuple(F(x, 2) for x in s))
    assert len(roots) == len(set(roots)) == 240
    return roots


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rank(rows):
    A = [list(map(F, r)) for r in rows]
    if not A:
        return 0
    m, n, rr = len(A), len(A[0]), 0
    for c in range(n):
        p = next((i for i in range(rr, m) if A[i][c]), None)
        if p is None:
            continue
        A[rr], A[p] = A[p], A[rr]
        z = A[rr][c]
        A[rr] = [x / z for x in A[rr]]
        for i in range(m):
            if i != rr and A[i][c]:
                z = A[i][c]
                A[i] = [A[i][j] - z * A[rr][j] for j in range(n)]
        rr += 1
    return rr


def main(write=True):
    # Source locks: fail loudly if the ownership files disappear.
    required = [
        ROOT / "tools/toe_closed_form_selection_rules.py",
        ROOT / "tools/toe_sm_cubic_firewall_analysis.py",
        ROOT / "tests/test_toe_new_results.py",
    ]
    assert all(p.exists() for p in required)

    # E6 fundamental: matter parity is Qpsi mod 2.
    assert sum(REP27.values()) == 27
    odd27 = sum(n for q, n in REP27.items() if q % 2)
    even27 = sum(n for q, n in REP27.items() if not q % 2)
    assert (odd27, even27) == (16, 11)

    # Every certified E6 cubic conserves Qpsi and is therefore parity-even.
    assert sum(v["count"] for v in CUBIC_PATTERNS.values()) == 45
    assert all(sum(pat) == 0 for pat in CUBIC_PATTERNS)
    assert all(sum(q & 1 for q in pat) % 2 == 0 for pat in CUBIC_PATTERNS)
    assert CUBIC_PATTERNS[(-2, 1, 1)]["count"] == 40
    assert CUBIC_PATTERNS[(-2, -2, 4)]["count"] == 5

    # Full E8 root-channel Qpsi parity.
    total = even = odd = 0
    by_grade = {}
    for grade, hist in ROOT_QPSI.items():
        e = sum(n for q, n in hist.items() if q % 2 == 0)
        o = sum(n for q, n in hist.items() if q % 2 != 0)
        by_grade[grade] = {"even": e, "odd": o, "total": e + o}
        even += e
        odd += o
        total += e + o
    assert total == 240
    assert (even, odd) == (112, 128)
    assert by_grade == {
        "g0_e6": {"even": 40, "odd": 32, "total": 72},
        "g0_a2": {"even": 6, "odd": 0, "total": 6},
        "g1": {"even": 33, "odd": 48, "total": 81},
        "g2": {"even": 33, "odd": 48, "total": 81},
    }

    # Independent standard-coordinate E8 construction.
    R = roots_e8()
    h = tuple(F(1) for _ in range(7)) + (F(-1),)
    std_even = [r for r in R if int(dot(h, r)) % 2 == 0]
    std_odd = [r for r in R if int(dot(h, r)) % 2 != 0]
    assert len(std_even) == 112 and len(std_odd) == 128
    assert all(sum(x.denominator != 1 for x in r) == 0 for r in std_even)
    assert all(all(abs(x) == F(1, 2) for x in r) for r in std_odd)
    assert rank(std_even) == 8

    # The even roots are exactly the standard D8 root system +-e_i+-e_j.
    d8 = set()
    for i, j in itertools.combinations(range(8), 2):
        for a in (1, -1):
            for b in (1, -1):
                v = [F(0)] * 8
                v[i], v[j] = F(a), F(b)
                d8.add(tuple(v))
    assert set(std_even) == d8 and len(d8) == 112

    fixed_dim = len(std_even) + 8
    assert fixed_dim == 120
    assert fixed_dim + len(std_odd) == 248

    out = {
        "schema": "w33.qpsi_matter_parity_e8_d8_bridge.v1",
        "status": "PASS_QPSI_MATTER_PARITY_EXTENDS_TO_E8_D8_INVOLUTION",
        "headline": (
            "The exact E6 U(1)_psi charge reduces mod 2 to matter parity on the 27: "
            "16_1 is odd while 10_-2 and 1_4 are even.  Extending the repository's "
            "certified Qpsi spectrum to all 240 E8 root channels gives exactly 112 "
            "even roots and 128 odd roots.  An independent standard E8 construction "
            "identifies the 112 even roots with D8 and the 128 odd roots with the "
            "half-spinor shell, hence the involution branching 248=120+128.  The "
            "45 E6 cubic triads occur only as 40*(16,16,10)+5*(10,10,1), so every "
            "cubic is automatically matter-parity even."
        ),
        "E6_27": {
            "branching": "27 = 16_1 + 10_-2 + 1_4",
            "Qpsi_histogram": {str(k): v for k, v in sorted(REP27.items())},
            "matter_parity": "(-1)^Qpsi",
            "odd_dimension": odd27,
            "even_dimension": even27,
        },
        "E6_cubic": {
            "total_triads": 45,
            "patterns": [
                {
                    "Qpsi": list(pat),
                    "count": meta["count"],
                    "firewall_forbidden": meta["firewall_forbidden"],
                    "sum_Qpsi": sum(pat),
                    "parity_even": True,
                }
                for pat, meta in sorted(CUBIC_PATTERNS.items())
            ],
            "representation_reading": "40*(16,16,10) + 5*(10,10,1)",
            "all_cubics_matter_parity_even": True,
        },
        "E8_Qpsi_mod2": {
            "source_histograms": {
                g: {str(k): v for k, v in sorted(hh.items())}
                for g, hh in ROOT_QPSI.items()
            },
            "by_Z3_grade": by_grade,
            "even_roots": even,
            "odd_roots": odd,
            "fixed_cartan": 8,
            "fixed_lie_dimension": fixed_dim,
            "branching": "248 = 120_even + 128_odd",
        },
        "standard_E8_crosscheck": {
            "parity_functional": [1, 1, 1, 1, 1, 1, 1, -1],
            "even_roots": 112,
            "even_root_system": "D8",
            "odd_roots": 128,
            "odd_shell": "one chiral half-spinor weight shell of Spin(16)",
            "rank_even_roots": 8,
        },
        "crossrepo_reading": (
            "Holotrade's field-level result that matter parity is exactly 16-membership "
            "is the E6 restriction of this E8 D8/spinor Z2.  Therefore a dangerous "
            "matter-odd MSSM monomial can enter an E6-invariant coupling only together "
            "with another odd factor; this matches the measured order-four udd couplings "
            "that require a matter-odd singlet."
        ),
        "provenance": [
            "tools/toe_closed_form_selection_rules.py",
            "tools/toe_sm_cubic_firewall_analysis.py",
            "tests/test_toe_new_results.py",
            "Holotrade data/w33_matter_parity_is_the_16.json",
            "Holotrade data/w33_matter_parity_z2_correction.json",
        ],
        "boundary": (
            "The 240-channel Qpsi histograms are source-locked to the repository's "
            "existing metadata pipeline; this lightweight verifier does not regenerate "
            "the heavyweight metadata artifact absent from ordinary CI.  The standard "
            "D8 construction proves the conjugacy-class identification, not a coordinatewise "
            "Weyl map between the archived E8 basis and the standard coordinates."
        ),
        "checks": {
            "matter_parity_is_Qpsi_mod2_on_27": True,
            "all_45_cubics_parity_even": True,
            "E8_Qpsi_even_odd_is_112_128": True,
            "standard_E8_even_roots_are_D8": True,
            "fixed_dimension_120": True,
            "adjoint_248_split": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
