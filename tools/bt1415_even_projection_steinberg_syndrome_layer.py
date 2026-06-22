#!/usr/bin/env python3
"""BT1415: even Q4 projection as a Steinberg/CSS syndrome ledger.

BT1412 identified the every-other Q4 clock projection as the eight-word
even-parity distance-2 layer.  BT1375 identified the concrete central C3 action
on the 81-dimensional Steinberg memory as 27 three-cycles.  BT1414 identified a
24-flag Q4 plaquette guard band.  This packet composes those facts on the
existing W33 CSS edge ledger:

    27 Steinberg central cycles * 8 even Q4 clock states = 216 syndrome rows
    216 syndrome rows + 24 Q4 plaquette guards = 240 CSS edge rows.

The parity check is binary front-end clock logic; the protected memory remains
the existing F3 Steinberg/CSS register.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1415_even_projection_steinberg_syndrome_layer.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def parity(word: list[int]) -> int:
    return sum(word) % 2


def hamming(left: list[int], right: list[int]) -> int:
    return sum(a != b for a, b in zip(left, right))


def bits_to_int(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def flip_bit(word: list[int], bit: int) -> list[int]:
    out = list(word)
    out[bit] ^= 1
    return out


def build_result() -> dict[str, Any]:
    bt1375 = load_json("data/bt1375_steinberg_cycle_operator_scheduler_lift.json")
    bt1412 = load_json("data/bt1412_toroidal_q4_oscillator_boundary.json")
    bt1414 = load_json("data/bt1414_csaszar_szilassi_dual_physical_port.json")

    even_projection = bt1412["q4_toroidal_clock"]["even_projection"]
    even_words = [list(row) for row in even_projection["vertices"]]
    even_ticks = even_projection["ticks"]
    central_cycles = int(bt1375["central_operator"]["cycle_length_profile"]["3"])

    syndrome_rows = []
    for cycle_id in range(central_cycles):
        for clock_state, (tick, word) in enumerate(zip(even_ticks, even_words)):
            syndrome_rows.append(
                {
                    "css_edge_index": cycle_id * len(even_words) + clock_state,
                    "row_type": "EVEN_Q4_PARITY_SYNDROME",
                    "steinberg_central_cycle": cycle_id,
                    "even_clock_state": clock_state,
                    "q4_tick": tick,
                    "q4_word": word,
                    "binary_check_vector": [1, 1, 1, 1],
                    "allowed_parity": 0,
                    "syndrome_if_clean": parity(word),
                }
            )

    guard_rows = []
    for offset, guard in enumerate(bt1414["guard_band_rows"]):
        guard_rows.append(
            {
                "css_edge_index": len(syndrome_rows) + offset,
                "row_type": "Q4_PLAQUETTE_GUARD",
                "tomotope_flag": guard["tomotope_flag"],
                "q4_plaquette": guard["q4_plaquette"],
                "guard_role": guard["role"],
            }
        )

    single_bit_error_rows = []
    for clock_state, word in enumerate(even_words):
        for bit in range(4):
            errored = flip_bit(word, bit)
            single_bit_error_rows.append(
                {
                    "even_clock_state": clock_state,
                    "source_tick": even_ticks[clock_state],
                    "source_word": word,
                    "flipped_bit": bit,
                    "errored_word": errored,
                    "errored_tick": bits_to_int(errored),
                    "syndrome": parity(errored),
                }
            )

    pairwise_distances = [
        hamming(left, right) for left, right in combinations(even_words, 2)
    ]
    total_rows = len(syndrome_rows) + len(guard_rows)
    external_literature_audit = {
        "status": "heuristic_only_not_a_validation_source",
        "primary_paper": {
            "title": "Golden Quartic Polynomial and Moebius-Ball Electron",
            "author": "Hans H. Otto",
            "url": "https://www.scirp.org/pdf/jamp_2022053015152222.pdf",
            "reading": (
                "The proposal uses golden-ratio/quartic and icosahedral/Moebius-ball "
                "structure as an electron-shape model. BT1415 only borrows the "
                "closed-loop/toroidal-field caution: keep topology, chirality, and "
                "scale normalization separated."
            ),
        },
        "newer_related_work": [
            {
                "title": "Can Artificial Intelligence Help to Verify the Most Probable Electron Structure Model",
                "url": "https://www.researchgate.net/publication/389905106_Can_Artificial_Intelligence_Help_to_Verify_the_Most_Probable_Electron_Structure_Model",
                "reading": "Related 2025 ResearchGate preprint around the same electron-model program.",
            },
            {
                "title": "Critical Review of Zitterbewegung Electron Models",
                "url": "https://www.mdpi.com/2073-8994/17/3/360",
                "reading": "Recent review framing extended electron models as Zitterbewegung/field-dynamics hypotheses.",
            },
        ],
        "repo_boundary": (
            "The repo's exact quartic frontier remains the two independent D4 "
            "quartic atoms in scripts/w33_standard_model_minimal_magic_audit.py. "
            "The Moebius-ball paper is not used as evidence for electron mass, "
            "spin, or a physical waveguide layout."
        ),
    }

    checks = {
        "bt1375_steinberg_operator_loaded": bt1375["verified"] is True,
        "bt1412_even_projection_loaded": bt1412["verified"] is True,
        "bt1414_dual_port_loaded": bt1414["verified"] is True,
        "even_projection_has_eight_words": len(even_words) == 8,
        "even_projection_is_parity_zero": all(parity(word) == 0 for word in even_words),
        "even_projection_min_distance_two": min(pairwise_distances) == 2,
        "single_bit_q4_errors_toggle_syndrome": all(
            row["syndrome"] == 1 for row in single_bit_error_rows
        ),
        "steinberg_has_27_central_cycles": central_cycles == 27,
        "syndrome_rows_are_27_times_8": len(syndrome_rows) == 27 * 8 == 216,
        "guard_rows_are_bt1414_guard_band": len(guard_rows)
        == bt1414["port_summary"]["guard_slots"]
        == 24,
        "syndrome_plus_guard_rows_fill_css_edge_ledger": total_rows
        == bt1375["chain_complex"]["C1_edges"]
        == 240,
        "steinberg_memory_dimension_is_81": bt1375["chain_complex"]["basis_vectors"]
        == 81
        and central_cycles * 3 == 81,
        "central_nilpotent_rank_profile_preserved": bt1375["central_operator"][
            "nilpotent_rank_profile"
        ]
        == [54, 27, 0],
        "guard_rows_occupy_css_tail": [row["css_edge_index"] for row in guard_rows]
        == list(range(216, 240)),
        "external_audit_is_boundary_only": external_literature_audit["status"]
        == "heuristic_only_not_a_validation_source",
    }

    return {
        "bt": 1415,
        "title": "Even Q4 projection Steinberg/CSS syndrome layer",
        "verified": all(checks.values()),
        "syndrome_summary": {
            "steinberg_central_cycles": central_cycles,
            "even_q4_clock_states": len(even_words),
            "parity_syndrome_rows": len(syndrome_rows),
            "q4_plaquette_guard_rows": len(guard_rows),
            "css_edge_ledger_rows": total_rows,
            "identity": "27 central cycles * 8 even Q4 states + 24 plaquette guards = 240 CSS edge rows",
            "field_boundary": "binary Q4 clock syndrome front-end over F2; Steinberg/CSS memory remains over F3",
        },
        "single_bit_error_profile": {
            "tested_edges": len(single_bit_error_rows),
            "unique_odd_error_words": len(
                {tuple(row["errored_word"]) for row in single_bit_error_rows}
            ),
            "all_single_bit_errors_detected": all(
                row["syndrome"] == 1 for row in single_bit_error_rows
            ),
            "sample": single_bit_error_rows[:12],
        },
        "syndrome_rows_sample": syndrome_rows[:16],
        "guard_rows": guard_rows,
        "external_literature_audit": external_literature_audit,
        "physical_reading": (
            "The packet clock supplies a cheap binary front-end check: every "
            "allowed every-other Q4 state has even parity, and every one-bit "
            "clock fault toggles it. Repeating the eight allowed states over the "
            "27 Steinberg central cycles gives 216 rows; the 24 Q4 plaquette "
            "guards fill the remaining W33 CSS edge ledger rows."
        ),
        "boundary": (
            "BT1415 is a finite syndrome-ledger and scheduling certificate. It "
            "does not replace the W33 CSS stabilizer construction, does not claim "
            "a physical electron model, and does not promote external Moebius-ball "
            "electron papers as evidence for the repo's exact quartic atoms."
        ),
        "syndrome_rows": syndrome_rows,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "css_edge_ledger_rows": result["syndrome_summary"][
                    "css_edge_ledger_rows"
                ],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
