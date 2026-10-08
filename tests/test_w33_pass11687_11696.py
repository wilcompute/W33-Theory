"""Regression for Passes 11687-11692 (Claude track): the two-qutrit E8 dictionary and tick symmetries."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))


def load(name):
    return json.load(open(ROOT / "data" / name))


def test_11687_centralisers_and_triality():
    d = load("w33_pass11687_11691_two_qutrit_e8_dictionary.json")["11687"]
    assert d["point (Z on qutrit 1)"]["components"] == [72, 6] and d["point (Z on qutrit 1)"]["dim"] == 86
    assert d["hyperplane p^perp"]["components"] == [6]
    assert d["Lagrangian line <Z1,Z2>"]["components"] == [6, 6, 6, 6]
    assert d["qutrit-1 Paulis (tensor factor)"]["components"] == [24]
    t = d["triality"]
    assert t["coset_sizes"] == [64, 64, 64] and t["mixed_charges_with_three_distinct_cosets"] == 64
    assert t["omega_cycles_three_cosets"]


def test_11688_magic_gate():
    d = load("w33_pass11687_11691_two_qutrit_e8_dictionary.json")["11688"]
    assert d["T(x)I"]["fixed_dim"] == 82 and d["T(x)I"]["root_components"] == [72, 2]
    assert d["T(x)I"]["eigenphase_multiplicities_units_2pi_over_9"] == {"0": 82, "1": 54, "2": 27, "3": 2, "6": 2, "7": 27, "8": 54}
    assert d["Z(x)I"]["fixed_dim"] == 86 and d["Z(x)I"]["root_components"] == [72, 6]


def test_11689_chirality_character():
    d = load("w33_pass11687_11691_two_qutrit_e8_dictionary.json")["11689"]
    assert d["character_is_eps_times_tau"]


def test_11690_intertwiner():
    d = load("w33_pass11687_11691_two_qutrit_e8_dictionary.json")["11690"]
    assert d["odd_ranks"] == [1] and d["codex_ray_overlaps"] == [0.0, 0.333333]
    assert d["intertwiner_solution_space_dims"] == {"antilinear": [1], "linear": []}
    assert d["intertwiner_unitary"] and d["codex_rays_onto_root_rays"] == 40 and d["label_map_is_xz_swap"] == 40


def test_11691_unique_dimension():
    d = load("w33_pass11687_11691_two_qutrit_e8_dictionary.json")["11691"]
    assert d["closing_dimensions"] == [9]


def test_11692_tick_symmetry():
    d = load("w33_pass11692_tick_symmetry_in_e8.json")
    assert sorted(d["calibration_T_on_qutrit_1"]) == ["A1", "E6"] and sorted(d["calibration_Z_on_qutrit_1"]) == ["A2", "E6"]
    assert all(x["standard_model_shaped_count"] == 0 for x in d["clifford_only"])
    assert all(x["standard_model_shaped_count"] > 0 for x in d["with_T"])


def test_11692_live_unbroken_type():
    import w33_pass11692_tick_symmetry_in_e8 as S
    z9 = np.exp(2j * np.pi / 9)
    assert sorted(S.unbroken_type(np.kron(np.array([1, z9, z9 ** -1]), np.ones(3)))) == ["A1", "E6"]
    assert S.unbroken_type(np.ones(9)) == ("E8",)
