from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass2716_integer_transceiver_reference.py"
DATA = ROOT / "data" / "w33_pass2716_2721_incidence_transceiver.json"
RTL = ROOT / "rtl" / "w33_pass2717_incidence_transceiver.sv"
EXPECTED_SHA = "ceedf1972f11c6a0f8309558ea0d93d907943cbfe5da352bd373c9bec288c2dd"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_pass2716", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_certificate_recomputes() -> None:
    module = load_module()
    result = module.certificate()
    assert result["status"] == "PASS_EXACT_MULTIPLIER_FREE_DIGITAL_TRANSCEIVER_WITH_OPTICAL_BOUNDARY"
    assert result["sha256_without_hash_field"] == EXPECTED_SHA
    assert all(result["checks"].values())
    assert result["digital_core"]["general_multipliers"] == 0
    assert result["digital_core"]["polar_square_gain"] == 600


def test_frozen_certificate_matches_live_reconstruction() -> None:
    module = load_module()
    frozen = json.loads(DATA.read_text(encoding="utf-8"))
    assert frozen == module.certificate()


def test_rtl_masks_match_exact_geometry() -> None:
    module = load_module()
    result = module.certificate()
    expected = Counter(
        result["geometry"]["forward_masks_hex"]
        + result["geometry"]["reverse_masks_hex"]
    )
    text = RTL.read_text(encoding="utf-8")
    found = Counter(value.lower() for value in re.findall(r"40'h([0-9a-fA-F]{10})", text))
    assert found == expected
    assert "module w33_pass2717_incidence_core" in text
    assert "module w33_pass2717_incidence_serial" in text
    assert "local_sum[40] <<< 3" in text
    assert "local_sum[40] <<< 1" in text
    assert "REVERSE ? reverse_mask : forward_mask" in text


def test_optical_boundary_is_fail_closed() -> None:
    module = load_module()
    boundary = module.certificate()["boundary"]
    for phrase in (
        "optical 1/sqrt(6)",
        "loss budget",
        "detector model",
        "calibration procedure",
    ):
        assert phrase in boundary
