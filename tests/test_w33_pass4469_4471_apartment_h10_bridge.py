from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = [
    ROOT / "analysis" / "w33_pass4469_apartment_css_h10_intertwiner.py",
    ROOT / "analysis" / "w33_pass4470_apartment_h10_quadratic_fixed_layer.py",
    ROOT / "analysis" / "w33_pass4471_general_gq_apartment_incidence_bridge.py",
]

CERTS = [
    ROOT / "data" / "PART_W33_PASS4469_APARTMENT_CSS_H10_INTERTWINER.json",
    ROOT / "data" / "PART_W33_PASS4470_APARTMENT_H10_QUADRATIC_FIXED_LAYER.json",
    ROOT / "data" / "PART_W33_PASS4471_GENERAL_GQ_APARTMENT_INCIDENCE_BRIDGE.json",
]


def test_executable_witnesses_pass_and_regenerate_frozen_certificates() -> None:
    before = [json.loads(path.read_text(encoding="utf-8")) for path in CERTS]
    for script in SCRIPTS:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    after = [json.loads(path.read_text(encoding="utf-8")) for path in CERTS]
    assert after == before


def test_pass4469_certificate_boundary_and_dimensions() -> None:
    data = json.loads(CERTS[0].read_text(encoding="utf-8"))
    assert data["checks"] == {"passed": 23, "total": 23}
    assert data["dimensions"]["apartment_quotient"] == 10
    assert data["dimensions"]["H10_Cperp_mod_C"] == 10
    assert data["gram_rank"] == 10
    assert data["intertwiner"]["exhaustive_nonzero_quotient_kernel_classes"] == 0
    assert "not the full 20-dimensional logical Pauli space" in data["boundary"]


def test_pass4470_quadratic_fixed_layer_certificate() -> None:
    data = json.loads(CERTS[1].read_text(encoding="utf-8"))
    assert data["checks"] == {"passed": 29, "total": 29}
    assert data["quadratic_refinements"]["apartment_singular_classes_including_zero"] == 528
    assert data["quadratic_refinements"]["H10_singular_classes_including_zero"] == 528
    assert data["raw_incidence_map"]["symplectic"] is True
    assert data["raw_incidence_map"]["quadratic"] is False
    assert data["raw_incidence_map"]["defect_nonzero_classes"] == 512
    assert data["defect_class"]["target_identification"] == "Phi(a) spans im(A_point mod 2)/C"
    assert data["repair"]["all_1024_classes_verified"] is True
    assert "not asserted to be a physical gate" in data["boundary"]


def test_pass4471_orientation_criterion_certificate() -> None:
    data = json.loads(CERTS[2].read_text(encoding="utf-8"))
    assert data["checks"] == {"passed": 8, "total": 8}
    assert data["sweep_mismatches"] == []
    assert data["examples"]["GQ(3,3)=W(3,3)"]["criterion"] is True
    assert data["examples"]["GQ(3,9)=Q(5,3)"]["criterion"] is True
    assert data["examples"]["GQ(9,3) dual parameter set"]["criterion"] is False
    assert "does not explain or predict" in data["boundary"]


def test_all_three_manuscripts_include_shared_bridge_insert_once() -> None:
    needle = r"\input{analysis/PASS4469_4471_apartment_css_bridge_insert}%"
    for name in ("w33_paper.tex", "photonic_holonet.tex", "holonet_machine_blueprint.tex"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert text.count(needle) == 1


def test_public_sources_are_registered_without_replacing_old_card() -> None:
    cfg = json.loads(
        (ROOT / "data" / "w33_public_frontier_extension_pass4461_4464.json").read_text(
            encoding="utf-8"
        )
    )
    tokens = [entry["token"] for entry in cfg["public_sections"]]
    assert tokens == [
        "pass4461-4464-line-signing-apartment-parity",
        "pass4469-4471-apartment-h10-bridge",
    ]
    old = (ROOT / "analysis" / "PASS4461_4464_line_signing_apartment_index_insert.html").read_text(
        encoding="utf-8"
    )
    new = (ROOT / "analysis" / "PASS4469_4471_apartment_h10_index_insert.html").read_text(
        encoding="utf-8"
    )
    assert 'id="pass4461-4464-line-signing-apartment-parity"' in old
    assert 'id="pass4469-4471-apartment-h10-bridge"' in new
    assert "20-dimensional logical Pauli space" in new
    assert "not being promoted to a hardware gate" in new
