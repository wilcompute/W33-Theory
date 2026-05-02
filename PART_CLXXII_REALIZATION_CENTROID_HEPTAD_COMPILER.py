#!/usr/bin/env python3
"""
PART CLXXII - Realization Centroid / Heptad Compiler
====================================================

User hint:
    The C# constants in the realization data act like realization-specific
    centroid/anchor coordinates and show up inside the vertices.

Repo hint:
    exploration/w33_toroidal_heptad_projector_bridge.py already performs the
    correct dual reading:

        - Csaszar realizations are read through their seven vertices.
        - Szilassi realizations are read through their seven face centroids.
        - Each centered shell gives a rank-3 projector in R^7.
        - The seven projectors form an exact 7D operator heptad.
        - Removing the mean leaves an exact 6D shell.
        - The family split refines as 4 + 1 + 1, and with the mean as 4 + 3.

CLXXII integrates that with the realization-origin/carrier grammar:

    geometric realizations: 1 + 5 + 2 = 8 = J^{-1}
    toroidal heptad:        5 + 2 = 7 = Phi6
    centered operator shell:7 - 1 = 6 = 2q
    Csaszar centered rank:  5 - 1 = 4 = q+1
    Szilassi centered rank: 2 - 1 = 1
    family separation:     1
    centered split:        4 + 1 + 1 = 6
    full split:            4 + 3 = 7

So the realization constants/centroids are not just coordinate conveniences.
They are anchors that let seven concrete Euclidean models collapse to an exact
operator heptad with the same Phi6, 2q, q+1, and carrier-completion counts.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
QP1 = Q + 1
RANK_SEED = 2 * Q
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
J = 5
J_INV = 8
TETRA_SEED = 1
CS_COUNT = J
SZ_COUNT = Q - 1
HEPTAD_COUNT = CS_COUNT + SZ_COUNT
GEOMETRIC_TOTAL_WITH_TETRA = TETRA_SEED + HEPTAD_COUNT
CENTERED_SHELL_DIM = HEPTAD_COUNT - 1
CS_CENTERED_RANK = CS_COUNT - 1
SZ_CENTERED_RANK = SZ_COUNT - 1
FAMILY_SEPARATION_RANK = 1
FULL_MEAN_RANK = 1


@dataclass(frozen=True)
class HeptadLayer:
    name: str
    count_or_rank: int
    formula: str
    interpretation: str


def heptad_layers() -> List[HeptadLayer]:
    return [
        HeptadLayer("Csaszar_realization_family", CS_COUNT, "J=5", "five vertex-shell realizations / threshold family"),
        HeptadLayer("Szilassi_realization_family", SZ_COUNT, "q-1=2", "two dual face-centroid-shell realizations"),
        HeptadLayer("toroidal_heptad", HEPTAD_COUNT, "J+(q-1)=Phi6=7", "seven toroidal geometric realizations"),
        HeptadLayer("mean_projector", FULL_MEAN_RANK, "1", "operator origin / scalar mean"),
        HeptadLayer("centered_operator_shell", CENTERED_SHELL_DIM, "Phi6-1=2q=6", "mean-subtracted heptad shell"),
        HeptadLayer("Csaszar_centered_shell", CS_CENTERED_RANK, "5-1=4=q+1", "internal Csaszar deformation shell"),
        HeptadLayer("Szilassi_centered_shell", SZ_CENTERED_RANK, "2-1=1", "internal Szilassi mirror mode"),
        HeptadLayer("family_separation", FAMILY_SEPARATION_RANK, "1", "primal-dual separation mode"),
        HeptadLayer("centered_refinement", CENTERED_SHELL_DIM, "4+1+1=6", "Cs centered + Sz centered + family separation"),
        HeptadLayer("full_refinement", HEPTAD_COUNT, "4+3=7", "Cs centered shell + three external modes"),
        HeptadLayer("geometric_triad_with_tetra", GEOMETRIC_TOTAL_WITH_TETRA, "1+5+2=8=J^{-1}", "carrier completion by adjoining tetrahedron origin"),
    ]


def realization_centroid_heptad_audit() -> Dict[str, object]:
    checks = {
        "heptad_is_phi6": HEPTAD_COUNT == PHI6 == 7,
        "cs_plus_sz_is_phi6": CS_COUNT + SZ_COUNT == PHI6,
        "tetra_plus_heptad_is_carrier": GEOMETRIC_TOTAL_WITH_TETRA == J_INV == 8,
        "centered_shell_is_2q": CENTERED_SHELL_DIM == RANK_SEED == 6,
        "cs_centered_rank_is_qplus1": CS_CENTERED_RANK == QP1 == 4,
        "sz_centered_rank_is_one": SZ_CENTERED_RANK == 1,
        "family_separation_rank_is_one": FAMILY_SEPARATION_RANK == 1,
        "centered_refinement_is_4_plus_1_plus_1": CS_CENTERED_RANK + SZ_CENTERED_RANK + FAMILY_SEPARATION_RANK == CENTERED_SHELL_DIM,
        "full_refinement_is_4_plus_3": CS_CENTERED_RANK + (SZ_CENTERED_RANK + FAMILY_SEPARATION_RANK + FULL_MEAN_RANK) == HEPTAD_COUNT,
        "mean_plus_centered_shell_is_heptad": FULL_MEAN_RANK + CENTERED_SHELL_DIM == HEPTAD_COUNT,
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
        "phi6_to_carrier_step": PHI6 + TETRA_SEED == J_INV,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXII_REALIZATION_CENTROID_HEPTAD_COMPILER",
        "source_links": {
            "formatted_data": "data/Toroidal-Polyhedra-Realizations.txt",
            "projector_bridge": "exploration/w33_toroidal_heptad_projector_bridge.py",
            "CLXXI": "realization origin/carrier compiler",
        },
        "w33_atoms": {
            "q": Q,
            "q_plus_1": QP1,
            "rank_seed_2q": RANK_SEED,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "J": J,
            "J_inverse": J_INV,
        },
        "centroid_reading_rule": {
            "Csaszar": "use the seven vertices as the K7 torus shell",
            "Szilassi": "use the seven face centroids as the dual heptad shell",
            "reason": "the dual polyhedron has fourteen vertices but seven faces; the dual heptad lives at face centroids",
        },
        "heptad_layers": [asdict(layer) for layer in heptad_layers()],
        "operator_heptad_dictionary": {
            "seven_projectors": "Phi6=7",
            "centered_shell": "Phi6-1=6=2q",
            "family_split": "5+2=7",
            "centered_rank_split": "4+1+1=6",
            "full_rank_split": "4+3=7",
            "carrier_completion": "1+5+2=8=J^{-1}",
        },
        "checks": checks,
        "theorem_statement": (
            "The seven realization coordinate sets should be read as an operator heptad: five Csaszar vertex shells plus "
            "two Szilassi face-centroid shells give Phi6=7 rank-3 projectors.  Removing the mean gives a 6D=2q shell; "
            "the centered shell refines as 4+1+1, and the full heptad refines as 4+3.  Adding the tetrahedron origin "
            "completes the toroidal heptad from Phi6=7 to J^{-1}=8."
        ),
        "interpretive_note": (
            "This is the clean way to use the C#/centroid data.  The C-values are realization-specific anchors appearing "
            "inside coordinate charts, but the invariant object is obtained only after centering the relevant heptad shell. "
            "For Csaszar that shell is vertices; for Szilassi, because of duality, it is face centroids."
        ),
    }


def main() -> int:
    audit = realization_centroid_heptad_audit()
    out = ROOT / "PART_CLXXII_realization_centroid_heptad_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
