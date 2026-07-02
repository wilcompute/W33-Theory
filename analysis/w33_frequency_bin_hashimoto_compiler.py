#!/usr/bin/env python3
"""Lower the Hashimoto packet phase bridge into a frequency-bin control plan.

This is the spectral-hardware sibling of the existing time-bin compiler.  It
does not claim a measured chip layout.  It verifies the exact ABI object that a
frequency-bin photonic processor would need: nine Hesse outcome bins, two
Hashimoto sector sidebands, and line-by-line phase settings for the packet
PHASE lane.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_frequency_bin_hashimoto_compiler.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def find_phase_tick(frame: dict[str, Any]) -> int:
    ticks = [
        int(row["microframe_tick"])
        for row in frame["packet_word"]
        if row["lane"] == "PHASE"
    ]
    if len(ticks) != 1:
        raise ValueError(f"frame {frame['h']} has {len(ticks)} PHASE ticks")
    return ticks[0]


def hesse_frequency_bins(scope: dict[str, Any]) -> list[dict[str, Any]]:
    bins: list[dict[str, Any]] = []
    for frame in scope["frames"]:
        phase_trit = int(frame["phase_trit"])
        route_trit = int(frame["route_trit"])
        h = int(frame["h"])
        bins.append(
            {
                "bin_index": h,
                "label": f"H{h}",
                "role": "hesse_phase_lane",
                "route_trit": route_trit,
                "phase_trit": phase_trit,
                "phase_lane_tick": find_phase_tick(frame),
                "qutrit_phase_degrees": (120 * phase_trit) % 360,
                "frequency_offset_units": h - 4,
            }
        )
    return bins


def sector_sidebands(bridge: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "bin_index": 9,
            "label": "S_gauge",
            "role": "hashimoto_sector_sideband",
            "sector": "gauge",
            "phase_degrees": bridge["phase_analyzers"]["gauge"][
                "analyzer_phase_degrees"
            ],
            "complex_modes_bound": bridge["phase_analyzers"]["gauge"][
                "complex_mode_count"
            ],
            "binds_to": "48 packet-body phase ticks",
        },
        {
            "bin_index": 10,
            "label": "S_chiral",
            "role": "hashimoto_sector_sideband",
            "sector": "chiral",
            "phase_degrees": bridge["phase_analyzers"]["chiral"][
                "analyzer_phase_degrees"
            ],
            "complex_modes_bound": bridge["phase_analyzers"]["chiral"][
                "complex_mode_count"
            ],
            "binds_to": "30 packet frames per mirror atlas",
        },
    ]


def build_certificate() -> dict[str, Any]:
    bridge = load_json("data/w33_hashimoto_packet_phase_bridge.json")
    scope = load_json("data/bt1404_holonet_scope_microframe.json")
    fabric = load_json("data/w33_holonet_firmware_fabric_profile.json")

    hesse_bins = hesse_frequency_bins(scope)
    sidebands = sector_sidebands(bridge)
    all_bins = hesse_bins + sidebands

    branch_width = int(round(bridge["phase_analyzers"]["gauge"]["radius_squared"]))
    packets_per_mirror = int(fabric["mirror_fabric"]["packet_frames_per_mirror_atlas"])
    packets_per_supercycle = int(
        fabric["mirror_fabric"]["packet_frames_per_supercycle"]
    )
    supercycle_slots = int(fabric["mirror_fabric"]["supercycle_slots"])
    sector_count = len(sidebands)
    hesse_count = len(hesse_bins)
    mirror_phase_probes = packets_per_mirror * hesse_count * sector_count
    supercycle_phase_probes = packets_per_supercycle * hesse_count * sector_count

    qfp_chain = [
        {
            "component": "comb_or_frequency_bin_source",
            "role": "supply the 11 addressable frequency lines for one packet phase word",
            "calibration_placeholder": "bin_power_flatness",
        },
        {
            "component": "pre_eom_frequency_mixer",
            "role": "coherently mix adjacent bins before sector phase masking",
            "calibration_placeholder": "rf_phase_and_modulation_index",
        },
        {
            "component": "line_by_line_pulse_shaper",
            "role": "apply Hesse qutrit phases and the two Hashimoto analyzer phases",
            "calibration_placeholder": "per_bin_phase_error",
        },
        {
            "component": "post_eom_frequency_mixer",
            "role": "recombine masked bins into the packet PHASE lane",
            "calibration_placeholder": "rf_phase_closure_error",
        },
        {
            "component": "frequency_or_time_resolved_detector",
            "role": "read sector-probe interference without claiming a measured fringe yet",
            "calibration_placeholder": "efficiency_dark_jitter",
        },
    ]

    checks = {
        "source_bridge_verified": bridge["verified"] is True,
        "source_scope_verified": scope["verified"] is True,
        "source_fabric_verified": fabric["verified"] is True,
        "nine_hesse_bins": hesse_count == 9,
        "two_hashimoto_sidebands": sector_count == 2,
        "eleven_total_bins_equal_hashimoto_branch_width": len(all_bins)
        == branch_width
        == 11,
        "phase_lane_ticks_preserved": [b["phase_lane_tick"] for b in hesse_bins]
        == bridge["packet_binding"]["phase_lane_ticks"],
        "qutrit_phase_mask_is_three_valued": sorted(
            {b["qutrit_phase_degrees"] for b in hesse_bins}
        )
        == [0, 120, 240],
        "sideband_phases_match_bridge": (
            sidebands[0]["phase_degrees"]
            == bridge["phase_analyzers"]["gauge"]["analyzer_phase_degrees"]
            and sidebands[1]["phase_degrees"]
            == bridge["phase_analyzers"]["chiral"]["analyzer_phase_degrees"]
        ),
        "mirror_phase_probe_budget_is_540": mirror_phase_probes == 540,
        "supercycle_phase_probe_budget_is_12960": supercycle_phase_probes == 12960,
        "phase_probe_budget_is_one_quarter_runtime_slots": supercycle_phase_probes * 4
        == supercycle_slots,
        "qfp_chain_has_two_eoms_and_one_pulse_shaper": (
            sum("eom" in row["component"] for row in qfp_chain) == 2
            and sum("pulse_shaper" in row["component"] for row in qfp_chain) == 1
        ),
        "all_components_have_calibration_placeholders": all(
            row["calibration_placeholder"] for row in qfp_chain
        ),
    }

    return {
        "theorem": "W33 frequency-bin Hashimoto compiler",
        "verified": all(checks.values()),
        "breakthrough": (
            "The packet phase bridge can be lowered to an 11-bin frequency plan: "
            "nine Hesse outcome bins plus two Hashimoto sector sidebands.  One "
            "mirror atlas contains 30*9*2 = 540 sector probes, and the full "
            "720-packet supercycle contains 720*9*2 = 12960 probes, exactly "
            "one quarter of the 51840 runtime slots."
        ),
        "external_inspiration": [
            {
                "topic": "quantum frequency processors",
                "use": "line-by-line spectral phase masks plus EOM mixing motivate this compiler target",
                "url": "https://arxiv.org/abs/2204.12320",
            },
            {
                "topic": "synthetic frequency dimensions",
                "use": "frequency bins can serve as a synthetic photonic dimension; this certificate only fixes the finite ABI",
                "url": "https://arxiv.org/abs/2602.14240",
            },
            {
                "topic": "quantum walks and zeta functions",
                "use": "Ihara/Grover-walk links motivate keeping the Hashimoto sector phases explicit",
                "url": "https://arxiv.org/abs/1103.0079",
            },
        ],
        "frequency_plan": {
            "total_bins": len(all_bins),
            "hashimoto_branch_width": branch_width,
            "frequency_spacing_units": "symbolic_delta_omega",
            "hesse_bins": hesse_bins,
            "hashimoto_sidebands": sidebands,
            "all_bin_labels": [row["label"] for row in all_bins],
        },
        "probe_budget": {
            "sector_count": sector_count,
            "hesse_phase_bins_per_packet": hesse_count,
            "packets_per_mirror_atlas": packets_per_mirror,
            "packets_per_supercycle": packets_per_supercycle,
            "phase_probes_per_mirror_atlas": mirror_phase_probes,
            "phase_probes_per_supercycle": supercycle_phase_probes,
            "runtime_slots_per_supercycle": supercycle_slots,
            "runtime_slots_per_phase_probe": supercycle_slots
            // supercycle_phase_probes,
        },
        "component_chain": qfp_chain,
        "source_certificates": [
            "data/w33_hashimoto_packet_phase_bridge.json",
            "data/bt1404_holonet_scope_microframe.json",
            "data/w33_holonet_firmware_fabric_profile.json",
        ],
        "claim_boundary": [
            "This is a frequency-bin compiler/control certificate, not a fabricated photonic chip.",
            "Bin spacing, RF drive power, insertion loss, thermal drift, detector efficiency, and measured fringe visibility remain bench parameters.",
            "The external literature motivates the hardware vocabulary; all promoted equalities are local repo certificate equalities.",
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
        "  bins: "
        f"{cert['frequency_plan']['total_bins']} = "
        f"{len(cert['frequency_plan']['hesse_bins'])} Hesse + "
        f"{len(cert['frequency_plan']['hashimoto_sidebands'])} sidebands"
    )
    print(
        "  probes: "
        f"{cert['probe_budget']['phase_probes_per_supercycle']} per supercycle = "
        f"1/{cert['probe_budget']['runtime_slots_per_phase_probe']} runtime slots"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
