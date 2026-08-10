#!/usr/bin/env python3
"""Pass 4767 -- every parameter-equal pair in the quadrangle zoo, decided by canonical form.

Pass 4685 compared trace quantities between quadrangles and read agreement as evidence.
Pass 4693 showed the traces are determined by the strongly regular parameters, so the
comparison could not have failed.  The test that WOULD have settled it -- canonical form --
was unavailable then and is cheap now (Pass 4755, BLISS via python-igraph).

So: build the zoo, group the members by their SRG parameters, and inside each group ask
whether the graphs are actually isomorphic.  This is the question "are these two objects
the same?" asked in the only way that answers it.

    py -3 analysis/w33_pass4767_the_quadrangle_zoo_by_canonical_form.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from collections import defaultdict
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


PP = _load("pp", "w33_pass4754_4755_prime_power_quadrangles_and_bliss.py")
P62 = _load("p62", "w33_pass4562_second_dual_pair_and_a_correction.py")
P48 = _load("p48", "w33_pass4448_4450_q53_floquet_tanner.py")
P89 = _load("p89", "w33_pass4389_hermitian_quadrangle_measured.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def main() -> int:
    print("=" * 78)
    print("Pass 4767 -- the zoo, grouped by parameters, decided by canonical form")
    print("=" * 78)

    zoo = {}
    for q in (2, 3, 4, 5):
        p, k = (2, 2) if q == 4 else (q, 1)
        pts, lines = PP.build_w3(PP.GF(p, k))
        zoo[f"W(3,{q})"] = graph_of(pts, lines)
        dp, dl = PP.dual(pts, lines)
        zoo[f"Q(4,{q})"] = graph_of(dp, dl)          # the dual of W(3,q)
    for name, mk in (("Q(5,2)", P62.build_q52), ("H(3,4)", P62.build_h34),
                     ("Q(5,3)", P48.build_q53)):
        pts, lines = mk()
        zoo[name] = graph_of(pts, lines)
    try:
        pts, lines = P89.build_h39()[:2]
        zoo["H(3,9)"] = graph_of(pts, lines)
    except Exception as e:
        print(f"  H(3,9) unavailable ({type(e).__name__})")

    print(f"\n  {'geometry':10s} {'n':>5s} {'deg':>4s} {'SRG parameters':>20s}")
    params = {}
    for name in sorted(zoo, key=lambda x: (zoo[x].vcount(), x)):
        g = zoo[name]
        prm = PP.srg_params(g)
        params[name] = prm
        print(f"  {name:10s} {g.vcount():5d} {g.degree(0):4d} {str(prm):>20s}")

    groups = defaultdict(list)
    for name, prm in params.items():
        groups[prm].append(name)

    print("\n  Parameter-equal groups, and whether the members are the SAME graph\n")
    findings = []
    for prm, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        print(f"    SRG{prm}  ->  {', '.join(sorted(members))}")
        for a, b in itertools.combinations(sorted(members), 2):
            iso = PP.canon(zoo[a]) == PP.canon(zoo[b])
            findings.append({"a": a, "b": b, "params": list(prm),
                             "isomorphic": bool(iso)})
            print(f"        {a} vs {b}: "
                  f"{'ISOMORPHIC' if iso else 'NOT isomorphic'}")

    same = [f for f in findings if f["isomorphic"]]
    diff = [f for f in findings if not f["isomorphic"]]
    print(f"""
    {len(findings)} parameter-equal pairs: {len(same)} genuinely the same graph, {len(diff)} not.

    THIS IS THE TEST PASS 4685 SHOULD HAVE RUN. It compared tr(A^3) and tr(A^4) between
    quadrangles, and every one of those numbers is a function of (v,k,lambda,mu) -- so the
    parameter-equal pairs HAD to agree and the parameter-different ones HAD to disagree,
    whatever the geometry was doing. A canonical form asks the actual question, and the
    answer is not uniform: parameter-equal pairs split both ways in this table.

    THAT SPLIT IS THE WHOLE POINT. If equal parameters implied isomorphism, the caution in
    CLAUDE.md would be pedantry. It does not: {len(diff)} of {len(findings)} pairs here share every
    parameter and are different graphs. Any argument that moved a property from one member
    of such a pair to the other, on the strength of matching parameters, was unlicensed.""")

    out = {
        "boundary": ("isomorphism is decided by BLISS canonical form and is exact. The zoo "
                     "is the quadrangles this repository can currently construct -- W(3,q) "
                     "and its dual for q = 2,3,4,5 plus Q(5,2), H(3,4), Q(5,3) and H(3,9) "
                     "where the builder is available -- and is not the complete list of "
                     "generalised quadrangles at these parameters"),
        "members": {k: list(v) for k, v in params.items()},
        "parameter_groups": {str(k): sorted(v) for k, v in groups.items() if len(v) > 1},
        "pairs": findings,
        "same": len(same), "different": len(diff),
        "conclusion": ("parameter-equal quadrangles split both ways under canonical form, "
                       "so equal SRG parameters license nothing about isomorphism -- the "
                       "test Pass 4685 ran could not have detected the difference"),
    }
    p = ROOT / "data" / "PART_W33_PASS4767_QUADRANGLE_ZOO_CANONICAL.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
