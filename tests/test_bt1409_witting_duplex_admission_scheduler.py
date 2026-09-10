#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool() -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "bt1409_witting_duplex_admission_scheduler.py"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (ROOT / "data" / "bt1409_witting_duplex_admission_scheduler.json").read_text(
            encoding="utf-8"
        )
    )


def test_bt1409_scheduler_runs_true() -> None:
    out = run_tool()
    assert out == {
        "basis_witness_aperture": "1/10",
        "bt": 1409,
        "state_accept_unique": "13/40",
        "verified": True,
    }

    data = load_result()
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["checks"]["basis_aperture_rate_is_ks_defect"] is True
    assert data["checks"]["incidence_accept_rate_matches_ks_defect"] is True
    assert "basis_aperture_rate_is_contextual_fraction" not in data["checks"]
    assert "incidence_accept_rate_matches_contextual_fraction" not in data["checks"]


def test_bt1409_duplex_law_counts() -> None:
    data = load_result()

    assert data["histograms"] == {
        "basis_accept_count": {"4": 40},
        "basis_reject_count": {"36": 40},
        "compatible_distinct_count": {"12": 40},
        "compatible_incidence_count": {"16": 40},
        "compatible_state_unique_count": {"13": 40},
        "incompatible_state_count": {"27": 40},
    }
    assert data["rates"] == {
        "basis_retry_shadow": "36/40",
        "basis_witness_aperture": "1/10",
        "incidence_accept": "1/10",
        "state_accept_unique": "13/40",
        "state_reject_unique": "27/40",
    }
    assert "13/40" in data["duplex_law"]["state_query"]
    assert "4/40 = 1/10" in data["duplex_law"]["basis_query"]
    assert "KS satisfiability defect" in data["duplex_law"]["basis_query"]
    assert "36/40" in data["duplex_law"]["basis_shadow"]
    assert data["contextuality_quantities"] == {
        "ks_satisfiability_defect": "1/10",
        "abramsky_barbosa_contextual_fraction": 1,
        "why_distinct": (
            "The KS defect asks how close a Boolean marking can come to "
            "satisfying all exactly-one context constraints (36/40). The "
            "Abramsky-Barbosa contextual fraction is 1 because no global "
            "section exists at all."
        ),
    }


def test_bt1409_frame_budget_and_sample_epoch() -> None:
    data = load_result()

    assert data["frame_budget_for_one_selected_ray"] == {
        "basis_witness_frames": 4,
        "basis_witness_ticks_if_all_apertures_are_audited": 288,
        "communication_frames": 13,
        "communication_ticks_if_all_compatible_states_are_served": 936,
        "frame_ticks": 72,
        "reading": (
            "BT1409 does not require every rejected choice to consume a "
            "BT1407 frame.  It separates the accepted communication frames "
            "from the smaller basis-witness aperture used for contextual "
            "tamper evidence."
        ),
    }
    sample = data["sample_ray_0"]
    assert sample["ray"] == 0
    assert sample["basis_accept_count"] == 4
    assert sample["basis_reject_count"] == 36
    assert sample["state_accept_rate"] == "13/40"
    assert sample["basis_accept_rate"] == "1/10"
    assert sample["compatible_incidence_rate"] == "1/10"
    assert sample["same_ray_incidence_multiplicity"] == 4
    assert len(sample["compatible_unique"]) == 13
    assert len(sample["compatible_distinct"]) == 12
    assert (
        len([row for row in sample["basis_epoch"] if row["mode"] == "WITNESS_APERTURE"])
        == 4
    )
    assert (
        len([row for row in sample["basis_epoch"] if row["mode"] == "RETRY_SHADOW"])
        == 36
    )


def test_bt1409_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet_wrapper = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    single = " ".join(
        (ROOT / "single_photon_universal_computation.tex")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "BT1409: Witting duplex admission scheduler" in docs
    assert "BT1409_witting_duplex_admission_scheduler.md" in docs
    assert r"\input{photonic_holonet_body.tex}" in holonet_wrapper
    assert (ROOT / "photonic_holonet_body.tex").is_file()
    assert "BT1409 Witting Duplex Admission Scheduler" in single
    assert "communication throughput" in single
    # Current manuscript prose states the BT823 relation through its corrected
    # noncontextual ceiling rather than repeating the older label verbatim.
    assert "corrected BT823 noncontextual ceiling" in single


if __name__ == "__main__":
    test_bt1409_scheduler_runs_true()
    test_bt1409_duplex_law_counts()
    test_bt1409_frame_budget_and_sample_epoch()
    test_bt1409_publication_anchors()
    print("BT1409 focused tests passed")
