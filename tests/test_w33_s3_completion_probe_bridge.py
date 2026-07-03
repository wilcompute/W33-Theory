import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_bridge() -> dict:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analysis" / "w33_s3_completion_probe_bridge.py"),
        ],
        cwd=ROOT,
        check=True,
    )
    return json.loads(
        (ROOT / "data" / "w33_s3_completion_probe_bridge.json").read_text(
            encoding="utf-8"
        )
    )


def test_completion_surface_matches_probe_clock():
    data = run_bridge()
    frontier = data["frontier_completion_surface"]
    probe = data["probe_control_surface"]

    assert data["verified"] is True
    assert all(data["checks"].values())
    assert frontier["ordered_nonlocal_paths"] == 4320
    assert frontier["completions_per_path"] == 3
    assert frontier["completion_incidences"] == 12960
    assert frontier["nonlocal_quadrangles"] == 1620
    assert frontier["ordered_paths_per_quadrangle"] == 8
    assert probe["mirror_atlases"] == 24
    assert probe["probes_per_mirror_atlas"] == 540
    assert probe["supercycle_probes"] == 12960
    assert probe["runtime_slots_per_probe"] == 4
    assert probe["supercycle_runtime_slots"] == 51840


def test_completion_bridge_uses_atlas_as_probe_surface_not_exact_cover():
    data = run_bridge()
    frontier = data["frontier_completion_surface"]
    boundary = " ".join(data["claim_boundary"])

    assert frontier["target_cover_size"] == 540
    assert frontier["found_exact_cover"] is False
    assert "not a canonical golden selector" in boundary
    assert "found no exact cover" in boundary
    assert "not a solved branch packet" in boundary
    assert "does not identify a unique geometric completion" in boundary


def test_completion_probe_samples_hit_control_word_boundaries():
    data = run_bridge()
    samples = {
        row["completion_incidence_id"]: row for row in data["completion_probe_samples"]
    }

    assert samples[0]["ordered_path_id_budget"] == 0
    assert samples[0]["completion_choice_budget"] == 0
    assert samples[1]["completion_choice_budget"] == 1
    assert samples[2]["completion_choice_budget"] == 2
    assert samples[3]["ordered_path_id_budget"] == 1
    assert samples[539]["ordered_path_in_atlas_budget"] == 179
    assert samples[540]["control_word_at_probe_start"]["mirror_atlas_id"] == 1
    assert samples[12959]["control_word_at_probe_start"]["mirror_atlas_id"] == 23
    assert samples[12959]["control_word_at_probe_start"]["runtime_slot_start"] == 51836


def test_completion_probe_publication_anchor():
    data = run_bridge()
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert (
        "artifacts/w33_periodic_table_organization_summary.json"
        in data["source_certificates"]
    )
    assert "data/w33_architecture_control_plane_abi.json" in data["source_certificates"]
    assert 'id="holonet-s3-completion-probe-bridge"' in docs
    assert "w33_s3_completion_probe_bridge.py" in docs
    assert "w33_s3_completion_probe_bridge.json" in docs
    assert "4320&times;3 = 12960" in docs
    assert "24&times;540 = 12960" in docs
