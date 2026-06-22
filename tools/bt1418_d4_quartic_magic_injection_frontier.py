#!/usr/bin/env python3
"""BT1418: finite D4-quartic magic injection frontier.

BT1415 and BT1416 reserve 24 guard rows at the tail of the 240-edge CSS
ledger.  The exact minimal-magic audit says the remaining signed non-Clifford
frontier is two independent irreducible D4 quartic atoms.  This packet matches
those facts without using continuum electron-model assumptions:

    2 quartic atoms * 4 algebraic branches * 3 qutrit phases = 24 guard apertures
    24 guard apertures * 8 D4 orientations = 192 tomotope orientation tokens.

For each atom, the Steinberg lift gives 4 branches * 27 central cycles *
8 D4 orientations = 864, exactly the existing repo Golden D4/Weyl shell.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from scripts.w33_standard_model_minimal_magic_audit import (  # noqa: E402
    analyze as analyze_magic,
)

OUT = ROOT / "data" / "bt1418_d4_quartic_magic_injection_frontier.json"

D4_ORIENTATION_LABELS = [
    "forward_start_anchor",
    "forward_start_left_endpoint",
    "forward_start_bridge",
    "forward_start_right_endpoint",
    "reverse_start_anchor",
    "reverse_start_left_endpoint",
    "reverse_start_bridge",
    "reverse_start_right_endpoint",
]


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def build_atoms(magic: dict[str, Any]) -> list[dict[str, Any]]:
    quartic = magic["quartic_magic_atoms"]
    return [
        {
            "atom": 0,
            "name": "H_2:-+",
            "quartic_polynomial": quartic["h2_quartic_polynomial"],
            "galois_group_label": quartic["h2_galois_group_label"],
            "galois_group_order": quartic["h2_galois_group_order"],
        },
        {
            "atom": 1,
            "name": "Hbar_2:+-",
            "quartic_polynomial": quartic["hbar2_quartic_polynomial"],
            "galois_group_label": quartic["hbar2_galois_group_label"],
            "galois_group_order": quartic["hbar2_galois_group_order"],
        },
    ]


def build_result() -> dict[str, Any]:
    bt1413 = load_json("data/bt1413_q4_plaquette_tomotope_face_compiler.json")
    bt1415 = load_json("data/bt1415_even_projection_steinberg_syndrome_layer.json")
    bt1416 = load_json("data/bt1416_css_sparse_intertwiner_matrices.json")
    golden = load_json("data/PART_MMCCCLXXIV_GOLDEN_D4_WEYL_BRIDGE_results.json")
    magic = analyze_magic()
    atoms = build_atoms(magic)

    guard_rows = bt1415["guard_rows"]
    central_cycles = bt1415["syndrome_summary"]["steinberg_central_cycles"]
    apertures = []
    for atom in atoms:
        for branch in range(4):
            for qutrit_phase in range(3):
                aperture = atom["atom"] * 12 + branch * 3 + qutrit_phase
                guard = guard_rows[aperture]
                apertures.append(
                    {
                        "resource_aperture": aperture,
                        "atom": atom["atom"],
                        "atom_name": atom["name"],
                        "quartic_branch": branch,
                        "qutrit_phase": qutrit_phase,
                        "css_edge_index": guard["css_edge_index"],
                        "guard_tomotope_flag": guard["tomotope_flag"],
                        "q4_plaquette": guard["q4_plaquette"],
                    }
                )

    oriented_tokens = []
    for aperture in apertures:
        for orientation, label in enumerate(D4_ORIENTATION_LABELS):
            oriented_tokens.append(
                {
                    "resource_token": len(oriented_tokens),
                    "tomotope_flag": aperture["resource_aperture"] * 8 + orientation,
                    "resource_aperture": aperture["resource_aperture"],
                    "atom": aperture["atom"],
                    "quartic_branch": aperture["quartic_branch"],
                    "qutrit_phase": aperture["qutrit_phase"],
                    "d4_orientation": orientation,
                    "d4_orientation_label": label,
                }
            )

    per_atom_golden_shell = 4 * central_cycles * len(D4_ORIENTATION_LABELS)
    checks = {
        "bt1413_flag_bus_loaded": bt1413["verified"] is True,
        "bt1415_ledger_loaded": bt1415["verified"] is True,
        "bt1416_intertwiner_loaded": bt1416["verified"] is True,
        "minimal_magic_has_two_atoms": len(atoms) == 2
        and magic["quartic_magic_atoms"]["packet_size"] == 2,
        "both_atoms_are_irreducible_d4_quartics": all(
            atom["galois_group_label"] == "D4" and atom["galois_group_order"] == 8
            for atom in atoms
        ),
        "atoms_are_field_independent": magic["quartic_magic_atoms"][
            "shared_quadratic_subfield_squarefree_parts"
        ]
        == ()
        and magic["quartic_magic_atoms"]["quartic_splitting_field_galois_group"]
        == "D4 x D4"
        and magic["quartic_magic_atoms"]["quartic_splitting_field_compositum_degree"]
        == 64,
        "canonical_mixing_raises_degree": magic["quartic_magic_atoms"][
            "mixed_product_degree"
        ]
        == 8
        and magic["quartic_magic_atoms"]["mixed_ratio_degree"] == 8
        and magic["quartic_magic_atoms"]["mixed_sum_degree"] == 16,
        "guard_apertures_are_two_atoms_four_branches_three_phases": len(apertures)
        == 2 * 4 * 3
        == len(guard_rows)
        == 24,
        "apertures_use_css_tail": [row["css_edge_index"] for row in apertures]
        == list(range(216, 240)),
        "d4_orientation_lift_fills_tomotope_flag_bus": len(oriented_tokens)
        == len(apertures) * 8
        == len(bt1413["flag_rows"])
        == 192,
        "oriented_tokens_are_bijective_tomotope_flags": sorted(
            row["tomotope_flag"] for row in oriented_tokens
        )
        == list(range(192)),
        "per_atom_steinberg_d4_shell_matches_golden_d4_weyl_shell": per_atom_golden_shell
        == golden["counts"]["ordered_failures"]
        == 864,
        "two_atom_shell_is_double_golden_shell": 2 * per_atom_golden_shell == 1728,
        "external_moebius_ball_not_used_as_validation": bt1415[
            "external_literature_audit"
        ]["status"]
        == "heuristic_only_not_a_validation_source",
    }

    return {
        "bt": 1418,
        "title": "Finite D4-quartic magic injection frontier",
        "verified": all(checks.values()),
        "atom_summary": {
            "atoms": atoms,
            "quartic_atoms": 2,
            "quartic_branches_per_atom": 4,
            "qutrit_phases": 3,
            "guard_apertures": len(apertures),
            "d4_orientations": len(D4_ORIENTATION_LABELS),
            "oriented_tomotope_tokens": len(oriented_tokens),
            "identity": "2 atoms * 4 branches * 3 qutrit phases = 24; times 8 D4 orientations = 192",
        },
        "golden_shell_comparison": {
            "repo_golden_d4_weyl_shell": golden["counts"]["ordered_failures"],
            "per_atom_steinberg_d4_shell": per_atom_golden_shell,
            "two_atom_steinberg_d4_shell": 2 * per_atom_golden_shell,
            "identity": "4 quartic branches * 27 Steinberg cycles * 8 D4 orientations = 864 per atom",
            "reading": (
                "The exact finite counterpart of a golden-quartic topology is the "
                "repo's D4/Weyl orientation shell, not the continuum Moebius-ball "
                "electron hypothesis."
            ),
        },
        "resource_apertures": apertures,
        "oriented_resource_tokens_sample": oriented_tokens[:48],
        "oriented_resource_token_count": len(oriented_tokens),
        "physical_reading": (
            "The 24 Q4 guard apertures become the non-Clifford injection rail: "
            "two independent D4 quartic atoms, four branches each, three qutrit "
            "phases per branch. The internal D4 orientation torsor expands those "
            "24 apertures to the full 192 tomotope flag bus."
        ),
        "boundary": (
            "BT1418 is a finite resource-state injection certificate. It does not "
            "derive electron structure, does not calibrate an optical nonlinear "
            "source, and does not collapse the two independent D4 atoms into one."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "guard_apertures": result["atom_summary"]["guard_apertures"],
                "oriented_tomotope_tokens": result["atom_summary"][
                    "oriented_tomotope_tokens"
                ],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
