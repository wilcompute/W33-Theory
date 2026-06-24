#!/usr/bin/env python3
"""BT1683 — Schur/isotypic proof certificate for the oriented bridge twirl."""
from __future__ import annotations

import json
from pathlib import Path

RESULT = {
    "theorem": "BT1683 Formal Schur/Isotypic Proof Certificate",
    "statement": "If the Levi H1 representation under PSp(4,3) is irreducible, then the automorphism average of any rank-r oriented H1 subspace projector is (r/81) P_H1. For the BT1681 bridge r=8, so the average is (8/81) P_H1.",
    "objects": {
        "group": "PSp(4,3), projective symplectic action order 25920",
        "ambient_edge_space_dimension": 160,
        "levi_h1_dimension": 81,
        "fixed_bridge_rank": 8
    },
    "proof_steps": [
        "Let P_B be the orthogonal projector onto the fixed oriented bridge subspace B inside H1.",
        "Define A = |G|^{-1} sum_{g in G} rho(g) P_B rho(g)^{-1}.",
        "A commutes with every rho(h), so A belongs to the commutant of the H1 representation.",
        "If H1 is irreducible, Schur's lemma gives A = alpha P_H1.",
        "Taking traces gives tr(A)=tr(P_B)=8 and tr(P_H1)=81, hence alpha=8/81.",
        "Therefore A=(8/81)P_H1."
    ],
    "BT1681_numerical_certificate": {
        "averaged_projector_trace": 7.999999999999972,
        "frobenius_error_to_(8/81)P_H1": 1.0598553943057821e-14,
        "relative_frobenius_error": 1.1923373185940048e-14,
        "nonzero_eigenvalue": 0.09876543209876543,
        "multiplicity": 81
    },
    "distinction_from_support_twirl": "BT1675 averaged an all-positive support vector and got zero H1. BT1681/BT1683 average an oriented H1 subspace projector and get isotropic H1 density. These are different functors: support vector average versus subspace-projector average.",
    "what_remains_for_a_paper_proof": "Either cite/derive irreducibility of the 81-dimensional Levi H1 module under PSp(4,3), or include the commutant-dimension computation as a machine-checkable certificate.",
    "boundary": "This is a formal proof conditional on H1 irreducibility, backed by the BT1681 numerical average. A fully formal representation-theoretic paper proof still needs the irreducibility lemma."
}


def main() -> None:
    out = Path("data/PART_BT1683_SCHUR_ISOTYPIC_PROOF_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(RESULT, indent=2) + "\n")
    print(json.dumps(RESULT, indent=2))


if __name__ == "__main__":
    main()
