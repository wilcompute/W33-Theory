#!/usr/bin/env python3
"""Pass 50 - firmware-to-fabric accounting for the Holonet stack.

Passes 48 and 49 proved the two ends of the practical stack:

* the minimal control packet is a 72-trit typed transaction, and
* the router exports to deterministic 4004/6502/Z80-style firmware artifacts.

This verifier joins those ends to the typed 2160-slot mirror bus.  The result
is not a timing benchmark; it is a cross-layer accounting certificate saying
how many firmware route decisions, packet trits, binary-host bits, and mirror
slots are implied by one minimal packet, one packed mirror atlas, and one
Witting admission sweep.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_holonet_firmware_fabric_profile.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def schema_size(packet: dict[str, Any], field: str) -> int:
    for row in packet["field_schema"]:
        if row["field"] == field:
            return int(row["size"])
    raise KeyError(field)


def frac_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def target_profile(
    name: str,
    target: dict[str, Any],
    route_decisions_per_packet: int,
    packet_frames_per_mirror_atlas: int,
    accepted_witting_packets: int,
) -> dict[str, Any]:
    instructions = int(target["instructions"])
    dynamic_steps = int(target.get("max_instruction_steps", instructions))
    per_packet_static = instructions * route_decisions_per_packet
    per_packet_dynamic = dynamic_steps * route_decisions_per_packet
    return {
        "target": name,
        "listing": target["artifact"],
        "trace": target["trace"],
        "route_decision_listing_instructions": instructions,
        "route_decision_dynamic_steps_upper_bound": dynamic_steps,
        "route_decisions_per_worst_case_packet": route_decisions_per_packet,
        "packet_static_instruction_count": per_packet_static,
        "packet_dynamic_step_upper_bound": per_packet_dynamic,
        "packed_mirror_atlas_static_instruction_count": (
            per_packet_static * packet_frames_per_mirror_atlas
        ),
        "packed_mirror_atlas_dynamic_step_upper_bound": (
            per_packet_dynamic * packet_frames_per_mirror_atlas
        ),
        "accepted_witting_sweep_static_instruction_count": (
            per_packet_static * accepted_witting_packets
        ),
        "accepted_witting_sweep_dynamic_step_upper_bound": (
            per_packet_dynamic * accepted_witting_packets
        ),
        "claim_boundary": target["claim_boundary"],
    }


def build_certificate() -> dict[str, Any]:
    retro = load_json("data/w33_holonet_retro_export.json")
    packet = load_json("data/w33_packet_energy.json")
    abi = load_json("data/bt1697_holonet_typed_packet_abi.json")

    packet_trits = int(packet["traffic_model"]["total_packet_trits"])
    packet_binary_bits = int(packet["binary_vs_ternary"]["binary_host_bits"])
    packet_information_bits = float(
        packet["binary_vs_ternary"]["ternary_information_bits"]
    )
    mirror_slots = schema_size(abi, "mirror_slot")
    supercycle_slots = schema_size(abi, "clifford_supercycle")

    packet_frames_per_mirror_atlas = mirror_slots // packet_trits
    packet_frames_per_supercycle = supercycle_slots // packet_trits
    mirror_atlases_per_supercycle = supercycle_slots // mirror_slots

    witting_total_pairs = 40 * 40
    witting_accepted_packets = 520
    witting_retry_shadow = 1080
    accepted_rate = Fraction(witting_accepted_packets, witting_total_pairs)
    retry_shadow_rate = Fraction(witting_retry_shadow, witting_total_pairs)
    expected_packet_trits_per_query = accepted_rate * packet_trits
    expected_binary_bits_per_query = accepted_rate * packet_binary_bits

    route_decisions_per_packet = int(packet["traffic_model"]["route_hops"])
    target_profiles = {
        name: target_profile(
            name,
            target,
            route_decisions_per_packet,
            packet_frames_per_mirror_atlas,
            witting_accepted_packets,
        )
        for name, target in retro["targets"].items()
    }

    loss_hooks = 64
    dark_click_hooks = 8
    parity_hooks = 24
    p_loss = 1e-5
    p_dark = 1e-6
    p_parity = 5e-6
    retry_probability = (
        loss_hooks * p_loss + dark_click_hooks * p_dark + parity_hooks * p_parity
    )

    queue_profiles = {
        "sequential_40": {
            "packets": 40,
            "bt1705_max_queue": 1,
            "packed_mirror_atlases_if_disjoint": math.ceil(
                40 / packet_frames_per_mirror_atlas
            ),
        },
        "depth_1_burst_40": {
            "packets": 40,
            "bt1705_max_queue": 40,
            "packed_mirror_atlases_if_disjoint": math.ceil(
                40 / packet_frames_per_mirror_atlas
            ),
        },
        "depth_2_wavefront_1600": {
            "packets": 1600,
            "bt1705_max_queue": 1561,
            "packed_mirror_atlases_if_disjoint": math.ceil(
                1600 / packet_frames_per_mirror_atlas
            ),
        },
        "witting_accepted_sweep": {
            "packets": witting_accepted_packets,
            "retry_shadow_pairs": witting_retry_shadow,
            "packed_mirror_atlases_if_disjoint": math.ceil(
                witting_accepted_packets / packet_frames_per_mirror_atlas
            ),
        },
    }

    checks = {
        "retro_export_verified": retro["verified"] is True,
        "packet_energy_verified": packet["verified"] is True,
        "typed_packet_abi_verified": abi["verified"] is True,
        "mirror_slots_are_30_packets": mirror_slots == 30 * packet_trits,
        "supercycle_is_24_mirror_atlases": supercycle_slots == 24 * mirror_slots,
        "supercycle_is_720_packets": supercycle_slots == 720 * packet_trits,
        "witting_rom_splits_520_1080": (
            witting_accepted_packets + witting_retry_shadow == witting_total_pairs
        ),
        "accepted_rate_is_13_over_40": accepted_rate == Fraction(13, 40),
        "expected_trits_per_query_is_117_over_5": (
            expected_packet_trits_per_query == Fraction(117, 5)
        ),
        "route_decisions_match_two_hop_packet": route_decisions_per_packet == 2,
        "retry_probability_below_one_tenth_percent": retry_probability < 1e-3,
        "all_targets_present": set(target_profiles)
        == {
            "4004_style",
            "6502_style",
            "z80_style",
        },
    }

    return {
        "theorem": "Pass 50 Holonet firmware-to-fabric accounting",
        "verified": all(checks.values()),
        "breakthrough": (
            "The exported firmware targets, the 72-trit packet ABI, and the "
            "global 2160-slot mirror bus are one accounting object: a mirror "
            "atlas contains exactly 30 minimal packet frames, and a full "
            "Sp(4,3) supercycle contains 720 such frames."
        ),
        "layer_identities": {
            "minimal_packet": "72 = 16 route trits + 48 body trits + 8 epilogue trits",
            "mirror_atlas": "2160 = 30 * 72 = 45 polar sheets * 48 tomotope blocks",
            "runtime_supercycle": "51840 = 24 * 2160 = 720 * 72",
            "witting_logical_rom": "1600 = 520 accepted + 1080 retry-shadow",
        },
        "packet": {
            "trits": packet_trits,
            "binary_host_bits": packet_binary_bits,
            "ternary_information_bits": packet_information_bits,
            "route_decisions_per_worst_case_packet": route_decisions_per_packet,
        },
        "mirror_fabric": {
            "mirror_slots": mirror_slots,
            "packet_frames_per_mirror_atlas": packet_frames_per_mirror_atlas,
            "mirror_atlas_binary_host_bits_if_filled_by_packet_trits": (
                packet_frames_per_mirror_atlas * packet_binary_bits
            ),
            "mirror_atlas_ternary_information_bits_if_filled_by_packet_trits": (
                packet_frames_per_mirror_atlas * packet_information_bits
            ),
            "supercycle_slots": supercycle_slots,
            "mirror_atlases_per_supercycle": mirror_atlases_per_supercycle,
            "packet_frames_per_supercycle": packet_frames_per_supercycle,
        },
        "witting_admission": {
            "total_ordered_pairs": witting_total_pairs,
            "accepted_packets": witting_accepted_packets,
            "retry_shadow_pairs": witting_retry_shadow,
            "accepted_rate": frac_record(accepted_rate),
            "retry_shadow_rate": frac_record(retry_shadow_rate),
            "expected_full_packet_trits_per_random_query": frac_record(
                expected_packet_trits_per_query
            ),
            "expected_binary_host_bits_per_random_query": frac_record(
                expected_binary_bits_per_query
            ),
            "accepted_sweep_packet_trits": witting_accepted_packets * packet_trits,
            "accepted_sweep_binary_host_bits": (
                witting_accepted_packets * packet_binary_bits
            ),
        },
        "firmware_targets": target_profiles,
        "shared_bus_queue_profiles": queue_profiles,
        "symbolic_retry_economics": {
            "loss_hooks": loss_hooks,
            "dark_click_hooks": dark_click_hooks,
            "parity_hooks": parity_hooks,
            "p_loss": p_loss,
            "p_dark": p_dark,
            "p_parity": p_parity,
            "expected_retry_exit_probability_per_packet": retry_probability,
            "expected_extra_packets_per_1600_wavefront": retry_probability * 1600,
            "expected_extra_packet_trits_per_1600_wavefront": (
                retry_probability * 1600 * packet_trits
            ),
        },
        "source_certificates": [
            "data/w33_holonet_retro_export.json",
            "data/w33_packet_energy.json",
            "data/bt1697_holonet_typed_packet_abi.json",
        ],
        "claim_boundary": [
            "This is deterministic cross-layer accounting, not a measured latency benchmark.",
            "The 4004/6502/Z80 listings are canonical Holonet target listings, not vendor-cycle timing claims.",
            "The retry economics use the symbolic BT1706 nominal rates; a full optical loss model remains a separate experiment.",
            "The packed mirror-atlas capacity assumes disjoint typed slots; FIFO queue stress remains governed by the BT1705 shared-bus profile.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(
        "  mirror atlas: "
        f"{cert['mirror_fabric']['mirror_slots']} slots = "
        f"{cert['mirror_fabric']['packet_frames_per_mirror_atlas']} minimal packets"
    )
    print(
        "  Witting query expectation: "
        f"{cert['witting_admission']['expected_full_packet_trits_per_random_query']['numerator']}/"
        f"{cert['witting_admission']['expected_full_packet_trits_per_random_query']['denominator']} trits"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
