from __future__ import annotations

import json
from pathlib import Path
import sys

sys.set_int_max_str_digits(20000)

from analysis.w33_pass5436_5443_bicycle_apartment_scheme_packet import (
    allq_formula_certificate,
    bfs_basis_q3,
    q3_orbital_certificate,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_q3_orbital_refinement_and_center():
    out = q3_orbital_certificate()
    assert out["group_order"] == 25920
    assert out["stabilizer_order"] == 16
    assert out["orbital_rank"] == 131
    assert out["orbital_size_census"] == {"1": 2, "2": 3, "4": 17, "8": 25, "16": 84}
    assert out["symmetric_orbitals"] == 25
    assert out["directed_transpose_pairs"] == 53
    assert out["tensor_nonzero_entries"] == 159065
    assert out["tensor_sha256"] == "868ffd6ea89ab41b95557cdd97b4ffca6198771238a0bb0f8c006974c7885b19"
    assert out["orbital_algebra_center_dimension"] == 17
    assert out["burnside_sum"] == 2096

    bfs = bfs_basis_q3(out["geometry"])
    assert bfs["cotree_edges_apartment_basis"] == 81
    assert bfs["basis_rank"] == 81
    assert bfs["gram_determinant_factorization"] == "2^83*5^23"
    assert "x**2 - 17*x + 40" in bfs["gram_charpoly"]
    assert "x**2 - 8*x + 10" in bfs["gram_charpoly"]


def test_allq_basis_tanner_and_critical_formulas():
    out = allq_formula_certificate()
    q3 = out["anchors"]["3"]
    assert q3["cycle_rank"] == 81
    assert q3["minimum_apartment_basis_size"] == 81
    assert q3["all_apartments"] == 1620
    assert q3["R4_degree"] == 16
    assert q3["R4_adjacent_common_neighbors"] == 2
    assert q3["theta_triangles"] == 4320
    assert q3["root_tanner_triangles"] == 4320
    assert q3["R4_total_triangles"] == 8640
    assert int(q3["levi_spanning_tree_order"]) == 2**83 * 5**23


def test_cross_regressions_and_q3_filtration():
    summary = load("data/PART_W33_PASS5436_5443_BICYCLE_APARTMENT_SCHEME.json")
    p5420 = load("data/PART_W33_PASS5420_5427_APARTMENT_DUALITY_PACKET.json")
    p5066 = load("data/PART_W33_PASS5066_5073_RESULTS.json")
    p5031 = load("data/PART_W33_PASS5031_CRITICAL_GROUPS.json")
    p5079 = load("data/PART_W33_PASS5079_ALL_Q_TANNER_SIX_CYCLES.json")

    assert p5420["5426_footprint_bicycle_amalgam"]["q3"]["bicycle_dimension"] == 29
    assert p5066["5068"]["spaces"] == ["H1_81", "Bike29", "Bike29", "W23", "J", "J", "0"]
    assert p5066["5068"]["point_half"]["dimension"] == 15
    assert p5066["5068"]["line_half_chain"] == [1, 9, 15]
    assert summary["5436_q3_bicycle_filtration"]["dimensions"] == [0, 1, 15, 23, 29]
    assert summary["5436_q3_bicycle_filtration"]["successive_factor_dimensions"] == [1, 14, 8, 6]

    assert p5079["status"] == "THEOREM"
    assert p5079["anchors_from_repo"]["q3"] == 4320
    assert p5031["levi"]["tree_order"] == "2^83*5^23"
    assert summary["5441_bonkers_cycle_lattice_critical_determinant"]["q3"] == "tau=2^83*5^23"
