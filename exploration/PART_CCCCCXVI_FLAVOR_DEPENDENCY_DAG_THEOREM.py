#!/usr/bin/env python3
"""
PART CCCCCXVI: Flavor Dependency DAG Theorem

PART CCCCCXV reduced the flavor sector to three finite operators:

  O1 = Perron determinant compactification
  O2 = E6 excited cumulant/gap generator
  O3 = Z12 holonomy unit group

This verifier makes the dependency structure explicit as a directed acyclic
graph.  It separates:

  - primitive operator nodes,
  - W(3,3) atom nodes,
  - intermediate derived nodes,
  - final observable nodes.

The point is to prevent hidden circularity.  Each flavor observable must be
reachable from the three operator basis plus the W(3,3) atoms, and the final
observable set must match the values from CCCCCXV.

Run:
    python exploration/PART_CCCCCXVI_FLAVOR_DEPENDENCY_DAG_THEOREM.py
"""
from __future__ import annotations

import json
import math
from collections import defaultdict, deque
from fractions import Fraction
from pathlib import Path


def topo_sort(nodes: set[str], edges: list[tuple[str, str]]) -> list[str]:
    out: dict[str, list[str]] = defaultdict(list)
    indeg = {n: 0 for n in nodes}
    for a, b in edges:
        out[a].append(b)
        indeg[b] += 1
    q = deque(sorted([n for n, d in indeg.items() if d == 0]))
    order: list[str] = []
    while q:
        u = q.popleft()
        order.append(u)
        for w in sorted(out[u]):
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    if len(order) != len(nodes):
        raise ValueError("cycle detected")
    return order


def reachable_from(starts: set[str], edges: list[tuple[str, str]]) -> set[str]:
    out: dict[str, list[str]] = defaultdict(list)
    for a, b in edges:
        out[a].append(b)
    seen = set(starts)
    q = deque(starts)
    while q:
        u = q.popleft()
        for w in out[u]:
            if w not in seen:
                seen.add(w)
                q.append(w)
    return seen


def frac_str(x: Fraction | int) -> str:
    if isinstance(x, Fraction):
        return str(x)
    return str(x)


def main() -> None:
    # W(3,3) atoms from true master seed.
    q = 3
    assert math.factorial(q) == 2 * q
    lam = 2
    mu = 4
    k = q * (q + 1)
    v = (q + 1) * (q*q + 1)
    E = v * k // 2
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1
    delta_r = k - r
    delta_s = k - s

    # Primitive operator outputs.
    O1 = v + 1
    O2_exc_total = 2*f + 2*g
    O2_exc_moment = 2*f*delta_r + 2*g*delta_s
    O2_exc_mean = Fraction(O2_exc_moment, O2_exc_total)
    O2_gap_ratio = Fraction(delta_s, delta_r)
    O3_units = [1, mu+1, phi6, k-1]

    # Derived values.
    D_t = O1
    D_b = q*D_t + lam
    D_c = D_b + k
    lambda_H = O2_gap_ratio / O2_exc_mean
    M_vac = (k-1) * ((k-lam)**2 + 1)
    Delta_M = Fraction(q, lam*(k-1))
    M_eff = Fraction(M_vac, 1) + Delta_M
    alpha_slip = Fraction(v, 1) / M_eff

    values: dict[str, Fraction | int] = {
        "q": q,
        "lambda": lam,
        "mu": mu,
        "k": k,
        "v": v,
        "Phi3": phi3,
        "Phi4": phi4,
        "Phi6": phi6,
        "Delta_r": delta_r,
        "Delta_s": delta_s,
        "O1_PerronDet": O1,
        "O2_E6Mean": O2_exc_mean,
        "O2_GapRatio": O2_gap_ratio,
        "O3_BottomUnit": mu+1,
        "O3_CKMCPUnit": phi6,
        "O3_PMNSCPUnit": k-1,
        "D_t": D_t,
        "D_b": D_b,
        "D_c": D_c,
        "lambda_H": lambda_H,
        "M_vac": M_vac,
        "Delta_M": Delta_M,
        "alpha_slip": alpha_slip,
        "y_t_cubed": Fraction(v, D_t),
        "lambda_CKM": Fraction(q*q, v),
        "compactified_CKM": Fraction(q*q, D_t),
        "y_b": Fraction(q, D_b),
        "y_c": Fraction(1, D_c),
        "y_tau": lambda_H * Fraction(q, D_b)**2 / Fraction(1, D_c),
        "A_CKM": Fraction(q**4, phi3) * lambda_H,
        "PMNS_theta13": Fraction(q*q, lam*lam*phi3) * lambda_H,
        "rho_bar": Fraction(lam, mu+1)**2,
        "eta_bar": Fraction(phi6, phi4)**3,
        "PMNS_delta_over_pi": Fraction(k-1, phi4),
        "PMNS_solar": Fraction(mu, phi3),
        "PMNS_atmospheric": Fraction(mu, phi6),
        "alpha_inverse_refined": Fraction(D_c, 1) + alpha_slip,
    }

    primitive_nodes = {
        "q", "lambda", "mu", "k", "v", "Phi3", "Phi4", "Phi6", "Delta_r", "Delta_s",
        "O1_PerronDet", "O2_E6Mean", "O2_GapRatio", "O3_BottomUnit", "O3_CKMCPUnit", "O3_PMNSCPUnit",
    }
    intermediate_nodes = {"D_t", "D_b", "D_c", "lambda_H", "M_vac", "Delta_M", "alpha_slip"}
    observable_nodes = {
        "y_t_cubed", "lambda_CKM", "compactified_CKM", "y_b", "y_c", "y_tau", "A_CKM",
        "PMNS_theta13", "rho_bar", "eta_bar", "PMNS_delta_over_pi", "PMNS_solar", "PMNS_atmospheric",
        "alpha_inverse_refined",
    }
    nodes = primitive_nodes | intermediate_nodes | observable_nodes

    edges = [
        ("O1_PerronDet", "D_t"),
        ("q", "D_b"), ("D_t", "D_b"), ("lambda", "D_b"),
        ("D_b", "D_c"), ("k", "D_c"),
        ("O2_GapRatio", "lambda_H"), ("O2_E6Mean", "lambda_H"),
        ("k", "M_vac"), ("lambda", "M_vac"),
        ("q", "Delta_M"), ("lambda", "Delta_M"), ("k", "Delta_M"),
        ("v", "alpha_slip"), ("M_vac", "alpha_slip"), ("Delta_M", "alpha_slip"),
        ("v", "y_t_cubed"), ("D_t", "y_t_cubed"),
        ("q", "lambda_CKM"), ("v", "lambda_CKM"),
        ("q", "compactified_CKM"), ("D_t", "compactified_CKM"),
        ("q", "y_b"), ("D_b", "y_b"),
        ("D_c", "y_c"),
        ("lambda_H", "y_tau"), ("y_b", "y_tau"), ("y_c", "y_tau"),
        ("q", "A_CKM"), ("Phi3", "A_CKM"), ("lambda_H", "A_CKM"),
        ("q", "PMNS_theta13"), ("lambda", "PMNS_theta13"), ("Phi3", "PMNS_theta13"), ("lambda_H", "PMNS_theta13"),
        ("lambda", "rho_bar"), ("O3_BottomUnit", "rho_bar"),
        ("O3_CKMCPUnit", "eta_bar"), ("Phi4", "eta_bar"),
        ("O3_PMNSCPUnit", "PMNS_delta_over_pi"), ("Phi4", "PMNS_delta_over_pi"),
        ("mu", "PMNS_solar"), ("Phi3", "PMNS_solar"),
        ("mu", "PMNS_atmospheric"), ("Phi6", "PMNS_atmospheric"),
        ("D_c", "alpha_inverse_refined"), ("alpha_slip", "alpha_inverse_refined"),
    ]

    order = topo_sort(nodes, edges)
    reachable = reachable_from(primitive_nodes, edges)

    expected = {
        "y_t_cubed": Fraction(40, 41),
        "lambda_CKM": Fraction(9, 40),
        "compactified_CKM": Fraction(9, 41),
        "y_b": Fraction(3, 125),
        "y_c": Fraction(1, 137),
        "y_tau": Fraction(16029, 1562500),
        "A_CKM": Fraction(81, 100),
        "PMNS_theta13": Fraction(9, 400),
        "rho_bar": Fraction(4, 25),
        "eta_bar": Fraction(343, 1000),
        "PMNS_delta_over_pi": Fraction(11, 10),
        "PMNS_solar": Fraction(4, 13),
        "PMNS_atmospheric": Fraction(4, 7),
        "alpha_inverse_refined": Fraction(669969, 4889),
    }

    dim_G2 = lam*phi6
    dim_SU5 = f
    dim_SO10 = q*q*(mu+1)
    dim_E6 = lam*q*phi3
    dim_E8 = E + lam**3

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "dag_is_acyclic": len(order) == len(nodes),
        "all_observables_reachable_from_primitives": observable_nodes.issubset(reachable),
        "no_observable_is_primitive": primitive_nodes.isdisjoint(observable_nodes),
        "expected_values_match": all(values[name] == val for name, val in expected.items()),
        "minimal_operator_values": (O1, O2_exc_mean, O2_gap_ratio, sorted(O3_units)) == (41, Fraction(160,13), Fraction(8,5), [1,5,7,11]),
        "intermediate_values": (D_t, D_b, D_c, lambda_H, alpha_slip) == (41,125,137,Fraction(13,100),Fraction(880,24445)),
        "dimensions": (dim_G2, dim_SU5, dim_SO10, dim_E6, dim_E8) == (14,24,45,78,248),
    }

    result = {
        "part": "CCCCCXVI",
        "title": "Flavor Dependency DAG Theorem",
        "primitive_nodes": sorted(primitive_nodes),
        "intermediate_nodes": sorted(intermediate_nodes),
        "observable_nodes": sorted(observable_nodes),
        "edge_count": len(edges),
        "topological_order": order,
        "generated_values": {name: frac_str(values[name]) for name in sorted(values)},
        "expected_observables": {name: frac_str(val) for name, val in expected.items()},
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The three-operator flavor basis forms an explicit acyclic dependency graph. All final flavor observables "
            "are reachable from the primitive W(3,3) atoms plus the three operator nodes, while none of the final "
            "observables is primitive. This makes the generative structure non-circular and auditable."
        ),
    }

    out = Path("PART_CCCCCXVI_flavor_dependency_dag_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXVI: Flavor Dependency DAG Theorem")
    print("=" * 88)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 88)
    print(f"nodes={len(nodes)}, edges={len(edges)}")
    print(f"observables={len(observable_nodes)} all reachable={observable_nodes.issubset(reachable)}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
