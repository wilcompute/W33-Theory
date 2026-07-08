#!/usr/bin/env python3
"""
Pass 93 -- A second strongly regular graph out of W(3,3): SRG(135,70,37,35) from the glue group.

Pass 92 showed the discriminant form of the W(3,3) code-lattice is the E8/2E8 = O+_8(2) form, with
135 nonzero isotropic glue cosets.  The E8 literature notes that the graph on those 135 isotropic
vectors, joined when their inner product is 0 mod 2, is the O+_8(2) polar graph SRG(135,70,37,35).

This pass builds that graph directly from W(3,3)'s own binary code C_2(W)=[40,16,8]:
  * take the 135 weight-8 (isotropic) cosets of C in C^perp (the (Z/2)^8 glue group),
  * join two cosets when their Hamming inner product is 0 mod 2 (well-defined on C^perp/C),
and verifies it is SRG(135,70,37,35) with spectrum {70^1, 7^50, (-5)^84}.

So the 40-point E6 generalized quadrangle W(3,3) generates the 135-point E8 polar graph through its
own code-lattice -- an explicit E6 -> E8 bridge inside a single finite object.  (Note 135 + 120 = 255
= 2^8-1, and 40 -> 135 -> ... the exceptional tower surfacing again.)

Self-contained (GF(2) linear algebra).  ASCII-only.
"""

from __future__ import annotations

import json
from collections import Counter

import numpy as np

from w33_pass92_discriminant_e8 import (
    build_graph,
    nullspace_basis,
    rowspace_basis,
    to_int,
)


def isotropic_cosets():
    _, A = build_graph()
    C_basis = rowspace_basis([to_int(A[i]) for i in range(40)])
    Cp_basis = nullspace_basis(A)
    Cvecs = [0]
    for b in C_basis:
        Cvecs = Cvecs + [x ^ b for x in Cvecs]
    allb = list(C_basis)
    glue = []
    for v in Cp_basis:
        r = v
        for b in allb:
            r = min(r, r ^ b)
        if r:
            allb.append(r)
            allb.sort(reverse=True)
            glue.append(v)
    reps = [0]
    for e in glue:
        reps = reps + [x ^ e for x in reps]
    iso = [rep for rep in reps if min((rep ^ c).bit_count() for c in Cvecs) == 8]
    return iso


def srg_params(M):
    n = M.shape[0]
    deg = Counter(int(M[i].sum()) for i in range(n))
    A2 = M @ M
    lam, mu = Counter(), Counter()
    for i in range(n):
        for j in range(i + 1, n):
            c = int(A2[i, j])
            (lam if M[i, j] else mu)[c] += 1
    ev = sorted(np.rint(np.linalg.eigvalsh(M.astype(float))).astype(int).tolist())
    return deg, lam, mu, Counter(ev)


def main():
    iso = isotropic_cosets()
    n = len(iso)
    M = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            if i != j and (iso[i] & iso[j]).bit_count() % 2 == 0:
                M[i, j] = 1

    deg, lam, mu, spec = srg_params(M)
    is_srg = (
        n == 135 and dict(deg) == {70: 135} and set(lam) == {37} and set(mu) == {35}
    )
    spec_ok = dict(spec) == {70: 1, 7: 50, -5: 84}

    checks = {
        "135_isotropic_vertices": n == 135,
        "70_regular": dict(deg) == {70: 135},
        "lambda_37": set(lam) == {37},
        "mu_35": set(mu) == {35},
        "is_SRG_135_70_37_35": is_srg,
        "spectrum_70_7^50_-5^84": spec_ok,
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print(
        "PASS 93 -- SRG(135,70,37,35) FROM THE W(3,3) GLUE GROUP (O+_8(2) POLAR GRAPH)"
    )
    print("=" * 78)
    print(
        f"vertices = {n} isotropic glue cosets; degree {list(deg)[0]}; "
        f"lambda {list(lam)[0]}; mu {list(mu)[0]}"
    )
    print(f"spectrum: {dict(spec)}  (= 70^1, 7^50, (-5)^84)")
    print(f"is SRG(135,70,37,35): {is_srg}; spectrum matches: {spec_ok}")
    print()
    print(
        "E6 -> E8 bridge: the 40-point E6 GQ W(3,3) generates the 135-point E8 polar graph"
    )
    print(
        "   SRG(135,70,37,35) = O+_8(2) polar graph, via its binary code's glue group (Pass 92)."
    )
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 78)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)

    payload = {
        "schema": "w33.pass93.srg135.v1",
        "status": "PASS" if all_ok else "FAIL",
        "vertices": n,
        "degree": list(deg)[0],
        "lambda": list(lam)[0],
        "mu": list(mu)[0],
        "spectrum": {str(k): v for k, v in sorted(spec.items())},
        "is_SRG_135_70_37_35": is_srg,
        "construction": (
            "135 weight-8 (isotropic) cosets of C_2(W)=[40,16,8] in C^perp, joined when "
            "their Hamming inner product is 0 mod 2 (the O+_8(2) polar graph)."
        ),
        "reading": (
            "A second strongly regular graph -- SRG(135,70,37,35), the O+_8(2) polar graph "
            "of E8/2E8 -- falls directly out of W(3,3)'s own code-lattice glue group. The "
            "40-point E6 generalized quadrangle generates the 135-point E8 polar graph: an "
            "explicit E6 -> E8 bridge inside one finite object."
        ),
        "grounding": "E8 lattice: the graph on the 135 isotropic vectors of E8/2E8 is SRG(135,70,37,35).",
        "checks": checks,
    }
    with open("w33_pass93_srg135.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass93_srg135.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
