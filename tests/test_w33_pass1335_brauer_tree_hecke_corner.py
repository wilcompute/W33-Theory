from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "analysis" / "w33_pass1335_export_hecke_gap_input.py"
WITNESS = ROOT / "analysis" / "w33_pass1335_brauer_tree_hecke_corner.g"
CERT = ROOT / "data" / "w33_pass1335_brauer_tree_hecke_corner.json"


def test_frozen_certificate_has_closed_ext_boundary():
    data = json.loads(CERT.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert len(data["group_block_records"]) == 3
    assert data["outer_81_relation"]["ordinary_positions"] == [24, 25]
    assert "nontrivial linear character" in data["outer_81_relation"]["relation"]
    for record in data["group_block_records"]:
        assert sorted(record["ordinary_degrees"]) == [1, 6, 24, 64, 81]
        assert sorted(record["brauer_degrees"]) == [1, 6, 23, 58]
        assert record["shared_vertex_ordinary_degree"] == 81
        assert record["ext_23_58_dimension"] == 1
        assert record["ext_58_23_dimension"] == 1


def test_hecke_corner_and_color_boundary():
    data = json.loads(CERT.read_text(encoding="utf-8"))
    literal = data["literal_432_character"]
    assert literal["hecke_rank"] == 26
    assert literal["cyclic_defect_corner_dimension"] == 9
    assert literal["species20_corner_dimension"] == 9
    assert literal["species20_block_defect"] == 0
    assert data["hecke_scalar_ext"]["nonzero_entries"] == [
        [5, 6, 1],
        [5, 7, 1],
        [6, 5, 1],
        [7, 5, 1],
    ]
    assert data["hecke_scalar_ext"]["label_definition"].startswith(
        "h_i is the i-th one-dimensional simple"
    )
    assert data["color_characteristic_5"]["middle_dimensions_over_F5"] == [81, 162]
    assert data["color_characteristic_5"]["middle_dimensions_over_F25"] == [81, 81, 81]
    assert data["color_characteristic_5"]["cross_color_ext"] == 0


def test_gap_witness_reproduces_certificate():
    gap = shutil.which("gap")
    if gap is None:
        return
    subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True)
    completed = subprocess.run(
        [gap, "-q", str(WITNESS)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        timeout=180,
    )
    assert "PASS 1335 COMPLETE" in completed.stdout
    data = json.loads(CERT.read_text(encoding="utf-8"))
    assert data["failed_checks"] == []
    assert data["check_count"] == 32
