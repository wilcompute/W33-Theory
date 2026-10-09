"""Regression tests for Passes 11713-11716 (family E6 grade dictionary; heterotic two-qutrit level dictionary)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11713_family_e6_grade_dictionary as F  # noqa: E402
import w33_pass11714_11716_heterotic_two_qutrit_levels as P  # noqa: E402

DATA = ROOT / "data"


def test_family_su3_centraliser_is_e6_and_grades():
    m, Y, F5 = F.configuration()
    rest = [t for t in range(9) if t not in F5]
    d = F.family_dictionary(m, Y, F5, rest[-1])
    assert d["centraliser"] == ["E6"] and d["sm_in_centraliser"] and d["epsilon_family_structure"]
    assert all(v == 27 for v in d["roots_per_family"].values())
    for split in d["grade_split"].values():
        assert split == {"operator": 6, "three-fermion": 15, "three-hole": 6}


def test_z3_vacuum_branching_and_anomaly():
    b = F.z3_branching()
    assert b["net_tens_per_plane"] == 3 and b["net_tens_total"] == 9 and b["net_5bar"] == 9
    assert P.anomaly_wedge(9, 3) == 9 and P.anomaly_wedge(9, 1) == 1
    summary = (DATA / "w33_pass11714_z3_vacuum_orbifolder_summary.txt").read_text()
    assert "SU(9) and SO(14) and U(1)" in summary and "3 ( 84,  1)_l" in summary and "27 ( -9,  1)_l" in summary


def test_flagship_levels_and_hypercharge():
    data = json.load(open(DATA / "w33_pass11714_orbifolder_frozen_states.json"))
    flag = [m for m in data["models"] if m["label"] == "SM_20260917_3"][0]
    r = P.analyse_model(flag)
    assert r["sm_in_su9"] and abs(r["net_32"]) == 3 and r["net_32_untwisted"] == 3
    assert r["flavour_partition"]["disjoint_cover"] and r["two_plus_one_with_swap"]
    assert r["top_cubics"] > 0 and r["top_cubics"] == r["top_cubics_partitioning_nine_levels"]
    assert r["doublet_triplet_same_level_pair"]
    six_y = P.flagship_hypercharge()
    col, weak = set(r["colour_levels"]), set(r["weak_levels"])
    assert all(six_y[i] == 2 for i in col) and all(six_y[i] == -3 for i in weak)
    assert all(six_y[i] == 0 for i in range(9) if i not in col | weak)


def test_census_certificate():
    c = json.load(open(DATA / "w33_pass11714_11716_heterotic_two_qutrit_levels.json"))
    assert (c["models"], c["with_A8_half"], c["sm_in_su9"], c["all_three_doublets_untwisted"]) == (87, 47, 33, 33)
    for k in ("flavour_partition_holds", "two_plus_one_with_swap", "top_cubic_exists", "doublet_triplet_same_pair"):
        assert c[k] == 31, k
    assert c["every_top_cubic_partitions_levels"] == 33
