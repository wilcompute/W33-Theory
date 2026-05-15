#!/usr/bin/env python3
"""Part DCCXXIX: Pauli-Klitzing codec ladder bridge.

Bridges three validated objects already in-repo:

1) DCCXXVIII two-qutrit Pauli geometry gives W(3,3) valency k = 12.
2) Klitzing tomotope mod_b operation ladder gives 12 -> 24 -> 48 -> 96.
3) Partial-sheet lift gives inferred mod_a ladder 24 -> 48 -> 96 -> 192.

This part proves those are one coherent doubling tower rooted at the Pauli
commutation valency and records the exact arithmetic identities.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
EXPLORATION = ROOT / "exploration"
if str(EXPLORATION) not in sys.path:
    sys.path.insert(0, str(EXPLORATION))

from verify_dccxxviii_ternary_quaternion_codec_tower import CODEC, Q, W33_K
from exploration.w33_tomotope_klitzing_partial_operation_commutation import (
    partial_a_operation_counts_inferred,
    partial_b_operation_counts,
)
from scripts.PART_CCCCCXCII_tomotope_two_192_mechanisms import build as build_two_192


OUT_PATH = ROOT / "data" / "dccxxix_pauli_klitzing_codec_ladder_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    q_value: int
    pauli_valency_12: int
    klitzing_rectified_12: int
    mod_b_omnitruncated_96: int
    mod_a_omnitruncated_192: int
    all_identities_hold: bool


def _powers_of_two_from(base: int, length: int) -> list[int]:
    return [base * (2**i) for i in range(length)]


def build_bridge() -> dict[str, Any]:
    b_ladder = partial_b_operation_counts()  # 12,24,48,96
    a_ladder = partial_a_operation_counts_inferred()  # 24,48,96,192
    two_192 = build_two_192()

    expected_b = tuple(_powers_of_two_from(W33_K, 4))
    expected_a = tuple(_powers_of_two_from(2 * W33_K, 4))

    identities = {
        "w33_pauli_valency_equals_codec_equals_12": (W33_K == CODEC == 12),
        "klitzing_mod_b_ladder_is_exactly_12_24_48_96": (b_ladder == (12, 24, 48, 96)),
        "mod_b_ladder_is_codec_times_powers_of_two": (b_ladder == expected_b),
        "mod_a_ladder_is_sheet_lift_of_mod_b": (
            a_ladder == expected_a and all(a == 2 * b for a, b in zip(a_ladder, b_ladder))
        ),
        "mod_a_omnitruncated_192_matches_two_192_mechanism_carrier": (
            a_ladder[-1] == 192 and two_192.tomotope_flag_carrier_192 == 192
        ),
        "omnitruncated_step_ratio_is_two": (
            b_ladder[-1] // b_ladder[-2] == 2 and a_ladder[-1] // a_ladder[-2] == 2
        ),
        "full_codec_tower_is_12_times_1_2_4_8_16": (
            [*b_ladder, a_ladder[-1]] == [12, 24, 48, 96, 192]
            and a_ladder[-1] // W33_K == 16
        ),
        "q_three_explains_eightfold_operation_growth_as_2_to_q": (
            Q == 3 and b_ladder[-1] // b_ladder[0] == 2**Q
        ),
    }

    summary = BridgeSummary(
        q_value=Q,
        pauli_valency_12=W33_K,
        klitzing_rectified_12=b_ladder[0],
        mod_b_omnitruncated_96=b_ladder[-1],
        mod_a_omnitruncated_192=a_ladder[-1],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "ladders": {
            "mod_b_direct": list(b_ladder),
            "mod_a_sheet_lift": list(a_ladder),
            "stage_names": [
                "rectified",
                "truncated",
                "maximal_expanded",
                "omnitruncated",
            ],
        },
        "bridge_claim": {
            "statement": (
                "The Klitzing operation ladder is a Pauli-anchored codec doubling tower: "
                "W(3,3) valency k=12 is the rectified base, mod_b runs 12->24->48->96, "
                "and sheet lifting yields mod_a 24->48->96->192."
            )
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
