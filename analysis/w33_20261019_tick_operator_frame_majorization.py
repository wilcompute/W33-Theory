"""Tick-projector operator-frame certificate and universal simplex no-go.

Independent continuation of Pass 12055. The single-tick free-energy
minimum at positive T is a generic rank-r projector majorization result;
the W33 geometry first enters through noncommuting pairs, not the
pairwise Hilbert-Schmidt Gram of distinct Pauli directions.

Run: python analysis/w33_20261019_tick_operator_frame_majorization.py
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_20261019_tick_operator_frame_majorization.json"
OMEGA = np.exp(2j * np.pi / 3)
X = np.roll(np.eye(3), 1, axis=0)
Z = np.diag([1, OMEGA, OMEGA**2])


def points():
    return [
        v for v in itertools.product(range(3), repeat=4)
        if any(v) and next(a for a in v if a) == 1
    ]


def symp(u, v):
    return (u[0]*v[2] + u[1]*v[3] - u[2]*v[0] - u[3]*v[1]) % 3


def pauli(v):
    a, b, c, d = v
    return np.kron(
        np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, c),
        np.linalg.matrix_power(X, b) @ np.linalg.matrix_power(Z, d),
    )


def build_projectors(ps):
    eye = np.eye(9)
    out = []
    for p in ps:
        W = pauli(p)
        W2 = W @ W
        for k in range(3):
            out.append((eye + OMEGA**(-k)*W + OMEGA**(-2*k)*W2)/3)
    return np.array(out)


def certify():
    ps = points()
    P = build_projectors(ps)
    N = len(P)
    flat = P.reshape(N, 81)
    gram = (flat.conj() @ flat.T).real
    expected = 3*np.eye(N) + np.kron(np.ones((40, 40))-np.eye(40), np.ones((3, 3)))
    eigs = np.linalg.eigvalsh(gram)
    spectrum = [(0, 39), (3, 80), (120, 1)]
    count = Counter()
    comm_energy = {}
    max_error = 0.0
    for i in range(N):
        for j in range(i+1, N):
            if i//3 == j//3:
                kind = "same_point_different_outcome"
                expected_norm = 0.0
            elif symp(ps[i//3], ps[j//3]) == 0:
                kind = "collinear_distinct_point"
                expected_norm = 0.0
            else:
                kind = "noncollinear_distinct_point"
                expected_norm = 4/3
            C = P[i] @ P[j] - P[j] @ P[i]
            norm = float(np.vdot(C, C).real)
            max_error = max(max_error, abs(norm-expected_norm))
            count[kind] += 1
            comm_energy.setdefault(kind, norm)

    # At fixed total rate R: H=R(I-Q), Q=sum w_a P_a, w>=0, sum w=1.
    # Q has 0<=Q<=I, trace Q=3, so lambda(Q) is majorized by (1,1,1,0^6).
    # Schur-convexity of sum exp(x lambda) proves
    #   F_T(H)>=-T log(3+6 exp(-R/T)), T>0.
    # Equality requires Q be a rank-3 projection, hence a single distinct tick.
    rng = np.random.default_rng(20261019)
    temps = [0.2, 1.0, 5.0]
    R = 1.0
    max_partition_excess = -float("inf")
    min_free_gap = float("inf")
    for T in temps:
        baseline = -T*np.log(3+6*np.exp(-R/T))
        for _ in range(50):
            w = rng.random(120)
            w /= w.sum()
            Q = np.tensordot(w, P, axes=1)
            evals = np.linalg.eigvalsh(R*(np.eye(9)-Q))
            free = -T*np.log(np.exp(-evals/T).sum())
            min_free_gap = min(min_free_gap, float(free-baseline))
            max_partition_excess = max(max_partition_excess, float(baseline-free))

    # Universal extension: FIXED positive l_p norm for ANY p>=1.
    # If ||phi||_p=R, phi>=0, then S=||phi||_1>=R.
    # Majorization at total S gives F(phi)>=f_T(S)>=f_T(R), since
    # f_T'(S)=6 exp(-S/T)/(3+6 exp(-S/T)) > 0 at T>0.
    # Thus the L2-sphere claim in Pass 12055 is exact, not only numerical.
    lp_gaps = {}
    for order in (1, 2, 3):
        smallest = float("inf")
        for T in temps:
            baseline = -T*np.log(3+6*np.exp(-R/T))
            for _ in range(30):
                phi = rng.random(120)
                phi /= np.linalg.norm(phi, ord=order)
                evals = np.linalg.eigvalsh(np.tensordot(phi, np.eye(9)-P, axes=1))
                free = -T*np.log(np.exp(-evals/T).sum())
                smallest = min(smallest, float(free-baseline))
        lp_gaps[str(order)] = smallest

    # T=0 is exceptional: any two commuting distinct directions admit a
    # common one-dimensional eigenspace for suitable k,l.
    q = next(j for j in range(1,40) if symp(ps[0],ps[j])==0)
    mixed_H = 0.5*(np.eye(9)-P[0])+0.5*(np.eye(9)-P[3*q])
    t0_gap = float(np.linalg.eigvalsh(mixed_H)[0])

    # Same projector inner products for collinear/noncollinear points:
    # geometry appears only in commutator-sensitive interactions.
    checks = {
        "forty_projective_Pauli_directions": len(ps) == 40,
        "120_rank_three_projectors": N == 120 and all(abs(np.trace(a)-3)<1e-9 for a in P),
        "projectors_hermitian_idempotent": bool(np.allclose(P,P.conj().transpose(0,2,1),atol=1e-10)
                                                  and np.allclose(P@P,P,atol=1e-10)),
        "projector_sum_equals_40I": bool(np.allclose(P.sum(axis=0),40*np.eye(9),atol=1e-10)),
        "operator_Gram_closed_form": bool(np.allclose(gram, expected, atol=1e-9)),
        "operator_frame_rank_81": int(np.linalg.matrix_rank(flat,tol=1e-8)) == 81,
        "Gram_eigenvalue_multiplicities": all(np.sum(abs(eigs-k)<1e-7)==m for k,m in spectrum),
        "pair_census_120_2160_4860": dict(count) == {
            "same_point_different_outcome":120,
            "collinear_distinct_point":2160,
            "noncollinear_distinct_point":4860,
        },
        "commutator_norm_squared_0_or_4_over_3": max_error < 1e-9,
        "positive_temperature_majorization_bound": min_free_gap > -1e-10,
        "all_fixed_lp_spheres_p_ge_1": all(g >= -1e-10 for g in lp_gaps.values()),
        "T0_commuting_mixture_ground_state": abs(t0_gap) < 1e-9,
    }
    result = {
        "paper_scope":"two-qutrit rank-3 Pauli eigenspace ticks, Pass 12055",
        "projector_rank":3,"Hilbert_dimension":9,
        "n_points":40,"n_projectors":120,
        "Gram_formula":"3 I_120 + (J_40-I_40) tensor J_3",
        "Gram_spectrum":[{"eigenvalue":k,"multiplicity":m} for k,m in spectrum],
        "pair_types":dict(count),
        "commutator_squared_norm":{"same_point":0,"collinear":0,"noncollinear":4/3},
        "maximum_numeric_commutator_residual":max_error,
        "positive_T_exact_bound":"F_T >= -T log(3+6 exp(-R/T)) for R>0, T>0",
        "lp_theorem":"For all p>=1, phi>=0, ||phi||_p=R, and T>0, F_T>=-T log(3+6 exp(-R/T)); singleton is unique up to labels.",
        "sampled_lp_orders":[1,2,3],"sampled_lp_min_gaps":lp_gaps,
        "T0_commuting_mixture_smallest_eigenvalue":t0_gap,
        "equality":"one tick (up to identical projectors) at T>0; mixed compatible ticks may also minimize at T=0",
        "meaning":"Generic majorization gives vertex selection; W33 enters the commutator, not pair Gram.",
        "tested_temperatures":temps,"numerical_interior_gap_min":min_free_gap,
        "checks":checks,"all_checks_pass":all(checks.values()),
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"checks":checks,"Gram_spectrum":spectrum,
          "pair_types":dict(count),"max_error":max_error,"interior_gap_min":min_free_gap},indent=2))
    assert result["all_checks_pass"]
    return result


if __name__ == "__main__":
    certify()
