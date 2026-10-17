from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, output: str) -> dict:
    subprocess.run([sys.executable, str(ROOT / "analysis" / script)], cwd=ROOT, check=True)
    return json.loads((ROOT / "data" / output).read_text(encoding="utf-8"))


def test_month_claim_genealogy_and_evidence_debt() -> None:
    genealogy = run("bt3193_month_claim_genealogy.py", "PART_BT3193_MONTH_CLAIM_GENEALOGY_results.json")
    debt = run("bt3200_repository_evidence_debt.py", "PART_BT3200_REPOSITORY_EVIDENCE_DEBT_results.json")
    assert genealogy["claim_families"] == 12
    assert debt["open_pull_count_in_audit"] == 21
    assert debt["active_stack"] == [242, 243, 244]
    assert debt["merge_authority"] == "none: this artifact schedules evidence work but never converts queued, failed or source-complete states into merge permission"


def test_curvature_causal_quotient() -> None:
    result = run("bt3194_curvature_causal_quotient.py", "PART_BT3194_CURVATURE_CAUSAL_QUOTIENT_results.json")
    assert result["untyped_quotient"]["all_recursive_states"] == 470
    assert result["curvature_aware_quotient"]["all_recursive_states"] == 876
    assert result["additional_fixed_bits"] == 1
    assert result["curvature_partition"] == {"curved": 1656, "flat": 1725, "none": 45445}


def test_runtime_information_fusion_is_fail_closed() -> None:
    result = run("bt3195_runtime_information_fusion.py", "PART_BT3195_RUNTIME_INFORMATION_FUSION_results.json")
    assert result["information_records"] == 194
    assert result["status"] in {
        "PARTIAL_RUNTIME_1_OF_194_PLUS_2_BASELINES",
        "COMPLETE_RUNTIME_194_OF_194",
    }
    if result["status"] == "PARTIAL_RUNTIME_1_OF_194_PLUS_2_BASELINES":
        assert result["runtime_records_total"] == 3
        assert result["joined_records"] == 1
        assert result["out_of_census_baseline_count"] == 2
        assert result["pending_runtime_records"] == 193
        assert {row["runtime"]["name"] for row in result["out_of_census_baselines"]} == {
            "current4",
            "low4",
        }
        assert result["joined_records_detail"][0]["runtime"]["name"] == "fast6"
    else:
        assert result["runtime_records_total"] == result["joined_records"] == 194
        assert result["out_of_census_baseline_count"] == 0
        assert result["pending_runtime_records"] == 0


def test_four_edit_epoch_and_proof_authorization() -> None:
    epoch = run("bt3196_four_edit_phase_epoch.py", "PART_BT3196_FOUR_EDIT_PHASE_EPOCH_results.json")
    envelope = run("bt3197_proof_envelope_authorization.py", "PART_BT3197_PROOF_ENVELOPE_AUTHORIZATION_results.json")
    assert epoch["marker_length"] == 9
    assert epoch["radius_four_ball_size_per_phase"] == 536_484_991
    assert epoch["total_distinct_phase_labelled_traces"] == 6_437_819_892
    assert envelope["positive_control"]["authorized"] is True
    assert envelope["digest_tamper_control"]["authorized"] is False
    assert envelope["missing_witness_control"]["authorized"] is False
    assert envelope["rejected_candidate_control"]["authorized"] is False


def test_concurrent_virtualization_and_bridge_falsifier() -> None:
    virtualization = run("bt3198_concurrent_belief_virtualization.py", "PART_BT3198_CONCURRENT_BELIEF_VIRTUALIZATION_results.json")
    bridge = run("bt3199_chromatic_curvature_bridge_falsifier.py", "PART_BT3199_CHROMATIC_CURVATURE_BRIDGE_results.json")
    rows = {row["concurrent_paths"]: row for row in virtualization["rows"]}
    assert rows[64]["minimum_live_contexts"] == 70
    assert rows[64]["minimum_live_bits"] == 3640
    assert rows[1024]["maximum_live_contexts"] == 5160
    assert bridge["route_edge_action"]["degree_32_orbital_unions"] == 3
    assert bridge["equivariant_bridge_exists_for_natural_relations"] is False
    assert all(not row["chromatic_polynomial_identity"] for row in bridge["degree_32_candidates"])
