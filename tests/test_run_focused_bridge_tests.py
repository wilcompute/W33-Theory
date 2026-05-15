from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_focused_bridge_tests import (  # noqa: E402
    SUITES,
    build_pytest_command,
    expand_suites,
)


def test_focused_bridge_runner_has_expected_core_suites() -> None:
    assert {
        "photonic-qec",
        "dcc-weld",
        "tomotope-klitzing",
        "sector-split",
        "closure-clock",
    } <= set(SUITES)
    assert "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py" in SUITES["photonic-qec"]
    assert "tests/test_dccxl_closure_jordan_resolvent_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxliv_nilpotent_action_variation_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxlv_nilpotent_hessian_convexity_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxlvi_nilpotent_action_jet_tower_bridge.py" in SUITES["closure-clock"]
    assert "tests/test_dccxlvii_nilpotent_ward_recursion_bridge.py" in SUITES["closure-clock"]


def test_focused_bridge_runner_architecture_alias_dedupes_paths() -> None:
    paths = expand_suites(["architecture"])

    assert "tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py" in paths
    assert "tests/test_dccxl_closure_jordan_resolvent_bridge.py" in paths
    assert "tests/test_dccxliv_nilpotent_action_variation_bridge.py" in paths
    assert "tests/test_dccxlv_nilpotent_hessian_convexity_bridge.py" in paths
    assert "tests/test_dccxlvi_nilpotent_action_jet_tower_bridge.py" in paths
    assert "tests/test_dccxlvii_nilpotent_ward_recursion_bridge.py" in paths
    assert len(paths) == len(set(paths))
    assert len(paths) >= 32


def test_focused_bridge_runner_builds_noconftest_command() -> None:
    command = build_pytest_command(["tests/test_dccxv_photonic_fusion_syndrome_qec_bridge.py"], ["-k", "qec"])

    assert command[:4] == [sys.executable, "-m", "pytest", "--noconftest"]
    assert "-q" in command
    assert command[-2:] == ["-k", "qec"]
