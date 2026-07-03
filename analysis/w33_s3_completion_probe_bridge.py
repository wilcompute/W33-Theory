#!/usr/bin/env python3
"""Bridge the S3 completion frontier to the Holonet phase-probe clock.

The existing architecture work exposed two surfaces with the same size:

* the frontier carrier: 4320 ordered nonlocal paths, each with three S3
  completions, for 12960 completion incidences;
* the control plane: 24 mirror atlases, each with 540 frequency-bin probes,
  for 12960 supercycle probes.

This certificate identifies them as the same schedulable measurement surface.
It does not choose a canonical golden-selector completion.  In fact, it keeps
the older 540-cover no-go as the honesty boundary: a mirror atlas is the full
probe/admission surface for the completion problem, not a solved exact cover.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_s3_completion_probe_bridge.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def decode_probe_start(probe_id: int, radix: dict[str, int]) -> dict[str, int | str]:
    sector_labels = ("gauge", "chiral")

    sector_id = probe_id % radix["hashimoto_sectors"]
    hesse_bin = (probe_id // radix["hashimoto_sectors"]) % radix["hesse_bins"]
    packet_frame = (
        probe_id // (radix["hashimoto_sectors"] * radix["hesse_bins"])
    ) % radix["packet_frames_per_selector_sheet"]
    sheet_in_atlas = (
        probe_id
        // (
            radix["hashimoto_sectors"]
            * radix["hesse_bins"]
            * radix["packet_frames_per_selector_sheet"]
        )
    ) % radix["selector_sheets_per_atlas"]
    atlas_id = probe_id // (
        radix["hashimoto_sectors"]
        * radix["hesse_bins"]
        * radix["packet_frames_per_selector_sheet"]
        * radix["selector_sheets_per_atlas"]
    )

    return {
        "probe_id": probe_id,
        "runtime_slot_start": probe_id * radix["probe_slots"],
        "mirror_atlas_id": atlas_id,
        "selector_sheet_in_atlas": sheet_in_atlas,
        "packet_frame_in_selector_sheet": packet_frame,
        "hesse_bin": hesse_bin,
        "hashimoto_sector_id": sector_id,
        "hashimoto_sector": sector_labels[sector_id],
    }


def build_completion_samples(
    completion_incidences: int, probes_per_atlas: int, radix: dict[str, int]
) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for incidence in [
        0,
        1,
        2,
        3,
        probes_per_atlas - 1,
        probes_per_atlas,
        completion_incidences - 1,
    ]:
        local_probe = incidence % probes_per_atlas
        samples.append(
            {
                "completion_incidence_id": incidence,
                "ordered_path_id_budget": incidence // 3,
                "completion_choice_budget": incidence % 3,
                "ordered_path_in_atlas_budget": local_probe // 3,
                "completion_choice_in_atlas_budget": local_probe % 3,
                "control_word_at_probe_start": decode_probe_start(incidence, radix),
            }
        )
    return samples


def build_certificate() -> dict[str, Any]:
    frontier = load_json("artifacts/w33_periodic_table_organization_summary.json")[
        "rows"
    ]["frontier_witness_row"]
    control = load_json("data/w33_architecture_control_plane_abi.json")
    selector = load_json("data/w33_selector_e6_e8_runtime_bridge.json")
    lab = load_json("data/w33_frequency_bin_lab_packet.json")

    path_carrier = frontier["finite_ordered_path_carrier"]
    no_go = frontier["quadrangle_branch_packet_no_go"]
    transport = frontier["shared_transport_shadow"]
    arch = control["derived_architecture"]
    radix = control["control_word"]["radix"]
    lab_summary = lab["schedule_summary"]

    ordered_paths = int(path_carrier["path_count"])
    completions_per_path = int(path_carrier["completion_fibre_size"])
    completion_incidences = ordered_paths * completions_per_path
    quadrangles = int(no_go["nonlocal_quadrangle_count"])
    ordered_paths_per_quadrangle = completion_incidences // quadrangles
    probes_per_atlas = int(lab_summary["rows"])
    mirror_atlases = int(radix["mirror_atlases"])
    runtime_slots_per_probe = int(radix["probe_slots"])
    atlas_ordered_paths = ordered_paths // mirror_atlases

    per_atlas_control_product = (
        radix["selector_sheets_per_atlas"]
        * radix["packet_frames_per_selector_sheet"]
        * radix["hesse_bins"]
        * radix["hashimoto_sectors"]
    )

    samples = build_completion_samples(completion_incidences, probes_per_atlas, radix)

    checks = {
        "source_frontier_table_has_completion_carrier": ordered_paths == 4320
        and completions_per_path == 3
        and int(path_carrier["seed_completion_action_size"]) == 6,
        "source_control_plane_verified": control["verified"] is True,
        "source_selector_bridge_verified": selector["verified"] is True,
        "source_lab_packet_verified": lab["verified"] is True,
        "s3_order_matches_completion_action": int(transport["reduced_group_order"])
        == 6
        == int(path_carrier["seed_completion_action_size"]),
        "ordered_path_completion_surface_is_12960": completion_incidences == 12960,
        "quadrangle_ordered_path_surface_is_12960": quadrangles
        * ordered_paths_per_quadrangle
        == 1620 * 8
        == 12960,
        "probe_supercycle_surface_is_12960": arch["supercycle_probes"]
        == lab_summary["supercycle_probe_rows"]
        == completion_incidences,
        "atlas_surface_is_540": probes_per_atlas
        == int(no_go["target_cover_size"])
        == per_atlas_control_product
        == 540,
        "atlas_is_not_claimed_as_exact_cover": no_go["found_exact_cover"] is False,
        "twenty_four_atlases_tile_completion_surface": mirror_atlases * probes_per_atlas
        == completion_incidences,
        "per_atlas_ordered_paths_complete_to_probe_rows": atlas_ordered_paths
        * completions_per_path
        == probes_per_atlas,
        "runtime_lift_is_we6_supercycle": completion_incidences
        * runtime_slots_per_probe
        == arch["supercycle_slots"]
        == 51840,
        "selector_sheets_cut_surface_into_108s": selector["selector_e6_surface"][
            "sheet_count"
        ]
        * arch["probes_per_selector_sheet"]
        == completion_incidences,
        "signed_sheets_cut_surface_into_54s": arch["signed_sheet_count"]
        * arch["probes_per_signed_sheet"]
        == completion_incidences,
        "control_word_keeps_540_probe_atlas": radix["selector_sheets_per_atlas"] == 5
        and radix["packet_frames_per_selector_sheet"] == 6
        and radix["hesse_bins"] == 9
        and radix["hashimoto_sectors"] == 2,
    }

    return {
        "theorem": "W33 S3 completion-probe bridge",
        "verified": all(checks.values()),
        "breakthrough": (
            "The S3 completion frontier and the Holonet control-plane probe "
            "clock are the same 12960-element admission surface: 4320 ordered "
            "nonlocal paths times three completions equals 24 mirror atlases "
            "times 540 frequency-bin probes.  Each incidence owns four runtime "
            "slots, giving the 51840 W(E6) supercycle."
        ),
        "source_certificates": [
            "artifacts/w33_periodic_table_organization_summary.json",
            "data/w33_architecture_control_plane_abi.json",
            "data/w33_selector_e6_e8_runtime_bridge.json",
            "data/w33_frequency_bin_lab_packet.json",
        ],
        "frontier_completion_surface": {
            "ordered_nonlocal_paths": ordered_paths,
            "completions_per_path": completions_per_path,
            "completion_incidences": completion_incidences,
            "nonlocal_quadrangles": quadrangles,
            "ordered_paths_per_quadrangle": ordered_paths_per_quadrangle,
            "quadrangle_ordered_path_incidences": quadrangles
            * ordered_paths_per_quadrangle,
            "s3_reduced_group_order": int(transport["reduced_group_order"]),
            "seed_completion_action_size": int(
                path_carrier["seed_completion_action_size"]
            ),
            "target_cover_size": int(no_go["target_cover_size"]),
            "found_exact_cover": bool(no_go["found_exact_cover"]),
        },
        "probe_control_surface": {
            "mirror_atlases": mirror_atlases,
            "probes_per_mirror_atlas": probes_per_atlas,
            "supercycle_probes": arch["supercycle_probes"],
            "runtime_slots_per_probe": runtime_slots_per_probe,
            "supercycle_runtime_slots": arch["supercycle_slots"],
            "control_word_atlas_probe_product": (
                "5 selector sheets * 6 packet frames * 9 Hesse bins * "
                "2 Hashimoto sectors = 540 probes"
            ),
            "runtime_lift": "12960 probes * 4 slots = 51840",
        },
        "bridge_identities": {
            "completion_carrier": "4320 ordered paths * 3 completions = 12960",
            "quadrangle_incidence": "1620 nonlocal quadrangles * 8 ordered boundary paths = 12960",
            "atlas_probe_clock": "24 mirror atlases * 540 probes = 12960",
            "atlas_path_clock": "180 ordered paths/atlas * 3 completions = 540 probes/atlas",
            "selector_sheet_probe_clock": "120 selector sheets * 108 probes = 12960",
            "signed_sheet_probe_clock": "240 signed sheets * 54 probes = 12960",
            "runtime_clock": "12960 probes * 4 runtime slots = 51840",
        },
        "completion_probe_samples": samples,
        "checks": checks,
        "claim_boundary": [
            "This is a completion-probe admission surface, not a canonical golden selector.",
            "The inherited 540-cover search explicitly found no exact cover, so one mirror atlas should be read as a full probe surface, not a solved branch packet.",
            "The budget map path/completion -> probe is an address schedule; it does not identify a unique geometric completion with a unique Hesse bin.",
            "Bench visibility, phase error, loss, detector efficiency, and physical frequency spacing remain outside this certificate.",
        ],
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print("  bridge: 4320*3 = 24*540 = 12960; 12960*4 = 51840")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
