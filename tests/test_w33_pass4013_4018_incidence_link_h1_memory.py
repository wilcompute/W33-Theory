from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/PART_4013_4018_INCIDENCE_LINK_H1_MEMORY.json"
EXPECTED_SHA = "bf19623ed99a287cde193ec3315e5a7f86b101f4340a1546a9dee394904c5bd3"


def load() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_certificate_and_all_checks() -> None:
    data = load()
    assert data["status"] == "PASS_EXACT_INCIDENCE_LINK_H1_MEMORY_BRIDGE"
    assert data["semantic_sha256"] == EXPECTED_SHA
    assert all(data["checks"].values())


def test_physical_link_h1_projector() -> None:
    data = load()["pass4013_physical_incidence_link_h1_projector"]
    assert data["incidence_layout"] == {"degree": 4, "modes": 80, "physical_links": 160}
    assert data["boundary_rank"] == 79
    assert data["cycle_rank"] == 81
    assert data["projector_rank"] == 81
    assert data["projector_diagonal"] == "81/160"
    assert data["edge_laplacian_spectrum"] == {
        "0": 81,
        "4": 30,
        "4+sqrt(6)": 24,
        "4-sqrt(6)": 24,
        "8": 1,
    }


def test_link_memory_reflection_and_separation() -> None:
    data = load()
    reflection = data["pass4014_exact_link_memory_reflection"]
    assert reflection["gate"] == "R_H1=I-2P_H1"
    assert reflection["eigenspaces"] == {"+1_cut": 79, "-1_cycle": 81}
    assert reflection["trace"] == -2
    separation = data["pass4018_mode_memory_vs_link_memory_separation"]
    assert separation["mode_space"]["H2_sector_ranks"] == [30, 48, 2]
    assert separation["link_current_space"] == {"cut_rank": 79, "cycle_H1_rank": 81, "dimension": 160}


def test_independent_revival_and_tomography() -> None:
    data = load()
    revival = data["pass4015_independent_two_step_incidence_revival"]
    assert revival["H2_spectrum"] == {"0": 30, "16": 2, "6": 48}
    assert revival["minimal_full_revival_time"] == "pi"
    assert revival["quarter_period_order"] == 4
    signed = data["pass4016_sign_resolved_four_moment_tomography"]
    assert signed["synthetic_populations"] == signed["recovered_populations"]
    delay = data["pass4017_full_incidence_delay_recovery"]
    assert delay["recovered_point_line_flags"] == 160
