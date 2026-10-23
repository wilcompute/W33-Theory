#!/usr/bin/env python3
"""Exact point-anchored W33 tick Hamiltonian spectral splitting.

Uniform base walk is *prior repo result* DCLXVIII; this script studies
a one-tick anisotropic defect, not a physical spacetime clock claim.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
import numpy as np
try:
    from analysis.w33_20261022_css_logical_sp43_generators import (
        J, P, perm_of_direction
    )
    from analysis.w33_20261022_pascal_css_logical_transvection_jordan import projective_points
except ModuleNotFoundError:
    from w33_20261022_css_logical_sp43_generators import (
        J, P, perm_of_direction
    )
    from w33_20261022_pascal_css_logical_transvection_jordan import projective_points


def exact_model():
    points = projective_points(3)
    X = np.asarray(points, dtype=np.int64)
    ident = np.eye(40, dtype=np.int64)
    all1 = np.ones((40,40), dtype=np.int64)
    adjacency = ((X @ J @ X.T) % 3 == 0).astype(np.int64) - ident
    B = all1 - ident - adjacency
    assert np.array_equal(adjacency @ adjacency, 8*ident-2*adjacency+4*all1)
    assert np.all(B.sum(axis=1) == 27)

    transvection = perm_of_direction(points, X[0])
    T = np.zeros((40,40), dtype=np.int64)
    T[np.arange(40), list(transvection)] = 1
    assert np.array_equal(T @ T, T.T)
    assert np.array_equal(T @ adjacency, adjacency @ T)
    assert int(np.trace(T)) == 13
    assert int(np.trace(T @ adjacency)) == 0
    assert int(np.trace(T @ (adjacency @ adjacency))) == 264

    # Exact numerators for rational Bose-Mesner primitive projectors.
    Er60 = (12*ident-adjacency) @ (adjacency+4*ident)
    Es96 = (adjacency-12*ident) @ (adjacency-2*ident)
    assert np.array_equal(Er60@Er60, 60*Er60)
    assert np.array_equal(Es96@Es96, 96*Es96)
    assert int(np.trace(Er60)) == 60*24
    assert int(np.trace(Es96)) == 96*15
    assert int(np.trace(T @ Er60)) == 360
    assert int(np.trace(T @ Es96)) == 576

    # Existing exact uniform complement walk K=(13I+B)/40 from DCLXVIII.
    # H0=40(I-K)=27I-B. The anchor cost is 2I-T-T^{-1}.
    H0 = 27*ident-B
    defect = 2*ident-T-T.T
    H = H0 + defect
    assert np.array_equal(H, H.T)
    assert np.array_equal(H0 @ defect, defect @ H0)
    assert np.array_equal(H @ all1, np.zeros((40,40),dtype=np.int64))
    assert int(np.trace(H)) == 1134
    assert int(np.trace(H @ H)) == 33426

    spectrum = {0:1, 24:9, 27:6, 30:12, 33:12}
    # Annihilator identity, exact integer matrix arithmetic.
    poly = ident.copy()
    for lam in spectrum:
        poly = poly @ (H-lam*ident)
    assert np.count_nonzero(poly) == 0
    # Independent floating eigensolver check is only secondary to exact identities.
    observed = np.rint(np.linalg.eigvalsh(H)).astype(int)
    expected = np.array([lam for lam,m in spectrum.items() for _ in range(m)])
    assert np.array_equal(observed, expected)

    # In E2: tr(T)=6, d=24 -> fixed12, rotating12.
    # In E-4: tr(T)=6, d=15 -> fixed9, rotating6.
    # Rotating eigenvalues e^{+-2pi i/3} have defect eigenvalue 3.
    return {
        "schema":"w33.anchored_transvection_hamiltonian.v1",
        "source_base_walk":"DCLXVIII: (13I+B)/40",
        "status":"EXACT_FINITE_SYMMETRY_BREAKING_TOY_NO_DERIVED_CLOCK",
        "hamiltonian":"H=27I-B+2I-T-T^(-1)",
        "anchor_stabilizer_order": 648,
        "W33_adjacency_spectrum":{"12":1,"2":24,"-4":15},
        "base_H0_spectrum":{"0":1,"24":15,"30":24},
        "anchored_H_spectrum":{str(k):v for k,v in spectrum.items()},
        "T_trace_on_E2":6,
        "T_trace_on_Eminus4":6,
        "E2_fixed_and_rotating":[12,12],
        "Eminus4_fixed_and_rotating":[9,6],
        "trace_H":1134,
        "trace_H_squared":33426,
        "exact_matrix_annihilator_verified":True,
        "continuous_epsilon_spectrum":{
            "E0":"0 (multiplicity 1)",
            "E2_fixed":"30 (multiplicity 12)",
            "E2_rotating":"30+3*epsilon (multiplicity 12)",
            "Eminus4_fixed":"24 (multiplicity 9)",
            "Eminus4_rotating":"24+3*epsilon (multiplicity 6)"
        },
        "dynamics_selects_anchor":False,
        "physical_implementation_verified":False
    }


if __name__=="__main__":
    payload=json.dumps(exact_model(),indent=2)+"\n"
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
