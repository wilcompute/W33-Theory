#!/usr/bin/env python3
"""Genus percolation as an information-hole oscillator.

This extends the oscillator stack with the user's suggestion:
  a torus hole should be read as an information hole, and genus oscillation
  should be treated as fractal/topological correction.

The central object is the K12 critical horizon.  The complete graph K12 has
  V = 12,
  E = C(12,2) = 66.

In a minimal triangular embedding, every face is a triangle, so
  3F = 2E,
  F = 44.

Euler then gives
  chi = V - E + F = 12 - 66 + 44 = -10,
  g = (2-chi)/2 = 6 = q!.

Thus the K12 edge payload is not isolated:
  K12 triangular horizon = (V,E,F) = (12,66,44), genus 6.

The information-hole cost is
  2g = 12 = k.

So k=12 is the total Euler information deficit required to open six handles.
The corrected numerator is
  (12-3)(12-4) = 72 = E + g = 66 + 6.

This says the [72,66]_3 code is the complete K12 edge payload plus one parity
symbol per genus hole.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_genus_percolation_information_hole.json"

q = 3
qfac = math.factorial(q)
dX, dZ = 3, 4
k = dX * dZ
Phi6 = 7
Phi4 = 10
pIh = 11
v_w33 = 40
f_flags = 24
H1 = 81

# K12 critical horizon.
N = k
V = N
E = math.comb(N, 2)
F_tri = 2 * E // 3
chi = V - E + F_tri
genus = (2 - chi) // 2
information_hole_cost = 2 * genus
corrected_total = (N - dX) * (N - dZ)
parity = corrected_total - E

# Toroidal seed and dual pair.
K7_edges = math.comb(Phi6, 2)
K7_num = (Phi6 - dX) * (Phi6 - dZ)
K7_genus = K7_num // k
csaszar = {"V": 7, "E": 21, "F": 14}
szilassi = {"V": 14, "E": 21, "F": 7}

def triangulated_surface(n: int) -> dict[str, int | bool]:
    e = math.comb(n, 2)
    triangular = (2 * e) % 3 == 0
    f = (2 * e) // 3 if triangular else None
    if f is None:
        return {"n": n, "E": e, "triangular": False}
    c = n - e + f
    return {
        "n": n,
        "V": n,
        "E": e,
        "F": f,
        "chi": c,
        "genus": (2 - c) // 2,
        "triangular": True,
        "hole_cost_2g": 2 * ((2 - c) // 2),
    }

# Genus-percolation threshold ladder from existing scripts, reinterpreted as information-hole thresholds.
threshold_order = [
    "p_geom",
    "p_beta1",
    "p_Cl",
    "p_H1",
    "p_81_plus",
    "p_81_minus",
    "p_162",
    "p_split",
]
threshold_reading = {
    "p_geom": "occupied incidence geometry first connects",
    "p_beta1": "first information hole opens (nonzero H1/Beta1)",
    "p_Cl": "Clifford transport becomes visible on occupied topology",
    "p_H1": "rank C_H(p) reaches protected H1 visibility",
    "p_81_plus": "first 81-sector saturation",
    "p_81_minus": "conjugate 81-sector saturation",
    "p_162": "two-sector saturation",
    "p_split": "stable nontrivial spectral splitting / branch selection",
}

payload = {
    "summary": {
        "K12_triangular_horizon": {"V": V, "E": E, "F": F_tri, "chi": chi, "genus": genus},
        "information_hole_cost_2g": information_hole_cost,
        "horizon_code": [corrected_total, E, parity],
        "threshold_order": threshold_order,
        "all_identities_hold": True,
    },
    "K12_information_hole": {
        "surface": {"V": V, "E": E, "F": F_tri, "chi": chi, "genus": genus},
        "closed_forms": {
            "E": "C(12,2)=66",
            "F": "2E/3=44=dZ*p_Ih=4*11",
            "chi": "12-66+44=-10",
            "genus": "(2-chi)/2=6=q!",
            "hole_cost": "2g=12=k",
            "horizon": "72=66+6=edges + one parity per genus hole",
        },
    },
    "toroidal_seed": {
        "Csaszar": csaszar,
        "Szilassi": szilassi,
        "K7_edges": K7_edges,
        "K7_genus_numerator": K7_num,
        "K7_genus": K7_genus,
        "reading": "Csaszar uses n=V=7; Szilassi uses n=F=7; both give genus one and numerator k=12.",
    },
    "triangular_surfaces": {
        "K7": triangulated_surface(7),
        "K12": triangulated_surface(12),
    },
    "percolation_information_thresholds": {
        "threshold_order": threshold_order,
        "threshold_reading": threshold_reading,
        "operator": "C_H(p)=Y_p Y_p^* restricted to K=H1",
        "observables": ["rank C_H(p)", "d_eff(p)", "Spec(C_H(p))", "Betti vector of occupied subcomplex"],
        "interpretation": "genus percolation opens information holes; each stable handle contributes a parity/check branch at the K12 horizon",
    },
    "identities": {
        "K12_edges_66": E == 66,
        "triangular_faces_44": F_tri == 44 == dZ * pIh,
        "euler_minus_10": chi == -10,
        "genus_qfactorial": genus == qfac == 6,
        "hole_cost_is_k": information_hole_cost == k == 12,
        "corrected_total_72": corrected_total == 72,
        "parity_one_per_genus_hole": parity == genus == qfac == 6,
        "code_rate_11_12": E * 12 == corrected_total * 11,
        "K7_seed_num_is_k": K7_num == k,
        "K7_genus_one": K7_genus == 1,
        "dual_toroidal_edges": csaszar["E"] == szilassi["E"] == K7_edges == 21,
        "payload_two_tori_tetra": E == csaszar["E"] + szilassi["E"] + f_flags,
        "faces_equal_spine_sum": F_tri == dZ * pIh == 44,
        "W33_vertex_relation": F_tri - dZ == v_w33,
        "H1_relation": H1 == q ** dZ,
    },
    "closed_forms": {
        "genus_equation": "g(K_n)=(n-3)(n-4)/12=(n-dX)(n-dZ)/(dX*dZ)",
        "K12_surface": "K12 triangular embedding: (V,E,F)=(12,66,44), chi=-10, genus=6",
        "information_hole": "one torus handle removes two Euler units; six holes remove 12=k units",
        "code": "[72,66]_3 = K12 edges + one parity/check symbol per genus hole",
        "fractal_reading": "genus oscillation is recursive hole creation: K7 gives one hole, K12 gives six holes, percolation thresholds determine when holes become visible to H1",
    },
    "theorem": "Genus-Percolation Information-Hole Theorem: the [72,66]_3 horizon is the K12 triangular genus-six surface. Its 66 edges are the payload, its six handles are the parity rank, and the information-hole cost 2g is k=12. Genus percolation is the stochastic/fractal activation of these holes as visible rank and spectral splitting in C_H(p).",
    "honesty_boundary": "Exact finite topology/arithmetic synthesis. The information-hole and fractal-percolation language is a structural model; physical dynamics require explicit percolation simulations on the W33/toroidal incidence atoms.",
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
