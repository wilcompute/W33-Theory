from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass7307_7309_double_six_naimark_isometry.py"
FROZEN = ROOT / "data" / "PART_W33_PASS7307_7309_DOUBLE_SIX_NAIMARK_ISOMETRY.json"


def load() -> dict:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def test_frozen_certificate_replays_byte_exact() -> None:
    result = subprocess.run(
        [sys.executable, str(SOURCE), "--check", str(FROZEN)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert "PASS frozen certificate" in result.stdout


def test_projector_and_objectwise_naimark_contract() -> None:
    payload = load()
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    assert payload["projector_resolution"] == {
        "E1": "J/36",
        "E15": "(6I+2A-J)/12",
        "E20": "(9I-3A+J)/18",
        "carrier_dimension": 36,
        "cross_gram": "(B-J/4)(N-J/3)^T=0",
        "identity": "E15+E20+E1=I36",
        "slice_gram": "(N-J/3)^T(N-J/3)=18E20",
        "split": "36 = 15 + 20 + 1",
        "visible_gram": "(B-J/4)^T(B-J/4)=18E15",
    }
    assert payload["naimark_completion"]["completed_shadow"].startswith("ETF(36,21)")


def test_integer_transform_contract() -> None:
    hardware = load()["integer_hardware_transform"]
    assert hardware["shape"] == [87, 36]
    assert hardware["identity"] == "K^T K=2592I36=(36sqrt(2))^2 I36"
    assert hardware["coefficient_census"] == {
        "-3": 1080,
        "-4": 1080,
        "6": 72,
        "8": 540,
        "9": 360,
    }


def test_prior_art_and_physics_boundaries_are_frozen() -> None:
    payload = load()
    owners = " ".join(payload["prior_art_boundary"]["already_owned"])
    for owner in ("Pass3694", "Parseval target audit", "Pass4992", "Pass7241", "Pass7249-7304"):
        assert owner in owners
    boundary = payload["physics_boundary"]
    assert "No interferometer mesh" in boundary
    assert "particle assignment" in boundary
    assert "continuum dynamics" in boundary
