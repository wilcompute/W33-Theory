#!/usr/bin/env python3
"""Exact oriented-A2 refinement of the E8 twisted-fibration weld.

Depends only on the already-certified Coxeter/root machinery in
analysis/w33_e8_twisted_fibration_weld.py.  It proves that the 80 order-three
root orbits are oriented A2 triangles and that pairing each orbit with its
negative recovers exactly the 40 Pass-1021 C6/Eisenstein fibres.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_e8_oriented_a2_refinement.json"

import w33_e8_twisted_fibration_weld as base


def row_tuple(M):
    out=[]
    for x in list(M):
        x=sp.Rational(x)
        assert x.q == 1
        out.append(int(x))
    return tuple(out)


def main(write=True):
    roots=base.e8_roots()
    idx={r:i for i,r in enumerate(roots)}
    c=sp.eye(8)
    for r in base.SIMPLE_ROOTS:
        c=c*base.reflection(r)
    g=c**10
    u=c**5

    def act(i,A):
        return idx[row_tuple(sp.Matrix([roots[i]])*A)]

    assert base.matrix_order(c,60)==30
    assert base.matrix_order(g,12)==3
    assert base.matrix_order(u,12)==6
    assert sp.eye(8)+g+g**2 == sp.zeros(8)

    unseen=set(range(240))
    oriented=[]
    while unseen:
        i=min(unseen)
        orb=(i,act(i,g),act(i,g**2))
        assert len(set(orb))==3
        unseen.difference_update(orb)
        vec=[sp.Matrix([roots[j]]) for j in orb]
        assert vec[0]+vec[1]+vec[2] == sp.zeros(1,8)
        ips=[]
        for a in range(3):
            for b in range(a+1,3):
                ips.append(sp.Rational((vec[a]*vec[b].T)[0],4))
        assert ips==[-1,-1,-1]
        oriented.append(frozenset(orb))
    assert len(oriented)==80
    assert len(set(oriented))==80

    orbit_id={i:k for k,o in enumerate(oriented) for i in o}
    neg_pairs=set()
    full_a2=[]
    for k,o in enumerate(oriented):
        i=min(o)
        ni=idx[tuple(-x for x in roots[i])]
        l=orbit_id[ni]
        assert l != k
        neg_pairs.add(tuple(sorted((k,l))))
    assert len(neg_pairs)==40

    for k,l in sorted(neg_pairs):
        six=set(oriented[k])|set(oriented[l])
        assert len(six)==6
        i=min(six)
        unit={act(i,u**j) for j in range(6)}
        assert unit==six
        full_a2.append(frozenset(six))
    assert len(set(full_a2))==40

    checks={
        "one_plus_g_plus_g2_is_zero": sp.eye(8)+g+g**2 == sp.zeros(8),
        "root_shell_has_80_g_orbits": len(oriented)==80,
        "every_g_orbit_sums_to_zero": True,
        "every_g_orbit_has_pairwise_inner_product_minus_one": True,
        "each_g_orbit_is_an_oriented_A2_triangle": True,
        "negation_pairs_80_oriented_triangles_into_40": len(neg_pairs)==40,
        "each_opposite_pair_is_six_roots": all(len(x)==6 for x in full_a2),
        "each_six_root_A2_equals_pass1021_c5_unit_orbit": True,
    }
    assert all(checks.values())
    result={
        "schema":"w33.e8_oriented_a2_refinement.v1",
        "status":"PASS",
        "headline":"The 80 nonzero twisted-register/Pauli labels are 80 oriented A2 root triangles; v and -v are opposite orientations of the same Pass-1021 six-root A2 fibre.",
        "prior_art":{
            "base_weld":"data/w33_e8_twisted_fibration_weld.json",
            "pass1021":"data/w33_pass1021_e8_fibration_over_forty.json",
        },
        "counts":{
            "E8_roots":240,
            "oriented_A2_triangles":80,
            "opposite_orientation_pairs":40,
            "roots_per_oriented_triangle":3,
            "roots_per_full_A2":6,
        },
        "identification":{
            "v":"{r,gr,g^2r}",
            "minus_v":"{-r,-gr,-g^2r}",
            "projective_point":"the union, a six-root A2 subsystem",
            "pass1021_fibre":"the same <c^5> = <-1,g> orbit",
        },
        "check_count":len(checks),
        "checks":checks,
        "scope":"Exact finite root-system refinement of the already-certified E8 twisted-register/root-fibration weld; no new physical claim.",
    }
    if write:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    return result

if __name__ == "__main__":
    main(True)
