#!/usr/bin/env python3
"""Pass 10945: exact Choi/Fourier three-channel temporal weld.

This packet factors the 27D operator-compatible Fourier sector into a
9-dimensional qutrit matrix-coefficient space times the external C3 clock,
then resolves the 54D retyping quotient into three exact 18D clock-phase
channels.  It also computes how pure and diagonal phase-weld backgrounds sit
inside those channels, entirely over Q(omega).
"""
from __future__ import annotations

import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

from w33_pass10944_five_front_computational_closure import (
    QomegaColumnBasis, QW_ZERO, QW_ONE, QW_POWERS,
    qw_mul, fourier_columns,
)
from w33_e6_cubic_fourier54_alignment import ordered_records

OUT = ROOT / "data/w33_pass10945_choi_fourier_three_channel_weld.json"
def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qscale(c, x):
    c = Fraction(c)
    return (c*x[0], c*x[1])


def qpow(k):
    return QW_POWERS[k % 3]


def rank(columns):
    b = QomegaColumnBasis()
    for col in columns:
        b.add(col)
    return b.rank


def restrict(columns, phases):
    rows = [3*eid+p for eid in range(27) for p in phases]
    return [[col[j] for j in rows] for col in columns]


def coordinate_slice(phase):
    cols = []
    for eid in range(27):
        v = [QW_ZERO]*81
        v[3*eid+phase] = QW_ONE
        cols.append(v)
    return cols
def localized_s1(s1_labeled, phase):
    """Inverse external Fourier transform: 9 S1 vectors supported on one phase."""
    lookup = {label: col for label, col in s1_labeled}
    out = []
    for r, i in itertools.product(range(3), repeat=2):
        v = [QW_ZERO]*81
        for t in range(3):
            coeff = qscale(Fraction(1, 3), qpow(-t*phase))
            col = lookup[("S1", t, r, i)]
            v = [qadd(a, qw_mul(coeff, b)) for a, b in zip(v, col)]
        for eid in range(27):
            for p in range(3):
                if p != phase:
                    assert v[3*eid+p] == QW_ZERO
        out.append(v)
    assert rank(out) == 9
    return out


def matmul(A, B):
    out = [[QW_ZERO for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for k in range(len(B)):
            for j in range(len(B[0])):
                out[i][j] = qadd(out[i][j], qw_mul(A[i][k], B[k][j]))
    return out
def matpow(A, n):
    I = [[QW_ONE if i == j else QW_ZERO for j in range(3)] for i in range(3)]
    R = I
    for _ in range(n % 3):
        R = matmul(R, A)
    return R


def madd(A, B):
    return [[qadd(A[i][j], B[i][j]) for j in range(3)] for i in range(3)]


def mscale(c, A):
    return [[qw_mul(c, A[i][j]) for j in range(3)] for i in range(3)]


def weyl_matrix_unit_certificate():
    X = [[QW_ZERO]*3 for _ in range(3)]
    for j in range(3):
        X[(j+1) % 3][j] = QW_ONE
    Z = [[QW_ZERO]*3 for _ in range(3)]
    for j in range(3):
        Z[j][j] = qpow(j)

    rows = []
    for i, r in itertools.product(range(3), repeat=2):
        b = (i-r) % 3
        E = [[QW_ZERO]*3 for _ in range(3)]
        E[i][r] = QW_ONE
        rhs = [[QW_ZERO]*3 for _ in range(3)]
        terms = []
        for a in range(3):
            coeff = qscale(Fraction(1, 3), qpow(-a*i))
            W = matmul(matpow(Z, a), matpow(X, b))
            rhs = madd(rhs, mscale(coeff, W))
            terms.append({"a": a, "coefficient": [str(coeff[0]), str(coeff[1])]})
        assert rhs == E
        rows.append({
            "matrix_unit": [i, r],
            "weyl_shift_b": b,
            "formula": "E_ir=(1/3) sum_a omega^(-a*i) Z^a X^(i-r)",
            "terms": terms,
        })
    return {
        "verified_matrix_units": 9,
        "exact_field": "Q(omega), omega^2+omega+1=0",
        "transform": "Weyl/Pauli operator basis <-> qutrit matrix-unit (Choi history) basis",
        "formula": "E_ir=(1/3) sum_{a=0}^2 omega^(-a*i) Z^a X^(i-r)",
        "rows": rows,
    }


def cubic_image(background):
    D = [[0]*81 for _ in range(81)]
    for u, x, o, c in ordered_records():
        D[o][x] += c*background[u]
    return [[(Fraction(D[row][col]), Fraction(0)) for row in range(81)]
            for col in range(81)]
def quotient_rank(s1, images):
    return rank(s1 + images) - rank(s1)


def main():
    bridge = json.loads((ROOT / "data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    e6_to_h = {
        int(i): tuple(map(int, h))
        for i, h in bridge["maps"]["e6id_to_current_H27_address"].items()
    }
    s1_labeled, _p, _q = fourier_columns(e6_to_h)
    s1 = [col for _label, col in s1_labeled]
    assert rank(s1) == 27

    phase_rows = []
    localized = {}
    for p in range(3):
        C = coordinate_slice(p)
        L = localized_s1(s1_labeled, p)
        localized[p] = L
        rsum = rank(s1 + C)
        inter = 27 + 27 - rsum
        qdim = rsum - 27
        assert (inter, qdim) == (9, 18)
        phase_rows.append({
            "phase": p,
            "coordinate_slice_dimension": 27,
            "S1_intersection_dimension": inter,
            "quotient_channel_dimension": qdim,
        })
    assert rank(localized[0] + localized[1] + localized[2]) == 27
    pair_dims = {}
    for a, b in itertools.combinations(range(3), 2):
        C = coordinate_slice(a) + coordinate_slice(b)
        pair_dims[f"{a}{b}"] = rank(s1 + C) - 27
    assert set(pair_dims.values()) == {36}
    all_coords = coordinate_slice(0) + coordinate_slice(1) + coordinate_slice(2)
    assert rank(s1 + all_coords) - 27 == 54

    coords = [(e6_to_h[eid], p) for eid in range(27) for p in range(3)]
    lift = lambda x: 1 + (int(x) % 3)
    backgrounds = {
        "center": [lift(h[2]) for h, p in coords],
        "external": [lift(p) for h, p in coords],
        "center_plus_external": [lift(h[2]+p) for h, p in coords],
        "center_minus_external": [lift(h[2]-p) for h, p in coords],
    }
    images = {name: cubic_image(bg) for name, bg in backgrounds.items()}
    expected = {"center": 36, "external": 36,
                "center_plus_external": 54, "center_minus_external": 54}
    bg_rows = {}
    for name, im in images.items():
        total = quotient_rank(s1, im)
        assert total == expected[name]
        singles = {}
        pairs = {}
        for p in range(3):
            rs = restrict(s1, (p,))
            ri = restrict(im, (p,))
            singles[str(p)] = rank(rs + ri) - rank(rs)
        for a, b in itertools.combinations(range(3), 2):
            rs = restrict(s1, (a, b))
            ri = restrict(im, (a, b))
            pairs[f"{a}{b}"] = rank(rs + ri) - rank(rs)
        assert set(singles.values()) == {18}
        assert set(pairs.values()) == {36}
        bg_rows[name] = {
            "total_quotient_rank": total,
            "single_phase_projection_ranks": singles,
            "two_phase_projection_ranks": pairs,
            "any_two_phases_determine_pure_background": total == 36,
        }

    wc, we = images["center"], images["external"]
    span_ce = quotient_rank(s1, wc + we)
    inter_ce = 36 + 36 - span_ce
    assert (span_ce, inter_ce) == (54, 18)

    out = {
        "schema": "w33.pass10945.choi_fourier_three_channel_weld.v1",
        "status": "PASS_CHOI_FOURIER_THREE_CHANNEL_TEMPORAL_WELD",
        "S1_factorization": {
            "dimension": 27,
            "factorization": "Coeff(V_omega) tensor Reg(C3_external)",
            "qutrit_matrix_coefficient_dimension": 9,
            "external_clock_dimension": 3,
            "localized_phase_basis_formula": (
                "L_{p,r,i}=(1/3) sum_t omega^(-tp) S1(t,r,i)"
            ),
            "localized_phase_basis_verified": True,
            "matrix_unit_intertwiner": weyl_matrix_unit_certificate(),
        },
        "three_phase_quotient": {
            "phase_channels": phase_rows,
            "pair_quotient_dimensions": pair_dims,
            "full_quotient_dimension": 54,
            "identity": "54 = 18 + 18 + 18",
            "parabolic_regrouping": "P=(phase0+phase1) gives 36; Q=phase2 gives 18",
            "S1_decomposition": "27 = 9 + 9 + 9 localized matrix-coefficient sectors",
        },
        "weld_geometry": {
            "backgrounds": bg_rows,
            "pure_center_dimension": 36,
            "pure_external_dimension": 36,
            "pure_center_external_span_dimension": span_ce,
            "pure_center_external_intersection_dimension": inter_ce,
            "inclusion_exclusion": "54 = 36 + 36 - 18",
            "diagonal_backgrounds_span_full_three_channel_quotient": True,
            "pure_background_projection_property": (
                "each pure 36D weld projects surjectively to every 18D phase channel "
                "and every 36D pair of channels, so its missing 18D freedom is a "
                "cross-phase relation rather than one absent phase channel"
            ),
        },
        "theorem": (
            "The 27-dimensional operator-compatible Fourier sector is exactly three "
            "external-clock copies of the nine-dimensional qutrit matrix-coefficient "
            "space. Inverse C3 Fourier transform localizes it as 9+9+9 across the "
            "three external phase slices, and the 54-dimensional retyping quotient "
            "therefore splits exactly as 18+18+18. Pure center and pure external "
            "backgrounds each occupy a 36-dimensional graph subspace with an "
            "18-dimensional intersection and 54-dimensional span; either diagonal "
            "background releases the remaining cross-phase relation and reaches all 54."
        ),
        "boundary": (
            "All ranks and the Weyl-to-matrix-unit transform are exact over Q(omega). "
            "The nine matrix units justify the term Choi/operator histories algebraically. "
            "No identification of the 18D channels with spacetime null/non-null events, "
            "particle sectors, or thermodynamic irreversibility is made."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "S1": out["S1_factorization"]["factorization"],
        "quotient": out["three_phase_quotient"]["identity"],
        "pure_intersection": inter_ce,
        "diagonal_rank": bg_rows["center_plus_external"]["total_quotient_rank"],
    }, indent=2))


if __name__ == "__main__":
    main()
