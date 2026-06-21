#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool() -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "bt1408_witting_contextual_communication_bridge.py"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (
            ROOT / "data" / "bt1408_witting_contextual_communication_bridge.json"
        ).read_text(encoding="utf-8")
    )


def test_bt1408_bridge_runs_true() -> None:
    out = run_tool()
    assert out == {
        "bt": 1408,
        "key_agreement_rate": "13/40",
        "per_ray_shell": "1 same + 12 compatible + 27 incompatible = 40",
        "verified": True,
    }

    data = load_result()
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["source_paper"]["arxiv"] == "2503.18431"
    assert "34/40" in data["source_paper"]["correction_boundary"]
    assert "36/40" in data["source_paper"]["correction_boundary"]


def test_bt1408_witting_pair_shell_counts() -> None:
    data = load_result()

    assert data["witting_configuration"] == {
        "basis_size_histogram": {"4": 40},
        "orthogonal_tetrads": 40,
        "ray_membership_histogram": {"4": 40},
        "rays": 40,
        "unordered_pair_common_basis_histogram": {"0": 540, "1": 240},
    }
    assert data["communication_profile"]["ordered_pair_counts"] == {
        "same": 40,
        "compatible_distinct": 480,
        "compatible_total": 520,
        "incompatible": 1080,
        "total": 1600,
    }
    assert data["communication_profile"]["common_basis_count_histogram"] == {
        "0": 1080,
        "1": 480,
        "4": 40,
    }
    assert data["communication_profile"]["rates"] == {
        "compatible_distinct": "3/10",
        "expected_raw_rounds_per_accept": "40/13",
        "key_agreement": "13/40",
        "reject": "27/40",
        "same": "1/40",
    }
    assert set(
        tuple(sorted(shell.items()))
        for shell in data["communication_profile"]["per_ray_shells"]
    ) == {
        (
            ("compatible_distinct", 12),
            ("incompatible", 27),
            ("same", 1),
        )
    }


def test_bt1408_contextual_and_packet_abi_bridge() -> None:
    data = load_result()

    assert data["contextuality_budget"] == {
        "noncontextual_max": 36,
        "contexts": 40,
        "deficit": 4,
        "contextual_fraction": "1/10",
        "reading": (
            "Communication acceptance is 13/40, but tamper evidence is "
            "checked against the corrected BT823 36/40 contextual ceiling."
        ),
    }
    bridge = data["holonet_abi_bridge"]
    assert bridge["accepted_round_rate"] == "13/40"
    assert bridge["mirror_slot_residues"] == [0, 1, 2, 3]
    assert bridge["bt1374_address_rule"] == (
        "tomotope_flag = 4 * tomotope_block + (mirror_slot mod 4)"
    )
    assert bridge["bt1407_frame_identity"] == (
        "48 Q6 body pulse ticks + 3 Hesse return words * 8 ticks = 72 ticks"
    )
    assert [row["mirror_slot_mod_4"] for row in bridge["sample_basis_slot_map"]] == [
        0,
        1,
        2,
        3,
    ]


def test_bt1408_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    single = " ".join(
        (ROOT / "single_photon_universal_computation.tex")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "BT1408: Witting contextual communication bridge" in docs
    assert "BT1408_witting_contextual_communication_bridge.md" in docs
    assert "BT1408 Witting contextual communication bridge" in holonet
    assert (
        "1 same ray plus 12 compatible orthogonal rays plus 27 incompatible rays"
        in holonet
    )
    assert "BT1408 Witting Contextual Communication Bridge" in single


if __name__ == "__main__":
    test_bt1408_bridge_runs_true()
    test_bt1408_witting_pair_shell_counts()
    test_bt1408_contextual_and_packet_abi_bridge()
    test_bt1408_publication_anchors()
    print("BT1408 focused tests passed")
