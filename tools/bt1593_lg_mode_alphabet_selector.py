#!/usr/bin/env python3
"""BT1593: explicit Laguerre-Gaussian mode alphabet and 24-word selector handoff."""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1495_72_tick_transaction_word_compiler import compile_word

OUT = ROOT / "data" / "bt1593_lg_mode_alphabet_selector.json"
MD = ROOT / "analysis" / "BT1593_lg_mode_alphabet_selector.md"

TRANSLATIONS = [
    (0, 0),
    (1, 0),
    (2, 0),
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def build_words() -> list[dict]:
    perms = sorted(itertools.permutations(range(4)))
    return [compile_word(i, perm) for i, perm in enumerate(perms)]


def mode_for_shift(shift: tuple[int, int]) -> dict:
    x_shift, z_shift = shift
    sector_id = 3 * x_shift + z_shift
    ell = sector_id - 4
    radial_shell = (x_shift + 2 * z_shift) % 3
    return {
        "sector_id": sector_id,
        "affine_shift": list(shift),
        "sector_label": f"X{x_shift}Z{z_shift}",
        "lg_radial_shell_p": radial_shell,
        "lg_oam_charge_ell": ell,
        "mode_label": f"LG(p={radial_shell}, ell={ell:+d})",
        "inverse_sector_id": ell + 4,
        "inverse_shift": [(ell + 4) // 3, (ell + 4) % 3],
    }


def selector_for_word(word: dict) -> dict:
    action_index = int(word["action_index"])
    fiber_phase = action_index // 8
    d4_slot = action_index % 8
    return {
        "word_index": action_index,
        "selector_label": f"F{fiber_phase}.D{d4_slot}",
        "fiber_phase": fiber_phase,
        "d4_slot": d4_slot,
        "perm": word["perm"],
        "order": word["order"],
        "word_level": word["level"],
        "ticks": word["tick_count"],
        "handoff": (
            "LG sector mode fixes the affine recenter row; the 24-word selector "
            "chooses the centered S4 fiber action without expanding the OAM alphabet."
        ),
    }


def main() -> None:
    tomography = load_json("data/bt1592_synthetic_lab_tomography_harness.json")
    tx = load_json("data/bt1495_72_tick_transaction_word_compiler.json")
    words = build_words()

    modes = [mode_for_shift(shift) for shift in TRANSLATIONS]
    selectors = [selector_for_word(word) for word in words]
    address_rows = []
    for mode in modes:
        for selector in selectors:
            address = mode["sector_id"] * 24 + selector["word_index"]
            address_rows.append(
                {
                    "address": address,
                    "sector_id": mode["sector_id"],
                    "affine_shift": mode["affine_shift"],
                    "mode_label": mode["mode_label"],
                    "lg_oam_charge_ell": mode["lg_oam_charge_ell"],
                    "lg_radial_shell_p": mode["lg_radial_shell_p"],
                    "word_index": selector["word_index"],
                    "selector_label": selector["selector_label"],
                    "word_level": selector["word_level"],
                    "fiber_phase": selector["fiber_phase"],
                    "d4_slot": selector["d4_slot"],
                    "address_formula": "sector_id*24 + word_index",
                }
            )

    ell_values = [mode["lg_oam_charge_ell"] for mode in modes]
    radial_shell_counts = Counter(mode["lg_radial_shell_p"] for mode in modes)
    fiber_phase_counts = Counter(selector["fiber_phase"] for selector in selectors)
    d4_slot_counts = Counter(selector["d4_slot"] for selector in selectors)
    level_address_counts = Counter(row["word_level"] for row in address_rows)
    checks = {
        "tomography_verified": tomography["verified"] is True,
        "transaction_words_verified": tx["verified"] is True,
        "nine_lg_modes": len(modes) == 9,
        "oam_charges_are_symmetric_minus4_to_4": sorted(ell_values)
        == list(range(-4, 5)),
        "mode_pairs_unique": len(
            {(mode["lg_radial_shell_p"], mode["lg_oam_charge_ell"]) for mode in modes}
        )
        == 9,
        "inverse_recovers_sector": all(
            mode["inverse_sector_id"] == mode["sector_id"]
            and mode["inverse_shift"] == mode["affine_shift"]
            for mode in modes
        ),
        "radial_shells_balanced": dict(sorted(radial_shell_counts.items()))
        == {0: 3, 1: 3, 2: 3},
        "twenty_four_selectors": len(selectors) == 24,
        "fiber_phases_balanced": dict(sorted(fiber_phase_counts.items()))
        == {0: 8, 1: 8, 2: 8},
        "d4_slots_balanced": dict(sorted(d4_slot_counts.items()))
        == {slot: 3 for slot in range(8)},
        "addresses_216": len(address_rows) == 216,
        "addresses_unique_and_contiguous": sorted(
            row["address"] for row in address_rows
        )
        == list(range(216)),
        "native_and_relabel_address_counts": dict(sorted(level_address_counts.items()))
        == {"native_d4_square_pulse": 72, "s4_analyzer_relabel": 144},
    }
    result = {
        "bt": 1593,
        "title": "Explicit LG mode alphabet and 24-word selector handoff",
        "verified": all(checks.values()),
        "source_packets": {
            "tomography_harness": "data/bt1592_synthetic_lab_tomography_harness.json",
            "transaction_words": "data/bt1495_72_tick_transaction_word_compiler.json",
        },
        "mode_rule": {
            "sector_id": "3*x_shift + z_shift",
            "oam_charge_ell": "sector_id - 4, giving ell=-4..4",
            "radial_shell_p": "(x_shift + 2*z_shift) mod 3",
            "inverse": "sector_id=ell+4, x=floor(sector_id/3), z=sector_id mod 3",
        },
        "selector_rule": {
            "fiber_phase": "word_index//8",
            "d4_slot": "word_index mod 8",
            "address": "sector_id*24 + word_index",
            "claim": "216 finite addresses use 9 physical sector modes plus a 24-word centered selector, not 216 separate OAM modes.",
        },
        "lg_mode_alphabet": modes,
        "word_selectors": selectors,
        "address_rows": address_rows,
        "counts": {
            "lg_modes": len(modes),
            "word_selectors": len(selectors),
            "finite_addresses": len(address_rows),
            "native_d4_addresses": level_address_counts["native_d4_square_pulse"],
            "s4_relabel_addresses": level_address_counts["s4_analyzer_relabel"],
        },
        "interpretation": (
            "BT1593 fixes the nine recenter sectors as LG modes with symmetric OAM "
            "charges ell=-4..4 and balanced radial shells p=0,1,2. The centered "
            "24-word S4 selector is a separate handoff layer, yielding 216 addresses "
            "without requiring 216 raw OAM channels."
        ),
        "honesty_boundary": (
            "This is an explicit mode alphabet and selector ABI. It is not a fabrication "
            "tolerance, mode-purity measurement, or loss budget."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1593 LG Mode Alphabet Selector\n\n"
        "BT1593 chooses a concrete nine-mode recenter alphabet: `sector_id=3*x+z`, "
        "`ell=sector_id-4`, and `p=(x+2*z) mod 3`. The OAM charges are symmetric "
        "`-4..4`, each radial shell appears three times, and the existing 24-word "
        "centered selector gives `216` exact finite addresses through "
        "`address=sector_id*24+word_index`.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1593,
                "verified": result["verified"],
                "modes": len(modes),
                "addresses": len(address_rows),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
