"""Exact W33 tick commutator Laplacian and sharp simplex extremum.

Self-contained enumerator of all maximal cliques in the 40-point
noncommutation graph. The Motzkin--Straus theorem turns its clique
number into a sharp maximum for the continuous interaction functional.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
from w33_20261019_tick_operator_frame_majorization import points, symp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_20261019_tick_commutator_extremum.json"


def maximal_cliques(bit_neighbors: list[int]):
    """Bron--Kerbosch with exact integer-bitset pivoting, all maximal cliques."""
    n = len(bit_neighbors)
    maximal = []

    def vertices(bits):
        while bits:
            low = bits & -bits
            yield low.bit_length()-1
            bits -= low

    def recurse(r, p, x):
        if not p and not x:
            maximal.append(tuple(vertices(r)))
            return
        union = p | x
        pivot = max(vertices(union), key=lambda u: (p & bit_neighbors[u]).bit_count()) if union else -1
        remaining = p & ~bit_neighbors[pivot] if pivot >= 0 else p
        for v in list(vertices(remaining)):
            recurse(r | (1 << v), p & bit_neighbors[v], x & bit_neighbors[v])
            p &= ~(1 << v)
            x |= (1 << v)

    recurse(0, (1 << n)-1, 0)
    return sorted(maximal)


def certify():
    ps = points()
    n = len(ps)
    B = np.array([[int(i != j and symp(u,v) != 0) for j,v in enumerate(ps)]
                  for i,u in enumerate(ps)],dtype=np.int64)
    A = np.ones((n,n),dtype=np.int64) - np.eye(n,dtype=np.int64) - B
    degA = A.sum(axis=1)
    common = A@A
    bg = [sum(int(B[i,j]) << j for j in range(n)) for i in range(n)]
    cliques = maximal_cliques(bg)
    hist = Counter(map(len,cliques))
    maximum = max(hist)
    seven = next(c for c in cliques if len(c)==maximum)

    # Pairwise squared commutator norm between projectors is 4/3 precisely
    # over noncommuting Pauli directions. Three outcome labels per direction.
    K = (4/3)*np.kron(B,np.ones((3,3)))
    evals = np.linalg.eigvalsh(K)
    spectrum = [(108,1),(12,15),(0,80),(-12,24)]
    lap_eigs = np.linalg.eigvalsh(108*np.eye(120)-K)
    lap_spec = [(0,1),(96,15),(108,80),(120,24)]

    # C(s)=(4/3)*sum_{i<j} B_ij s_i s_j, s>=0, sum s=1.
    # Motzkin--Straus gives maximum C=(2/3)(1-1/omega(B)).
    # An equally weighted maximum clique is always a witness.
    weights = np.zeros(n)
    weights[list(seven)] = 1/maximum
    extremum = float((2/3)*weights@B@weights)
    theoretical = 2/3*(1-1/maximum)
    rng = np.random.default_rng(19102026)
    random_weights = rng.random((300,n))
    random_weights /= random_weights.sum(axis=1,keepdims=True)
    sampled_max = max(float((2/3)*x@B@x) for x in random_weights)
    # Compare the exact certificate with the 120-projector lift formula.
    w120 = np.zeros(120)
    for i in seven:
        w120[3*i] = 1/maximum
    lifted = float(w120@K@w120/2)
    check = {
        "W33_srg_40_12_2_4": bool(n==40 and np.all(degA==12)
           and all(common[i,j]==(12 if i==j else 2 if A[i,j] else 4)
                   for i in range(n) for j in range(n))),
        "noncommutation_complement_srg_40_27_18_18": bool(
           np.all(B.sum(axis=1)==27)
           and all((B@B)[i,j]==(27 if i==j else 18)
                   for i in range(n) for j in range(n))),
        "maximal_clique_census":dict(hist)=={4:90,7:2880},
        "max_noncommuting_clique_7":maximum==7,
        "no_size_8_or_larger_clique":all(len(c)<=7 for c in cliques),
        "extremal_seven_is_clique":all(B[i,j]==1 for i in seven for j in seven if i!=j),
        "tick_commutator_spectrum":all(np.sum(np.abs(evals-k)<1e-8)==m for k,m in spectrum),
        "tick_commutator_laplacian_spectrum":all(
            np.sum(np.abs(lap_eigs-k)<1e-8)==m for k,m in lap_spec),
        "interaction_maximum_four_sevenths":abs(extremum-4/7)<1e-12 and abs(theoretical-4/7)<1e-12,
        "120_lift_matches_seven":abs(lifted-4/7)<1e-12,
        "random_points_below_sharp_bound":sampled_max <= 4/7+1e-12,
    }
    result = {
        "title":"Exact W33 tick noncommutation Laplacian and Motzkin-Straus bound",
        "n_directions":40,"n_outcome_projectors":120,
        "noncommuting_direction_edges":int(np.count_nonzero(B)//2),
        "noncommuting_tick_pairs":int(np.count_nonzero(np.kron(B,np.ones((3,3))))//2),
        "noncommutation_graph_srg":[40,27,18,18],
        "maximal_clique_size_histogram":dict(hist),
        "maximum_mutually_noncommuting_directions":maximum,
        "maximal_seven_cliques":int(hist[7]),
        "example_seven_projective_point_indices":list(seven),
        "tick_interaction_formula":"K = (4/3) [J40-I40-A_W33] tensor J3",
        "K_eigenvalues":[{"eigenvalue":a,"multiplicity":b} for a,b in spectrum],
        "L_eigenvalues":[{"eigenvalue":a,"multiplicity":b} for a,b in lap_spec],
        "sharp_simplex_interaction_maximum":"4/7",
        "sharp_simplex_interaction_minimum":"0",
        "motzkin_straus_formula":"max C = (2/3)(1-1/omega(noncommutation graph)); omega=7",
        "physics_scope":"New candidate interaction diagnostic; the sign and scale are not derived from the microscopic free energy.",
        "checks":check,"all_checks_pass":all(check.values()),
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"checks":check,"clique_census":dict(hist),
                      "interaction_maximum":theoretical},indent=2))
    assert result["all_checks_pass"]
    return result


if __name__=="__main__":
    certify()
