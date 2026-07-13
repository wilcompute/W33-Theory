"""Focused GAP-owned regression for the Pass 216 Q(4,3) dual carrier."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass216_q43_dual_ovoid_carrier.g"
CERTIFICATE = ROOT / "data" / "w33_pass216_q43_dual_ovoid_carrier.json"


@lru_cache(maxsize=1)
def _certificate() -> dict:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Pass 216"
    result = subprocess.run(
        [gap, "-q", str(SCRIPT.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    assert "PASS (27/27 checks)" in result.stdout, result.stdout
    assert "Syntax warning" not in result.stdout, result.stdout
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_pass216_gap_certificate_and_dual_chirality() -> None:
    cert = _certificate()
    assert cert["schema"] == "w33.pass216.q43_dual_ovoid_carrier.gap.v1"
    assert cert["producer"].startswith("GAP ")
    assert cert["status"] == "PASS"
    assert len(cert["checks"]) == 27
    assert all(cert["checks"].values())

    dual = cert["dual_geometry"]
    assert dual["W33"] == {
        "spreads": 36,
        "ovoids": 0,
        "noncollinear_span": 4,
    }
    assert dual["Q43"] == {
        "spreads": 0,
        "ovoids": 36,
        "noncollinear_span": 2,
    }
    assert "+36" in dual["spread_ovoid_imbalance"]
    assert "-36" in dual["spread_ovoid_imbalance"]
    assert "not an Euler characteristic" in dual["spread_ovoid_imbalance"]


def test_pass216_route_shell_and_owner_design() -> None:
    cert = _certificate()
    shell = cert["route_shell"]
    assert shell["double_sixes"] == shell["common_zero_q_ovoids"] == 36
    assert shell["generator_equivariance_cases"] == 1440

    design = cert["owner_design"]
    assert design["per_ovoid"] == {
        "points_on": 10,
        "points_off": 30,
        "owner_blocks": 15,
        "block_size": 4,
        "replication": 6,
        "pair_lambda": 2,
    }
    assert design["owner_map"] == (
        "30 external points -> 15 duad blocks with uniform fibre 2"
    )
    assert design["duad_equivariance_cases"] == 10800
    assert "full common perp" in design["mate_theorem"]
    assert "antiregular span equal to the pair" in design["mate_theorem"]


def test_pass216_complete_carrier_path_bijection() -> None:
    cert = _certificate()
    carrier = cert["carrier"]
    assert carrier["factorization"] == (
        "4320=36 ovoids * 15 duads * 2 owner-mate endpoints * 4 owner choices"
    )
    assert carrier["stage_sizes"] == [36, 540, 1080, 4320]
    assert carrier["stage_stabilizers"] == [
        "S6 order 720",
        "C2 x S4 order 48",
        "S4 order 24",
        "S3 order 6",
    ]
    assert carrier["paths"] == 4320
    assert carrier["equivariance_cases"] == 8640

    bijection = cert["bijection"]
    assert len(bijection) == 4320
    assert len({tuple(row["source"]) for row in bijection}) == 4320
    assert len({tuple(row["target"]) for row in bijection}) == 4320


def test_pass216_refutes_false_mirror_and_absolute_sheet() -> None:
    refutations = _certificate()["refutations"]
    assert refutations["same_type_Q_spread_carrier"] == (
        "REFUTED: Q(4,3) has zero spreads"
    )
    assert "incidence-dual typing of Pass 212" in refutations[
        "independent_mirror_carrier"
    ]
    assert "central C2" in refutations["owner_pair_as_absolute_chirality_bit"]
    assert "+36/-36" in refutations["surviving_chirality_invariant"]
