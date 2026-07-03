#!/usr/bin/env python3
"""Compile the Holonet runtime into a lookup-free control-plane address word.

The selector E6/E8 bridge proves that the 51,840-slot supercycle is shared by
the selector sheets, signed E8 budget, and frequency-bin lab packet.  This file
turns that accounting into an architecture primitive: every runtime slot has a
direct mixed-radix address

    atlas * sheet * frame * Hesse bin * Hashimoto sector * probe slot
    24    * 5     * 6     * 9         * 2                * 4 = 51840.

No canonical sheet-to-root bijection is claimed.  The claim is narrower and
more useful for a builder: the control plane can decode the whole supercycle
without a slot lookup table.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_architecture_control_plane_abi.json"

SECTOR_LABELS = ("gauge", "chiral")
SIGN_LABELS = ("positive", "negative")


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def decode_slot(slot: int, radix: dict[str, int]) -> dict[str, int | str]:
    slots_per_probe = radix["probe_slots"]
    sectors = radix["hashimoto_sectors"]
    hesse_bins = radix["hesse_bins"]
    frames_per_sheet = radix["packet_frames_per_selector_sheet"]
    sheets_per_atlas = radix["selector_sheets_per_atlas"]
    signed_frames = radix["packet_frames_per_signed_sheet"]

    probe_id = slot // slots_per_probe
    probe_slot = slot % slots_per_probe

    sector_id = probe_id % sectors
    hesse_bin = (probe_id // sectors) % hesse_bins
    packet_frame_in_sheet = (probe_id // (sectors * hesse_bins)) % frames_per_sheet
    sheet_in_atlas = (
        probe_id // (sectors * hesse_bins * frames_per_sheet)
    ) % sheets_per_atlas
    atlas_id = probe_id // (sectors * hesse_bins * frames_per_sheet * sheets_per_atlas)

    selector_sheet_id = atlas_id * sheets_per_atlas + sheet_in_atlas
    packet_frame_global = (
        atlas_id * sheets_per_atlas * frames_per_sheet
        + sheet_in_atlas * frames_per_sheet
        + packet_frame_in_sheet
    )

    sign_id = packet_frame_in_sheet // signed_frames
    signed_sheet_id = selector_sheet_id * 2 + sign_id
    packet_frame_in_signed_sheet = packet_frame_in_sheet % signed_frames
    selector_support_index = (
        packet_frame_in_sheet * hesse_bins * sectors + hesse_bin * sectors + sector_id
    )
    signed_support_index = (
        packet_frame_in_signed_sheet * hesse_bins * sectors
        + hesse_bin * sectors
        + sector_id
    )

    return {
        "runtime_slot": slot,
        "probe_id": probe_id,
        "probe_slot": probe_slot,
        "mirror_atlas_id": atlas_id,
        "selector_sheet_id": selector_sheet_id,
        "selector_sheet_in_atlas": sheet_in_atlas,
        "selector_support_index": selector_support_index,
        "signed_sheet_id": signed_sheet_id,
        "sign_id": sign_id,
        "sign_label": SIGN_LABELS[sign_id],
        "signed_support_index": signed_support_index,
        "packet_frame_global": packet_frame_global,
        "packet_frame_in_selector_sheet": packet_frame_in_sheet,
        "packet_frame_in_signed_sheet": packet_frame_in_signed_sheet,
        "hesse_bin": hesse_bin,
        "hashimoto_sector_id": sector_id,
        "hashimoto_sector": SECTOR_LABELS[sector_id],
    }


def encode_slot(word: dict[str, int | str], radix: dict[str, int]) -> int:
    probe_id = (
        int(word["mirror_atlas_id"])
        * radix["selector_sheets_per_atlas"]
        * radix["packet_frames_per_selector_sheet"]
        * radix["hesse_bins"]
        * radix["hashimoto_sectors"]
    )
    probe_id += (
        int(word["selector_sheet_in_atlas"])
        * radix["packet_frames_per_selector_sheet"]
        * radix["hesse_bins"]
        * radix["hashimoto_sectors"]
    )
    probe_id += (
        int(word["packet_frame_in_selector_sheet"])
        * radix["hesse_bins"]
        * radix["hashimoto_sectors"]
    )
    probe_id += int(word["hesse_bin"]) * radix["hashimoto_sectors"]
    probe_id += int(word["hashimoto_sector_id"])
    return probe_id * radix["probe_slots"] + int(word["probe_slot"])


def build_certificate() -> dict[str, Any]:
    bridge = load_json("data/w33_selector_e6_e8_runtime_bridge.json")
    fabric = load_json("data/w33_holonet_firmware_fabric_profile.json")
    compiler = load_json("data/w33_frequency_bin_hashimoto_compiler.json")
    lab = load_json("data/w33_frequency_bin_lab_packet.json")

    runtime = bridge["runtime_surface"]
    selector = bridge["selector_e6_surface"]
    mirror = fabric["mirror_fabric"]
    probe_budget = compiler["probe_budget"]
    frames_per_selector_sheet = (
        mirror["packet_frames_per_mirror_atlas"]
        // runtime["sheets_per_mirror_atlas_accounting"]
    )

    radix = {
        "mirror_atlases": runtime["mirror_atlases_per_supercycle"],
        "selector_sheets_per_atlas": runtime["sheets_per_mirror_atlas_accounting"],
        "packet_frames_per_selector_sheet": frames_per_selector_sheet,
        "hesse_bins": probe_budget["hesse_phase_bins_per_packet"],
        "hashimoto_sectors": probe_budget["sector_count"],
        "probe_slots": runtime["runtime_slots_per_probe"],
        "packet_frames_per_signed_sheet": frames_per_selector_sheet // 2,
    }

    derived = {
        "selector_sheet_slots": (
            radix["packet_frames_per_selector_sheet"]
            * radix["hesse_bins"]
            * radix["hashimoto_sectors"]
            * radix["probe_slots"]
        ),
        "signed_sheet_slots": (
            radix["packet_frames_per_signed_sheet"]
            * radix["hesse_bins"]
            * radix["hashimoto_sectors"]
            * radix["probe_slots"]
        ),
        "probes_per_selector_sheet": (
            radix["packet_frames_per_selector_sheet"]
            * radix["hesse_bins"]
            * radix["hashimoto_sectors"]
        ),
        "probes_per_signed_sheet": (
            radix["packet_frames_per_signed_sheet"]
            * radix["hesse_bins"]
            * radix["hashimoto_sectors"]
        ),
        "packet_frames_per_mirror_atlas": (
            radix["selector_sheets_per_atlas"]
            * radix["packet_frames_per_selector_sheet"]
        ),
        "probes_per_mirror_atlas": (
            radix["selector_sheets_per_atlas"]
            * radix["packet_frames_per_selector_sheet"]
            * radix["hesse_bins"]
            * radix["hashimoto_sectors"]
        ),
    }

    supercycle_slots = (
        radix["mirror_atlases"]
        * radix["selector_sheets_per_atlas"]
        * radix["packet_frames_per_selector_sheet"]
        * radix["hesse_bins"]
        * radix["hashimoto_sectors"]
        * radix["probe_slots"]
    )
    supercycle_probes = supercycle_slots // radix["probe_slots"]
    packet_frames = (
        radix["mirror_atlases"]
        * radix["selector_sheets_per_atlas"]
        * radix["packet_frames_per_selector_sheet"]
    )
    signed_sheet_count = (
        radix["mirror_atlases"] * radix["selector_sheets_per_atlas"] * 2
    )

    sample_slots = [
        0,
        1,
        3,
        4,
        derived["signed_sheet_slots"] - 1,
        derived["signed_sheet_slots"],
        derived["selector_sheet_slots"] - 1,
        derived["selector_sheet_slots"],
        mirror["mirror_slots"] - 1,
        mirror["mirror_slots"],
        mirror["supercycle_slots"] - 1,
    ]
    sample_words = [decode_slot(slot, radix) for slot in sample_slots]

    seen = set()
    ranges_ok = True
    roundtrip_ok = True
    for slot in range(supercycle_slots):
        word = decode_slot(slot, radix)
        encoded = encode_slot(word, radix)
        roundtrip_ok = roundtrip_ok and encoded == slot
        key = (
            word["mirror_atlas_id"],
            word["selector_sheet_in_atlas"],
            word["packet_frame_in_selector_sheet"],
            word["hesse_bin"],
            word["hashimoto_sector_id"],
            word["probe_slot"],
        )
        seen.add(key)
        ranges_ok = ranges_ok and (
            0 <= int(word["mirror_atlas_id"]) < radix["mirror_atlases"]
            and 0
            <= int(word["selector_sheet_in_atlas"])
            < radix["selector_sheets_per_atlas"]
            and 0
            <= int(word["packet_frame_in_selector_sheet"])
            < radix["packet_frames_per_selector_sheet"]
            and 0 <= int(word["hesse_bin"]) < radix["hesse_bins"]
            and 0 <= int(word["hashimoto_sector_id"]) < radix["hashimoto_sectors"]
            and 0 <= int(word["probe_slot"]) < radix["probe_slots"]
        )

    checks = {
        "source_selector_bridge_verified": bridge["verified"] is True,
        "source_firmware_profile_verified": fabric["verified"] is True,
        "source_frequency_compiler_verified": compiler["verified"] is True,
        "source_lab_packet_verified": lab["verified"] is True,
        "mixed_radix_product_is_supercycle": supercycle_slots
        == mirror["supercycle_slots"]
        == 51840,
        "atlas_product_is_2160": (
            radix["selector_sheets_per_atlas"]
            * radix["packet_frames_per_selector_sheet"]
            * radix["hesse_bins"]
            * radix["hashimoto_sectors"]
            * radix["probe_slots"]
        )
        == mirror["mirror_slots"]
        == 2160,
        "selector_sheet_is_six_packet_frames": (
            radix["packet_frames_per_selector_sheet"] == 6
            and derived["selector_sheet_slots"] == 432
            and derived["probes_per_selector_sheet"] == selector["sheet_self_support"]
        ),
        "signed_sheet_is_three_packet_frames": (
            radix["packet_frames_per_signed_sheet"] == 3
            and derived["signed_sheet_slots"]
            == runtime["runtime_slots_per_signed_sheet_accounting"]
            and derived["probes_per_signed_sheet"]
            == selector["sheet_self_support"] // 2
        ),
        "packet_frames_close_720": packet_frames
        == mirror["packet_frames_per_supercycle"]
        == 720,
        "probe_rows_close_12960": supercycle_probes
        == lab["schedule_summary"]["supercycle_probe_rows"]
        == 12960,
        "signed_sheets_close_e8_budget": signed_sheet_count == 240,
        "runtime_decoder_is_bijective": (
            len(seen) == supercycle_slots and roundtrip_ok and ranges_ok
        ),
        "sample_words_hit_boundary_slots": [row["runtime_slot"] for row in sample_words]
        == sample_slots,
    }

    return {
        "theorem": "W33 Holonet architecture control-plane ABI",
        "verified": all(checks.values()),
        "breakthrough": (
            "The 51,840-slot Holonet runtime can be decoded by one mixed-radix "
            "control word: 24 mirror atlases * 5 selector sheets * 6 packet "
            "frames * 9 Hesse bins * 2 Hashimoto sectors * 4 probe slots. "
            "This makes the selector E6/E8 bridge schedulable without a slot "
            "lookup table."
        ),
        "control_word": {
            "identity": "51840 = 24 * 5 * 6 * 9 * 2 * 4",
            "fields": [
                {
                    "name": "mirror_atlas_id",
                    "extent": radix["mirror_atlases"],
                    "meaning": "one of the 24 mirror atlases in the supercycle",
                },
                {
                    "name": "selector_sheet_in_atlas",
                    "extent": radix["selector_sheets_per_atlas"],
                    "meaning": "one of five selector sheets assigned to the atlas",
                },
                {
                    "name": "packet_frame_in_selector_sheet",
                    "extent": radix["packet_frames_per_selector_sheet"],
                    "meaning": "six 72-tick packet frames carried by one selector sheet",
                },
                {
                    "name": "hesse_bin",
                    "extent": radix["hesse_bins"],
                    "meaning": "one of the nine Hesse phase bins",
                },
                {
                    "name": "hashimoto_sector_id",
                    "extent": radix["hashimoto_sectors"],
                    "meaning": "gauge or chiral Hashimoto sideband",
                },
                {
                    "name": "probe_slot",
                    "extent": radix["probe_slots"],
                    "meaning": "four runtime ticks owned by one frequency-bin probe",
                },
            ],
            "radix": radix,
        },
        "derived_architecture": {
            **derived,
            "supercycle_slots": supercycle_slots,
            "supercycle_probes": supercycle_probes,
            "packet_frames_per_supercycle": packet_frames,
            "signed_sheet_count": signed_sheet_count,
            "selector_sheet_count": selector["sheet_count"],
            "hashimoto_sector_labels": list(SECTOR_LABELS),
            "sign_labels": list(SIGN_LABELS),
        },
        "runtime_decode_samples": sample_words,
        "decoder_pseudocode": [
            "probe_id = runtime_slot // 4; probe_slot = runtime_slot % 4",
            "sector = probe_id % 2",
            "hesse_bin = (probe_id // 2) % 9",
            "frame_in_sheet = (probe_id // 18) % 6",
            "sheet_in_atlas = (probe_id // 108) % 5",
            "atlas = probe_id // 540",
        ],
        "source_certificates": [
            "data/w33_selector_e6_e8_runtime_bridge.json",
            "data/w33_holonet_firmware_fabric_profile.json",
            "data/w33_frequency_bin_hashimoto_compiler.json",
            "data/w33_frequency_bin_lab_packet.json",
        ],
        "checks": checks,
        "claim_boundary": [
            "This is an address/scheduling ABI, not a canonical E8-root ordering.",
            "The sheet ordering is a quotient control-plane ordering: five sheets per atlas and two signs per sheet.",
            "Physical bin spacing, phase visibility, loss, detector efficiency, and chip layout remain bench work.",
            "The decoder removes slot lookup tables; it does not replace route, fault, or calibration policy.",
        ],
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  control word: {cert['control_word']['identity']}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
