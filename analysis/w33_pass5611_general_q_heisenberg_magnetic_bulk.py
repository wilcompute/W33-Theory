#!/usr/bin/env python3
"""Pass5611: exact all-q affine Heisenberg magnetic spectrum and continuum firewall.

For odd q (implemented replay anchors are odd primes), put V=F_q^2 and

    A((x,y),(x',y')) = 1[x!=x',y!=y'] chi(x y' - x' y).

This is the affine bulk of the normalized Segre-section phase after the diagonal
gauge f(x,y)=xy.  The exact spectrum follows from the symplectic Fourier kernel K
and the same-x/same-y projectors R,C:

    A = K-R-C+I,
    K^2=q^2 I, R^2=qR, C^2=qC,
    KR=RK=qR, KC=CK=qC, RCR=qR, CRC=qC.

The spectrum is
  -(q-1)       mult q(q-1)/2,
   q+1         mult q(q-3)/2,
   1-sqrt(q)   mult q,
   1+sqrt(q)   mult q.

Consequently the empirical spectral measure of A/q converges to
(1/2)delta_-1+(1/2)delta_+1.  The O(q) projective boundary of the normalized
P1xP1 section is a low-rank perturbation of the q^2 affine block, so that chosen
section has the same limiting empirical measure.

IMPORTANT: Pass5613 records that a projective section is not intrinsic.  This file
therefore proves a theorem about the canonical affine Heisenberg bulk and a chosen
normalized projective section, not a projectively intrinsic spacetime Hamiltonian.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS5611_GENERAL_Q_MAGNETIC_BULK.json"


def affine_matrix(q: int) -> np.ndarray:
    pts = list(itertools.product(range(q), repeat=2))
    zeta = np.exp(2j * np.pi / q)
    A = np.zeros((q*q, q*q), dtype=np.complex128)
    for i, (x, y) in enumerate(pts):
        for j, (u, v) in enumerate(pts):
            if x != u and y != v:
                A[i, j] = zeta ** ((x*v-u*y) % q)
    assert np.allclose(A, A.conj().T)
    return A


def expected_bands(q: int) -> list[tuple[float, int]]:
    out = [
        (-(q-1), q*(q-1)//2),
        (1-math.sqrt(q), q),
        (1+math.sqrt(q), q),
    ]
    if q > 3:
        out.append((q+1, q*(q-3)//2))
    return sorted(out)


def numerical_bands(A: np.ndarray) -> list[tuple[float, int]]:
    ev = np.linalg.eigvalsh(A)
    c = Counter(float(x) for x in np.round(ev, 8))
    return sorted((k, v) for k, v in c.items())


def verify_anchor(q: int) -> dict:
    A = affine_matrix(q)
    got = numerical_bands(A)
    want = expected_bands(q)
    assert len(got) == len(want)
    for (x, mx), (y, my) in zip(got, want):
        assert mx == my and abs(x-y) < 1e-7, (q, got, want)
    return {
        "q": q,
        "dimension": q*q,
        "numerical_bands": [[x, m] for x, m in got],
        "formula_verified": True,
    }


def main() -> None:
    anchors = [verify_anchor(q) for q in (3, 5, 7, 11)]
    out = {
        "pass": 5611,
        "status": "THEOREM_EXACT_AFFINE_MAGNETIC_SPECTRUM_AND_ATOMIC_LIMIT",
        "operator": "A((x,y),(u,v))=1[x!=u,y!=v] chi(xv-uy)",
        "exact_spectrum": [
            {"eigenvalue": "-(q-1)", "multiplicity": "q(q-1)/2"},
            {"eigenvalue": "q+1", "multiplicity": "q(q-3)/2"},
            {"eigenvalue": "1-sqrt(q)", "multiplicity": "q"},
            {"eigenvalue": "1+sqrt(q)", "multiplicity": "q"},
        ],
        "proof_algebra": [
            "A=K-R-C+I",
            "K^2=q^2 I; R^2=qR; C^2=qC",
            "KR=RK=qR; KC=CK=qC; RCR=qR; CRC=qC",
            "on K=-q, R=C=0",
            "on K=+q, R/q and C/q are rank-q isoclinic projectors with principal overlap 1/sqrt(q)",
        ],
        "normalized_esd_limit": "(1/2) delta_-1 + (1/2) delta_+1",
        "projective_boundary": {
            "affine_points": "q^2",
            "normalized_P1xP1_points": "(q+1)^2",
            "boundary_points": "2q+1",
            "rank_perturbation_bound": "<=2(2q+1)",
            "empirical_CDF_difference_bound": "<=2(2q+1)/(q+1)^2 -> 0",
        },
        "anchors": anchors,
        "physics_firewall": (
            "Heisenberg holonomy splits finite-q degeneracies but the all-q bulk still has an atomic, not Weyl, continuum limit. "
            "A projective section is not intrinsic (Pass5613), so this is a bulk/section theorem rather than a derived spacetime Hamiltonian."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
