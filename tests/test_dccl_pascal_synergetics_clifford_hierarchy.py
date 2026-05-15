"""Part DCCL -- Pascal/Synergetics/Clifford hierarchy tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccl_pascal_synergetics_clifford_hierarchy import (  # noqa: E402
    OUT_PATH,
    Q,
    QP1,
    binomial_row,
    build_bridge,
    central_binomial,
    clifford_grades,
    e_from_binomial,
    hierarchy_w33_integer_match,
    phi_from_pascal_diagonals,
    pi_from_central_binomial,
    rhombic_dodecahedron_data,
    synergetics_hierarchy,
    trinomial_row_sum,
    write_bridge,
)


def test_pascal_row_q_is_1_3_3_1():
    assert binomial_row(Q) == [1, 3, 3, 1]


def test_pascal_row_qp1_is_1_4_6_4_1():
    assert binomial_row(QP1) == [1, 4, 6, 4, 1]


def test_cl3_total_dim_is_8():
    cl3 = clifford_grades(3)
    assert cl3["total_dim"] == 8
    assert cl3["grades"] == [1, 3, 3, 1]


def test_cl4_total_dim_is_16():
    cl4 = clifford_grades(4)
    assert cl4["total_dim"] == 16
    assert cl4["grades"] == [1, 4, 6, 4, 1]
    assert cl4["central_entry"] == 6 == math.factorial(Q)


def test_cl3_bivectors_is_q():
    cl3 = clifford_grades(3)
    assert cl3["bivector_grade"] == Q == 3


def test_cl4_bivectors_is_q_factorial():
    cl4 = clifford_grades(4)
    assert cl4["bivector_grade"] == math.factorial(Q) == 6


def test_central_binomial_at_q_is_20():
    assert central_binomial(Q) == 20


def test_trinomial_row_q_sums_to_27():
    assert trinomial_row_sum(Q) == Q ** Q == 27


def test_trinomial_row_qp1_sums_to_81():
    assert trinomial_row_sum(QP1) == Q ** QP1 == 81


def test_e_approximation():
    assert abs(e_from_binomial(10_000) - math.e) < 1e-3


def test_pi_approximation():
    assert abs(pi_from_central_binomial(1000) - math.pi) < 1e-2


def test_phi_approximation():
    phi_true = (1 + math.sqrt(5)) / 2
    assert abs(phi_from_pascal_diagonals(40) - phi_true) < 1e-6


def test_synergetics_hierarchy_has_W33_volumes():
    matches = hierarchy_w33_integer_match()
    volumes = [m["volume"] for m in matches]
    assert volumes == [1, 3, 4, 5, 6, 20]


def test_rhombic_dodecahedron_f_vector():
    rd = rhombic_dodecahedron_data()
    assert rd["V"] == 14
    assert rd["E"] == 24
    assert rd["F"] == 12
    assert rd["vol_synergetics"] == 6


def test_rhombic_dodecahedron_vertex_split():
    rd = rhombic_dodecahedron_data()
    split = rd["vertex_split"]
    assert split["tetrahedral_voids"] == 8
    assert split["octahedral_voids"] == 6
    assert split["total"] == 14


def test_rd_E_matches_tetrahedron_flags():
    rd = rhombic_dodecahedron_data()
    assert rd["E"] == 24    # = tetrahedron flag count


def test_rd_F_matches_codec():
    rd = rhombic_dodecahedron_data()
    assert rd["F"] == 12    # = codec


def test_rd_volume_matches_q_factorial():
    rd = rhombic_dodecahedron_data()
    assert rd["vol_synergetics"] == math.factorial(Q) == 6


def test_synergetics_hierarchy_size():
    h = synergetics_hierarchy()
    assert len(h) >= 10


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Pascal-Synergetics-Clifford Theorem" in b["theorem"]
    assert "Pascal" in b["one_line"]


def test_pascal_row_q_sum_equals_2_to_q():
    assert sum(binomial_row(Q)) == 2 ** Q == 8


def test_pascal_row_qp1_sum_equals_2_to_qp1():
    assert sum(binomial_row(QP1)) == 2 ** QP1 == 16


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "pascal_triangle_rows",
        "pascal_tetrahedron_rows",
        "central_binomial",
        "clifford_grades",
        "synergetics_hierarchy",
        "synergetics_integer_volumes_W33_matches",
        "three_natural_constants",
        "rhombic_dodecahedron_as_hub",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
