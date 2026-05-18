from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmlxxxiii_bass_cnub_entropy_branch_selector import (  # noqa: E402
    DATA_PATH,
    RESULT_PATH,
    build_selector,
    write_selector,
)


def test_metadata_and_prior_audit_dependency_are_pinned() -> None:
    payload = build_selector()
    summary = payload["summary"]
    prior = payload["previous_audit_summary"]
    ids = payload["identities"]

    assert summary["part"] == "DCMLXXXIII"
    assert summary["decimal"] == 983
    assert summary["depends_on_part"] == "DCMLXXXII"
    assert summary["depends_on_decimal"] == 982
    assert prior["part"] == "DCMLXXXII"
    assert prior["decimal"] == 982
    assert prior["live_bass_parameter"] == 11
    assert prior["shadow_coefficient"] == 12
    assert ids["part_number_is_983"] is True
    assert ids["depends_on_dcmlxxxii"] is True


def test_standard_entropy_packet_is_exact_four_over_eleven() -> None:
    payload = build_selector()
    entropy = payload["standard_entropy_packet"]
    ids = payload["identities"]

    assert entropy["photon_entropy_degrees"]["text"] == "2/1"
    assert entropy["electron_positron_entropy_degrees"]["text"] == "7/2"
    assert entropy["em_entropy_degrees_before_annihilation"]["text"] == "11/2"
    assert entropy["em_entropy_degrees_after_annihilation"]["text"] == "2/1"
    assert entropy["photon_heating_cubed"]["text"] == "11/4"
    assert entropy["cnub_temperature_cubed"]["text"] == "4/11"
    assert ids["standard_entropy_ratio_is_4_over_11"] is True
    assert ids["standard_photon_heating_is_11_over_4"] is True


def test_live_bass_11_branch_matches_standard_cnub_ratio() -> None:
    payload = build_selector()
    live = payload["live_bass_11_branch"]
    comparison = payload["branch_comparison"]
    ids = payload["identities"]

    assert live["name"] == "live_bass_11"
    assert live["mu"] == 4
    assert live["denominator"] == 11
    assert live["temperature_cube_ratio"]["text"] == "4/11"
    assert live["photon_heating_cubed"]["text"] == "11/4"
    assert comparison["bass_decrement"] == {
        "graph_degree": 12,
        "live_nonbacktracking_denominator": 11,
        "removed_return_channels": 1,
        "reading": (
            "The 12-regular graph has one forbidden immediate-return edge after "
            "the first step, so the live nonbacktracking denominator is 11."
        ),
    }
    assert ids["live_branch_matches_standard_ratio"] is True
    assert ids["bass_decrement_removes_one_return_channel"] is True


def test_coefficient_12_shadow_is_wrong_entropy_denominator() -> None:
    payload = build_selector()
    shadow = payload["coefficient_12_shadow_branch"]
    comparison = payload["branch_comparison"]
    ids = payload["identities"]

    assert shadow["name"] == "coefficient_12_shadow"
    assert shadow["denominator"] == 12
    assert shadow["temperature_cube_ratio"]["text"] == "1/3"
    assert shadow["photon_heating_cubed"]["text"] == "3/1"
    assert comparison["temperature_cube_gap_live_minus_shadow"]["text"] == "1/33"
    assert comparison["photon_heating_gap_shadow_minus_standard"]["text"] == "1/4"
    assert comparison["shadow_relative_to_live"]["text"] == "11/12"
    assert ids["shadow_branch_is_one_third"] is True
    assert ids["shadow_branch_is_not_standard_ratio"] is True
    assert ids["live_minus_shadow_gap_is_one_over_33"] is True
    assert ids["shadow_heating_misses_standard_by_one_fourth"] is True


def test_source_anchors_and_static_external_references_are_present() -> None:
    payload = build_selector()
    anchors = payload["source_anchor_checks"]
    sources = payload["static_external_sources"]
    ids = payload["identities"]

    assert anchors == {
        "w33_paper_contains_cnub_ratio": True,
        "dcmlxxxii_contains_live_bass_11": True,
        "dcmlxxxii_keeps_classical_rh_open": True,
    }
    assert {source["label"] for source in sources} == {
        "PDG 2025 Neutrinos in Cosmology",
        "Rangarajan 2017 Ihara-Bass proof for regular graphs",
    }
    assert all(source["runtime_dependency"] is False for source in sources)
    assert ids["source_anchors_are_present"] is True
    assert ids["external_sources_are_static"] is True


def test_honesty_boundary_remains_narrow() -> None:
    payload = build_selector()
    boundary = payload["honesty_boundary"]
    ids = payload["identities"]

    assert boundary["verified_statement"] == "exact branch-selector arithmetic"
    assert boundary["not_claimed"] == [
        "direct CnuB detection",
        "full neutrino decoupling dynamics from W33 alone",
        "classical Riemann Hypothesis",
    ]
    assert "entropy-decoupling handoff" in boundary["next_proof_target"]
    assert payload["summary"]["classical_rh_status"] == "OPEN"
    assert ids["classical_rh_boundary_remains_open"] is True


def test_write_and_reload() -> None:
    data_path, result_path = write_selector()
    assert data_path == DATA_PATH
    assert result_path == RESULT_PATH

    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert result["decimal"] == 983
    assert result["status"].startswith("VERIFIED")


def test_public_index_exposes_bass_cnub_selector() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    compact = " ".join(index.split())

    assert "Bass/CnuB Entropy Branch Selector" in index
    assert "live Bass-11 branch gives" in compact
    assert "<code>4/11</code>" in compact
    assert "coefficient-12 shadow gives" in compact
    assert "<code>1/3</code>" in compact
    assert "wrong CnuB entropy denominator" in compact
