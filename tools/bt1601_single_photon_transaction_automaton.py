#!/usr/bin/env python3
"""BT1601: compile the 1600-frame Witting cycle into a physical automaton."""
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
from bt1598_witting_accepted_control_rail import (
    balanced_same_ray_basis_matching,
    slot_in_basis,
)

OUT = ROOT / "data" / "bt1601_single_photon_transaction_automaton.json"
MD = ROOT / "analysis" / "BT1601_single_photon_transaction_automaton.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def reject_targets_by_source(
    pair_to_bases: dict[tuple[int, int], list[int]]
) -> dict[int, list[int]]:
    return {
        source: [
            target
            for target in range(40)
            if not pair_to_bases.get((source, target), [])
        ]
        for source in range(40)
    }


def fuel_payload(
    source_ray: int,
    target_ray: int,
    reject_by_source: dict[int, list[int]],
    alphabet_by_address: dict[int, dict],
) -> dict:
    incompatible_index = reject_by_source[source_ray].index(target_ray)
    gate_index = source_ray // 8
    local_abi_address = (source_ray % 8) * 27 + incompatible_index
    sector_id = local_abi_address // 24
    word_index = local_abi_address % 24
    fuel_segment = gate_index * 216 + local_abi_address
    alphabet_row = alphabet_by_address[local_abi_address]
    return {
        "fuel_segment": fuel_segment,
        "witness_gate_index": gate_index,
        "witness_gate_source_slot": source_ray % 8,
        "witting_incompatible_index": incompatible_index,
        "local_abi_address": local_abi_address,
        "sector_id": sector_id,
        "word_index": word_index,
        "lg_mode": {
            "ell": alphabet_row["lg_oam_charge_ell"],
            "p": alphabet_row["lg_radial_shell_p"],
            "label": alphabet_row["mode_label"],
            "selector_label": alphabet_row["selector_label"],
        },
    }


def accepted_payload(
    source_ray: int,
    target_ray: int,
    tetrads: list[tuple[int, int, int, int]],
    pair_to_bases: dict[tuple[int, int], list[int]],
    same_matching: dict[int, int],
    analyzer_by_basis: dict[int, dict],
) -> dict:
    common_bases = pair_to_bases[(source_ray, target_ray)]
    if source_ray == target_ray:
        selected_basis = same_matching[source_ray]
        mode = "SAME_RAY_MATCHED_CONTROL_APERTURE"
    else:
        selected_basis = common_bases[0]
        mode = "COMPATIBLE_UNIQUE_BASIS_CONTROL"
    tetrad = tetrads[selected_basis]
    source_slot = slot_in_basis(tetrad, source_ray)
    detector_slot = slot_in_basis(tetrad, target_ray)
    return {
        "control_mode": mode,
        "selected_basis": selected_basis,
        "basis_options": common_bases,
        "source_slot": source_slot,
        "detector_slot": detector_slot,
        "mirror_slot_mod_4": detector_slot,
        "tomotope_flag": 4 * selected_basis + detector_slot,
        "optical_family": analyzer_by_basis[selected_basis]["optical_family"],
    }


def frame_windows(frame_start_tick: int) -> dict[str, list[int]]:
    return {
        "source_switch": [frame_start_tick, frame_start_tick + 7],
        "program_delay": [frame_start_tick + 8, frame_start_tick + 31],
        "analyzer_or_fuel_body": [frame_start_tick + 32, frame_start_tick + 47],
        "detector_or_hesse_handoff": [frame_start_tick + 48, frame_start_tick + 63],
        "dark_reference": [frame_start_tick + 64, frame_start_tick + 71],
    }


def build_rows() -> tuple[list[dict], dict[str, Counter]]:
    control = load_json("data/bt1598_witting_accepted_control_rail.json")
    cycle = load_json("data/bt1600_full_witting_transaction_cycle.json")
    fuel = load_json("data/bt1595_witting_matter_fuel_bijection.json")
    alphabet = load_json("data/bt1593_lg_mode_alphabet_selector.json")
    analyzers = load_json("data/bt1411_witting_basis_analyzer_unitaries.json")

    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    ray_to_bases, pair_to_bases = memberships(tetrads)
    same_matching = balanced_same_ray_basis_matching(ray_to_bases, tetrads)
    reject_by_source = reject_targets_by_source(pair_to_bases)
    alphabet_by_address = {row["address"]: row for row in alphabet["address_rows"]}
    analyzer_by_basis = {row["basis_id"]: row for row in analyzers["all_analyzers"]}

    rows = []
    rail_hist: Counter[str] = Counter()
    switch_hist: Counter[str] = Counter()
    detector_slot_hist: Counter[int] = Counter()
    dark_reference_hist: Counter[str] = Counter()
    loss_placeholder_hist: Counter[str] = Counter()
    source_profile: dict[int, Counter[str]] = {}
    for source_ray in range(40):
        for target_ray in range(40):
            cycle_frame = len(rows)
            frame_start_tick = cycle_frame * 72
            accepted = bool(pair_to_bases.get((source_ray, target_ray), []))
            if accepted:
                payload = accepted_payload(
                    source_ray,
                    target_ray,
                    tetrads,
                    pair_to_bases,
                    same_matching,
                    analyzer_by_basis,
                )
                rail = "ACCEPTED_CONTROL"
                switch_bank = "WITTING_BASIS_ANALYZER_SWITCH"
                detector_slot = payload["detector_slot"]
                switch = {
                    "source_select": source_ray,
                    "target_select": target_ray,
                    "basis_select": payload["selected_basis"],
                    "delay_line": payload["selected_basis"] % 8,
                    "mirror_slot": detector_slot,
                }
                detector = {
                    "detector_slot": detector_slot,
                    "readout": "WITTING_ANALYZER_SLOT",
                    "tomotope_flag": payload["tomotope_flag"],
                    "handoff": "detector_slot -> mirror_slot mod 4 -> tomotope flag",
                }
                delay = {
                    "profile": "CONTROL_ANALYZER_DELAY",
                    "symbolic_delay_line": f"basis_{payload['selected_basis'] % 8}",
                    "coarse_delay_bank": payload["selected_basis"] // 8,
                }
            else:
                payload = fuel_payload(
                    source_ray, target_ray, reject_by_source, alphabet_by_address
                )
                rail = "CONTEXTUAL_FUEL"
                switch_bank = "OAM_HESSE_FUEL_SWITCH"
                detector_slot = payload["word_index"] % 4
                switch = {
                    "source_select": source_ray,
                    "target_select": target_ray,
                    "witness_gate_index": payload["witness_gate_index"],
                    "sector_select": payload["sector_id"],
                    "word_select": payload["word_index"],
                }
                detector = {
                    "detector_slot": detector_slot,
                    "readout": "OAM_HESSE_LANE_SLOT",
                    "local_abi_address": payload["local_abi_address"],
                    "fuel_segment": payload["fuel_segment"],
                    "handoff": "OAM sector -> 24-word lane -> Hesse/T microframe",
                }
                delay = {
                    "profile": "OAM_RECENTER_HESSE_DELAY",
                    "symbolic_delay_line": f"sector_{payload['sector_id']}",
                    "coarse_delay_bank": payload["witness_gate_index"],
                }
            dark_reference_bin = f"DARK_FRAME_{cycle_frame:04d}"
            loss_channel = f"L_{rail}_{source_ray:02d}_{target_ray:02d}"
            row = {
                "cycle_frame": cycle_frame,
                "source_ray": source_ray,
                "target_ray": target_ray,
                "rail": rail,
                "photon_id": "single_photon_transaction_packet",
                "successor_frame": (cycle_frame + 1) % 1600,
                "frame_start_tick": frame_start_tick,
                "frame_end_tick": frame_start_tick + 71,
                "frame_windows": frame_windows(frame_start_tick),
                "switch_bank": switch_bank,
                "switch": switch,
                "delay": {
                    **delay,
                    "frame_ticks": 72,
                    "calibrated_delay_ps": None,
                    "calibration_status": "PLACEHOLDER_REQUIRED",
                },
                "detector": detector,
                "loss_placeholder": {
                    "symbolic_loss_channel": loss_channel,
                    "calibrated_loss_db": None,
                    "dark_count_probability": None,
                    "calibration_status": "PLACEHOLDER_REQUIRED",
                },
                "dark_reference": {
                    "bin": dark_reference_bin,
                    "tick_window": [frame_start_tick + 64, frame_start_tick + 71],
                    "role": "per-frame dark/reference subtraction placeholder",
                },
                "payload": payload,
            }
            rows.append(row)
            rail_hist[rail] += 1
            switch_hist[switch_bank] += 1
            detector_slot_hist[detector_slot] += 1
            dark_reference_hist[dark_reference_bin] += 1
            loss_placeholder_hist[loss_channel] += 1
            source_profile.setdefault(source_ray, Counter())[rail] += 1

    histograms = {
        "rail": rail_hist,
        "switch_bank": switch_hist,
        "detector_slot": detector_slot_hist,
        "dark_reference": dark_reference_hist,
        "loss_placeholder": loss_placeholder_hist,
    }
    checks = {
        "cycle_verified": cycle["verified"] is True,
        "control_verified": control["verified"] is True,
        "fuel_verified": fuel["verified"] is True,
        "alphabet_verified": alphabet["verified"] is True,
        "analyzers_verified": analyzers["verified"] is True,
        "single_automaton_has_1600_frames": len(rows) == 1600,
        "tick_budget_is_115200": rows[-1]["frame_end_tick"] + 1 == 115200,
        "rail_histogram_is_520_1080": dict(sorted(rail_hist.items()))
        == {"ACCEPTED_CONTROL": 520, "CONTEXTUAL_FUEL": 1080},
        "switch_bank_histogram_matches_rails": dict(sorted(switch_hist.items()))
        == {
            "OAM_HESSE_FUEL_SWITCH": 1080,
            "WITTING_BASIS_ANALYZER_SWITCH": 520,
        },
        "detector_slots_balanced_across_whole_cycle": dict(
            sorted(detector_slot_hist.items())
        )
        == {0: 400, 1: 400, 2: 400, 3: 400},
        "each_source_has_13_control_27_fuel": all(
            dict(hist) == {"ACCEPTED_CONTROL": 13, "CONTEXTUAL_FUEL": 27}
            for hist in source_profile.values()
        ),
        "successor_relation_is_closed_cycle": all(
            row["successor_frame"] == (row["cycle_frame"] + 1) % 1600 for row in rows
        ),
        "every_frame_has_loss_placeholder": sorted(loss_placeholder_hist.values())
        == [1] * 1600,
        "every_frame_has_dark_reference": sorted(dark_reference_hist.values())
        == [1] * 1600,
        "single_photon_label_conserved": {row["photon_id"] for row in rows}
        == {"single_photon_transaction_packet"},
        "dark_reference_window_is_last_eight_ticks": all(
            row["frame_windows"]["dark_reference"]
            == [row["frame_start_tick"] + 64, row["frame_start_tick"] + 71]
            for row in rows
        ),
    }
    histograms["checks"] = Counter({key: int(value) for key, value in checks.items()})
    if not all(checks.values()):
        raise RuntimeError(checks)
    return rows, histograms


def main() -> None:
    rows, histograms = build_rows()
    checks = {key: bool(value) for key, value in histograms.pop("checks").items()}
    result = {
        "bt": 1601,
        "title": "Single-photon Witting transaction automaton",
        "verified": all(checks.values()),
        "source_packets": {
            "full_witting_cycle": "data/bt1600_full_witting_transaction_cycle.json",
            "accepted_control": "data/bt1598_witting_accepted_control_rail.json",
            "contextual_fuel": "data/bt1595_witting_matter_fuel_bijection.json",
            "lg_alphabet": "data/bt1593_lg_mode_alphabet_selector.json",
            "analyzers": "data/bt1411_witting_basis_analyzer_unitaries.json",
        },
        "automaton_identity": {
            "carrier": "one single-photon transaction packet",
            "states": "1600 ordered Witting pair frames",
            "ticks": "1600 frames * 72 ticks = 115200",
            "switch_split": "520 Witting analyzer frames + 1080 OAM/Hesse fuel frames",
            "detector_slots": "accepted 130 per slot + fuel 270 per slot = 400 per slot",
        },
        "frame_template": {
            "source_switch": "ticks 0..7",
            "program_delay": "ticks 8..31",
            "analyzer_or_fuel_body": "ticks 32..47",
            "detector_or_hesse_handoff": "ticks 48..63",
            "dark_reference": "ticks 64..71",
        },
        "counts": {
            "frames": len(rows),
            "ticks": rows[-1]["frame_end_tick"] + 1,
            "accepted_control_frames": histograms["rail"]["ACCEPTED_CONTROL"],
            "contextual_fuel_frames": histograms["rail"]["CONTEXTUAL_FUEL"],
            "dark_reference_placeholders": len(histograms["dark_reference"]),
            "loss_placeholders": len(histograms["loss_placeholder"]),
        },
        "histograms": {
            "rail": dict(sorted(histograms["rail"].items())),
            "switch_bank": dict(sorted(histograms["switch_bank"].items())),
            "detector_slot": dict(sorted(histograms["detector_slot"].items())),
        },
        "automaton_rows_sample": rows[:24] + rows[-24:],
        "interpretation": (
            "BT1601 turns the BT1600 Witting cycle into a single physical automaton. "
            "Every frame carries an explicit switch bank, delay placeholder, detector "
            "handoff, symbolic loss channel, and dark-reference bin."
        ),
        "honesty_boundary": (
            "The loss, delay, and dark-count fields are deliberately uncalibrated "
            "placeholders. This certificate compiles the physical interface; it does "
            "not claim measured optical performance."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1601 Single-Photon Transaction Automaton\n\n"
        "BT1601 compiles the full BT1600 ordered-pair cycle into one physical "
        "single-photon automaton.  The automaton has `1600` states, `115200` "
        "ticks, `520` Witting analyzer switch frames, and `1080` OAM/Hesse fuel "
        "switch frames.  Every state includes an explicit switch bank, delay "
        "placeholder, detector handoff, symbolic loss channel, and dark-reference "
        "placeholder.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1601,
                "verified": result["verified"],
                "frames": result["counts"]["frames"],
                "ticks": result["counts"]["ticks"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
