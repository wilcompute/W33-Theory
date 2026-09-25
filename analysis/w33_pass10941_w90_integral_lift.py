#!/usr/bin/env python3
"""Run and freeze the Pass 10941 rational central-idempotent W90 lift."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GAP = ROOT / "analysis/w33_pass10941_w90_integral_lift.g"
MATRIX = ROOT / "data/w33_pass10941_w90_integral_projector.tsv"
OUT = ROOT / "data/w33_pass10941_w90_integral_lift.json"


def rank_mod(A: np.ndarray, p: int) -> int:
    A = A.copy() % p
    rank = 0
    for col in range(A.shape[1]):
        hits = np.flatnonzero(A[rank:, col])
        if len(hits) == 0:
            continue
        pivot = rank + int(hits[0])
        A[[rank, pivot]] = A[[pivot, rank]]
        A[rank] = A[rank] * pow(int(A[rank, col]), -1, p) % p
        for row in np.flatnonzero(A[:, col]):
            if row != rank:
                A[row] = (A[row] - A[row, col] * A[rank]) % p
        rank += 1
        if rank == A.shape[0]:
            break
    return rank


def main(write: bool = True):
    if not shutil.which("gap"):
        raise RuntimeError("GAP is required for the integral W90 lift")
    run = subprocess.run(
        ["gap", "-q", str(GAP)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True,
    )
    assert "PASS_W90_CHARACTERISTIC_ZERO_INTEGRAL_LIFT true" in run.stdout
    A = np.loadtxt(MATRIX, dtype=np.int64, delimiter="\t")
    assert A.shape == (240, 240)
    assert int(np.gcd.reduce(A.ravel())) == 1
    assert np.array_equal(A @ A, 48 * A)
    assert int(np.trace(A)) == 4320
    ranks = {str(p): rank_mod(A, p) for p in (2, 3, 5, 7, 103)}
    assert ranks == {"2": 14, "3": 25, "5": 90, "7": 90, "103": 90}
    digest = hashlib.sha256(MATRIX.read_bytes()).hexdigest()
    values = sorted(set(map(int, A.ravel())))

    out = {
        "schema": "w33.pass10941.w90_integral_lift.v1",
        "status": "PASS_W90_CHARACTERISTIC_ZERO_AND_INTEGRAL_TARGET_LIFT",
        "character": {
            "W_E6_irreducible_id": 25,
            "degree": 90,
            "field_of_values": "Q",
            "frobenius_schur_indicator": 1,
            "multiplicity_in_canonical_induced_qutrit_lane": 1,
            "multiplicity_in_signed_edge_lane": 1,
        },
        "central_idempotent": {
            "formula": "e90=(1/48)A=(90/51840) sum_g chi90(g^-1) rho_edge(g)",
            "primitive_integer_matrix_shape": [240, 240],
            "integer_content": 1,
            "nonzero_entries": int(np.count_nonzero(A)),
            "entry_values": values,
            "trace_A": int(np.trace(A)),
            "identity": "A^2=48A",
            "rational_projector_trace_and_rank": 90,
            "commutes_with_all_three_W_E6_generators": True,
            "matrix_path": str(MATRIX.relative_to(ROOT)),
            "matrix_sha256": digest,
        },
        "integral_lattice": {
            "definition": "L90=A Z^240 inside the signed-edge lattice Z^240",
            "rank": 90,
            "W_E6_stable": True,
            "reason": "A commutes with every integral signed-permutation generator",
            "rational_span": "im_Q(e90), the unique rational W90 constituent",
        },
        "modular_reductions": {
            "ranks_of_primitive_A": ranks,
            "good_prime_103": "rank 90 and the projector denominator 48 is invertible",
            "bad_prime_boundary": "at p=2 and p=3 the central idempotent denominator is not invertible and A degenerates to ranks 14 and 25",
        },
        "lift_conclusion": (
            "There is no characteristic-zero or integral-target obstruction: the "
            "GF(103) W90 target is the good-prime reduction of the explicit W-stable "
            "integral lattice L90. The frozen object does not choose a 90x90 integral "
            "basis isomorphism from the cyclotomic induced qutrit lattice."
        ),
        "boundary": (
            "This lifts the common W90 representation and the target lattice. It does "
            "not assert that the original MeatAxe basis matrix lifts entry by entry, "
            "nor that the full 240D induced module has a rational integral model."
        ),
        "parents": [
            "analysis/w33_pass409_qutrit_edge_intertwiner.g",
            "data/w33_pass409_qutrit_edge_intertwiner.json",
        ],
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = main(True)
    print(json.dumps({"status": result["status"], "ranks": result["modular_reductions"]["ranks_of_primitive_A"]}, indent=2))
