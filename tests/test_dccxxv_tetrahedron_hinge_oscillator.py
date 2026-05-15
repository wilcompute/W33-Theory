"""Part DCCXXV -- Tetrahedron self-dual hinge tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxv_tetrahedron_hinge_oscillator import (  # noqa: E402
    CODEC,
    OUT_PATH,
    Q,
    QP1,
    TOMOTOPE,
    build_bridge,
    chirality_split_argument,
    csaszar_flag_data,
    flags_per_polygon,
    oscillator_phases,
    szilassi_flag_data,
    tetrahedron_flag_data,
    total_flags,
    write_bridge,
)


def test_flags_per_polygon():
    assert flags_per_polygon(3) == 6
    assert flags_per_polygon(6) == 12


def test_tetrahedron_has_24_flags():
    t = tetrahedron_flag_data()
    assert t["flags"] == 24
    assert t["aut_group_order"] == 24
    assert t["self_dual"] is True


def test_tetrahedron_24_equals_2_codec():
    t = tetrahedron_flag_data()
    assert t["flags"] == 2 * CODEC


def test_tetrahedron_12_plus_12_chirality():
    t = tetrahedron_flag_data()
    assert t["orientation_split"] == [12, 12]
    assert t["rotation_subgroup_order"] == CODEC == 12


def test_csaszar_84_flags():
    c = csaszar_flag_data()
    assert c["flags"] == 84
    assert c["V"] == 7
    assert c["E"] == 21
    assert c["F"] == 14
    assert c["realizations"] == 5
    assert c["genus"] == 1


def test_szilassi_84_flags():
    s = szilassi_flag_data()
    assert s["flags"] == 84
    assert s["V"] == 14
    assert s["E"] == 21
    assert s["F"] == 7
    assert s["realizations"] == 2
    assert s["genus"] == 1


def test_csaszar_szilassi_dual_swap():
    c = csaszar_flag_data()
    s = szilassi_flag_data()
    assert c["V"] == s["F"]
    assert c["F"] == s["V"]
    assert c["E"] == s["E"]


def test_seven_toroidal_realizations():
    c = csaszar_flag_data()
    s = szilassi_flag_data()
    assert c["realizations"] + s["realizations"] == 7


def test_flag_sum_equals_192():
    t = tetrahedron_flag_data()
    c = csaszar_flag_data()
    s = szilassi_flag_data()
    assert t["flags"] + c["flags"] + s["flags"] == 192


def test_192_equals_tomotope_flags():
    assert TOMOTOPE["flags"] == 192


def test_mode_sum_equals_8():
    osc = oscillator_phases()
    assert osc["totals"]["modes"] == 8


def test_8_equals_tomotope_cells():
    assert TOMOTOPE["C"] == 8


def test_tomotope_f_vector_sum_40():
    assert TOMOTOPE["f_vector_total"] == 40  # = W(3,3) vertex count


def test_tomotope_edges_equal_codec():
    assert TOMOTOPE["E"] == CODEC == 12


def test_tomotope_vertices_equal_q_plus_one():
    assert TOMOTOPE["V"] == QP1 == 4


def test_chirality_split_argument_count():
    c = chirality_split_argument()
    assert len(c) == 4


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_flag_accounting_matches_tomotope():
    b = build_bridge()
    fa = b["flag_accounting"]
    assert fa["match"] is True
    assert fa["h0_h1_total"] == 192
    assert fa["tomotope_flag_count"] == 192


def test_mode_accounting_matches_tomotope():
    b = build_bridge()
    ma = b["mode_accounting"]
    assert ma["match"] is True
    assert ma["h0_plus_h1"] == 8
    assert ma["tomotope_cells"] == 8


def test_abstract_polytope_bookends():
    b = build_bridge()
    book = b["abstract_polytope_bookends"]
    assert book["11_cell"]["cells"] == 11
    assert book["57_cell"]["cells"] == 57
    assert book["tomotope_in_between"]["cells"] == 8
    assert book["tomotope_in_between"]["f_vector"] == [4, 12, 16, 8]


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Self-Dual Hinge Theorem" in b["theorem"]
    assert "tomotope" in b["one_line"].lower()


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
        "tetrahedron",
        "csaszar",
        "szilassi",
        "tomotope",
        "oscillator_phases",
        "chirality_split",
        "flag_accounting",
        "mode_accounting",
        "abstract_polytope_bookends",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
