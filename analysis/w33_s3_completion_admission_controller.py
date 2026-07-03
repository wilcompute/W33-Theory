#!/usr/bin/env python3
"""Compile the S3 completion-probe surface into an admission controller.

The completion-probe bridge made the missing selector frontier addressable.
This file turns that addressability into a runtime transaction shape:

    one ordered path = three candidate completions * four probe slots = 12 ticks
    one atlas        = 180 ordered paths * 12 ticks = 2160 ticks
    one supercycle   = 4320 ordered paths * 12 ticks = 51840 ticks

The controller is intentionally conservative.  It can accept a branch only
from measured evidence with a unique winner; without bench data it emits an
unresolved/escalation schema.  The inherited exact-cover no-go remains a hard
guardrail: this is not a static 540-quadrangle selector packet.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_s3_completion_admission_controller.json"

PROBE_TICKS = (
    "LOAD_PATH_CONTEXT",
    "EMIT_COMPLETION_PROBE",
    "LATCH_BRANCH_EVIDENCE",
    "ADJUDICATE_OR_ESCALATE",
)


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def adjudicate_branch(
    evidence: list[float | None],
    *,
    minimum_signal: float,
    minimum_margin: float,
) -> dict[str, Any]:
    if len(evidence) != 3:
        raise ValueError("S3 admission evidence must have three completion channels")
    if any(value is None for value in evidence):
        return {
            "state": "UNMEASURED",
            "accepted_completion": None,
            "reason": "bench evidence has not been supplied for all three branches",
        }

    numeric = [float(value) for value in evidence]
    ranked = sorted(enumerate(numeric), key=lambda item: (-item[1], item[0]))
    winner, best = ranked[0]
    runner_up, second = ranked[1]
    margin = best - second

    if best < minimum_signal:
        return {
            "state": "NO_SIGNAL",
            "accepted_completion": None,
            "reason": "strongest branch is below the preregistered signal floor",
            "winner": winner,
            "runner_up": runner_up,
            "margin": margin,
        }
    if margin < minimum_margin:
        return {
            "state": "AMBIGUOUS",
            "accepted_completion": None,
            "reason": "top two branches are not separated by the preregistered margin",
            "winner": winner,
            "runner_up": runner_up,
            "margin": margin,
        }
    return {
        "state": "BRANCH_ACCEPTED",
        "accepted_completion": winner,
        "reason": "unique measured winner clears signal and margin thresholds",
        "winner": winner,
        "runner_up": runner_up,
        "margin": margin,
    }


def path_word_sample(
    path_id: int, completions_per_path: int, slots_per_probe: int
) -> dict[str, Any]:
    base_probe = path_id * completions_per_path
    branch_words = []
    for completion in range(completions_per_path):
        probe_id = base_probe + completion
        tick_start = probe_id * slots_per_probe
        branch_words.append(
            {
                "completion_choice": completion,
                "probe_id": probe_id,
                "runtime_slots": list(range(tick_start, tick_start + slots_per_probe)),
                "tick_roles": list(PROBE_TICKS),
            }
        )
    return {
        "ordered_path_id": path_id,
        "path_runtime_slots": list(
            range(
                base_probe * slots_per_probe,
                (base_probe + completions_per_path) * slots_per_probe,
            )
        ),
        "branch_words": branch_words,
    }


def build_certificate() -> dict[str, Any]:
    bridge = load_json("data/w33_s3_completion_probe_bridge.json")
    control = load_json("data/w33_architecture_control_plane_abi.json")
    branch_search = load_json("artifacts/w33_periodic_table_organization_summary.json")[
        "rows"
    ]["frontier_witness_row"]["quadrangle_branch_packet_no_go"]

    frontier = bridge["frontier_completion_surface"]
    probe = bridge["probe_control_surface"]
    arch = control["derived_architecture"]

    ordered_paths = int(frontier["ordered_nonlocal_paths"])
    completions_per_path = int(frontier["completions_per_path"])
    runtime_slots_per_probe = int(probe["runtime_slots_per_probe"])
    path_word_ticks = completions_per_path * runtime_slots_per_probe
    mirror_atlases = int(probe["mirror_atlases"])
    paths_per_atlas = ordered_paths // mirror_atlases
    probes_per_path = completions_per_path
    probes_per_atlas = paths_per_atlas * probes_per_path

    thresholds = {
        "minimum_signal": 1.0,
        "minimum_margin": 0.25,
        "threshold_units": "normalized bench evidence units",
        "threshold_status": "schema placeholder; preregister before bench runs",
    }
    example_adjudications = {
        "unmeasured": adjudicate_branch(
            [None, None, None],
            minimum_signal=thresholds["minimum_signal"],
            minimum_margin=thresholds["minimum_margin"],
        ),
        "accepted": adjudicate_branch(
            [2.0, 1.1, 0.7],
            minimum_signal=thresholds["minimum_signal"],
            minimum_margin=thresholds["minimum_margin"],
        ),
        "ambiguous": adjudicate_branch(
            [2.0, 1.9, 0.3],
            minimum_signal=thresholds["minimum_signal"],
            minimum_margin=thresholds["minimum_margin"],
        ),
        "no_signal": adjudicate_branch(
            [0.4, 0.2, 0.1],
            minimum_signal=thresholds["minimum_signal"],
            minimum_margin=thresholds["minimum_margin"],
        ),
    }

    sample_path_ids = [0, 1, paths_per_atlas - 1, paths_per_atlas, ordered_paths - 1]
    samples = [
        path_word_sample(path_id, completions_per_path, runtime_slots_per_probe)
        for path_id in sample_path_ids
    ]

    checks = {
        "source_completion_probe_bridge_verified": bridge["verified"] is True,
        "source_control_plane_verified": control["verified"] is True,
        "controller_uses_s3_three_branch_evidence": completions_per_path == 3,
        "probe_word_has_four_named_ticks": runtime_slots_per_probe
        == len(PROBE_TICKS)
        == 4,
        "ordered_path_word_is_12_ticks": path_word_ticks == 12,
        "atlas_has_180_ordered_paths": paths_per_atlas == 180,
        "atlas_has_540_probes": probes_per_atlas
        == int(probe["probes_per_mirror_atlas"])
        == 540,
        "atlas_runtime_is_2160": paths_per_atlas * path_word_ticks
        == arch["packet_frames_per_mirror_atlas"] * 72
        == 2160,
        "supercycle_runtime_is_51840": ordered_paths * path_word_ticks
        == arch["supercycle_slots"]
        == 51840,
        "exact_cover_no_go_is_guardrail": bool(branch_search["found_exact_cover"])
        is False
        and int(branch_search["target_cover_size"]) == 540,
        "adjudicator_accepts_only_unique_margin_winner": (
            example_adjudications["accepted"]["state"] == "BRANCH_ACCEPTED"
            and example_adjudications["accepted"]["accepted_completion"] == 0
            and example_adjudications["ambiguous"]["state"] == "AMBIGUOUS"
            and example_adjudications["no_signal"]["state"] == "NO_SIGNAL"
            and example_adjudications["unmeasured"]["state"] == "UNMEASURED"
        ),
        "sample_path_words_hit_atlas_boundaries": (
            samples[0]["path_runtime_slots"][0] == 0
            and samples[2]["path_runtime_slots"][-1] == 2159
            and samples[3]["path_runtime_slots"][0] == 2160
            and samples[-1]["path_runtime_slots"][-1] == 51839
        ),
    }

    return {
        "theorem": "W33 S3 completion admission controller",
        "verified": all(checks.values()),
        "breakthrough": (
            "The 12960-probe completion surface is now a conservative runtime "
            "admission controller.  Each ordered path owns a 12-tick S3 word: "
            "three candidate completions, each with four probe/adjudication "
            "ticks.  One atlas is 180 such path words, exactly 2160 ticks; the "
            "full 4320-path surface is exactly the 51840-slot supercycle."
        ),
        "source_certificates": [
            "data/w33_s3_completion_probe_bridge.json",
            "data/w33_architecture_control_plane_abi.json",
            "artifacts/w33_periodic_table_organization_summary.json",
        ],
        "admission_word": {
            "ordered_paths": ordered_paths,
            "completions_per_path": completions_per_path,
            "runtime_slots_per_probe": runtime_slots_per_probe,
            "path_word_ticks": path_word_ticks,
            "paths_per_mirror_atlas": paths_per_atlas,
            "probes_per_mirror_atlas": probes_per_atlas,
            "mirror_atlases": mirror_atlases,
            "probe_tick_roles": list(PROBE_TICKS),
            "identity": "4320 paths * 3 completions/path * 4 ticks/completion = 51840",
        },
        "adjudication_policy": {
            "state_order": [
                "UNMEASURED",
                "NO_SIGNAL",
                "AMBIGUOUS",
                "BRANCH_ACCEPTED",
                "ESCALATE_HOLONOMY",
            ],
            "thresholds": thresholds,
            "example_adjudications": example_adjudications,
            "guardrail": (
                "The controller never promotes a raw 540-quadrangle exact cover; "
                "that model is already certified to have no solution."
            ),
        },
        "runtime_samples": samples,
        "checks": checks,
        "claim_boundary": [
            "This is an admission/state-machine ABI, not measured branch evidence.",
            "Thresholds are schema placeholders and must be preregistered before lab runs.",
            "A branch can be accepted only from supplied evidence with a unique margin winner.",
            "The exact-cover no-go remains active: a 540-row atlas is not a canonical quadrangle packet.",
        ],
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print("  admission word: 4320*3*4 = 51840")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
