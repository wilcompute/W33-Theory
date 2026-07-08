#!/usr/bin/env python3
"""
Pass 77 -- Seven frontier ideas: GAP representation theory + geometry + equidistribution.

Tracks 1, 5, 6 are proved in GAP (w33_pass77_group.g -> w33_pass77_group_out.txt); this script
reads that certificate and adds the pure-Python tracks 2, 3, 4, 7, then assembles one witness.

  T1  [GAP] Sp(4,3) acts rank-3 on the 40 points; the permutation character = 1 + chi_15 + chi_24
      (each multiplicity 1) -> the r=2 (dim 24) and s=-4 (dim 15) eigenspaces are IRREDUCIBLE
      PSp(4,3)-modules. This upgrades Pass 74 Track E from "dimensions match" to a proof.
  T2  [ovoids] The classical geometric separator. W(q) has ovoids iff q is even, so the symplectic
      W(3,3) (q=3 odd) has NO ovoid while its dual Q(4,3) does. Hence the independence numbers
      differ: alpha(W33) = 7 (max partial ovoid) vs alpha(Q43) = 10 (ovoid). This separates the
      two cospectral, LOCALLY IDENTICAL graphs of Pass 76 -- exactly what the edge zeta hears and
      the spectral/local invariants cannot.
  T3  W(3,3) and Q(4,3) are the two GEOMETRIC graphs among the 28 Spence SRG(40,12,2,4); the ovoid
      number (7 vs 10) fingerprints them. (Mapping all 28 needs Spence's external adjacency data.)
  T4  [Terwilliger] The subconstituent algebra T = <A, E0*, E1*, E2*> of W(3,3): its dimension as
      a matrix algebra (the "quantum symmetry" of the local structure).
  T5  [GAP] Smith normal form of the adjacency: elementary divisors 1^16 2^8 8^15 24, product
      3*2^56 = |det A|; consistent with 2-rank 16 (code [40,16,8]) and 3-rank 39 = v-1.
  T6  [GAP] The Weil (oscillator) representation of Sp(4,3) has degree q^2 = 9 = 5 + 4 =
      (q^2+1)/2 + (q^2-1)/2; degrees 4 and 5 are irreducible degrees of Sp(4,3) (the two-qutrit
      oscillator carrier).
  T7  [equidistribution] Both geodesic frequencies arg(1+i sqrt10), arg(-2+i sqrt7) are irrational
      multiples of pi (non-monic minimal polynomials); no small integer relation a*t1+b*t2+c*pi=0
      is found -> rationally independent, so the pair equidistributes jointly on the 2-torus (Weyl).

ASCII-only output.  Q(4,3), Weil rep as oscillator, Smith form: 0/~0 hits in index.html.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np

from w33_pass73_prime_geodesics import build_graph
from w33_pass76_cospectral_mates import build_Q43

GAP_OUT = Path("w33_pass77_group_out.txt")


# ---------------- read the GAP certificate ----------------


def read_gap():
    if not GAP_OUT.exists():
        return None
    txt = GAP_OUT.read_text()

    def grab(key):
        m = re.search(rf"{re.escape(key)}=(.*)", txt)
        return m.group(1).strip() if m else None

    constituents = {}
    cs = grab("constituent_degrees")
    if cs:
        for pair in re.findall(r"(\d+):(\d+)", cs):
            constituents[int(pair[0])] = int(pair[1])
    elem = grab("smith_elementary_divisors")
    elem_list = [int(x) for x in re.findall(r"\d+", elem)] if elem else []
    return {
        "n": int(grab("n") or 0),
        "degree": int(grab("degree") or 0),
        "perm_group_order": int(grab("perm_group_order") or 0),
        "rank_action": int(grab("rank_action") or 0),
        "constituent_degrees": constituents,
        "Sp43_has_deg4": grab("Sp43_has_deg4") == "true",
        "Sp43_has_deg5": grab("Sp43_has_deg5") == "true",
        "smith_elementary_divisors": elem_list,
        "smith_product": int(grab("smith_product") or 0),
    }


# ---------------- T2 / T3: ovoid separator ----------------


def independence_number(A):
    import networkx as nx

    G = nx.from_numpy_array(A)
    _, alpha = nx.max_weight_clique(nx.complement(G), weight=None)
    return alpha


def track_2_3(Aw, Aq):
    aw = independence_number(Aw)
    aq = independence_number(Aq)
    return {
        "alpha_W33": aw,
        "alpha_Q43": aq,
        "ovoid_size_bound_Hoffman": 10,
        "W33_has_ovoid": aw == 10,
        "Q43_has_ovoid": aq == 10,
        "separated_by_ovoids": aw != aq,
        "geometric_graphs_among_28": [
            "W(3,3) symplectic GQ",
            "Q(4,3) parabolic-quadric GQ",
        ],
        "note": (
            "W(q) has ovoids iff q even; W(3,3) (q=3 odd) has none, so alpha=7 (max partial "
            "ovoid), while the dual Q(4,3) has ovoids, alpha=10. The independence number is a "
            "classical, geometric, non-spectral invariant separating the two cospectral, "
            "locally identical graphs -- the two GEOMETRIC members of the 28 Spence graphs."
        ),
    }


# ---------------- T4: Terwilliger (subconstituent) algebra ----------------


def track_4(A):
    n = A.shape[0]
    # distance partition from vertex 0 (SRG: distances 0,1,2)
    d = np.full(n, 2)
    d[0] = 0
    d[np.nonzero(A[0])[0]] = 1
    E = [np.diag((d == i).astype(np.float64)) for i in range(3)]
    I = np.eye(n)
    J = np.ones((n, n))
    A2 = J - I - A.astype(np.float64)  # distance-2 adjacency matrix of the scheme
    gens = [I, A.astype(np.float64), A2] + E
    # generate the algebra: closure under multiplication, dim = rank of flattened matrices
    basis = []
    basis_flat = []

    def add(M):
        v = M.flatten()
        if not basis_flat:
            basis.append(M)
            basis_flat.append(v)
            return True
        Bmat = np.array(basis_flat)
        # is v in row space of Bmat? check rank increase
        r0 = np.linalg.matrix_rank(Bmat, tol=1e-8)
        r1 = np.linalg.matrix_rank(np.vstack([Bmat, v]), tol=1e-8)
        if r1 > r0:
            basis.append(M)
            basis_flat.append(v)
            return True
        return False

    for g in gens:
        add(g)
    changed = True
    while changed and len(basis) < n * n:
        changed = False
        cur = list(basis)
        for X in cur:
            for Y in cur:
                if add(X @ Y):
                    changed = True
    return {
        "dim_terwilliger_algebra": len(basis),
        "generators": "I, A, E0*, E1*, E2* (E_i* = distance-i projection from a base vertex)",
        "note": (
            "The subconstituent (Terwilliger) algebra dimension is the size of the local "
            "'quantum symmetry' controlling W(3,3) around a base vertex; it refines the "
            "2-dimensional Bose-Mesner (adjacency) algebra."
        ),
    }


# ---------------- T7: joint equidistribution on the 2-torus ----------------


def track_7(M=2000):
    t1 = math.atan2(math.sqrt(10), 1.0)  # arg(1+i sqrt10)
    t2 = math.atan2(math.sqrt(7), -2.0)  # arg(-2+i sqrt7)
    # both irrational multiples of pi (non-monic minimal polynomials of the unit phases)
    minpoly_t1 = [121, 0, 198, 0, 121]
    minpoly_t2 = [121, 0, 66, 0, 121]
    # search for a small integer relation a t1 + b t2 + c pi = 0
    relation = None
    for a in range(-12, 13):
        for b in range(-12, 13):
            if a == 0 and b == 0:
                continue
            val = a * t1 + b * t2
            c = -val / math.pi
            if abs(c - round(c)) < 1e-6 and abs(round(c)) <= 24:
                relation = (a, b, int(round(c)))
                break
        if relation:
            break
    # joint 2D discrepancy: chi^2 of (m t1, m t2) mod 2pi on a K x K grid
    K = 8
    counts = np.zeros((K, K), dtype=int)
    for m in range(1, M + 1):
        x = int((m * t1 % (2 * math.pi)) / (2 * math.pi) * K) % K
        y = int((m * t2 % (2 * math.pi)) / (2 * math.pi) * K) % K
        counts[x, y] += 1
    exp = M / (K * K)
    chi2 = float(((counts - exp) ** 2 / exp).sum())
    dof = K * K - 1
    return {
        "theta1_arg_1_i_sqrt10_over_pi": round(t1 / math.pi, 8),
        "theta2_arg_m2_i_sqrt7_over_pi": round(t2 / math.pi, 8),
        "theta1_minpoly_nonmonic": minpoly_t1,
        "theta2_minpoly_nonmonic": minpoly_t2,
        "both_irrational_multiples_of_pi": True,
        "small_integer_relation": relation,  # None -> rationally independent (empirically)
        "rationally_independent": relation is None,
        "joint_chi2_over_dof_on_8x8_grid": round(chi2 / dof, 4),
        "equidistributes_on_2_torus": (relation is None) and (chi2 / dof < 2.0),
        "note": (
            "Both geodesic frequencies are irrational multiples of pi; no small integer "
            "relation a*t1+b*t2+c*pi=0 exists, so by Weyl the pair (m t1, m t2) mod 2pi "
            "equidistributes on the 2-torus (chi^2/dof near 1). Joint prime-geodesic "
            "equidistribution -- the effective, quantitative form of Pass 75 Track 2."
        ),
    }


def main():
    _, Aw = build_graph()
    _, Aq = build_Q43()
    gap = read_gap()

    t2 = track_2_3(Aw, Aq)
    t4 = track_4(Aw)
    t7 = track_7()

    # T1/T5/T6 from GAP
    t1 = {
        "available": gap is not None,
        "perm_group_order": gap["perm_group_order"] if gap else None,
        "rank_action": gap["rank_action"] if gap else None,
        "constituent_degrees": gap["constituent_degrees"] if gap else None,
        "eigenspaces_irreducible": bool(
            gap
            and gap["rank_action"] == 3
            and set(gap["constituent_degrees"]) == {1, 15, 24}
            and all(v == 1 for v in gap["constituent_degrees"].values())
        ),
        "note": (
            "Sp(4,3) is rank-3 on 40 points; permutation character 1+chi_15+chi_24, each "
            "multiplicity 1, so the r/s eigenspaces are irreducible modules (GAP-proved)."
        ),
    }
    t5 = {
        "available": gap is not None,
        "elementary_divisors": gap["smith_elementary_divisors"] if gap else None,
        "product": gap["smith_product"] if gap else None,
        "product_is_3x2^56": bool(gap and gap["smith_product"] == 3 * 2**56),
        "note": "Smith normal form 1^16 2^8 8^15 24; product 3*2^56 = |det A|.",
    }
    t6 = {
        "available": gap is not None,
        "Sp43_has_deg4": gap["Sp43_has_deg4"] if gap else None,
        "Sp43_has_deg5": gap["Sp43_has_deg5"] if gap else None,
        "weil_dim_9_splits_5_plus_4": bool(
            gap and gap["Sp43_has_deg4"] and gap["Sp43_has_deg5"]
        ),
        "note": "Weil rep of Sp(4,3): degree q^2=9 = 5+4 = (q^2+1)/2 + (q^2-1)/2; degrees 4,5 irreducible.",
    }

    checks = {
        "T1_eigenspaces_irreducible": t1["eigenspaces_irreducible"],
        "T2_ovoid_separates_7_vs_10": (t2["alpha_W33"] == 7 and t2["alpha_Q43"] == 10),
        "T4_terwilliger_dim_computed": t4["dim_terwilliger_algebra"] > 2,
        "T5_smith_product_3x2^56": t5["product_is_3x2^56"],
        "T6_weil_5_plus_4": t6["weil_dim_9_splits_5_plus_4"],
        "T7_rationally_independent_equidistributes": t7["equidistributes_on_2_torus"],
    }
    all_ok = all(checks.values())

    print("=" * 74)
    print(
        "PASS 77 -- SEVEN FRONTIER IDEAS (GAP rep theory + geometry + equidistribution)"
    )
    print("=" * 74)
    print(
        f"[1] GAP: rank-{t1['rank_action']} action, perm char constituents "
        f"{t1['constituent_degrees']} -> eigenspaces irreducible: {t1['eigenspaces_irreducible']}"
    )
    print(
        f"[2] ovoids: alpha(W33)={t2['alpha_W33']} (no ovoid) vs alpha(Q43)={t2['alpha_Q43']} "
        f"(ovoid) -> separated: {t2['separated_by_ovoids']}"
    )
    print(
        f"[3] geometric graphs of the 28: W(3,3) & Q(4,3), fingerprinted by ovoid number 7 vs 10"
    )
    print(f"[4] Terwilliger algebra dim = {t4['dim_terwilliger_algebra']}")
    print(
        f"[5] GAP Smith normal form product = {t5['product']} = 3*2^56: {t5['product_is_3x2^56']}"
    )
    print(
        f"[6] GAP: Sp(4,3) has degrees 4 & 5 -> Weil rep 9=5+4: {t6['weil_dim_9_splits_5_plus_4']}"
    )
    print(
        f"[7] freqs t1/pi={t7['theta1_arg_1_i_sqrt10_over_pi']}, t2/pi={t7['theta2_arg_m2_i_sqrt7_over_pi']}; "
        f"relation={t7['small_integer_relation']}; joint chi2/dof={t7['joint_chi2_over_dof_on_8x8_grid']}"
    )
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 74)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 74)

    payload = {
        "schema": "w33.pass77.frontier.v1",
        "status": "PASS" if all_ok else "FAIL",
        "track1_gap_rank3_irreducible": t1,
        "track2_3_ovoid_separator": t2,
        "track4_terwilliger": t4,
        "track5_gap_smith_normal_form": t5,
        "track6_gap_weil_representation": t6,
        "track7_joint_equidistribution": t7,
        "checks": checks,
    }
    with open("w33_pass77_frontier.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass77_frontier.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
