from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "analysis/w33_pass4480_line_logical_apartment_twins.py",
    ROOT / "analysis/w33_pass4481_apartment_radical_module_filtration.py",
    ROOT / "analysis/w33_pass4482_ten_line_protected_readout.py",
]
CERTS = [
    ROOT / "data/PART_W33_PASS4480_LINE_LOGICAL_APARTMENT_TWINS.json",
    ROOT / "data/PART_W33_PASS4481_APARTMENT_RADICAL_MODULE_FILTRATION.json",
    ROOT / "data/PART_W33_PASS4482_TEN_LINE_PROTECTED_READOUT.json",
]


def test_witnesses_regenerate_frozen_certificates() -> None:
    before = [json.loads(p.read_text(encoding="utf-8")) for p in CERTS]
    for script in SCRIPTS:
        proc = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, capture_output=True)
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    after = [json.loads(p.read_text(encoding="utf-8")) for p in CERTS]
    assert after == before


def test_4480_twin_boundary() -> None:
    d = json.loads(CERTS[0].read_text(encoding="utf-8"))
    assert d["pass"] == 4480
    assert d["checks"] == {"passed": 14, "total": 14}
    assert d["single_line"] == {
        "apartment_weight": 162,
        "classes": 40,
        "logical_weight": 4,
        "pairing_graph": "dual W33",
    }
    assert d["quadratic_twin"]["fixed_class_unique"] is True
    assert "not a second physical code" in d["boundary"]


def test_4481_radical_profile() -> None:
    d = json.loads(CERTS[1].read_text(encoding="utf-8"))
    assert d["pass"] == 4481
    assert d["checks"] == {"passed": 12, "total": 12}
    assert d["exact_sequence"] == "0 -> K/J (29) -> C_ap (39) -> H10 (10) -> 0"
    assert d["radical_profile"] == "8 | (6 + 1) | 14"
    assert d["irreducible_factors"] == [8, 6, 14]


def test_4482_optimal_readout() -> None:
    d = json.loads(CERTS[2].read_text(encoding="utf-8"))
    assert d["pass"] == 4482
    assert d["checks"] == {"passed": 11, "total": 11}
    assert d["basis_graph"]["type"] == "P4 disjoint-union 3K2"
    assert d["basis_graph"]["minimum_intersections"] == 6
    assert d["basis_graph"]["maximum_induced_matching"] == 4
    assert d["readout"]["all_1024_classes_verified"] is True
    assert "not ten physical apartment measurements" in d["boundary"]


def test_collision_cleanup_and_manuscript_integration() -> None:
    for stale in [
        "analysis/w33_pass4474_line_logical_apartment_twins.py",
        "analysis/w33_pass4475_apartment_radical_module_filtration.py",
        "analysis/w33_pass4476_ten_line_protected_readout.py",
        "analysis/PASS4477_apartment_h10_prior_art_boundary.md",
        "analysis/PASS4474_4478_RESERVATION.md",
        "analysis/PASS4474_4477_apartment_h10_continuation_insert.tex",
    ]:
        assert not (ROOT / stale).exists(), stale
    needle = r"\input{analysis/PASS4480_4483_apartment_h10_continuation_insert}%"
    for name in ["w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex"]:
        assert (ROOT / name).read_text(encoding="utf-8").count(needle) == 1


def test_public_extension_registers_parallel_and_renumbered_cards() -> None:
    cfg = json.loads((ROOT / "data/w33_public_frontier_extension_pass4461_4464.json").read_text(encoding="utf-8"))
    tokens = [x["token"] for x in cfg["public_sections"]]
    assert "pass4472-4479-apartment-module-thermo-ihara-pauli" in tokens
    assert "pass4480-4483-apartment-h10-geometric-readout" in tokens
    page = (ROOT / "docs/apartment-h10-geometric-readout.html").read_text(encoding="utf-8")
    assert "P4 ⊔ 3K2" in page
    assert "not ten physical apartment measurements" not in page.lower()  # prose uses 'This is not a ten-measurement' style
    assert "not a ten-measurement syndrome-acquisition theorem" in page
