from __future__ import annotations

import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

FILES = {
    "twisted": DATA / "PART_BT3250_BT3251_TWISTED_PORT_LOCAL_SYSTEMS.json",
    "verifier": DATA / "PART_BT3252_BT3253_INDEPENDENT_CURVATURE_VERIFIER.json",
    "runtime": DATA / "PART_BT3254_BT3255_TYPED_RUNTIME_UNIVERSES.json",
    "reset": DATA / "PART_BT3256_BT3257_CONSTRAINED_RESET_SEMIGROUP.json",
    "closure": DATA / "PART_BT3250_BT3261_TWISTED_ROM_RUNTIME_RESET_CLOSURE.json",
}


@lru_cache(maxsize=1)
def results() -> dict[str, dict]:
    scripts = [
        "bt3250_3251_twisted_port_local_systems.py",
        "bt3252_3253_independent_curvature_verifier.py",
        "bt3254_3255_typed_runtime_universes.py",
        "bt3256_3257_constrained_reset_semigroup.py",
        "bt3250_3261_twisted_rom_runtime_reset_closure.py",
    ]
    if not all(path.exists() for path in FILES.values()):
        for script in scripts:
            subprocess.run([sys.executable, str(ROOT / "analysis" / script)], cwd=ROOT, check=True)
    return {name: json.loads(path.read_text(encoding="utf-8")) for name, path in FILES.items()}


def test_twisted_local_system_dimension_law() -> None:
    data = results()["twisted"]
    assert data["collapsed_complex"] == {
        "vertices": 45,
        "edges": 480,
        "free_rank": 436,
        "elementary_face_edge_pairs_removed": 240,
        "collapse_manifest_sha256": data["collapsed_complex"]["collapse_manifest_sha256"],
    }
    rows = {row["name"]: row for row in data["local_systems"]}
    assert rows["constant_F3_rank1"]["twisted_H1_dimension"] == 436
    assert rows["sign_F3_rank1"]["twisted_H1_dimension"] == 435
    assert rows["unipotent_F3_rank2"]["twisted_H1_dimension"] == 871
    assert rows["D4_standard_F3_rank2"]["twisted_H1_dimension"] == 870
    assert rows["S3_standard_F5_rank2"]["twisted_H1_dimension"] == 870
    for row in rows.values():
        assert row["same_rank_constant_H1_dimension"] - row["twisted_H1_dimension"] == row["fiber_rank"] - row["twisted_H0_dimension"]


def test_independent_quotient_and_mutation_controls() -> None:
    data = results()["verifier"]
    assert data["status"] == "PASS_INDEPENDENT_876_STATE_VERIFICATION"
    assert data["counts"]["hypotheses"] == 48_826
    assert data["counts"]["raw_reachable_subsets"] == 5_620
    assert data["counts"]["unique_initial_states"] == 770
    assert data["counts"]["all_recursive_states"] == 876
    assert data["counts"]["terminal_states"] == 3
    assert data["semantic_sha256"] == data["expected_pass3216_semantic_sha256"]
    assert data["numbering_permutation_control"]["accepted"] is True
    assert data["action_mutation_control"]["accepted"] is False
    assert data["cycle_mutation_control"]["accepted"] is False


def test_typed_runtime_universes_are_fail_closed() -> None:
    data = results()["runtime"]
    universes = data["universes"]
    assert universes["affine_universal_4op_v1"]["member_count"] == 24
    assert universes["affine_universal_5_6op_v1"]["member_count"] == 194
    assert universes["affine_universal_5_6op_v1"]["member_count_by_opcode_count"] == {"5": 80, "6": 114}
    assert data["admissions"]["current4"]["comparison_only"] is True
    assert data["admissions"]["low4"]["comparison_only"] is True
    assert data["admissions"]["fast6"]["census_member"] is True
    migration = data["pass3195_migration"]
    assert migration["typed_census_joined"] == ["fast6"]
    assert migration["typed_out_of_census_baselines"] == ["current4", "low4"]
    assert migration["pending_194_census_records"] == 193
    assert migration["global_194_runtime_optimum_allowed"] is False
    assert all(not row["accepted"] for row in data["negative_controls"].values())
    assert data["missing_projection_rejected"] is True


def test_passive_rank_floor_and_shortest_authorized_reset() -> None:
    data = results()["reset"]
    passive = data["passive_result"]
    assert passive["minimum_rank"] == 3
    assert passive["constructive_word_length"] == 20
    assert passive["rank_history"] == [876, 722, 638, 561, 491, 421, 351, 281, 218, 176, 120, 85, 50, 36, 29, 22, 15, 11, 7, 5, 3]
    authorized = data["authorized_reset"]
    assert authorized["extended_states"] == 1_752
    assert authorized["minimum_passive_rank_on_extended_space"] >= 6
    assert authorized["valid_authorization_rank"] == 876
    assert authorized["reset_without_prior_authorization_rank"] == 876
    assert authorized["authorize_then_reset_rank"] == 1
    assert authorized["shortest_rank_one_word_length"] == 2


def test_coordinator_preserves_all_claim_boundaries() -> None:
    data = results()["closure"]
    assert data["status"] == "PASS_EXACT_FIVE_FRONT_CLOSURE_SOURCE_EVIDENCE_PENDING"
    assert all(data["checks"].values())
    assert "pending" in data["evidence_boundary"]
    assert "No laboratory" in data["evidence_boundary"]["physical"]
