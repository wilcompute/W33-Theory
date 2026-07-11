from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass173_incidence_transceiver_route_dark_lattice.py"
DATA = ROOT / "data" / "w33_pass173_incidence_transceiver_route_dark_lattice.json"


def payload() -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
        timeout=360,
    )
    assert "Pass 173: PASS" in completed.stdout
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_pass173_witness_and_transceiver() -> None:
    result = payload()
    assert result["status"] == "PASS"
    assert result["checks"] and all(result["checks"].values())
    assert result["incidence_transceiver"]["rank"] == 24
    assert result["selector_analyzer"] == {
        "selectors": 480,
        "input_norm": 6,
        "output_norm": 36,
        "output_histogram": {"-3": 1, "-1": 9, "0": 20, "1": 9, "3": 1},
        "decode": "x = N^T(Nx)/6",
        "tight_frame": "X^T X=120 E_24(point), Y^T Y=720 E_24(line)",
    }


def test_pass173_asymmetric_dark_lattices() -> None:
    result = json.loads(DATA.read_text(encoding="utf-8"))
    address = result["dark_lattices"]["address_point"]
    route = result["dark_lattices"]["route_line"]
    assert address["determinant"] == 2**17 * 3**10
    assert route["determinant"] == 2**11 * 3**14
    assert address["smith_profile"] == {"2": 5, "6": 9, "24": 1}
    assert route["smith_profile"] == {"1": 1, "3": 5, "6": 8, "24": 1}
    assert address["binary_code"] == "[40,15,8]"
    assert route["binary_code"] == "[40,15,10]"
    assert address["minimum"]["minimal_vector_count"] == 90
    assert route["minimum"] == {
        "minimal_vector_count": 432,
        "minimal_norm": 10,
        "half_shell_columns": 216,
    }
    assert route["binary_hull_dimension"] == 9
    assert result["dark_lattices"]["context_dual_split"] == {
        "address_A4_A6_A8_A10": [40, 240, 5085, 47824],
        "route_A4_A6_A8_A10": [40, 240, 3645, 54736],
        "reading": (
            "the two 25-dimensional context duals agree at weights "
            "4 and 6, then first separate at weight 8"
        ),
    }
    assert result["dark_lattices"]["unscaled_parity_lattice_opening"] == {
        "address_q4": 14640,
        "route_q4": 3120,
        "route_q5": 221184,
        "reading": (
            "the address code is doubly even and self-orthogonal; "
            "the route code has weight-10 words and is not "
            "self-orthogonal, so the usual scaled integral "
            "Construction-A quotient exists only on the address side"
        ),
    }


def test_pass173_route_shell_is_the_pentad_core_carrier() -> None:
    result = json.loads(DATA.read_text(encoding="utf-8"))
    shell = result["route_minimal_shell"]
    assert shell["signed_vectors"] == 432
    assert shell["projective_rays_and_supports"] == 216
    assert shell["special_pentads"] == 432
    assert shell["support_geometry"] == "K_5,5 minus a perfect matching"
    assert shell["skew_charts"] == 540
    assert shell["chart_cover_multiplicity"] == 2
    assert shell["psp_signed_orbits"] == [216, 216]
    assert shell["stabilizer_order"] == 120


def test_pass173_is_published_on_requested_surfaces() -> None:
    expected = {
        ROOT / "w33_paper.tex": "Pass 173",
        ROOT / "photonic_holonet.tex": "route-dark lattice",
        ROOT / "holonet_practical_implications.tex": "[40,15,10]",
        ROOT / "docs" / "index.html": "pass173-incidence-transceiver",
    }
    for path, needle in expected.items():
        assert needle in path.read_text(encoding="utf-8"), (path, needle)
