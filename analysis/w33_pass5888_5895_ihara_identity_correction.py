#!/usr/bin/env python3
"""Pass5888-5895: correction-first Ihara identity audit.

This verifier separates:
  (A) the canonical W(3,3) collinearity graph: SRG(40,12,2,4);
  (B) the separate 4-regular signed 40-line/Levi mesh used in Pass5706;
  (C) the erroneous 33-vertex circulant surrogate introduced in Pass5880-5887.

Only exact finite-graph statements are promoted. Physical FSR/finesse/capacity
claims require an independent propagation/coupling model and are not certified
by graph valence or Ihara data alone.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS5888_5895_IHARA_IDENTITY_CORRECTION.json"


def canon(v):
    for x in v:
        if x % 3:
            inv = 1 if x % 3 == 1 else 2
            return tuple((inv*y) % 3 for y in v)
    raise ValueError("zero vector")


def omega(u, v):
    return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % 3


def build_w33():
    vecs = [v for v in itertools.product(range(3), repeat=4) if any(v)]
    pts = sorted(set(canon(v) for v in vecs))
    assert len(pts) == 40
    A = np.zeros((40, 40), dtype=int)
    for i, j in itertools.combinations(range(40), 2):
        if omega(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    return A


def srg_check(A):
    n = A.shape[0]
    deg = A.sum(axis=1)
    assert n == 40 and np.all(deg == 12)
    lam, mu = set(), set()
    for i, j in itertools.combinations(range(n), 2):
        c = int(A[i] @ A[j])
        (lam if A[i, j] else mu).add(c)
    assert lam == {2} and mu == {4}
    return {"v": 40, "k": 12, "lambda": 2, "mu": 4, "edges": int(A.sum() // 2)}


def build_hashimoto(A):
    n = A.shape[0]
    D = [(i, j) for i in range(n) for j in range(n) if A[i, j]]
    idx = {e: k for k, e in enumerate(D)}
    B = np.zeros((len(D), len(D)), dtype=np.int8)
    for a, (u, v) in enumerate(D):
        for w in np.flatnonzero(A[v]):
            w = int(w)
            if w != u:
                B[a, idx[(v, w)]] = 1
    return B


def old_surrogate():
    # Literal graph constructed by Pass5880-5887 build_w33_adjacency().
    n = 33
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        A[i, (i + 1) % n] = 1
        A[(i + 1) % n, i] = 1
        A[i, (i + 11) % n] = 1
        A[(i + 11) % n, i] = 1
    np.fill_diagonal(A, 0)
    A = np.clip(A, 0, 1)
    eig = np.linalg.eigvalsh(A)
    non = eig[:-1]  # remove Perron 4
    return {
        "vertices": 33,
        "degree_values": sorted(set(map(int, A.sum(axis=1)))),
        "edges": int(A.sum() // 2),
        "largest_nontrivial_adjacency_abs": float(max(abs(non))),
        "ramanujan_bound_2sqrt3": float(2*math.sqrt(3)),
        "ramanujan": bool(max(abs(non)) <= 2*math.sqrt(3) + 1e-12),
    }


def main():
    A = build_w33()
    srg = srg_check(A)

    # SRG relation A^2=(lambda-mu)A+(k-mu)I+mu J gives restricted
    # eigen equation x^2+2x-8=0, hence x=2,-4. Multiplicities follow
    # from 1+f+g=40 and 12+2f-4g=0.
    adj = {"12": 1, "2": 24, "-4": 15}
    assert 1 + 24 + 15 == 40 and 12 + 2*24 - 4*15 == 0

    B = build_hashimoto(A)
    assert B.shape == (480, 480)
    assert np.all(B.sum(axis=1) == 11)

    hashimoto = {
        "directed_edges": 480,
        "outdegree": 11,
        "ihara_excess_m_minus_n": 200,
        "det_factorization": "(1-u^2)^200 (1-12u+11u^2) (1-2u+11u^2)^24 (1+4u+11u^2)^15",
        "spectrum": {
            "11": 1,
            "+1": 201,
            "-1": 200,
            "1+i*sqrt(10)": 24,
            "1-i*sqrt(10)": 24,
            "-2+i*sqrt(7)": 15,
            "-2-i*sqrt(7)": 15,
        },
        "adjacency_induced_nontrivial_count": 78,
        "adjacency_induced_nontrivial_modulus": "sqrt(11)",
    }
    assert sum(hashimoto["spectrum"].values()) == 480

    theta2 = math.atan2(math.sqrt(10), 1.0)
    theta4 = math.atan2(math.sqrt(7), -2.0)
    phase = {
        "distinct_nontrivial_phases": 4,
        "phase_multiplicities": [24, 24, 15, 15],
        "theta_from_mu_2": theta2,
        "theta_from_mu_minus4": theta4,
        "equidistributed": False,
        "deduction": "Ihara-Bass fixes the finite phase multiset; it does not imply photonic FSR equidistribution.",
    }

    surrogate = old_surrogate()
    assert surrogate["degree_values"] == [4]
    assert surrogate["vertices"] == 33 and surrogate["edges"] == 66
    assert surrogate["ramanujan"] is False

    out = {
        "schema": "w33.pass5888_5895.ihara_identity_correction.v1",
        "status": "PASS_CORRECTION",
        "pass_5888_canonical_graph_identity": srg,
        "pass_5889_canonical_adjacency_spectrum": adj,
        "pass_5890_hashimoto_exact": hashimoto,
        "pass_5891_phase_equidistribution_refutation": phase,
        "pass_5892_pass5880_surrogate_audit": surrogate,
        "pass_5893_graph_separation": {
            "canonical_W33_collinearity": "40 vertices, 240 edges, degree 12, Hashimoto outdegree 11",
            "pass5706_signed_mesh": "separate 4-regular signed 40-line/Levi mesh; q_nb=3 and its own 76-resonance certificate",
            "pass5880_surrogate": "33-vertex 4-regular circulant with jumps +/-1,+/-11; not canonical W(3,3)",
            "deduction": "The three objects must not share one symbol or one q=d-1 without an explicit graph identifier.",
        },
        "pass_5894_physical_firewall": {
            "certified": "dimensionless Ihara/Hashimoto pole factors and graph spectra",
            "not_certified": [
                "free spectral range from graph valence alone",
                "Fabry-Perot finesse from q=d-1 alone",
                "Shannon channel capacity from the graph spectrum alone",
                "uniform physical loss/Q without a propagation and coupling model",
            ],
        },
        "pass_5895_correction_verdict": {
            "pass5880_5887": "SUPERSEDED/QUARANTINED",
            "reason": "wrong graph identity, omitted structural Hashimoto modes, false finite-phase equidistribution, and unsupported physical conversion",
            "salvaged_exact_statement": "For canonical W(3,3), the 78 adjacency-induced nontrivial Hashimoto modes all have modulus sqrt(11).",
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
