#!/usr/bin/env python3
"""Pass 10958: exact Albert mu4 missing-mode intertwiner.

Pass10954's missing clock module is A=diag(i,-i). Pass10956 now supplies
exact rational matrices Chi and U on the Albert Peirce 16 with
Chi^2=I, U^2=-I, and U Chi = - Chi U. This pass proves over Q(i) that
the Albert 16 is eight copies of the exact missing two-character C4 module.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
MATS = ROOT / "data/w33_pass10956_albert_spin8_exact_matrices.json"
OUT = ROOT / "data/w33_pass10958_exact_albert_mu4_missing_mode_intertwiner.json"
INT = ROOT / "data/w33_pass10958_mu4_intertwiner_matrix.json"


def parse_matrix(rows):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in rows])


def strings(M):
    return [[str(sp.simplify(M[i, j])) for j in range(M.cols)]
            for i in range(M.rows)]


def sha_matrix(M):
    payload = json.dumps(strings(M), sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()

def main():
    mats = json.loads(MATS.read_text(encoding="utf-8"))
    Chi = parse_matrix(mats["chirality_involution"])
    R = parse_matrix(mats["rotation_generator_R"])
    U = parse_matrix(mats["halfturn_U_equals_R_over_2"])
    I16 = sp.eye(16)

    assert Chi * Chi == I16
    assert R * R == -4 * I16
    assert U == R / 2
    assert U * U == -I16
    assert U ** 4 == I16
    assert U * Chi + Chi * U == sp.zeros(16, 16)
    assert U.trace() == 0

    lam = sp.symbols("lambda")
    cp = sp.factor(U.charpoly(lam).as_expr())
    assert sp.expand(cp - (lam ** 2 + 1) ** 8) == 0

    Eplus = (U - sp.I * I16).nullspace()
    Eminus = (U + sp.I * I16).nullspace()
    assert len(Eplus) == len(Eminus) == 8

    paired_minus = [sp.simplify(Chi * v) for v in Eplus]
    assert all((U + sp.I * I16) * v == sp.zeros(16, 1)
               for v in paired_minus)
    assert sp.Matrix.hstack(*paired_minus).rank() == 8

    cols = []
    for vp, vm in zip(Eplus, paired_minus):
        cols.extend([vp, vm])
    W = sp.Matrix.hstack(*cols)
    assert W.shape == (16, 16)
    assert W.det() != 0

    A2 = sp.diag(sp.I, -sp.I)
    X2 = sp.Matrix([[0, 1], [1, 0]])
    A8 = sp.diag(*([A2] * 8))
    X8 = sp.diag(*([X2] * 8))

    assert U * W == W * A8
    assert Chi * W == W * X8
    assert A8 * A8 == -sp.eye(16)
    assert A8 ** 4 == sp.eye(16)
    assert A8 * X8 + X8 * A8 == sp.zeros(16, 16)

    W2 = W[:, :2]
    assert W2.rank() == 2
    assert U * W2 == W2 * A2
    assert Chi * W2 == W2 * X2

    Pchi_plus = (I16 + Chi) / 2
    Pchi_minus = (I16 - Chi) / 2
    Ep = sp.Matrix.hstack(*Eplus)
    Em = sp.Matrix.hstack(*Eminus)
    assert sp.Matrix.hstack(Ep, Pchi_plus).rank() == 16
    assert sp.Matrix.hstack(Ep, Pchi_minus).rank() == 16
    assert sp.Matrix.hstack(Em, Pchi_plus).rank() == 16
    assert sp.Matrix.hstack(Em, Pchi_minus).rank() == 16

    p54 = json.loads(
        (ROOT / "data/w33_pass10954_regular_c8_clock_completion.json")
        .read_text(encoding="utf-8"))
    assert p54["compressed_clock"]["missing_character_exponents"] == [2, 6]
    assert p54["compressed_clock"]["missing_phase_values"] == ["+i", "-i"]
    assert p54["oriented_A2_4_clock_cover"]["missing_modes_deck_even"] is True

    p57 = json.loads(
        (ROOT / "data/w33_pass10957_mu4_schur_cover_converter.json")
        .read_text(encoding="utf-8"))
    c4 = p57["clock_C4_square_root"]
    assert c4["chi_plus_values"] == ["1", "i", "-1", "-i"]
    assert c4["chi_minus_values"] == ["1", "-i", "-1", "i"]

    p50 = json.loads(
        (ROOT / "data/w33_pass10950_clock_albert_lorentz_spinor.json")
        .read_text(encoding="utf-8"))
    assert p50["matter_parity"]["peirce_symmetry_U_(2c-e)"]["A1/2"] is True

    p56 = json.loads(
        (ROOT / "data/w33_pass10956_albert_spin8_halfspin_normalizer.json")
        .read_text(encoding="utf-8"))
    h56 = p56["spin9_normalizer_halfturn"]
    assert h56["exact_halfturn_square"] == "-I16"
    assert h56["exact_anticommutes_with_chirality"] is True

    intertwiner = {
        "schema": "w33.pass10958.mu4-intertwiner-matrix.v1",
        "field": "Q(i)",
        "two_column_embedding_W2": strings(W2),

        "full_change_of_basis_W": strings(W),
        "target_two_mode_generator_A2": [["i", "0"], ["0", "-i"]],
        "target_chirality_swap_X2": [["0", "1"], ["1", "0"]],
        "relations": [
            "U W = W diag(A2,...,A2)",
            "Chi W = W diag(X2,...,X2)",
            "U W2 = W2 A2",
            "Chi W2 = W2 X2",
        ],
    }
    INT.write_text(json.dumps(intertwiner, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")

    out = {
        "schema": "w33.pass10958.exact-albert-mu4-missing-mode-intertwiner.v1",
        "status": "PASS_EXACT_ALBERT_MU4_MISSING_MODE_INTERTWINER",
        "exact_albert_halfturn": {
            "formula": "U=R/2 over Q",
            "R_squared": "-4I16",
            "U_squared": "-I16",
            "U_fourth": "+I16",
            "minimal_polynomial": "x^2+1",

            "characteristic_polynomial": "(x^2+1)^8",
            "trace": 0,
            "plus_i_eigenspace_dimension": len(Eplus),
            "minus_i_eigenspace_dimension": len(Eminus),
        },
        "exact_mu4_module": {
            "generator": "A2=diag(i,-i)",
            "A2_squared": "-I2",
            "A2_fourth": "+I2",
            "pass10954_missing_C8_exponents": [2, 6],
            "pass10954_missing_phases": ["+i", "-i"],
            "clock_factorization":
                "the missing sector factors the C8 clock through C4 because A2^4=I",
        },
        "carrier_intertwiner": {
            "field": "Q(i)",
            "two_mode_embedding_rank": W2.rank(),
            "full_change_of_basis_rank": W.rank(),
            "full_change_of_basis_sha256": sha_matrix(W),
            "two_mode_embedding_sha256": sha_matrix(W2),
            "exact_relations": {
                "U_W2_equals_W2_A2": True,
                "Chi_W2_equals_W2_X2": True,

                "U_W_equals_W_A2x8": True,
                "Chi_W_equals_W_X2x8": True,
            },
            "module_isomorphism":
                "Albert Peirce 16 over Q(i) = 8 copies of the Pass10954 missing C4 module",
        },
        "chirality_exchange_reading": {
            "exact_anticommutation": "U Chi = - Chi U",
            "paired_basis":
                "each +i Albert eigenvector is paired with Chi*v in the -i eigenspace",
            "plus_i_intersection_with_chirality_plus": 0,
            "plus_i_intersection_with_chirality_minus": 0,
            "minus_i_intersection_with_chirality_plus": 0,
            "minus_i_intersection_with_chirality_minus": 0,
            "conclusion":
                "the +/-i modes are eigenmodes of the chirality-exchanging halfturn, not chirality eigenstates",
        },
        "matter_parity": {
            "Albert_relation": "U^2=-I16",
            "pass10950_reading":
                "-I on the Peirce 16 is the 2pi Spin(9) matter-parity sign",
            "missing_module_relation": "A2^2=-I2",

            "objectwise_weld":
                "the missing two-mode clock module and the Albert halfturn have the same C4 central-square relation",
        },
        "pass10957_cover_converter": {
            "mu4_square_roots": ["+i", "-i"],
            "new_upgrade":
                "Pass10957 matched cocycles/projective phases; Pass10958 supplies an explicit Q(i) carrier embedding for the cyclic missing-mode sector",
            "remaining_gap":
                "the intertwiner is for the C4 missing-mode quotient only, not the full GL(2,3) clock or S4 action",
        },
        "theorem": (
            "The Pass10956 Albert Spin(9) normalizer halfturn is exactly the rational "
            "matrix U=R/2 with R^2=-4I, hence U^2=-I and U^4=I. Over Q(i) its "
            "characteristic polynomial is (x^2+1)^8, with eight +i and eight -i "
            "eigenvectors. Pairing a +i eigenbasis with its image under the exact "
            "Spin(8) chirality involution gives a full change of basis W in which "
            "U is eight copies of diag(i,-i) and chirality is eight copies of the "
            "swap matrix. Therefore the two missing Pass10954 clock characters "
            "k=2,6 are not merely phase-matched to the Albert halfturn: their exact "
            "two-dimensional C4 module embeds into the Peirce 16, which is eight "
            "copies of that module."
        ),

        "boundary": (
            "Exact cyclic-module result over Q(i). The larger finite-group "
            "representation map remains a separate problem."
        ),
    }
    OUT.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": out["status"],
        "plus_i_dim": out["exact_albert_halfturn"]["plus_i_eigenspace_dimension"],
        "minus_i_dim": out["exact_albert_halfturn"]["minus_i_eigenspace_dimension"],
        "W_rank": out["carrier_intertwiner"]["full_change_of_basis_rank"],
        "W2_rank": out["carrier_intertwiner"]["two_mode_embedding_rank"],
    }, indent=2))


if __name__ == "__main__":
    main()
