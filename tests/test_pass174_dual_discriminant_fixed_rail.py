from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass174_dual_discriminant_fixed_rail.py"
DATA = ROOT / "data" / "w33_pass174_dual_discriminant_fixed_rail.json"


def run_payload() -> dict:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert "Pass 174: PASS (66/66)" in completed.stdout
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_pass174_fixed_rail_correction() -> None:
    result = run_payload()
    assert result["status"] == "PASS"
    assert result["cross_checks"] and all(result["cross_checks"].values())
    address = result["address"]
    route = result["route"]
    assert address["lattice"]["p2_module"] == "(Z/2)^14 + Z/8"
    assert route["lattice"]["p2_module"] == "(Z/2)^8 + Z/8"
    assert address["cohomology"]["H1_dimension"] == 3
    assert route["cohomology"]["H1_dimension"] == 1
    for side in (address, route):
        assert side["cohomology"]["scalar1_is_coboundary"]
        assert not side["cohomology"]["scalar5_is_coboundary"]
        assert (
            side["cohomology"]["scalar5_H1_coordinates"]
            == side["cohomology"]["fixed_line_H1_coordinates"]
            == "0x1"
        )
        assert side["fixed_order8_rail"]["fixed_generator_q"] == "11/8"
    assert address["fixed_order8_rail"]["shift_count"] == 512
    assert address["fixed_order8_rail"]["q_preserving_shift_count"] == 256
    assert route["fixed_order8_rail"]["shift_count"] == 32
    assert route["fixed_order8_rail"]["q_preserving_shift_count"] == 16


def test_pass174_route_hull_reconstructs_e8_mod2_capstone() -> None:
    result = json.loads(DATA.read_text(encoding="utf-8"))
    shadow = result["route_hull_e8_shadow"]
    assert shadow["status"] == "PASS"
    assert shadow["checks"] and all(shadow["checks"].values())
    assert shadow["checks"]["hull_quadratic_equals_discriminant_quadratic"]
    assert shadow["checks"]["all_ones_is_discriminant_4h"]
    assert shadow["hull"] == {
        "definition": "H = R intersect R^perp",
        "fixed_radical": "<all-ones>",
        "fixed_radical_lattice_coefficients": "0x7fff",
        "fixed_radical_discriminant_coordinate": [0, 0, 0, 0, 0, 0, 0, 0, 4],
        "parameters": "[40,9,16]",
        "weight_enumerator": {
            "0": 1,
            "16": 135,
            "20": 240,
            "24": 135,
            "40": 1,
        },
    }
    quotient = shadow["quotient"]
    assert quotient["dimension"] == 8
    assert quotient["type"] == "plus"
    assert quotient["isotropic_vectors"] == 136
    assert quotient["anisotropic_vectors"] == 120
    assert quotient["PSp_orbits"] == [1, 135, 120]
    assert quotient["PSp_action_order"] == 25920
    assert quotient["outer_extension_order"] == 51840
    assert shadow["capstone_graphs"]["all_nonzero"]["parameters"] == [255, 126, 61, 63]
    assert shadow["capstone_graphs"]["isotropic"]["parameters"] == [135, 70, 37, 35]
    assert shadow["capstone_graphs"]["anisotropic"]["parameters"] == [120, 63, 30, 36]


def test_pass174_is_published() -> None:
    expected = {
        ROOT / "w33_paper.tex": "Pass 174",
        ROOT / "photonic_holonet.tex": "route-code hull",
        ROOT / "holonet_practical_implications.tex": "fixed order-eight rail",
        ROOT / "docs" / "index.html": "pass174-route-hull-fixed-rail",
    }
    for path, needle in expected.items():
        assert needle in path.read_text(encoding="utf-8"), (path, needle)
