"""GAP-backed regression tests for Passes 7313--7316.

Python only launches GAP, checks frozen source hashes, and parses the resulting
deterministic certificate.  GAP owns every finite-field and group computation.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass7313_7316_pauli_trace_and_stabilizer_scope.g"
CERTIFICATE = ROOT / "data" / "PART_W33_PASS7313_7316_PAULI_TRACE_STABILIZER_SCOPE.json"
GAP = shutil.which("gap")
pytestmark = pytest.mark.skipif(GAP is None, reason="GAP is required for Passes 7313--7316")


@lru_cache(maxsize=1)
def _certificate() -> dict:
    """Run GAP once and require byte-identical certificate regeneration."""

    assert GAP is not None, "GAP is required for the Passes 7313--7316 certificate"
    before = CERTIFICATE.read_bytes()
    result = subprocess.run(
        [GAP, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert "Passes 7313--7316: PASS (65/65)" in result.stdout
    assert "q=5: Sp/SL(2,3) order 24 -> PSp/A4 order 12" in result.stdout
    assert "q=9 trace firewall: 51 K4 blocks, every crossbar 4K2" in result.stdout
    after = CERTIFICATE.read_bytes()
    assert after == before, "the GAP certificate must be byte-deterministic"
    return json.loads(after)


def test_gap_certificate_is_exact_deterministic_and_source_frozen() -> None:
    cert = _certificate()
    assert cert["schema"] == "w33.pass7313_7316.pauli_trace_stabilizer_scope.v1"
    assert cert["status"] == "PASS"
    assert cert["gap"] == {"version": "4.12.1", "check_count": 65}
    assert cert["all_checks_pass"] is True

    for source in cert["source_certificates"]:
        payload = (ROOT / source["path"]).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == source["sha256"]
        parsed = json.loads(payload)
        assert len(parsed["points"]) == source["size"]


def test_typed_sp_psp_pcsp_stabilizers_are_not_conflated() -> None:
    assert _certificate()["typed_stabilizers"] == [
        {
            "q": 3,
            "sp_order": 51_840,
            "psp_order": 25_920,
            "pcsp_order": 51_840,
            "linear_sp_stabilizer_order": 18,
            "projective_psp_stabilizer_order": 9,
            "projective_pcsp_stabilizer_order": 18,
        },
        {
            "q": 5,
            "sp_order": 9_360_000,
            "psp_order": 4_680_000,
            "pcsp_order": 9_360_000,
            "linear_sp_stabilizer_order": 24,
            "projective_psp_stabilizer_order": 12,
            "projective_pcsp_stabilizer_order": 12,
        },
        {
            "q": 7,
            "sp_order": 276_595_200,
            "psp_order": 138_297_600,
            "pcsp_order": 276_595_200,
            "linear_sp_stabilizer_order": 2,
            "projective_psp_stabilizer_order": 1,
            "projective_pcsp_stabilizer_order": 2,
        },
        {
            "q": 9,
            "sp_order": 3_443_212_800,
            "psp_order": 1_721_606_400,
            "pcsp_order": 3_443_212_800,
            "linear_sp_stabilizer_order": 4,
            "projective_psp_stabilizer_order": 2,
            "projective_pcsp_stabilizer_order": 2,
        },
    ]


def test_q5_frozen_set_has_binary_tetrahedral_and_tetrahedral_stabilizers() -> None:
    q5 = _certificate()["q5_exact_stabilizer"]
    assert q5["linear_sp"] == {
        "order": 24,
        "id_group": [24, 3],
        "structure": "SL(2,3)",
    }
    assert q5["projective_psp"] == {
        "order": 12,
        "id_group": [12, 3],
        "structure": "A4",
    }
    assert q5["projective_pcsp"] == {
        "order": 12,
        "id_group": [12, 3],
        "structure": "A4",
    }
    assert q5["psp_orbit_size"] == 390_000
    assert q5["selected_point_orbit_sizes"] == [6, 4, 4, 4]
    assert q5["selected_action_kernel_order"] == 1
    assert "not an alpha upper bound" in q5["scope"]


def test_q7_q9_involutions_have_exact_square_class_scope() -> None:
    involutions = {
        entry["q"]: entry for entry in _certificate()["antisymplectic_involutions"]
    }

    q7 = involutions[7]
    assert q7["squares_to_identity"] is True
    assert q7["multiplier_minus_one"] is True
    assert [q7["plus_eigenspace_dimension"], q7["minus_eigenspace_dimension"]] == [2, 2]
    assert [q7["fixed_ambient_points"], q7["fixed_selected_points"]] == [16, 1]
    assert q7["minus_one_is_square"] is False
    assert q7["projectivity_is_in_psp"] is False

    q9 = involutions[9]
    assert q9["squares_to_identity"] is True
    assert q9["multiplier_minus_one"] is True
    assert [q9["plus_eigenspace_dimension"], q9["minus_eigenspace_dimension"]] == [2, 2]
    assert [q9["fixed_ambient_points"], q9["fixed_selected_points"]] == [20, 1]
    assert q9["minus_one_is_square"] is True
    assert q9["projectivity_is_in_psp"] is True


def test_q9_absolute_trace_field_reduction_is_the_51_block_switch() -> None:
    q9 = _certificate()["q9_trace_field_reduction"]
    assert q9["ambient_f9_projective_points"] == 820
    assert q9["ambient_spread_blocks"] == 820
    assert q9["f3_projective_points_per_block"] == 4
    assert q9["ambient_f3_projective_points"] == 3_280
    assert q9["selected_f9_points"] == 51
    assert q9["selected_spread_blocks"] == 51
    assert q9["selected_f3_projective_points"] == 204
    assert q9["within_block_graph"] == "K4"
    assert q9["within_block_edges"] == 6
    assert q9["between_each_block_pair_graph"] == "4K2 perfect matching"
    assert q9["between_each_block_pair_edges"] == 4
    assert q9["commuting_graph_degree"] == 53
    assert q9["commuting_graph_edges"] == 5_406
    assert q9["degree_identity"] == "53=3+50"
    assert q9["edge_identity"] == "5406=51*C(4,2)+C(51,2)*4"
    assert q9["stored_representative_pair_count"] == 1_275
    assert q9["stored_representative_f9_orthogonal_pairs"] == 0
    assert q9["stored_representative_absolute_trace_distribution"] == {
        "0": 283,
        "1": 496,
        "-1": 496,
    }
    assert "depends on representative gauge" in q9["gauge_warning"]


def test_certificate_enforces_finite_and_physics_boundaries() -> None:
    boundaries = _certificate()["boundaries"]
    assert "Exact finite-field" in boundaries["finite_geometry"]
    assert "standard Galois-Pauli commutator uses Tr_GF(q)/GF(p)(B)" in boundaries["pauli"]
    assert "not 51 pairwise-noncommuting physical Pauli classes" in boundaries["q9"]
    assert "PCSp need not be Clifford" in boundaries["clifford"]
    assert "alpha(W(3,9)) is not determined" in boundaries["alpha"]
    assert "No continuum dynamics" in boundaries["physics"]
