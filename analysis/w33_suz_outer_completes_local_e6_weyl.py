#!/usr/bin/env python3
"""The Suzuki outer automorphism supplies the missing local E6 factor of two.

The repository's exhaustive parent certificate
``w33_suzuki_w33_stabilizer_projective_quotient.json`` proves that for one
embedded full W(3,3), the 2.Suz block stabilizer has linear image Sp(4,3)
but projective action only PSp(4,3), order 25920, on the 27 complementary
three-W33 decompositions.  All 270270 Schreier generators are inner there.

This file adds the actual ATLAS 12-dimensional GF(3) representation of
2.Suz:2.  Its second standard generator D is literally the old Suzuki B
matrix.  The new generator C is a symplectic similitude of multiplier -1.
For the repository's chosen W33 block U, C(U) is reached from U by the explicit
inner word

    BABABABABABBABABABABBABABA

in the old 2.Suz generators.  Hence C times the inverse of that transporter is
an explicit outer-coset element fixing U.  This upgrades the classification
argument to a constructive block-stabilizer witness.

Published ATLAS input supplies the stabilizer structure:
  Suz      : 2^(1+6).U4(2)   at index 135135;
  Suz:2    : 2^(1+6).U4(2).2 at the same index.
The normal 2-core acts trivially on the transitive odd 27-set, while the inner
U4(2) socle is already faithful by the exhaustive repository computation.
Thus the explicit outer stabilizer element completes the image to U4(2):2,
order 51840, classically W(E6), the full Schlaefli/cubic-surface symmetry.

Finite group/geometry theorem only; no physical E6 gauge symmetry is inferred.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_suz_outer_completes_local_e6_weyl.json"
P = 3
TRANS_WORD = "BABABABABABBABABABABBABABA"


def load_tower():
    path = ROOT / "analysis" / "w33_suzuki_w33_e6_incidence_tower.py"
    spec = importlib.util.spec_from_file_location("tower", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def invp(M):
    M = np.array(M, dtype=np.int64) % P
    n = M.shape[0]
    X = np.concatenate([M, np.eye(n, dtype=np.int64)], axis=1)
    for c in range(n):
        p = next(i for i in range(c, n) if X[i, c])
        X[[c, p]] = X[[p, c]]
        X[c] = X[c] * pow(int(X[c, c]), -1, P) % P
        for i in range(n):
            if i != c and X[i, c]:
                X[i] = (X[i] - X[i, c] * X[c]) % P
    return X[:, n:] % P


def multiplier(g, J):
    X = g @ J @ g.T % P
    for m in (1, 2):
        if np.array_equal(X, m * J % P):
            return m
    return None


def main(write=True):
    parent = json.loads((ROOT / "data" / "w33_suzuki_w33_stabilizer_projective_quotient.json").read_text())
    assert parent["status"] == "PASS"
    assert parent["projective_27_action"]["order"] == 25920
    assert parent["projective_27_action"]["group"] == "PSp(4,3)"
    assert parent["exhaustive_schreier"]["outer_generators_seen"] == 0

    T = load_tower()
    A = T.parse_meataxe(ROOT / "data/atlas/2SuzG1-f3r12B0.m1")
    B = T.parse_meataxe(ROOT / "data/atlas/2SuzG1-f3r12B0.m2")
    C = T.parse_meataxe(ROOT / "data/atlas/2Suzd2G1-f3r12aB0.m1")
    D = T.parse_meataxe(ROOT / "data/atlas/2Suzd2G1-f3r12aB0.m2")
    U = np.array(T.U1, dtype=np.int64)
    J = np.array(T.J, dtype=np.int64)

    assert np.array_equal(D, B)
    assert multiplier(A, J) == multiplier(B, J) == 1
    assert multiplier(C, J) == 2

    # Explicit old-group transporter from U to C(U).
    M = np.eye(12, dtype=np.int64)
    for ch in TRANS_WORD:
        M = M @ (A if ch == "A" else B) % P
    assert T.rref_key(U @ M % P) == T.rref_key(U @ C % P)

    # Outer-coset element fixing U.  It is a multiplier-2 similitude, therefore
    # not contained in the old symplectic 2.Suz image.
    h = C @ invp(M) % P
    assert T.rref_key(U @ h % P) == T.rref_key(U)
    assert multiplier(h, J) == 2

    suz = 448345497600
    suz2 = 2 * suz
    degree = 135135
    inner_stab = suz // degree
    outer_stab = suz2 // degree
    u42 = 25920
    u42d2 = 2 * u42
    core = 128
    assert inner_stab == 3317760 == core * u42
    assert outer_stab == 6635520 == core * u42d2

    out = {
      "schema": "w33.suz_outer_completes_local_e6_weyl.v2",
      "status": "PASS_WITH_CONSTRUCTIVE_ATLAS_OUTER_WITNESS",
      "headline": "Inside 2.Suz the local 27-decomposition action is exactly PSp(4,3), order 25920. In the vendored ATLAS 2.Suz:2 representation, the new standard generator C has symplectic multiplier -1 and sends the chosen W33 block U to the same block reached by the explicit old-group word BABABABABABBABABABABBABABA. Therefore h=C T^{-1} is an explicit outer-coset element fixing U. Combined with the published stabilizer 2^(1+6).U4(2).2 and the already-faithful inner U4(2) action, this completes the local image to U4(2):2 ~= W(E6), order 51840.",
      "computed_parent": {
        "source": "data/w33_suzuki_w33_stabilizer_projective_quotient.json",
        "2Suz_projective_image": "PSp(4,3)",
        "order": 25920,
        "outer_Schreier_generators_in_2Suz": 0
      },
      "constructive_outer_witness": {
        "ATLAS_representation": "2Suzd2G1-f3r12aB0 over GF(3)",
        "D_equals_old_B": True,
        "C_symplectic_multiplier_mod3": 2,
        "old_transport_word": TRANS_WORD,
        "old_transport_word_length": len(TRANS_WORD),
        "U_times_C_equals_U_times_transport_as_subspace": True,
        "outer_block_stabilizer": "h = C * T^{-1}",
        "h_fixes_U_projectively": True,
        "h_symplectic_multiplier_mod3": 2,
        "consequence": "h lies outside the old symplectic 2.Suz image while stabilizing the chosen W33 block"
      },
      "ATLAS_stabilizers": {
        "Suz": "2^(1+6).U4(2), order 3317760, index 135135",
        "Suz2": "2^(1+6).U4(2).2, order 6635520, index 135135",
        "normal_2_core_order": core,
        "U4_2_order": u42,
        "U4_2_outer_order": 2
      },
      "deduction": {
        "normal_2_core_local_action": "trivial by the odd transitive 27-set block argument",
        "inner_socle_action": "faithful U4(2) ~= PSp(4,3)",
        "explicit_outer_coset_block_stabilizer": True,
        "Suz2_local_image_order": u42d2,
        "identification": "U4(2):2 ~= W(E6)"
      },
      "interpretation": "The E6 factor of two absent from the 2.Suz-induced projective action is realized constructively by adjoining the Suzuki outer automorphism; the corresponding ATLAS generator is an anti-symplectic/similitude outer operation on the 12-dimensional ternary carrier.",
      "sources": [
        "ATLAS 2.Suz:2 12a-dimensional GF(3) representation, vendored under data/atlas",
        "ATLAS maximal subgroups of Suz and Suz:2",
        "ATLAS U4(2)=S4(3): order 25920, Out=2",
        "classical cubic-surface 27-line graph automorphism group W(E6)"
      ],
      "boundary": "The matrix witness and finite-group completion are exact. They do not establish physical availability of the outer similitude, E6 gauge dynamics, or a continuum unification mechanism.",
      "checks": {
        "parent_inner_25920": True,
        "D_is_old_B": True,
        "C_multiplier_minus_one": True,
        "explicit_26_step_inner_transporter": True,
        "outer_element_fixes_U": True,
        "outer_element_not_symplectic": True,
        "outer_stabilizer_128_times_51840": True,
        "full_outer_image_51840": True
      }
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
