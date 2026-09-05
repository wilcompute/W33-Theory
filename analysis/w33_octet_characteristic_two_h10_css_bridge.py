#!/usr/bin/env python3
"""Characteristic-two shadow of the BT768 octet filter.

Two independently constructed 45-by-40 / 40-by-45 matrices in the repository
are in fact the same incidence object.

* T is the Pass4625 center-quad / quotient-point support incidence: its 45 rows
  are the antipodal center-quad 8-point supports.
* M is the BT768 point/octet incidence: its 45 columns are the 45 intrinsic
  minimum weight-8 octets in the binary W33 adjacency code.

This verifier reconstructs both from W33 and proves, after the unique support
matching,

    T = M^T.

It then makes the characteristic-two rank jump exact:

    rank_Q(T)=25,   rank_F2(T)=15,
    Smith(T)=1^15 2^10 0^15.

Hence ker_Q(M^T) is 15-dimensional.  The primitive integral kernel reduces
modulo two to im_F2(M), still 15-dimensional, while ker_F2(M^T) has dimension
25.  Therefore the TEN newly available characteristic-two kernel dimensions
are exactly

    H10 = ker_F2(M^T) / im_F2(M),

and the canonical Bockstein identifies this H10 with Tor_2 coker_Z(M^T) =
(Z/2)^10.  Reusing M^T as both X and Z checks is exactly the existing
[[40,10,4]] CSS code.

The rational 15-dimensional BT768 killed sector and the centered 36-spread
polar frame remain related exactly as already proved by w33_bt768_o5_24_15_
closure.py.  They live on inequivalent point/line carriers for odd q, so this
file does NOT silently identify their 40 coordinates.  What becomes objectwise
here is the octet/H10 matrix itself: T=M^T.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
from collections import Counter

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

from exploration.w33_center_quad_gq42_e6_bridge import (
    quotient_points,
    w33_collinearity,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_octet_characteristic_two_h10_css_bridge.json"


def rank2(M: np.ndarray) -> int:
    A = np.asarray(M, dtype=np.uint8).copy() & 1
    m, n = A.shape
    r = 0
    for c in range(n):
        z = np.flatnonzero(A[r:, c])
        if not len(z):
            continue
        p = r + int(z[0])
        A[[r, p]] = A[[p, r]]
        for i in np.flatnonzero(A[:, c]):
            if i != r:
                A[i] ^= A[r]
        r += 1
        if r == m:
            break
    return r


def primitive(v: sp.Matrix) -> list[int]:
    den = 1
    for x in v:
        den = sp.ilcm(den, x.q)
    a = [int(x * den) for x in v]
    g = 0
    for x in a:
        g = math.gcd(g, abs(x))
    return [x // g for x in a] if g else a


def intrinsic_octets() -> set[frozenset[int]]:
    """BT768 construction: minimum weight-8 words of the W33 adjacency code."""
    col = w33_collinearity()
    rows = []
    for i in range(40):
        x = 0
        for j in col[i]:
            x |= 1 << j
        rows.append(x)
    span = {0}
    for r in rows:
        span |= {x ^ r for x in tuple(span)}
    assert len(span) == 2 ** 16
    octets = {
        frozenset(i for i in range(40) if (x >> i) & 1)
        for x in span if x.bit_count() == 8
    }
    assert len(octets) == 45
    return octets


def build() -> dict:
    # Pass4625 object, reconstructed independently from antipodal center quads.
    qp = quotient_points()
    T = np.zeros((45, 40), dtype=np.int64)
    t_supports = []
    for i, p in enumerate(qp):
        S = frozenset(p.support_vertices)
        assert len(S) == 8
        t_supports.append(S)
        T[i, list(S)] = 1
    assert len(set(t_supports)) == 45

    # BT768 object, reconstructed from the binary adjacency code only.
    octets = intrinsic_octets()
    assert set(t_supports) == octets
    # Reorder the 45 octets by the T rows; this is the unique support match.
    M = np.zeros((40, 45), dtype=np.int64)
    for j, S in enumerate(t_supports):
        M[list(S), j] = 1
    assert np.array_equal(T, M.T)

    rq = int(sp.Matrix(T).rank())
    rf2 = rank2(T)
    assert (rq, rf2) == (25, 15)

    D = smith_normal_form(sp.Matrix(T), domain=ZZ)
    diag = [abs(int(D[i, i])) for i in range(min(D.shape))]
    snf = Counter(diag)
    assert snf == Counter({1: 15, 2: 10, 0: 15})

    T2 = (T % 2).astype(np.uint8)
    M2 = (M % 2).astype(np.uint8)
    assert not np.any((T2 @ T2.T) % 2)
    assert not np.any((M2.T @ M2) % 2)

    ker_q = sp.Matrix(T).nullspace()
    assert len(ker_q) == 15
    KZ2 = np.array([[x & 1 for x in primitive(v)] for v in ker_q], dtype=np.uint8)
    assert rank2(KZ2) == 15
    # im(M)=row(T).  Primitive integral kernel reduction equals that image.
    assert rank2(np.vstack([KZ2, T2])) == 15

    ker_f2_dim = 40 - rf2
    im_m_dim = rank2(M2)
    h10_dim = ker_f2_dim - im_m_dim
    assert (ker_f2_dim, im_m_dim, h10_dim) == (25, 15, 10)

    # Existing exact certificates are consistency anchors, not inputs to T=M^T.
    p4625 = json.loads((ROOT / "data" / "PART_W33_PASS4625_INTRINSIC_45X40_THREE_CARRIER.json").read_text())
    p4630 = json.loads((ROOT / "data" / "PART_W33_PASS4630_T_BOCKSTEIN_H10_CSS.json").read_text())
    bt768 = json.loads((ROOT / "data" / "w33_bt768_o5_24_15_closure.json").read_text())
    enum = json.loads((ROOT / "data" / "w33_pass228_sentinel_weight_enumerator.json").read_text())
    assert p4625["matrix"]["rank_Q"] == 25 and p4625["matrix"]["rank_F2"] == 15
    assert p4630["binary_complex"]["middle_homology_dimension"] == 10
    assert p4630["bockstein"]["isomorphism"]
    assert p4630["CSS"]["parameters"] == "[[40,10,4]]"
    assert bt768["checks"]["BT768_octet_Gram_recovered"]
    assert enum["sentinel_40_15_8"]["min_distance"] == 8
    assert enum["context_40_25_4_via_macwilliams"]["min_distance"] == 4

    checks = {
        "45_center_quad_supports_reconstructed": len(t_supports) == 45,
        "45_intrinsic_binary_octets_reconstructed": len(octets) == 45,
        "support_sets_are_identical": set(t_supports) == octets,
        "T_equals_M_transpose_after_support_match": bool(np.array_equal(T, M.T)),
        "rank_Q_is_25": rq == 25,
        "rank_F2_is_15": rf2 == 15,
        "smith_is_1pow15_2pow10_0pow15": snf == Counter({1: 15, 2: 10, 0: 15}),
        "M_transpose_M_zero_mod2": not np.any((M2.T @ M2) % 2),
        "primitive_rational_kernel_reduces_to_im_M": rank2(KZ2) == 15 and rank2(np.vstack([KZ2, T2])) == 15,
        "binary_kernel_dimension_is_25": ker_f2_dim == 25,
        "binary_boundary_dimension_is_15": im_m_dim == 15,
        "characteristic_two_kernel_jump_is_H10": h10_dim == 10,
        "bockstein_target_is_Z2_pow10": snf[2] == 10,
        "existing_CSS_is_40_10_4": p4630["CSS"]["parameters"] == "[[40,10,4]]",
        "BT768_companion_spread_sector_certificate_is_green": bt768["status"] == "PASS",
    }
    assert all(checks.values())

    return {
        "schema": "w33.octet-characteristic-two-h10-css-bridge.v1",
        "status": "PASS",
        "checks": checks,
        "objectwiseIdentity": {
            "T": "45x40 antipodal-center-quad support incidence",
            "M": "40x45 intrinsic BT768 point/octet incidence",
            "identity": "T = M^T after the unique equality-of-supports ordering",
            "rowsOrColumns": 45,
            "supportSize": 8,
        },
        "integerAndBinaryRanks": {
            "rankQ": rq,
            "rankF2": rf2,
            "smith": {"1": 15, "2": 10, "0": 15},
            "uniqueRankDropPrime": 2,
        },
        "characteristicTwoShadow": {
            "rationalKernelDimension": len(ker_q),
            "primitiveIntegralKernelMod2Dimension": rank2(KZ2),
            "primitiveIntegralKernelMod2EqualsImM": True,
            "binaryKernelDimension": ker_f2_dim,
            "newKernelDimensionsAtTwo": h10_dim,
            "H10": "ker_F2(M^T) / im_F2(M)",
            "bockstein": "H10 ~= Tor_2 coker_Z(M^T) = (Z/2)^10",
        },
        "CSS": {
            "checks": "H_X=H_Z=M^T",
            "parameters": "[[40,10,4]]",
            "logicalSpace": "H10",
            "distanceWitness": "weight-4 W33 line/context words lie in ker(M^T), while im(M) is the sentinel [40,15,8] code",
        },
        "BT768Relation": {
            "rationalStatement": "MM^T=8I+J+2A has a 15-dimensional rational kernel and a transmitted 24-dimensional complement.",
            "spreadFrame": "The existing BT768/O5 closure realizes the corresponding line-side 15-sector by the centered 36-spread polar frame C0 and proves N C0=0.",
            "carrierBoundary": "At odd q, W33 point and line carriers are inequivalent; no coordinatewise point=line identification is asserted here.",
            "newSynthesis": "Modulo two the primitive integral 15-kernel becomes im(M), while ker(M^T) expands to dimension 25. The ten-dimensional quotient is exactly H10/Smith-2/CSS logical homology.",
        },
        "theorem": "The BT768 octet filter and the H10 Smith/CSS incidence are the same integral matrix transposed. Characteristic two is the unique rank-drop prime, and its ten extra kernel dimensions are exactly H10, equivalently the ten Smith-2 torsion bits and the [[40,10,4]] CSS logical space.",
        "boundary": "Exact finite integral/binary coding statement. It does not identify W33 point and line coordinates or imply a physical error-correcting implementation by itself.",
    }


def main() -> int:
    out = build()
    if "--write" in __import__("sys").argv:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
