#!/usr/bin/env python3
"""BT1595: identify the 77760-tick witness loop with the Witting matter shell."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays,
    find_tetrads,
    memberships,
)

OUT = ROOT / "data" / "bt1595_witting_matter_fuel_bijection.json"
MD = ROOT / "analysis" / "BT1595_witting_matter_fuel_bijection.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def build_reject_pairs() -> dict[int, list[int]]:
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    _ray_to_bases, pair_to_bases = memberships(tetrads)
    by_source: dict[int, list[int]] = {}
    for source_ray in range(40):
        incompatible = [
            target_ray
            for target_ray in range(40)
            if not pair_to_bases.get((source_ray, target_ray), [])
        ]
        by_source[source_ray] = incompatible
    return by_source


def main() -> None:
    witting = load_json("data/bt1408_witting_contextual_communication_bridge.json")
    lanes = load_json("data/bt1590_full_witness_lane_sheet_compiler.json")
    alphabet = load_json("data/bt1593_lg_mode_alphabet_selector.json")
    hesse_loop = load_json("data/bt1594_hesse_t_universality_witness_loop.json")

    reject_by_source = build_reject_pairs()
    rows = []
    source_hist: Counter[int] = Counter()
    gate_hist: Counter[str] = Counter()
    gate_source_hist: dict[str, Counter[int]] = {}
    sector_hist: Counter[int] = Counter()
    word_hist: Counter[int] = Counter()
    address_hist: Counter[int] = Counter()
    pair_set: set[tuple[int, int]] = set()

    witness_gates = lanes["segment_grid"]["witness_gates"]
    for gate_index, gate in enumerate(witness_gates):
        for local_address in range(216):
            segment_index = gate_index * 216 + local_address
            sector_id = local_address // 24
            word_index = local_address % 24
            source_ray = gate_index * 8 + local_address // 27
            incompatible_index = local_address % 27
            target_ray = reject_by_source[source_ray][incompatible_index]
            pair = (source_ray, target_ray)
            pair_set.add(pair)
            source_hist[source_ray] += 1
            gate_hist[gate] += 1
            gate_source_hist.setdefault(gate, Counter())[source_ray] += 1
            sector_hist[sector_id] += 1
            word_hist[word_index] += 1
            address_hist[local_address] += 1
            rows.append(
                {
                    "fuel_segment": segment_index,
                    "witness_gate": gate,
                    "gate_index": gate_index,
                    "local_abi_address": local_address,
                    "sector_id": sector_id,
                    "word_index": word_index,
                    "witting_source_ray": source_ray,
                    "witting_incompatible_index": incompatible_index,
                    "witting_target_ray": target_ray,
                    "witting_pair": [source_ray, target_ray],
                    "segment_tick_start": segment_index * 72,
                    "segment_tick_end": segment_index * 72 + 71,
                    "address_formula": "local_abi_address = sector_id*24 + word_index",
                    "matter_formula": "source_ray = gate_index*8 + floor(local_abi_address/27)",
                }
            )

    all_reject_pairs = {
        (source, target)
        for source, targets in reject_by_source.items()
        for target in targets
    }
    checks = {
        "witting_verified": witting["verified"] is True,
        "lane_sheet_verified": lanes["verified"] is True,
        "alphabet_verified": alphabet["verified"] is True,
        "hesse_loop_verified": hesse_loop["verified"] is True,
        "witting_reject_shell_is_1080": len(all_reject_pairs) == 40 * 27 == 1080,
        "each_witting_source_has_27_rejects": sorted(
            len(targets) for targets in reject_by_source.values()
        )
        == [27] * 40,
        "witness_loop_has_1080_segments": lanes["counts"]["segments"] == 1080,
        "fuel_rows_biject_reject_pairs": len(rows)
        == len(pair_set)
        == len(all_reject_pairs)
        and pair_set == all_reject_pairs,
        "one_gate_is_216_addresses": all(value == 216 for value in gate_hist.values()),
        "one_gate_covers_8_sources_times_27_targets": all(
            len(hist) == 8 and sorted(hist.values()) == [27] * 8
            for hist in gate_source_hist.values()
        ),
        "five_gates_cover_all_40_witting_sources": sorted(source_hist)
        == list(range(40))
        and sorted(source_hist.values()) == [27] * 40,
        "sector_word_address_profiles_survive": sorted(sector_hist.values())
        == [120] * 9
        and sorted(word_hist.values()) == [45] * 24
        and sorted(address_hist.values()) == [5] * 216,
        "fuel_tick_budget_is_bt1594_loop": len(rows) * 72
        == hesse_loop["overlay_identity"]["total_ticks"]
        == 77760,
        "one_hesse_grid_per_reject_pair": sum(
            hesse_loop["hesse_outcome_counts"].values()
        )
        == len(rows) * 9,
    }
    result = {
        "bt": 1595,
        "title": "Witting matter-shell bijection for the 77760-tick witness loop",
        "verified": all(checks.values()),
        "source_packets": {
            "witting_bridge": "data/bt1408_witting_contextual_communication_bridge.json",
            "lane_sheet": "data/bt1590_full_witness_lane_sheet_compiler.json",
            "lg_mode_alphabet": "data/bt1593_lg_mode_alphabet_selector.json",
            "hesse_t_loop": "data/bt1594_hesse_t_universality_witness_loop.json",
        },
        "identity": {
            "witting_reject_pairs": "40 rays * 27 incompatible targets = 1080",
            "holonet_witness_segments": "5 gates * 9 recenter sectors * 24 words = 1080",
            "per_gate_refinement": "9*24 = 216 = 8 Witting source rays * 27 incompatible targets",
            "tick_identity": "1080 contextual fuel segments * 72 ticks = 77760",
        },
        "counts": {
            "fuel_segments": len(rows),
            "witting_sources": len(reject_by_source),
            "reject_targets_per_source": 27,
            "witness_gates": len(witness_gates),
            "sources_per_gate": 8,
            "local_abi_addresses_per_gate": 216,
            "ticks": len(rows) * 72,
        },
        "gate_source_blocks": {
            gate: {
                "source_rays": sorted(hist),
                "reject_pairs": sum(hist.values()),
            }
            for gate, hist in gate_source_hist.items()
        },
        "histograms": {
            "gate_segments": dict(sorted(gate_hist.items())),
            "sector_segments": dict(sorted(sector_hist.items())),
            "word_segments": dict(sorted(word_hist.items())),
            "source_reject_pairs": dict(sorted(source_hist.items())),
        },
        "fuel_rows_sample": rows[:18] + rows[-18:],
        "interpretation": (
            "BT1595 shows the BT1590/BT1594 77760-tick witness loop is not an "
            "arbitrary validation sweep. It is exactly the Witting incompatible "
            "ordered-pair shell: every rejected delayed-query pair becomes one "
            "72-tick contextual fuel segment carrying the OAM address and Hesse/T "
            "microframe."
        ),
        "honesty_boundary": (
            "This is a finite bijection and timing certificate. It does not prove "
            "cryptographic security, optical loss tolerance, or magic-state injection fidelity."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1595 Witting Matter-Shell Fuel Bijection\n\n"
        "BT1595 identifies the `77760`-tick OAM/Hesse witness loop with the "
        "Witting incompatible ordered-pair shell.  The equality is exact:\n\n"
        "```text\n"
        "40 Witting rays * 27 incompatible targets = 1080 reject pairs\n"
        "5 witness gates * 9 recenter sectors * 24 words = 1080 witness segments\n"
        "1080 * 72 ticks = 77760 ticks\n"
        "```\n\n"
        "Per gate, `9*24=216=8*27`, so each witness gate consumes the full "
        "incompatible shell of eight Witting source rays.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1595,
                "verified": result["verified"],
                "fuel_segments": len(rows),
                "ticks": len(rows) * 72,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
