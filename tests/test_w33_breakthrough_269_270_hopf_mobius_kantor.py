from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run_script(script: str) -> None:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)


def test_bt269_hopf_dimensions_and_uniqueness() -> None:
    _run_script("analysis/w33_BREAKTHROUGH_269_hopf_fibration_substrate.py")
    packet = json.loads(
        (ROOT / "data/w33_BREAKTHROUGH_269_hopf_fibration_substrate.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["quaternion_hopf"] == {
        "bundle": "S^3 -> S^7 -> S^4",
        "fiber_dim": 3,
        "total_dim": 7,
        "base_dim": 4,
    }
    assert packet["substrate_identity"] == "Phi_6 = mu + q"
    assert packet["all_three_dims_in_substrate"] is True
    assert [entry["all_match"] for entry in packet["adams_hopfs"]] == [
        False,
        True,
        False,
    ]
    assert packet["parallelizable_spheres_gt_1"] == [3, 7]


def test_bt270_mobius_kantor_q4_complementary_pair() -> None:
    _run_script("analysis/w33_BREAKTHROUGH_270_mobius_kantor_Q4_pair.py")
    packet = json.loads(
        (ROOT / "data/w33_BREAKTHROUGH_270_mobius_kantor_Q4_pair.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["mobius_kantor"]["V"] == packet["Q_4"]["V"] == 16
    assert packet["mobius_kantor"]["E"] == 24
    assert packet["Q_4"]["E"] == 32
    assert packet["mobius_kantor"]["deg"] + packet["Q_4"]["deg"] == 7
    assert packet["mobius_kantor"]["E"] + packet["Q_4"]["E"] == 56
    assert packet["complementary_identities"]["degree_sum"] == "q + mu = Phi_6 (Hopf)"
    assert packet["heawood_pairing"] == {
        "Heawood_plus_MK": 30,
        "Heawood_plus_Q4": 30,
        "common_value": "h(E_8) = 30",
    }
    assert [row["E"] for row in packet["three_cubic_bipartite_graphs"]] == [21, 24, 12]


if __name__ == "__main__":
    test_bt269_hopf_dimensions_and_uniqueness()
    test_bt270_mobius_kantor_q4_complementary_pair()
