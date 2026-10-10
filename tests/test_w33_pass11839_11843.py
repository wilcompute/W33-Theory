"""Regression tests for Passes 11839-11843 (crosscap holography, free fields, couplings, massive spin, E8 commutant)."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11843_e8_tits_lorentz_commutant as T  # noqa: E402

DATA = ROOT / "data"


def test_crosscap_holography():
    c = json.load(open(DATA / "w33_pass11839_11842_crosscap_fields_couplings_spin.json"))["crosscap"]
    assert c["T_squared_equals_P"] and c["symmetric_on_Rac"] and c["antisymmetric_on_Di"] and c["no_Rac_Di_mixing"]
    assert c["rac_equivariance_max_error"] < 1e-10 and c["image_in_bulk_eigenvalue3_max_residual"] < 1e-10
    assert c["span_rank_rac"] == 15 and c["span_rank_di"] == 6
    assert c["bulk_two_point_by_relation"] == {"non-orthogonal:-1.0": 720, "orthogonal:1.0": 540, "same:5.0": 36}


def test_free_fields_and_couplings():
    c = json.load(open(DATA / "w33_pass11839_11842_crosscap_fields_couplings_spin.json"))
    sh = c["free_fields"]["spinor_helicity"]
    assert all(v == 20.0 for v in sh["dims"].values()) and all(v == 1.0 for v in sh["norms"].values())
    assert all(v == 0.0 for v in sh["cross"].values())
    nul = c["free_fields"]["shell_propagators"]["null"]
    assert nul["null"] != nul["split_type"] and nul["split_type"] == nul["kramers_type"]
    cub = c["couplings"]["nonzero_cubic_invariants"]
    assert cub["Rac | Rac | S15 (bulk&boundary)"] == 1.0
    assert not any(k.startswith("Rac | Rac | b20") for k in cub)
    assert cub["b20 (bulk, splits) | c20 (Rac Di*) | c20 (Rac Di*)"] == 1.0


def test_massive_spin_has_no_three_doublets():
    s = json.load(open(DATA / "w33_pass11839_11842_crosscap_fields_couplings_spin.json"))["massive_spin"]
    assert s["kramers_type"]["decomposition"]["Di"] == {"2_0": 2.0}
    assert s["split_type"]["decomposition"]["Di"] == {"2_1": 1.0, "2_2": 1.0}


def test_e8_cocycle_and_tits_commutant():
    rng = np.random.default_rng(1)
    T.SIGN = 1
    B = T.bracket_basis()
    assert T.jacobi(B, rng) < 1e-8
    c = json.load(open(DATA / "w33_pass11843_e8_tits_lorentz_commutant.json"))
    lo = c["commutants"]["lorentz_W(A5)'_even_tits_words"]
    assert (lo["dim"], lo["rank"], lo["centre_dim"], lo["derived_dim"]) == (11, 3, 0, 11)
    assert c["commutants"]["contains_su3_A2"] and c["commutants"]["contains_su2_alpha"]
    assert c["commutants"]["control_W(E6)'_even_words"]["dim"] == 8
