from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_ramified_hesse_cubic_holonomy_bridge.py"
DATA = ROOT / "data/w33_ramified_hesse_cubic_holonomy_bridge.json"


def load():
    spec = importlib.util.spec_from_file_location("ramified_hesse_cubic", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_replay():
    assert load().main(write=False) == json.loads(DATA.read_text())


def test_ramified_bridge_contract():
    result = json.loads(DATA.read_text())
    reduction = result["ramified_compiler_reduction"]
    cubic = result["cubic_line_holonomy"]
    code = result["lifted_code"]
    assert reduction["characteristic_zero_rank"] == 36
    assert reduction["reduced_rank_F3"] == 12
    assert reduction["right_nullity_safe36_F3"] == 24
    assert reduction["reduced_gram"] == "Tbar^T Tbar = 0 over F3"
    assert cubic["full_line_kernel_dimension_F3"] == 24
    assert cubic["ordinary_projection_of_line_kernel_rank_F3"] == 24
    assert code["parameters"] == "[45,12,6]_3"
    assert code["word_count"] == 3**12
    assert code["minimum_word_count"] == 24
    assert code["minimum_words_are_exactly_plus_minus_generators"] is True
    assert code["systematic_coordinate_form"] == "[2*A_AG(2,3) | I12 tensor (1,1,1)]"
    assert code["fiber_correction_supports"] == "all twelve affine lines of AG(2,3)"
    assert code["gram_quotient_on_four_hesse_directions"] == [
        [int(left != right) for right in range(4)] for left in range(4)
    ]
    prior = result["external_prior_art_audit"]
    assert prior["same_parameters_published"] is True
    assert prior["equivalence_to_present_code_checked"] is False
    assert prior["parameter_novelty_claimed"] is False
    assert all(result["checks"].values())
