"""Regression for Pass 10968 (numbers established independently in scratch runs before the producer)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = json.loads((ROOT / "data" / "w33_pass10968_r_symmetry_parity_and_massless_exotics.json").read_text())
S = CERT["summary"]


def test_r_combinations_open_parity_in_three_models():
    assert S["A"] == {"models": 128, "parity_exists": 3, "closed_farkas": 2, "closed_rays": 0,
                      "with_realizable_fi_rays": 1}


def test_z6ii23_vacua():
    assert S["vacua"]["fi_rays"] == 360 and S["vacua"]["rays"] == 4242
    assert S["CD"]["supports"] == 38
    assert S["B"]["doublet_structure_ok"] == 38


def test_parity_is_a_genuine_symmetry():
    assert S["B"]["witness_noninvariant"] == 0 and S["B"]["witness_couplings_checked"] == 1524
    assert S["B"]["udd5_exact"] and S["B"]["udd5_mine"] == 144 and S["B"]["udd5_without_R"] == 672


def test_supersymmetric_but_exotics_massless():
    C = S["CD"]
    assert C["W_S_forbidden_all_orders"] == 38
    assert C["F_flat_to_K"] == 26
    assert C["d_bd_forbidden_all"] == 38 and C["u_bu_forbidden_all"] == 38 and C["e_be_forbidden_all"] == 38


def test_control_without_r_rules_allows_masses():
    ctrl = S["B"]["control_without_R"]
    assert ctrl["d.bd"] > 0 and ctrl["bl.l"] > 0


def test_z12_census():
    E = S["E"]
    assert sum(E.values()) == 289
    survivors = [n for n, r in CERT["z12_models"].items() if r.get("verdict", "").startswith("SURVIVES")]
    assert survivors == []
    dead = [n for n, r in CERT["z12_models"].items() if "support" in r]
    assert len(dead) == 14
