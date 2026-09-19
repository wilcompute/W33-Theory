from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "analysis" / "w33_qutrit_hamming_cross_incidence.py"
FROZEN = ROOT / "data" / "w33_qutrit_hamming_cross_incidence.json"

spec = importlib.util.spec_from_file_location("qutrit_hamming_cross_incidence", MOD)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_q3_cross_incidence_lock():
    B = mod.cross_matrix(3)
    assert int(B.det()) == 80 == 3**4 - 1
    snf = smith_normal_form(B, domain=ZZ)
    assert [int(snf[i, i]) for i in range(9)] == [1, 1, 1, 1, 1, 2, 2, 2, 10]

    rank, enum = mod.binary_weight_enumerator(B)
    assert rank == 5
    assert enum == {0: 1, 3: 6, 4: 9, 5: 9, 6: 6, 9: 1}


def test_all_q_determinant_controls_and_decoder():
    rows = [mod.control(q) for q in (2, 3, 4, 5)]
    assert [r["abs_det"] for r in rows] == [3, 80, 5103, 589824]
    assert [r["det_equals_q4_minus_1"] for r in rows] == [False, True, False, False]

    B3 = mod.cross_matrix(3)
    assert B3 * mod.inverse_formula(3) == mod.sp.eye(9)
    assert B3.inv() == mod.sp.Rational(1, 2) * mod.adjacency(3) - mod.sp.Rational(1, 5) * mod.sp.ones(9)


def test_native_characteristic_nilpotent_filtration():
    for q, expected in [(3, (4, 1, 0)), (5, (8, 1, 0)), (7, (12, 1, 0))]:
        B = mod.cross_matrix(q)
        N = B + mod.sp.eye(q * q)
        got = (mod.rank_mod(N, q), mod.rank_mod(N * N, q), mod.rank_mod(N * N * N, q))
        assert got == expected
        kernel = q * q - got[0]
        assert kernel == (q - 1) ** 2 + 1

    assert (3 - 1) ** 2 + 1 == 2 * 3 - 1
    assert (5 - 1) ** 2 + 1 != 2 * 5 - 1


def test_frozen_certificate_matches_build():
    out = mod.main(write=False)
    frozen = json.loads(FROZEN.read_text())
    assert out == frozen
