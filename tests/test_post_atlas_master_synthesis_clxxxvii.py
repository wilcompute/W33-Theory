"""
Regression tests for Part CLXXXVII — Post-Atlas Master Synthesis Compiler.
"""
import json
from pathlib import Path

import pytest

from PART_CLXXXVII_POST_ATLAS_MASTER_SYNTHESIS import (
    post_atlas_master_synthesis_audit,
    strengthened_checks,
    weld_register,
    # W33 atoms
    Q, Q2, Q3, Q4, V, K, LAM, MU, F, E,
    PHI3, PHI4, PHI6, PHI12, J, J_INV,
    # Bridge invariants
    DIRECTED_ARC_COUNT, HASHIMOTO_BRANCH, EMPIRE_PACKET,
    AFFINE_TRIADS, DELETED_FIBERS, CUBIC_TRIADS_183, ORIENTED_ROOTS_183,
    FANO_POINTS, CAYLEY_CARRIER, ALBERT_DIM_184,
    QUOTIENT_LINES, QUOTIENT_INCIDENCES, CUBIC_TRIADS_185,
    TAU, J_CONSTANT, LEECH_KISSING, MONSTER_CHI1, J_COEFF_1, V_SUZ,
    RUNG_0, RUNG_1, RUNG_2, RUNG_3, RUNG_4, RUNG_5,
)


# ---------------------------------------------------------------------------
# Fixture — full audit result (computed once per test session)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def audit():
    return post_atlas_master_synthesis_audit()


# ---------------------------------------------------------------------------
# 1. Audit passes without exceptions and returns expected top-level keys
# ---------------------------------------------------------------------------

def test_audit_runs(audit):
    assert audit is not None


def test_audit_has_required_keys(audit):
    for key in (
        "module", "source_span", "bridge_pass_flags",
        "weld_count", "strengthened_check_count",
        "w33_atoms", "master_ladder_rungs",
        "bridge_weld_table", "strengthened_checks",
        "theorem_statement",
    ):
        assert key in audit, f"Missing key: {key}"


def test_module_name(audit):
    assert audit["module"] == "PART_CLXXXVII_POST_ATLAS_MASTER_SYNTHESIS"


def test_source_span(audit):
    assert "CLXXX" in audit["source_span"]
    assert "CLXXXVI" in audit["source_span"]


# ---------------------------------------------------------------------------
# 2. All six bridge audits pass
# ---------------------------------------------------------------------------

def test_all_bridge_flags_true(audit):
    flags = audit["bridge_pass_flags"]
    failures = [k for k, v in flags.items() if not v]
    assert failures == [], f"Bridge audit failures: {failures}"


def test_six_bridges_present(audit):
    flags = audit["bridge_pass_flags"]
    assert len(flags) == 6


# ---------------------------------------------------------------------------
# 3. Weld register size and consistency
# ---------------------------------------------------------------------------

def test_weld_count(audit):
    assert audit["weld_count"] == 23


def test_weld_register_all_equal(audit):
    table = audit["bridge_weld_table"]
    for entry in table:
        assert entry["lhs"] == entry["rhs"], (
            f"Weld '{entry['identity'][:50]}': lhs={entry['lhs']} != rhs={entry['rhs']}"
        )


def test_all_five_bridges_in_weld_table(audit):
    table = audit["bridge_weld_table"]
    bridges_present = {e["bridge"] for e in table}
    for expected in ("CLXXXII", "CLXXXIII", "CLXXXIV", "CLXXXV", "CLXXXVI"):
        assert expected in bridges_present


# ---------------------------------------------------------------------------
# 4. Strengthened checks
# ---------------------------------------------------------------------------

def test_strengthened_check_count(audit):
    assert audit["strengthened_check_count"] == 26


def test_all_strengthened_checks_pass(audit):
    failures = [c["name"] for c in audit["strengthened_checks"] if not c["value"]]
    assert failures == [], f"Strengthened check failures: {failures}"


# ---------------------------------------------------------------------------
# 5. Master ladder rung values
# ---------------------------------------------------------------------------

def test_rung_phi6(audit):
    assert audit["master_ladder_rungs"]["rung_0_Phi6"] == 7


def test_rung_j_inv(audit):
    assert audit["master_ladder_rungs"]["rung_1_J_inv"] == 8


def test_rung_q3(audit):
    assert audit["master_ladder_rungs"]["rung_2_q3"] == 27


def test_rung_q4(audit):
    assert audit["master_ladder_rungs"]["rung_3_q4"] == 81


def test_rung_e6(audit):
    assert audit["master_ladder_rungs"]["rung_4_E6"] == 78


def test_rung_e8(audit):
    assert audit["master_ladder_rungs"]["rung_5_E8"] == 248


# ---------------------------------------------------------------------------
# 6. Key CLXXXII weld identities
# ---------------------------------------------------------------------------

def test_clxxxii_directed_arc_count():
    assert DIRECTED_ARC_COUNT == V * K == 480


def test_clxxxii_empire_packet_is_j_inv():
    assert EMPIRE_PACKET == J_INV == 8


def test_clxxxii_hashimoto_branch():
    assert HASHIMOTO_BRANCH == K - 1 == 11


# ---------------------------------------------------------------------------
# 7. Key CLXXXIII weld identities
# ---------------------------------------------------------------------------

def test_clxxxiii_deleted_fibers_is_q2():
    assert DELETED_FIBERS == Q2 == 9


def test_clxxxiii_cubic_triads():
    assert CUBIC_TRIADS_183 == AFFINE_TRIADS + DELETED_FIBERS == 45


def test_clxxxiii_h1_weld():
    assert ORIENTED_ROOTS_183 + Q2 == Q4 == 81


def test_clxxxiii_e6_weld():
    assert ORIENTED_ROOTS_183 + 2 * Q == 78


# ---------------------------------------------------------------------------
# 8. Key CLXXXIV weld identities
# ---------------------------------------------------------------------------

def test_clxxxiv_fano_is_phi6():
    assert FANO_POINTS == PHI6 == 7


def test_clxxxiv_cayley_carrier():
    assert CAYLEY_CARRIER == PHI6 + 1 == J_INV == 8


def test_clxxxiv_albert_dim():
    assert ALBERT_DIM_184 == 3 + 3 * J_INV == Q3 == 27


# ---------------------------------------------------------------------------
# 9. Key CLXXXV weld identities
# ---------------------------------------------------------------------------

def test_clxxxv_quotient_lines_is_q3():
    assert QUOTIENT_LINES == Q3 == 27


def test_clxxxv_cubic_triads():
    assert CUBIC_TRIADS_185 == K * Q + Q2 == 45


def test_clxxxv_cross_bridge_45():
    """CLXXXIII and CLXXXV both yield 45 cubic triads — same atom."""
    assert CUBIC_TRIADS_183 == CUBIC_TRIADS_185 == 45


# ---------------------------------------------------------------------------
# 10. Key CLXXXVI weld identities
# ---------------------------------------------------------------------------

def test_clxxxvi_tau():
    assert TAU == K * Q * PHI6 == 252


def test_clxxxvi_j_constant():
    assert J_CONSTANT == Q * E + F == 744


def test_clxxxvi_leech_kissing():
    assert LEECH_KISSING == TAU * (V * (V - 1) // 2) == 196560


def test_clxxxvi_monster_chi1():
    assert MONSTER_CHI1 == (V + PHI6) * (V + K + PHI6) * (PHI12 - LAM) == 196883


def test_clxxxvi_j_coeff():
    assert J_COEFF_1 == LEECH_KISSING + 4 * Q4 == 196884


def test_clxxxvi_suzuki_vertex():
    assert V_SUZ == PHI6 * TAU + LAM * Q2 == 1782


# ---------------------------------------------------------------------------
# 11. JSON output file exists and is valid
# ---------------------------------------------------------------------------

def test_results_json_exists():
    p = Path(__file__).resolve().parent.parent / "PART_CLXXXVII_post_atlas_master_synthesis_results.json"
    assert p.exists(), f"Results JSON not found at {p}"


def test_results_json_valid():
    p = Path(__file__).resolve().parent.parent / "PART_CLXXXVII_post_atlas_master_synthesis_results.json"
    if not p.exists():
        pytest.skip("Results JSON not yet generated")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["module"] == "PART_CLXXXVII_POST_ATLAS_MASTER_SYNTHESIS"
    assert data["weld_count"] == 23
    assert data["strengthened_check_count"] == 26
