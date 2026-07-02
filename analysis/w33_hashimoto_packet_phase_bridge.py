#!/usr/bin/env python3
"""Hashimoto phase settings lowered into the Holonet packet ABI.

The existing Hashimoto sector certificate gives two complex transport sectors:

    gauge:  1 +/- i sqrt(10),  24 conjugate pairs = 48 modes
    chiral: -2 +/- i sqrt(7), 15 conjugate pairs = 30 modes

The existing Holonet packet certificates give:

    packet body = 48 phase/body ticks
    mirror atlas = 30 packet frames
    supercycle = 720 packet frames

This verifier welds those facts into one ABI-level certificate. It is not an
optical fringe measurement; it is the finite protocol object that says where the
Hashimoto analyzer phases land in the already-typed packet and mirror bus.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_hashimoto_packet_phase_bridge.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def sector_by_lambda(payload: dict[str, Any], lambda_a: int) -> dict[str, Any]:
    for sector in payload["full_spectrum"]["sectors"]:
        if sector.get("lambda_A") == lambda_a:
            return sector
    raise KeyError(f"missing Hashimoto sector for lambda_A={lambda_a}")


def phase_record(name: str, sector: dict[str, Any]) -> dict[str, Any]:
    real = float(sector["real_part"])
    imag_sq = float(sector["imag_part_squared"])
    radius_sq = real * real + imag_sq
    radius = math.sqrt(radius_sq)
    angle = math.degrees(math.atan2(math.sqrt(imag_sq), real))
    pair_multiplicity = int(sector["lambda_A_mult"])
    mode_count = 2 * pair_multiplicity
    return {
        "sector": name,
        "lambda_A": int(sector["lambda_A"]),
        "pair_multiplicity": pair_multiplicity,
        "complex_mode_count": mode_count,
        "eigenvalue_plus": sector["u_eigenvalues_str"][0],
        "eigenvalue_minus": sector["u_eigenvalues_str"][1],
        "real_part": real,
        "imaginary_part_squared": imag_sq,
        "radius_squared": radius_sq,
        "radius": radius,
        "analyzer_phase_degrees": angle,
        "unit_cos": real / radius,
        "unit_sin": math.sqrt(imag_sq) / radius,
    }


def phase_lane_ticks(scope: dict[str, Any]) -> list[int]:
    ticks: list[int] = []
    for frame in scope["frames"]:
        phase_ticks = [
            int(row["microframe_tick"])
            for row in frame["packet_word"]
            if row["lane"] == "PHASE"
        ]
        if len(phase_ticks) != 1:
            raise ValueError(f"frame {frame['h']} has {len(phase_ticks)} PHASE lanes")
        ticks.append(phase_ticks[0])
    return ticks


def build_certificate() -> dict[str, Any]:
    hashimoto = load_json("data/w33_hashimoto_sector_spectrum.json")
    packet_energy = load_json("data/w33_packet_energy.json")
    fabric = load_json("data/w33_holonet_firmware_fabric_profile.json")
    scope = load_json("data/bt1404_holonet_scope_microframe.json")

    gauge = phase_record("gauge", sector_by_lambda(hashimoto, 2))
    chiral = phase_record("chiral", sector_by_lambda(hashimoto, -4))

    packet_trits = int(packet_energy["traffic_model"]["total_packet_trits"])
    body_phase_trits = int(packet_energy["traffic_model"]["body_phase_trits"])
    microframe_ticks = int(scope["timing"]["microframe_ticks"])
    mirror_packets = int(fabric["mirror_fabric"]["packet_frames_per_mirror_atlas"])
    supercycle_packets = int(fabric["mirror_fabric"]["packet_frames_per_supercycle"])
    lanes = phase_lane_ticks(scope)

    checks = {
        "source_hashimoto_on_ramanujan_circle": (
            hashimoto["ihara_ramanujan_check"]["all_on_circle"] is True
        ),
        "source_packet_energy_verified": packet_energy["verified"] is True,
        "source_firmware_fabric_verified": fabric["verified"] is True,
        "source_microframe_verified": scope["verified"] is True,
        "packet_is_one_72_tick_microframe": packet_trits == microframe_ticks == 72,
        "phase_lane_once_per_hesse_word": len(lanes) == 9
        and lanes == list(range(2, 72, 8)),
        "gauge_complex_modes_fill_packet_body": (
            gauge["complex_mode_count"] == body_phase_trits == 48
        ),
        "chiral_complex_modes_fill_one_mirror_atlas": (
            chiral["complex_mode_count"] == mirror_packets == 30
        ),
        "supercycle_tiles_gauge_modes_by_chiral_multiplicity": (
            supercycle_packets
            == chiral["pair_multiplicity"] * gauge["complex_mode_count"]
        ),
        "supercycle_tiles_chiral_modes_by_gauge_multiplicity": (
            supercycle_packets
            == gauge["pair_multiplicity"] * chiral["complex_mode_count"]
        ),
        "both_sectors_share_ihara_radius_squared_11": (
            abs(gauge["radius_squared"] - 11.0) < 1e-12
            and abs(chiral["radius_squared"] - 11.0) < 1e-12
        ),
        "phase_unit_vectors_are_normalized": (
            abs(gauge["unit_cos"] ** 2 + gauge["unit_sin"] ** 2 - 1.0) < 1e-12
            and abs(chiral["unit_cos"] ** 2 + chiral["unit_sin"] ** 2 - 1.0) < 1e-12
        ),
    }

    return {
        "theorem": "W33 Hashimoto packet phase bridge",
        "verified": all(checks.values()),
        "breakthrough": (
            "The two non-trivial Hashimoto transport sectors now have a typed "
            "packet ABI: the 48 gauge-sector complex modes fill the 48-tick "
            "tomotope packet body, the 30 chiral-sector complex modes fill the "
            "30 packet frames of one 2160-slot mirror atlas, and the 720 packet "
            "frames of a full supercycle tile both sectors as 15*48 = 24*30."
        ),
        "phase_analyzers": {
            "gauge": gauge,
            "chiral": chiral,
            "shared_radius": "sqrt(11), the Ihara-Ramanujan radius",
        },
        "packet_binding": {
            "minimal_packet_trits": packet_trits,
            "microframe_ticks": microframe_ticks,
            "phase_lane_ticks": lanes,
            "phase_lane_rule": "one PHASE lane at tick 2 of each 8-tick Hesse return word",
            "packet_body_phase_trits": body_phase_trits,
            "mirror_atlas_packet_frames": mirror_packets,
            "supercycle_packet_frames": supercycle_packets,
            "gauge_body_identity": "48 gauge complex modes = 48 packet body phase ticks",
            "chiral_atlas_identity": "30 chiral complex modes = 30 packet frames per mirror atlas",
            "supercycle_dual_tiling": "720 = 15*48 = 24*30",
        },
        "source_certificates": [
            "data/w33_hashimoto_sector_spectrum.json",
            "data/w33_packet_energy.json",
            "data/w33_holonet_firmware_fabric_profile.json",
            "data/bt1404_holonet_scope_microframe.json",
        ],
        "claim_boundary": [
            "This is an ABI/protocol certificate, not a measured photonic fringe experiment.",
            "It calibrates the two Hashimoto analyzer phase settings and their packet/mirror placement.",
            "Optical phase stability, loss, detector jitter, and physical fringe visibility remain separate bench measurements.",
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
        "  gauge: "
        f"{cert['phase_analyzers']['gauge']['complex_mode_count']} modes -> "
        f"{cert['packet_binding']['packet_body_phase_trits']} body ticks"
    )
    print(
        "  chiral: "
        f"{cert['phase_analyzers']['chiral']['complex_mode_count']} modes -> "
        f"{cert['packet_binding']['mirror_atlas_packet_frames']} mirror-atlas packets"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
