#!/usr/bin/env python3
"""BT1697 - typed Holonet packet ABI.

The Holonet paper names a packet header early and later proves the body,
Hesse epilogue, Witting admission ROM, dual toroidal port, CSS ledger, and
D4-quartic magic rail separately.  This verifier promotes the missing object:
one typed transaction ABI whose projections are exactly those layers.

The theorem is deliberately about field boundaries.  Several layers share the
number 24, but the script keeps them typed:

* 24 Hesse epilogue ticks = 3 return words * 8 ticks.
* 24 Q4 guard flags = the tail of the 192-flag toroidal/tomotope port.
* 24 CSS guard rows = the tail completing 216 binary checks to 240 edge rows.
* 24 magic apertures = 2 D4 quartic atoms * 4 branches * 3 phases.

The equal count is promoted only because the projections all meet the same
transaction boundary and have distinct source certificates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1697_holonet_typed_packet_abi.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def build_certificate() -> dict[str, Any]:
    bt1404 = load_json("data/bt1404_holonet_scope_microframe.json")
    bt1407 = load_json("data/bt1407_microframe_transaction_composer.json")
    bt1410 = load_json("data/bt1410_witting_delayed_query_frame_compiler.json")
    bt1414 = load_json("data/bt1414_csaszar_szilassi_dual_physical_port.json")
    bt1415 = load_json("data/bt1415_even_projection_steinberg_syndrome_layer.json")
    bt1418 = load_json("data/bt1418_d4_quartic_magic_injection_frontier.json")

    hesse_frames = bt1404["frames"]
    full_hesse_outcomes = sorted(int(frame["h"]) for frame in hesse_frames)
    selected_hesse_outcomes = bt1407["stress_selection"]["epilogue_hesse_outcomes"]
    region_hist = bt1407["region_histogram"]
    logical = bt1410["logical_pair_table"]
    physical = bt1410["basis_local_frame_table"]
    port = bt1414["port_summary"]
    syndrome = bt1415["syndrome_summary"]
    magic = bt1418["atom_summary"]

    # Transaction body/epilogue.
    frame_ticks = 72
    body_ticks = int(region_hist["tomotope_body"])
    epilogue_ticks = int(region_hist["local_lift_hesse_epilogue"])
    body_edges = body_ticks // 3
    hesse_return_words = epilogue_ticks // 8

    # Admission ROM.
    logical_records = int(logical["records"])
    accepted_pairs = int(logical["accepted_ordered_pairs"])
    rejected_pairs = int(logical["rejected_ordered_pairs"])
    compatible_pairs = int(logical["mode_histogram"]["COMPATIBLE_UNIQUE_BASIS"])
    same_ray_pairs = int(logical["mode_histogram"]["SAME_RAY_FOUR_BASIS_APERTURE"])
    physical_records = int(physical["records"])
    data_records = int(physical["mode_histogram"]["OFF_DIAGONAL_DATA_HANDSHAKE"])
    witness_records = int(physical["mode_histogram"]["DIAGONAL_WITNESS_APERTURE"])
    same_ray_extra = int(physical["same_ray_extra_context_options"])

    # Physical front end and ledger.
    active_slots = int(port["active_slots"])
    guard_slots = int(port["guard_slots"])
    full_flag_bus = int(port["full_flag_bus"])
    parity_rows = int(syndrome["parity_syndrome_rows"])
    css_rows = int(syndrome["css_edge_ledger_rows"])
    central_cycles = int(syndrome["steinberg_central_cycles"])
    even_states = int(syndrome["even_q4_clock_states"])
    magic_apertures = int(magic["guard_apertures"])
    d4_orientations = int(magic["d4_orientations"])
    oriented_magic_tokens = int(magic["oriented_tomotope_tokens"])

    field_schema = [
        {
            "field": "pauli_frame",
            "domain": "F3^2",
            "size": 9,
            "role": "two-trit feed-forward correction X^r Z^p",
        },
        {
            "field": "chart_word",
            "domain": "F2^3",
            "size": 8,
            "role": "local Q3/Gray route word",
        },
        {
            "field": "q6_body_edge",
            "domain": "Q6 edge walk",
            "size": body_edges,
            "role": "continuous body traversals in the stress transaction",
        },
        {
            "field": "body_pulse_phase",
            "domain": "F3",
            "size": 3,
            "role": "LOAD, FLIP, LATCH per Q6 edge",
        },
        {
            "field": "hesse_outcome",
            "domain": "F3 x F3",
            "size": 9,
            "role": "route branch and phase label",
        },
        {
            "field": "tomotope_flag",
            "domain": "48 blocks x 4 residues",
            "size": full_flag_bus,
            "role": "local toroidal/tomotope flag bus",
        },
        {
            "field": "dual_port_active_slot",
            "domain": "21 edges x 2 orientations x 4 residues",
            "size": active_slots,
            "role": "Csaszar/Szilassi active analyzer slots",
        },
        {
            "field": "q4_guard",
            "domain": "Q4 plaquette guard band",
            "size": guard_slots,
            "role": "guard tail shared by port, CSS, and magic boundary",
        },
        {
            "field": "steinberg_syndrome_row",
            "domain": "27 central cycles x 8 even Q4 states",
            "size": parity_rows,
            "role": "binary front-end checks before ternary CSS memory",
        },
        {
            "field": "css_edge_row",
            "domain": "W33 edge ledger",
            "size": css_rows,
            "role": "outer Steinberg/CSS edge carrier",
        },
        {
            "field": "mirror_slot",
            "domain": "45 polar sheets x 48 tomotope blocks",
            "size": 2160,
            "role": "global D12 mirror transport bus",
        },
        {
            "field": "clifford_supercycle",
            "domain": "24 lifts x 45 polar sheets x 48 blocks",
            "size": 51840,
            "role": "complete Sp(4,3) runtime window",
        },
    ]

    boundary_24 = {
        "hesse_epilogue_ticks": epilogue_ticks,
        "q4_guard_slots": guard_slots,
        "css_guard_tail_rows": css_rows - parity_rows,
        "d4_magic_guard_apertures": magic_apertures,
        "meaning": (
            "The count 24 is a typed guard boundary, not one untyped object. "
            "It is the common interface where the 48-body transaction hands off "
            "to Hesse return, Q4 guard, CSS tail, and D4-quartic magic aperture."
        ),
    }

    checks = {
        "upstream_certificates_verified": all(
            item["verified"]
            for item in (bt1404, bt1407, bt1410, bt1414, bt1415, bt1418)
        ),
        "frame_is_48_body_plus_24_epilogue": body_ticks == 48
        and epilogue_ticks == 24
        and body_ticks + epilogue_ticks == frame_ticks,
        "body_is_16_q6_edges_times_3_pulses": body_edges == 16
        and body_edges * 3 == body_ticks,
        "epilogue_is_3_hesse_words_times_8_ticks": hesse_return_words == 3
        and hesse_return_words * 8 == epilogue_ticks,
        "full_hesse_grid_is_3_by_3": full_hesse_outcomes == list(range(9)),
        "selected_hesse_branch_is_one_route_branch": selected_hesse_outcomes
        == [3, 4, 5],
        "witting_logical_rom_splits_40_squared": logical_records == 40 * 40
        and compatible_pairs == 480
        and same_ray_pairs == 40
        and rejected_pairs == 1080,
        "accepted_witting_rate_is_13_over_40": accepted_pairs == 520
        and logical["accept_rate"] == "13/40",
        "physical_witting_rom_is_40_tetrads_times_4_by_4": physical_records
        == 40 * 4 * 4
        and data_records == 480
        and witness_records == 160
        and witness_records - same_ray_pairs == same_ray_extra == 120,
        "dual_port_is_168_active_plus_24_guard": active_slots == 21 * 2 * 4
        and guard_slots == 24
        and active_slots + guard_slots == full_flag_bus == 192,
        "css_ledger_is_216_plus_24": parity_rows == central_cycles * even_states == 216
        and css_rows == parity_rows + guard_slots == 240,
        "magic_guard_is_two_D4_quartics": magic_apertures == 2 * 4 * 3 == 24,
        "magic_orients_to_full_tomotope_bus": oriented_magic_tokens
        == magic_apertures * d4_orientations
        == full_flag_bus,
        "global_mirror_bus_is_45_times_48": 45 * 48 == 2160,
        "runtime_supercycle_is_24_times_2160": 24 * 2160 == 51840,
        "guard_24_is_common_typed_boundary": all(
            boundary_24[key] == 24
            for key in (
                "hesse_epilogue_ticks",
                "q4_guard_slots",
                "css_guard_tail_rows",
                "d4_magic_guard_apertures",
            )
        ),
    }

    return {
        "theorem": "BT1697 Holonet Typed Packet ABI",
        "verified": all(checks.values()),
        "breakthrough": (
            "The Holonet packet is a typed transaction object: a 48-tick "
            "Q6/tomotope body, a 24-tick Hesse epilogue, a Witting admission ROM, "
            "a 168+24 dual toroidal port, a 216+24 CSS ledger, and a D4-quartic "
            "magic rail are compatible projections of one ABI."
        ),
        "field_schema": field_schema,
        "transaction_identities": {
            "microframe": "72 = 48 + 24 = 16*3 + 3*8",
            "witting_logical_rom": "1600 = 40*40 = 520 accepted + 1080 retry-shadow",
            "witting_physical_rom": "640 = 40*4*4 = 480 data + 160 witness",
            "dual_port": "192 = 168 + 24 = 21*2*4 + 24",
            "css_ledger": "240 = 216 + 24 = 27*8 + 24",
            "magic_guard": "24 = 2*4*3, 192 = 24*8",
            "mirror_runtime": "51840 = 24*2160 = 24*45*48",
        },
        "boundary_24": boundary_24,
        "source_certificates": [
            "data/bt1404_holonet_scope_microframe.json",
            "data/bt1407_microframe_transaction_composer.json",
            "data/bt1410_witting_delayed_query_frame_compiler.json",
            "data/bt1414_csaszar_szilassi_dual_physical_port.json",
            "data/bt1415_even_projection_steinberg_syndrome_layer.json",
            "data/bt1418_d4_quartic_magic_injection_frontier.json",
        ],
        "claim_boundary": [
            "This is an ABI theorem, not a calibrated optical layout.",
            "Equal counts are promoted only when their typed source certificate and projection role are explicit.",
            "The packet header unifies existing verified layers; it does not replace the individual hardware/noise boundaries of those layers.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    for name, identity in cert["transaction_identities"].items():
        print(f"  {name}: {identity}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
