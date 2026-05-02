#!/usr/bin/env python3
"""
PART CLXXXIV - Heptad Projector / Cayley Sign Bridge
====================================================

CLXXXI ranked the third bridge as:

    projector heptad -> Cayley signs.

The relevant source file is

    exploration/w33_toroidal_heptad_projector_bridge.py

which states/proves structurally that the seven toroidal realizations give
rank-3 shell projectors with exact packet data:

    5 Csaszar + 2 Szilassi = 7 = Phi6
    all seven projectors span a 7D heptad
    subtracting the mean leaves a 6D centered shell
    the centered split refines as 4 + 1 + 1 = 6
    the full heptad refines as 4 + 3 = 7
    the centered shell matches C(4,2)=6 bivectors
    the toroidal genus numerator 12 is the orientation double cover of 6

CLXXIV made the Cayley algebra:

    7 Fano residues -> imaginary octonion units
    1 + 7 = 8 carrier
    Fano lines determine signs/multiplication

CLXXXIV welds these as a sign-capacity theorem:

    The projector heptad supplies the 7 units and 6D bivector shell required by
    an oriented Fano/Cayley multiplication table.  Its orientation double cover
    12 matches the toroidal genus numerator and the mod-12 sign/phase wheel.

Important honesty note:
    The generated projector summary file

        data/w33_toroidal_heptad_projector_bridge_summary.json

    is not presently committed on master.  Therefore this file does not claim
    numerical Gram spectra beyond what is stated in the source file.  It records
    the structural Cayley-sign compatibility and the exact rerun protocol needed
    to upgrade this into a measured projector-sign audit.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent

Q = 3
Q2 = 9
Q3 = 27
Q4 = 81
PHI3 = 13
PHI6 = 7
J = 5
J_INV = 8
K = 12
RANK_SEED = 2 * Q

CSASZAR_PROJECTORS = J
SZILASSI_PROJECTORS = Q - 1
PROJECTOR_HEPTAD = CSASZAR_PROJECTORS + SZILASSI_PROJECTORS
MEAN_LINE = 1
CENTERED_SHELL = PROJECTOR_HEPTAD - MEAN_LINE
CSASZAR_CENTERED = CSASZAR_PROJECTORS - 1
SZILASSI_CENTERED = SZILASSI_PROJECTORS - 1
FAMILY_SEPARATION = 1
BIVECTOR_DIM_4 = 4 * 3 // 2
ORIENTATION_DOUBLE = 2 * CENTERED_SHELL
CAYLEY_CARRIER = 1 + PROJECTOR_HEPTAD
FANO_POINTS = PROJECTOR_HEPTAD
FANO_LINES = PROJECTOR_HEPTAD
FANO_PAIRS = PROJECTOR_HEPTAD * (PROJECTOR_HEPTAD - 1) // 2
OCTONION_IMAGINARY_PRODUCTS = FANO_PAIRS
ALBERT_DIM = 3 + 3 * CAYLEY_CARRIER

# Residue Fano/Cayley labels from CLXXIV.
HEPTAD_RESIDUES = [1, 5, 12, 8, 3, 6, 9]
FANO_LINES_RESIDUES: List[Tuple[int, int, int]] = [
    (1, 5, 3),
    (12, 8, 3),
    (1, 12, 6),
    (5, 8, 6),
    (1, 8, 9),
    (5, 12, 9),
    (3, 6, 9),
]

EXPECTED_PROJECTOR_ARTIFACTS = [
    "data/w33_toroidal_heptad_projector_bridge_summary.json",
]

SOURCE_TOOLS = [
    "exploration/w33_toroidal_heptad_projector_bridge.py",
    "data/Toroidal-Polyhedra-Realizations.txt",
    "PART_CLXXIV_FANO_CAYLEY_ALBERT_E6_ALGEBRA.py",
]


@dataclass(frozen=True)
class ProjectorCayleyLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def projector_cayley_layers() -> List[ProjectorCayleyLayer]:
    return [
        ProjectorCayleyLayer("Csaszar_family", CSASZAR_PROJECTORS, "J=5", "five vertex-shell projectors"),
        ProjectorCayleyLayer("Szilassi_family", SZILASSI_PROJECTORS, "q-1=2", "two face-centroid shell projectors"),
        ProjectorCayleyLayer("projector_heptad", PROJECTOR_HEPTAD, "5+2=Phi6=7", "seven rank-3 projectors / seven Fano units"),
        ProjectorCayleyLayer("mean_line", MEAN_LINE, "1", "scalar/projector mean line"),
        ProjectorCayleyLayer("centered_shell", CENTERED_SHELL, "7-1=6=2q", "mean-subtracted projector shell"),
        ProjectorCayleyLayer("centered_refinement", CENTERED_SHELL, "4+1+1=6", "Cs centered + Sz centered + family separation"),
        ProjectorCayleyLayer("full_refinement", PROJECTOR_HEPTAD, "4+3=7", "Cs internal shell plus three external modes"),
        ProjectorCayleyLayer("bivector_match", BIVECTOR_DIM_4, "C(4,2)=6", "Clifford bivector shell dimension"),
        ProjectorCayleyLayer("orientation_double", ORIENTATION_DOUBLE, "2*6=12=k", "oriented bivector/sign double cover"),
        ProjectorCayleyLayer("Cayley_carrier", CAYLEY_CARRIER, "1+7=8=J^{-1}", "octonion scalar plus heptad"),
        ProjectorCayleyLayer("Fano_pairs", FANO_PAIRS, "C(7,2)=21", "unordered imaginary unit products"),
        ProjectorCayleyLayer("Fano_lines", FANO_LINES, "7", "multiplication triples/sign cycles"),
        ProjectorCayleyLayer("Albert_generation", ALBERT_DIM, "3+3*8=27", "one Albert generation after Cayley completion"),
        ProjectorCayleyLayer("artifact_status", "rerun needed", "projector summary JSON absent", "explicit Gram-to-sign extraction not claimed here"),
    ]


def _pair_coverage(lines: List[Tuple[int, int, int]]) -> Dict[Tuple[int, int], int]:
    out: Dict[Tuple[int, int], int] = {}
    for a, b, c in lines:
        for x, y in [(a, b), (a, c), (b, c)]:
            key = tuple(sorted((x, y)))
            out[key] = out.get(key, 0) + 1
    return out


def heptad_projector_cayley_sign_bridge_audit() -> Dict[str, object]:
    pair_coverage = _pair_coverage(FANO_LINES_RESIDUES)
    checks = {
        "projector_heptad_is_phi6": PROJECTOR_HEPTAD == PHI6 == 7,
        "family_split_is_5_plus_2": CSASZAR_PROJECTORS == J == 5 and SZILASSI_PROJECTORS == Q - 1 == 2,
        "centered_shell_is_2q": CENTERED_SHELL == RANK_SEED == 6,
        "centered_refinement_is_4_plus_1_plus_1": CSASZAR_CENTERED + SZILASSI_CENTERED + FAMILY_SEPARATION == CENTERED_SHELL == 6,
        "full_refinement_is_4_plus_3": CSASZAR_CENTERED + (SZILASSI_CENTERED + FAMILY_SEPARATION + MEAN_LINE) == PROJECTOR_HEPTAD == 7,
        "bivector_dimension_match": BIVECTOR_DIM_4 == CENTERED_SHELL == 6,
        "orientation_double_is_k": ORIENTATION_DOUBLE == K == 12,
        "cayley_carrier_is_eight": CAYLEY_CARRIER == J_INV == 8,
        "albert_generation_is_27": ALBERT_DIM == Q3 == 27,
        "fano_points_are_heptad": len(HEPTAD_RESIDUES) == FANO_POINTS == 7,
        "fano_lines_are_seven": len(FANO_LINES_RESIDUES) == FANO_LINES == 7,
        "fano_pair_count_is_21": FANO_PAIRS == 21,
        "fano_lines_cover_each_pair_once": len(pair_coverage) == FANO_PAIRS and all(v == 1 for v in pair_coverage.values()),
        "source_tools_registered": len(SOURCE_TOOLS) == 3,
        "expected_projector_artifacts_registered": len(EXPECTED_PROJECTOR_ARTIFACTS) == 1,
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXXIV_HEPTAD_PROJECTOR_CAYLEY_SIGN_BRIDGE",
        "status": "structural sign-capacity audit; projector Gram/sign extraction artifact rerun still needed",
        "source_links": {
            "projector_bridge": "exploration/w33_toroidal_heptad_projector_bridge.py",
            "CLXXII": "realization centroid heptad compiler",
            "CLXXIV": "Fano-Cayley / Albert / E6 algebra",
            "CLXXX": "master identity ladder",
        },
        "source_tools": SOURCE_TOOLS,
        "expected_generated_artifacts": EXPECTED_PROJECTOR_ARTIFACTS,
        "w33_atoms": {
            "q": Q,
            "q2": Q2,
            "q3": Q3,
            "q4": Q4,
            "Phi3": PHI3,
            "Phi6": PHI6,
            "J": J,
            "J_inverse": J_INV,
            "k": K,
            "rank_seed_2q": RANK_SEED,
        },
        "projector_cayley_layers": [asdict(layer) for layer in projector_cayley_layers()],
        "fano_cayley_data": {
            "heptad_residues": HEPTAD_RESIDUES,
            "fano_lines_residue_labels": [list(line) for line in FANO_LINES_RESIDUES],
            "pair_coverage_count": len(pair_coverage),
            "each_unordered_pair_appears_once": all(v == 1 for v in pair_coverage.values()),
            "multiplication_rule": "each oriented Fano line supplies cyclic positive products and anti-cyclic negative products",
        },
        "bridge_identities": {
            "projector_to_units": "7 projectors = Phi6 = seven imaginary Cayley units",
            "mean_to_scalar": "mean line supplies the scalar/origin completion 1+7=8",
            "centered_to_bivectors": "centered projector shell dimension 6 matches C(4,2) bivectors",
            "orientation_to_signs": "2*6=12 gives the oriented sign/phase double cover needed for Cayley multiplication",
            "fano_capacity": "7 lines cover C(7,2)=21 pairs exactly once, so the heptad has the combinatorial capacity for octonion products",
            "measurement_gap": "explicit projector Gram spectra/sign extraction requires regenerating data/w33_toroidal_heptad_projector_bridge_summary.json",
        },
        "rerun_protocol": {
            "step_1": "python exploration/w33_toroidal_heptad_projector_bridge.py",
            "step_2": "commit data/w33_toroidal_heptad_projector_bridge_summary.json if generated",
            "step_3": "extract projector overlap matrix and centered Gram eigenvectors",
            "step_4": "compare Gram/parity orientation with PART_CLXXIV Fano-Cayley oriented lines",
            "desired_measurements": [
                "projector overlap matrix",
                "centered Gram eigenvectors/eigenvalues",
                "family separation vector orientation",
                "whether Gram parity determines Fano line signs",
                "residual between projector-induced signs and Cayley signs",
            ],
        },
        "checks": checks,
        "theorem_statement": (
            "Structurally, the toroidal projector heptad has exactly the sign capacity required by the Fano-Cayley algebra. "
            "The seven projectors supply the seven imaginary units; the mean supplies the scalar origin; the centered 6D shell "
            "matches the C(4,2) bivector space; and its orientation double cover 12 supplies the sign/phase wheel.  The Fano "
            "line system covers all 21 unordered pairs exactly once, giving the required octonion multiplication skeleton.  "
            "Numerical projector-Gram extraction is still needed to decide whether the realizations determine the signs uniquely."
        ),
        "interpretive_note": (
            "This is the careful bridge from geometry to algebra.  The projector data is already compatible with Cayley multiplication, "
            "but compatibility is weaker than derivation.  The next measurable step is to regenerate the projector summary and see whether "
            "the overlap/centered-Gram orientation selects the CLXXIV Fano sign convention."
        ),
    }


def main() -> int:
    audit = heptad_projector_cayley_sign_bridge_audit()
    out = ROOT / "PART_CLXXXIV_heptad_projector_cayley_sign_bridge_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
