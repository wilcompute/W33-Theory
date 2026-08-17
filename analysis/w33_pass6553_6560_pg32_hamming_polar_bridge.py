#!/usr/bin/env python3
"""Passes 6553--6560: PG(3,2) Hamming-polar bridge for the doily code.

Starting from the Pass6533 quadratic-evaluation code C=S+<q0>, this verifier
identifies S^perp as the binary [15,11,3] Hamming code and proves that adding
q0 to the primal code imposes exactly the symplectic-isotropy parity condition
on the 35 Hamming minimum words / PG(3,2) lines.

Consequences checked exactly:
  35 PG(3,2) lines = 15 isotropic doily lines + 20 nonisotropic lines;
  C^perp retains exactly the 15 isotropic minimum words;
  the 20 excluded nonisotropic lines are precisely tricentric triads;
  symplectic polarity pairs those 20 into 10 unordered pairs;
  the union of each polar pair is exactly one weight-6 support of C, hence the
  complement of one 9-point doily grid.

Scope: finite binary geometry/coding only.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE_PATH = HERE / "w33_pass6533_6540_doily_quadratic_evaluation_code.py"
OUT = ROOT / "data" / "PART_W33_PASS6553_6560_PG32_HAMMING_POLAR_BRIDGE.json"

spec = importlib.util.spec_from_file_location("doily_code_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)


def main():
    zero15 = (0,) * 15
    all_a = [base.ZERO] + base.V
    S = {base.codeword(a, 0) for a in all_a}
    C = {base.codeword(a, t) for a in all_a for t in (0, 1)}
    qword = base.codeword(base.ZERO, 1)
    assert len(S) == 16 and base.gf2_rank(list(S)) == 4
    assert len(C) == 32 and base.gf2_rank(list(C)) == 5

    sbasis = []
    for w in S:
        if base.gf2_rank(sbasis + [w]) > len(sbasis):
            sbasis.append(w)
    cbasis = []
    for w in C:
        if base.gf2_rank(cbasis + [w]) > len(cbasis):
            cbasis.append(w)
    assert len(sbasis) == 4 and len(cbasis) == 5

    H = []
    Cdual = []
    for mask in range(1 << 15):
        z = tuple((mask >> i) & 1 for i in range(15))
        if all(base.dot(b, z) == 0 for b in sbasis):
            H.append(z)
        if all(base.dot(b, z) == 0 for b in cbasis):
            Cdual.append(z)
    assert len(H) == 2048 and base.gf2_rank(H) == 11
    assert len(Cdual) == 1024 and base.gf2_rank(Cdual) == 10
    assert all(z in H for z in Cdual)
    assert all((base.dot(qword, z) == 0) == (z in Cdual) for z in H)

    H3 = [z for z in H if sum(z) == 3]
    C3 = [z for z in Cdual if sum(z) == 3]
    assert len(H3) == 35
    assert len(C3) == 15

    pg_lines = set()
    iso_lines = set()
    noniso_lines = set()
    for x, y in itertools.combinations(base.V, 2):
        z = base.add(x, y)
        L = frozenset((base.VIDX[x], base.VIDX[y], base.VIDX[z]))
        pg_lines.add(L)
        if base.B(x, y) == 0:
            iso_lines.add(L)
        else:
            noniso_lines.add(L)
    assert len(pg_lines) == 35
    assert len(iso_lines) == 15
    assert len(noniso_lines) == 20

    H3supports = {base.support(z) for z in H3}
    C3supports = {base.support(z) for z in C3}
    assert H3supports == pg_lines
    assert C3supports == iso_lines
    assert H3supports - C3supports == noniso_lines

    parity = Counter()
    for L in pg_lines:
        pts = [base.V[i] for i in L]
        p = sum(base.q0(x) for x in pts) & 1
        b = base.B(pts[0], pts[1])
        assert p == b
        parity["isotropic" if b == 0 else "nonisotropic"] += 1
    assert parity == Counter({"isotropic": 15, "nonisotropic": 20})

    # Each nonisotropic PG(3,2) line is a three-point pairwise-noncollinear
    # doily triad with exactly three common perpendicular points.
    polar = {}
    for L in noniso_lines:
        Lperp = frozenset(
            i for i, v in enumerate(base.V)
            if all(base.B(v, base.V[j]) == 0 for j in L)
        )
        assert len(Lperp) == 3
        assert Lperp in noniso_lines
        assert Lperp != L
        assert not (Lperp & L)
        # The three points of Lperp are exactly the common centers of L.
        centers = {
            i for i, v in enumerate(base.V)
            if all(base.B(v, base.V[j]) == 0 for j in L)
        }
        assert centers == set(Lperp)
        polar[L] = Lperp
    assert all(polar[polar[L]] == L for L in noniso_lines)
    polar_pairs = {frozenset((L, polar[L])) for L in noniso_lines}
    assert len(polar_pairs) == 10

    w6_supports = {base.support(w) for w in C if sum(w) == 6}
    pair_unions = {frozenset().union(*pair) for pair in polar_pairs}
    assert len(w6_supports) == 10
    assert pair_unions == w6_supports

    # Veldkamp all-perp lines: a Hamming line L={a,b,a+b} gives the three
    # simplex/perp words s_a,s_b,s_(a+b). Their common zero core is L^perp.
    core_types = Counter()
    for L in pg_lines:
        labels = [base.V[i] for i in L]
        perps = [base.codeword(a, 0) for a in labels]
        core = set(range(15))
        for w in perps:
            core &= set(base.zeros(w))
        core = frozenset(core)
        expected = frozenset(
            i for i, v in enumerate(base.V)
            if all(base.B(v, a) == 0 for a in labels)
        )
        assert core == expected
        if L in iso_lines:
            assert core == L
            core_types["collinear"] += 1
        else:
            assert core == polar[L]
            core_types["tricentric"] += 1
    assert core_types == Counter({"collinear": 15, "tricentric": 20})

    result = {
        "passes": "6553-6560",
        "object": "PG(3,2) Hamming-polar bridge",
        "codes": {
            "simplex": [15, 4, 8],
            "hamming_dual": [15, 11, 3],
            "quadratic_extension": [15, 5, 6],
            "quadratic_dual": [15, 10, 3],
            "relation": "C^perp = {h in Hamming(15,11,3) : <q0,h>=0}",
        },
        "hamming_minimum_shell": {
            "weight3_words": 35,
            "equals_all_PG32_lines": True,
            "isotropic_retained_in_Cdual": 15,
            "nonisotropic_excluded": 20,
            "selector_identity": "<q0,1_{x,y,x+y}> = B(x,y)",
        },
        "doily_veldkamp_split": {
            "15_isotropic_lines": "collinear all-perp Veldkamp cores",
            "20_nonisotropic_lines": "tricentric triads",
            "all_perp_total": 35,
        },
        "polarity_grid_bridge": {
            "nonisotropic_lines": 20,
            "polar_pairs": 10,
            "pair_union_size": 6,
            "pair_unions_equal_weight6_supports": True,
            "interpretation": "10 polar-pair unions = 10 grid complements",
        },
        "scope": "finite binary geometry/coding only",
        "checks": "PASS",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
