"""Smoke tests that formalize the live W33↔E8 artifact surface into CI checks.

- Asserts the stable correspondence summary reports `ALL_VERIFIED == true`,
  3 generations, and the GUT Weinberg prediction 3/8.
- Asserts the stable bijection artifact has nontrivial triangle-cocycle support.
"""

import json
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_json(relpath: str):
    p = ROOT / relpath
    if not p.exists():
        pytest.skip(f"Missing artifact: {p}")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_w33_e8_correspondence_all_verified_and_predictions():
    data = _load_json("checks/PART_CVII_w33_e8_correspondence_theorem.json")

    # verification flag
    assert data.get("verification", {}).get("ALL_VERIFIED", False) is True

    # generation prediction (should be exactly 3)
    n_gen = data.get("predictions", {}).get("generations", {}).get("n_generations")
    assert n_gen == 3

    # Weinberg-angle GUT prediction = 3/8
    gut_sin2 = (
        data.get("predictions", {})
        .get("weinberg_angle", {})
        .get("gut_scale_prediction", {})
        .get("value")
    )
    assert math.isclose(float(gut_sin2), 3.0 / 8.0, rel_tol=0, abs_tol=1e-15)


def test_e8_bijection_artifact_has_nontrivial_triangle_cocycle_support():
    data = _load_json("checks/PART_CVII_e8_bijection.json")
    tc = data.get("verification", {}).get("triangle_cocycle", {})

    total_checked = tc.get("total_checked")
    exact = tc.get("exact_match")
    root_sum_exists = tc.get("root_sum_exists")

    assert isinstance(total_checked, int)
    assert total_checked > 0
    assert isinstance(exact, int)
    assert isinstance(root_sum_exists, int)
    assert exact >= 1 or root_sum_exists >= 10
