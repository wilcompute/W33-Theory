from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/PART_BT3913_BT3928_CAP_GEWIRTZ_MODULAR_CLOSURE_results.json"
VERIFIER = ROOT / "analysis/bt3913_3928_cap_gewirtz_modular_closure.py"
PRIOR = ROOT / "data/PART_BT3871_BT3886_EIGHT_FRONT_CLOSURE_results.json"
WORKFLOW = ROOT / ".github/workflows/w33_pass3913_3928_cap_gewirtz_modular_closure.yml"
SEMANTIC_SHA = "753c9039c032574dbcf5c20b899444ccc74bd092be22646211173fbd36be9eb6"


def load_result() -> dict:
    return json.loads(RESULT.read_text())


def test_exact_regeneration(tmp_path: Path) -> None:
    regenerated = tmp_path / "result.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(VERIFIER),
            "--prior-results",
            str(PRIOR),
            "--json",
            str(regenerated),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert "PASS_5_FRONTS_PLUS_3_CONSTRUCTIONS" in completed.stdout
    assert json.loads(regenerated.read_text()) == load_result()


def test_frozen_boundaries_and_fronts() -> None:
    result = load_result()
    assert result["status"] == "PASS_5_FRONTS_PLUS_3_CONSTRUCTIONS"
    assert result["semantic_sha256"] == SEMANTIC_SHA
    assert result["live_boundaries"] == {
        "cap_maximum": [68, None],
        "chromatic_number": [10, 11],
        "covering_radius": [389, 435],
        "cubic_transversal": [106, 172],
    }

    cap = result["fronts"]["cap68_transversal172"]
    assert cap["cap_size"] == 68
    assert cap["transversal_size"] == 172
    assert cap["primary_witness"]["stabilizer_order"] == 1
    assert cap["primary_witness"]["orbit_size"] == 25920

    tripod = result["fronts"]["one_defect_69_tripod"]
    assert tripod["unique_violated_triple"] == [76, 80, 175]
    assert tripod["pairwise_inequivalent_free_orbits"] is True

    switching = result["fronts"]["petersen_blowup_association_scheme"]["switching"]
    assert switching["representatives_mod_complement"] == 512
    assert switching["degree12_blowups"] == 6
    assert switching["degree24_complement_blowups"] == 6
    assert switching["W33_hits"] == 0

    modular = result["fronts"]["top115_trivial_extension_structure"]
    assert modular["split_decomposition"] == "M115 = 1 direct_sum K114"
    assert modular["nonsplit_sequence"] == "0 -> 1 -> K114 -> Q113 -> 0"
    assert modular["self_dual"] is False
    assert modular["nondegenerate_invariant_bilinear_form"] is False


def test_orbit_codes_and_tight_frame() -> None:
    result = load_result()
    codes = result["constructions"]["four_constant_weight_orbit_codes"]
    assert {name: item["minimum_distance"] for name, item in codes.items()} == {
        "A": 8,
        "B76": 18,
        "B80": 20,
        "B175": 16,
    }
    assert all(
        item["length"] == 240 and item["size"] == 25920 and item["weight"] == 68
        for item in codes.values()
    )

    frame = result["constructions"]["cap68_fibre_whitened_tight_frame"]
    assert frame["centered_dimension"] == 39
    assert frame["whitened_vector_norm_squared"] == "13/8640"
    assert frame["unit_norm_tight_frame_bound"] == "8640/13"


def test_workflow_has_no_website_dependency() -> None:
    text = WORKFLOW.read_text()
    prohibited = "docs/" + "index.html"
    assert prohibited not in text
