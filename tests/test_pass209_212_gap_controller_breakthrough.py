"""GAP-owned certificates for the Pass 209--212 controller breakthrough."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = {
    209: ROOT / "analysis" / "w33_pass209_silent_spread_two_clock.g",
    210: ROOT / "analysis" / "w33_pass210_s6_route_atlas.g",
    211: ROOT / "analysis" / "w33_pass211_pgsp_controller_clifford.g",
    212: ROOT / "analysis" / "w33_pass212_4320_carrier_equivariant_bijection.g",
}
CERTIFICATES = {
    209: ROOT / "data" / "w33_pass209_silent_spread_two_clock.json",
    210: ROOT / "data" / "w33_pass210_s6_route_atlas.json",
    211: ROOT / "data" / "w33_pass211_pgsp_controller_clifford.json",
    212: ROOT / "data" / "w33_pass212_4320_carrier_equivariant_bijection.json",
}


@lru_cache(maxsize=1)
def _certificates() -> dict[int, dict]:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Passes 209--212"
    for pass_id, script in SCRIPTS.items():
        result = subprocess.run(
            [gap, "-q", str(script)],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=90,
        )
        assert "PASS" in result.stdout, (pass_id, result.stdout)
    return {
        pass_id: json.loads(path.read_text(encoding="utf-8"))
        for pass_id, path in CERTIFICATES.items()
    }


def test_pass209_silent_spread_and_relation_fusion() -> None:
    cert = _certificates()[209]
    assert cert["status"] == "PASS"
    assert cert["producer"].startswith("GAP ")
    assert cert["silent_spread_bridge"] == {
        "definition": "Sigma(D)={ell: v[ell]=0 for every v in D}",
        "dodecads": 36,
        "spreads": 36,
        "lines_per_spread": 10,
        "spreads_per_line": 9,
        "overlaps": {"1": 360, "4": 270},
        "generator_equivariance_cases": 1440,
    }
    assert cert["line_x_dodecad"]["orbits"] == [360, 1080]
    assert cert["axis_relation_fusion"]["orbits"] == [360, 720, 3240]
    assert all(cert["checks"].values())


def test_pass210_s6_atlas_and_two_strata() -> None:
    cert = _certificates()[210]
    assert cert["status"] == "PASS"
    assert cert["silent_line_atlas"]["unique_base_match"] is True
    assert cert["silent_line_atlas"]["equivariance_cases"] == 7200
    assert cert["derived_doily"]["point_graph"] == "SRG(15,6,1,3)"
    assert cert["clock_strata"] == {
        "active_1080": "S4 -> S3 with kernel V4; faithful on the four line points",
        "silent_360": "(S3 x S3):C2 -> C2 with kernel S3 x S3",
    }
    assert cert["PGSp_lift"]["dodecad_stabilizer"] == "S6 x C2"
    assert all(cert["checks"].values())


def test_pass211_pgsp_controller_and_sp20_correction() -> None:
    cert = _certificates()[211]
    controller = cert["controller"]
    clifford = cert["logical_clifford"]
    assert cert["status"] == "PASS"
    assert controller["group_order"] == 51840
    assert controller["ordered_nonlocal_paths"] == 4320
    assert controller["path_stabilizer_structure"] == "S3 x C2 (split central extension)"
    assert controller["chosen_branch_stabilizer"] == "V4"
    assert clifford["full_logical_pauli_dimension"] == 20
    assert clifford["ambient_clifford_quotient"] == "Sp(20,2)"
    assert clifford["physical_action"] == (
        "diag(M,M^(-T)) after choosing the dot-product dual Z basis"
    )
    assert all(cert["checks"].values())


def test_pass212_canonical_bijection_and_probe_obstruction() -> None:
    cert = _certificates()[212]
    assert cert["status"] == "PASS"
    assert cert["schema"] == "w33.pass212.4320_carrier_path_bijection.gap.v2"
    assert cert["theorem"]["verdict"] == "canonical PSp(4,3)-equivariant bijection"
    assert cert["counts"]["source_sheets"] == cert["counts"]["target_paths"] == 4320
    assert cert["counts"]["equivariance_cases"] == 8640
    assert len(cert["bijection"]) == 4320
    assert len({tuple(row["source"]) for row in cert["bijection"]}) == 4320
    assert len({tuple(row["target"]) for row in cert["bijection"]}) == 4320
    assert cert["pgsp_probe_boundary"]["completion_line_point_orbit_sizes"] == [1, 1, 2]
    assert cert["pgsp_probe_boundary"]["global_point_marked_flag_orbit_sizes"] == [
        12960,
        12960,
        25920,
    ]
    assert all(cert["checks"].values())


def test_pass209_212_visible_surfaces_and_honest_boundaries() -> None:
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    photonic = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    practical = (ROOT / "holonet_practical_implications.tex").read_text(
        encoding="utf-8"
    )
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for text in (paper, photonic, practical, index):
        assert "w33_pass212_4320_carrier_equivariant_bijection.g" in text.replace(
            "\\_", "_"
        )
    assert "operatorname{diag}(M,M^{-\\mathsf T})\\in\\Sp(20,2)" in paper
    assert "1+1+2" in paper
    assert "regular four-probe address" in photonic
    assert "\\emph{not}" in photonic
    assert "not one regular orbit of size" in practical
    assert "not the controller&rsquo;s four semantic probe slots" in index
