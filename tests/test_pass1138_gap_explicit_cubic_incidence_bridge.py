"""Focused regression for the GAP-owned Pass 1138 incidence bridge."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1138_explicit_cubic_incidence_bridge.g"
CERTIFICATE = (
    ROOT / "data" / "w33_pass1138_explicit_cubic_incidence_bridge.json"
)


@lru_cache(maxsize=1)
def _certificate() -> dict:
    """Run GAP once; Python only parses the GAP-produced certificate."""

    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for the Pass 1138 certificate"
    completed = subprocess.run(
        [gap, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    stdout = completed.stdout.replace("\n", "")
    assert "Pass1138 status=PASS checks=39" in stdout
    assert "M=45x2240 rank=45 live=240 composite_rank=25 line_fibers=40x6" in stdout
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


@pytest.mark.skipif(shutil.which("gap") is None, reason="GAP is required")
def test_explicit_M_constructs_the_missing_2240_to_45_map() -> None:
    cert = _certificate()
    matrix = cert["explicit_M"]

    assert cert["status"] == "PASS"
    assert cert["producer"] == "GAP 4.12.1 exact integer/rational arithmetic"
    assert cert["check_count"] == 39 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert matrix == {
        "orientation": (
            "rows are 45 cubic supports; columns are 2240 unordered A2 root triples"
        ),
        "definition": (
            "M[s,t]=1 iff every one of the nine doubled-E8 scalar products "
            "between s and t is zero"
        ),
        "shape": [45, 2240],
        "rank_over_Q": 45,
        "row_sum_distribution": {"32": 45},
        "column_sum_distribution": {"0": 2000, "6": 240},
        "live_columns": "exactly the unique W(E6) orbit of size 240",
        "killed_432_columns": 1296,
        "gram_identity": "M M^T = 24 I_45 - 6 A_45 + 8 J_45",
        "gram_off_diagonal_distribution": {"2": 720, "8": 270},
        "gram_spectrum": {"192": 1, "48": 20, "12": 24},
    }
    assert cert["e8_a2_carrier"]["orbit_profile"] == [
        1,
        1,
        27,
        27,
        27,
        27,
        27,
        27,
        240,
        270,
        270,
        432,
        432,
        432,
    ]


@pytest.mark.skipif(shutil.which("gap") is None, reason="GAP is required")
def test_live_240_module_locates_the_exact_195_dimensional_kernel() -> None:
    live = _certificate()["live_240_module"]

    assert live["stabilizer_order"] == 216
    assert live["stabilizer_structure"] == "(C3 x C3 x C3) : D8"
    assert live["permutation_decomposition_by_degree"] == [
        [1, 1],
        [15, 1],
        [20, 1],
        [24, 1],
        [30, 1],
        [60, 1],
        [90, 1],
    ]
    assert live["pass1135_label_crosswalk"] == (
        "1 + 15a + 20 + 24 + 30 + 60a + 90"
    )
    assert live["image_decomposition"] == "1 + 20 + 24"
    assert live["internal_kernel_decomposition"] == "15a + 30 + 60a + 90"
    assert live["internal_kernel_dimension"] == 195
    assert live["full_kernel_dimension"] == 2195


@pytest.mark.skipif(shutil.which("gap") is None, reason="GAP is required")
def test_octet_bijection_and_composite_factor_through_six_copies_of_each_line() -> None:
    cert = _certificate()
    bijection = cert["support_octet_bijection"]
    composite = cert["composite_C_equals_NM"]

    assert bijection["stabilizer_order"] == 1152
    assert bijection["equivariant"] is True
    assert bijection["relation_transport"] == (
        "disjoint E8 supports iff the corresponding W33 octets intersect in two points"
    )
    assert "no preferred global labeling" in bijection["choice_boundary"]

    assert composite == {
        "shape": [40, 2240],
        "rank_over_Q": 25,
        "image": "the W33 point-carrier 1+24 sector",
        "intermediate_kernel": "the 20-dimensional octet-only sector",
        "row_sum_distribution": {"288": 40},
        "column_sum_distribution": {"0": 2000, "48": 240},
        "entry_distribution": {"0": 80000, "1": 8640, "3": 960},
        "gram_identity": "C C^T = 96 I_40 + 24 A_W33 + 336 J_40",
        "gram_spectrum": {"13824": 1, "144": 24, "0": 15},
        "live_factorization": (
            "C_live = J_(40x240) + 2 R, where R pulls back "
            "W33 point-line incidence"
        ),
        "line_fibration": {
            "live_a2_triples": 240,
            "W33_lines": 40,
            "fiber_size": 6,
            "column_profile": {"1": 36, "3": 4},
        },
    }


def test_pass1138_cites_prior_45_layer_owners_and_keeps_scope_finite() -> None:
    cert = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    synthesis = (
        ROOT / "PASS1138_EXPLICIT_CUBIC_INCIDENCE_BRIDGE.md"
    ).read_text(encoding="utf-8")

    assert cert["prior_owners"] == {
        "cubic_character_decomposition": (
            "analysis/w33_pass1135_cubic_kernel_decomposition.py"
        ),
        "45_point_graph": "analysis/w33_flat_45_point_frame.py",
        "point_octet_projector": (
            "analysis/bt767_k44_octet_incidence_projector.py"
        ),
        "intrinsic_octet_identification": (
            "analysis/bt769_center_quad_octet_identification.py"
        ),
    }
    assert "not identified with qutrit phase sheets" in cert["scope"]
    assert "not a canonical labeling" in synthesis
    assert "does not identify the six sheets with qutrit phases" in synthesis
    assert "bt767_k44_octet_incidence_projector.py" in synthesis
    assert not (ROOT / "PASS1138_RESERVED.md").exists()
