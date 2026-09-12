#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_reye_v4_decoder_automorphism_576 import build_result  # noqa: E402


def test_reye_576_is_affine_v4_decoder_symmetry() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["orders"] == {
        "R": 4,
        "R_x_R_translation_kernel": 16,
        "GL_2_2": 6,
        "role_S3": 6,
        "complement": 36,
        "full_typed_automorphism_group": 576,
    }
    assert data["structure"]["normal_kernel"] == "R^2 ~= C2^4"
    assert data["structure"]["complement"] == "GL(2,2) x S3 ~= S3 x S3"
    assert data["structure"]["semidirect_product"] == "C2^4 : (S3 x S3)"
    assert data["structure"]["order_factorization"] == "576 = 16 * 6 * 6"


if __name__ == "__main__":
    test_reye_576_is_affine_v4_decoder_symmetry()
    print("Reye affine V4 decoder 576 test passed")
