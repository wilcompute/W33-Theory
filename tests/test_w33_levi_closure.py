"""Regression tests for the five Levi closure tracks."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_levi_closure as closure  # noqa: E402
import holonet_typed_packet as typed  # noqa: E402


def result() -> dict:
    return closure.analyze()


def test_all_five_tracks_pass() -> None:
    data = result()
    assert data["status"] == "PASS"
    assert data["checks"] == {"all_five_present": True, "all_five_pass": True}


def test_module_decomposition_is_8_plus_6_plus_14() -> None:
    data = result()["tracks"]["2_module_decomposition"]
    assert [data["point"]["dimension"]] + [x["dimension"] for x in data["line"]["summands"]] == [8, 6, 14]
    assert data["group_order"] == 25920
    assert [(row["dimension"], row["type"]) for row in data["line"]["summands"]] == [
        (6, "O-_6(2)"),
        (14, "O-_14(2)"),
    ]


def test_typed_packet_mirror_and_retag_guard() -> None:
    kernel = typed.LeviTypedKernel()
    source = kernel.encode(0, kernel.contexts[0].homology[0])
    target = kernel.mirror(source)
    assert target.type_bit == 1
    assert target.syndrome == 0
    with pytest.raises(typed.TypeConfusionError):
        kernel.raw_retag(source)


def test_typed_packet_fuzz() -> None:
    assert typed.LeviTypedKernel().fuzz(seed=7, trials=128)["all_pass"]


def test_selector_chain_closure() -> None:
    data = result()["tracks"]["4_selector_closure"]
    assert len(data["rows"]) == 8
    assert data["checks"]["weights_1_4_12_40"]


def test_exact_group_resolution() -> None:
    data = result()["tracks"]["5_group_bridge"]
    assert data["tomotope"]["structure"] == "(V4+V4):S3 = S4 fiber-product_over_S3 S4"
    assert data["tomotope"]["profile"] == {1: 1, 2: 27, 3: 32, 4: 36}
    assert sum(data["runtime_48"]["profile"].values()) == 48
    assert data["phase_doubled_runtime"]["is_tomotope"] is False


def test_certificate_matches_recomputed_status() -> None:
    certificate = json.loads(
        (ROOT / "data" / "PART_2026_07_10_LEVI_CLOSURE_results.json").read_text(encoding="utf-8")
    )
    assert certificate["status"] == result()["status"] == "PASS"
