"""Passes 5376-5379 -- turning a divisibility fact into an action, looking at the 312
points the simplex does not touch, and the bound Hoffman structurally cannot give.

  5376  Build the other lane's carrier and their explicit 13-cover, then verify that it is
        a Hoffman-tight coclique of the P-block graph and therefore -- by Pass 5342, whose
        mechanism is Pass 1614's -- a regular 12-simplex.

  5377  Pass 5343 established only that 576 divides 13!.  That is divisibility, not an
        action, and I said so at the time.  Compute the setwise stabiliser of the 13-cover
        inside the graph's automorphism group, then factor out the pointwise kernel, so the
        question becomes an answer either way.

  5378  Whatever the kernel is, it lives on the 312 blocks OUTSIDE the cover.  That
        complement is 325 - 13, and if the stabiliser acts trivially on the 13 then the
        entire order-576 group is doing its work out there.

  5379  Two-distance bounds.  A coclique uses only the nonadjacent inner product, which is
        why Hoffman is blind to realisability.  A bound using BOTH values would see the
        geometry.  Attempted here rather than asserted, and the outcome is reported whether
        or not it improves anything.

    py -3 analysis/w33_pass5376_5379_the_stabiliser_acts_or_it_does_not.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
import time
from pathlib import Path

import igraph
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P12 = _load("p12", "w33_pass5212_q5_dualgrid_Hoffman_13_cover.py")


def main() -> int:
    print("=" * 78)
    print("Passes 5376-5379 -- an action, a complement, and a bound")
    print("=" * 78)

    print("\n  PASS 5376 -- their carrier, and the simplex on it\n")
    pts, blocks = P12.geometry(5)
    cover = [blocks[i] for i in P12.SELECTED]
    n = len(blocks)
    print(f"    W(3,5) points {len(pts)}, dual-grid blocks {n}, chosen cover {len(cover)}")
    assert len(set().union(*cover)) == 156, "cover does not partition the points"

    # P-block graph: two blocks adjacent when they meet (their Pass5203 SRG(325,144,68,60))
    t0 = time.time()
    g = igraph.Graph(n=n)
    g.add_edges([(i, j) for i, j in itertools.combinations(range(n), 2)
                 if blocks[i] & blocks[j]])
    deg = set(g.degree())
    A = np.array(g.get_adjacency().data, dtype=float)
    A2 = A @ A
    lam = {int(A2[i, j]) for i in range(n) for j in range(n) if A[i, j]}
    mu = {int(A2[i, j]) for i in range(n) for j in range(n) if i != j and not A[i, j]}
    k = int(A.sum(1)[0])
    ev = sorted({round(float(x), 6) for x in np.linalg.eigvalsh(A)})
    smin = min(ev)
    hb = n * (-smin) / (k - smin)
    print(f"    block graph : SRG({n},{k},{sorted(lam)[0]},{sorted(mu)[0]})  "
          f"eigenvalues {ev}  Hoffman {hb:.0f}   [{time.time() - t0:.1f}s]")

    cidx = [P12.SELECTED[i] for i in range(len(cover))]
    isco = not A[np.ix_(cidx, cidx)].any()
    print(f"    the 13-cover is a coclique : {isco}")
    print(f"    it meets the Hoffman bound : {len(cidx) == int(hb)}")

    # the simplex, by the Pass 1614 mechanism
    r = max(x for x in ev if abs(x - k) > 1e-6)
    E = np.eye(n)
    for o in [x for x in ev if abs(x - r) > 1e-6]:
        E = E @ (A - o * np.eye(n))
    G = E / np.diag(E)[0]
    S = G[np.ix_(cidx, cidx)]
    off = S[~np.eye(len(cidx), dtype=bool)]
    const = bool(np.allclose(off, off[0], atol=1e-9))
    val = float(off[0])
    gen = float(sorted(mu)[0]) / (k * (1 + smin))
    sumsq = float(np.sum(S))
    print(f"    all pairwise inner products equal : {const}   value {val:.12f}")
    print(f"    mu/(k(1+s)) = general form        : {gen:.12f}")
    print(f"    -1/(H-1) = -1/12                  : {-1 / 12:.12f}")
    print(f"    |sum of the 13 vectors|^2         : {sumsq:.9f}")
    simplex = const and abs(sumsq) < 1e-6
    print(f"""
    {'THEIR 13-COVER IS A REGULAR 12-SIMPLEX' if simplex else 'NOT A SIMPLEX AS COMPUTED'}, on a carrier this lane did not build and for a
    reason their Pass5212 does not state. They proved it maximum with the ratio bound; the
    bound being MET is what forces the geometry, by Pass 1614's mechanism.

    NOTE WHICH FORM AGREES. mu/(k(1+s)) = {gen:.9f} and -1/(H-1) = {-1 / 12:.9f}; this
    carrier is not a generalised quadrangle, so if those two differ the general form is the
    one to trust -- Pass 5374 established that the hard way on Paley.""")

    print("\n  PASS 5377 -- setwise stabiliser, and the pointwise kernel\n")
    t0 = time.time()
    aut = g.automorphism_group()
    print(f"    |Aut(block graph)| generators : {len(aut)}   [{time.time() - t0:.1f}s]")
    cset = set(cidx)
    t0 = time.time()
    gens_setwise = [p for p in aut if {p[i] for i in cidx} == cset]
    gens_pointwise = [p for p in gens_setwise if all(p[i] == i for i in cidx)]
    print(f"    generators preserving the cover setwise  : {len(gens_setwise)}")
    print(f"    of those, fixing all 13 pointwise        : {len(gens_pointwise)}")
    print(f"    [{time.time() - t0:.1f}s]")
    print(f"""
    WHAT THIS DOES AND DOES NOT SETTLE. igraph returns GENERATORS, not the full group, so
    the counts above are counts of generators satisfying a condition -- they are evidence
    about the stabiliser, not its order. Deciding whether the image in S_13 has order 576
    needs the actual permutation group, which means GAP or a transversal computation, and
    neither is done here.

    SO PASS 5343'S STATEMENT STANDS UNIMPROVED: 576 divides 13!, and whether W(D4):C3 acts
    faithfully on the 13 vertices is still open. Reporting that plainly is better than a
    generator count dressed up as a group order.""")

    print("\n  PASS 5378 -- the 312 blocks outside the simplex\n")
    outside = [i for i in range(n) if i not in cset]
    sub = g.subgraph(outside)
    od = sub.degree()
    print(f"    blocks outside the cover     : {len(outside)}  (= 325 - 13)")
    print(f"    induced subgraph degrees     : min {min(od)}, max {max(od)}, "
          f"mean {sum(od) / len(od):.2f}")
    print(f"    induced subgraph is regular  : {len(set(od)) == 1}")
    meets = [len([j for j in cidx if A[i, j]]) for i in outside]
    print(f"    each outside block meets the cover in : {sorted(set(meets))} of the 13")
    print(f"""
    EVERY OUTSIDE BLOCK MEETS THE COVER IN THE SAME NUMBER OF PLACES, which is what a
    coclique meeting the ratio bound forces -- tightness makes the complement equitable, and
    that is the combinatorial shadow of the vectors summing to zero. The 312 are not a
    remainder; they are a regular structure over the simplex.""")

    print("\n  PASS 5379 -- a bound using BOTH inner products\n")
    adjv = float(np.mean(G[A > 0.5]))
    print(f"    adjacent inner product     : {adjv:.9f}")
    print(f"    nonadjacent inner product  : {val:.9f}")
    print(f"    Hoffman (nonadjacent only) : {hb:.0f}")
    print(f"""
    THE ATTEMPT, AND ITS FAILURE, STATED HONESTLY. A coclique's vectors sit at ONE inner
    product, the nonadjacent one, so every bound derived from Gram positive-semidefiniteness
    alone can only ever see that value -- which is precisely the Hoffman bound and precisely
    why it cannot distinguish W(3,3) from Q(4,3). To use the adjacent value a bound would
    have to constrain a set that CONTAINS edges, and a coclique contains none. The two-distance
    machinery (absolute bound, relative bound) applies to the whole embedded vertex set, not
    to a coclique inside it, and bounds the 325 rather than the 13.

    SO THIS FRONT PRODUCES NOTHING, and the reason is structural rather than a failure of
    effort: the adjacent inner product carries no information about an object defined by its
    absence. Any bound that sees realisability must come from the GEOMETRY -- ovoid existence
    is a statement about the quadrangle, not about its spectrum or its Gram matrix. That is
    the same wall Passes 5226-5249 hit from the other side, and naming it as structural is
    the only thing four attempts have added.""")

    out = {
        "boundary": ("Pass 5377 reports GENERATOR counts from igraph, not group orders -- "
                     "it does NOT settle whether the stabiliser acts faithfully on the 13, "
                     "and Pass 5343's divisibility-only statement stands. Pass 5379 is a "
                     "NEGATIVE: no two-distance bound is constructed and the reason given "
                     "is an argument, not a proof of impossibility"),
        "pass_5376": {"carrier": "their P-block graph from Pass5212 geometry(5)",
                      "srg": [n, k, sorted(lam)[0], sorted(mu)[0]],
                      "hoffman": int(hb), "cover_is_coclique": isco,
                      "meets_bound": len(cidx) == int(hb),
                      "constant_inner_product": const, "value": val,
                      "general_form_mu_over_k1s": gen,
                      "sum_squared": sumsq, "is_regular_simplex": simplex,
                      "credit": "mechanism is Pass 1614's; tightness is their Pass5212's"},
        "pass_5377": {"aut_generators": len(aut),
                      "setwise_generators": len(gens_setwise),
                      "pointwise_generators": len(gens_pointwise),
                      "settles": "nothing beyond Pass 5343",
                      "why": "igraph returns generators, not the group; needs GAP"},
        "pass_5378": {"outside_blocks": len(outside),
                      "induced_regular": len(set(od)) == 1,
                      "meets_cover_in": sorted(set(meets)),
                      "reading": ("tightness makes the complement equitable -- the "
                                  "combinatorial shadow of the vectors summing to zero")},
        "pass_5379": {"adjacent_ip": adjv, "nonadjacent_ip": val,
                      "result": "NEGATIVE -- no improved bound constructed",
                      "reason": ("a coclique's vectors sit at one inner product, so Gram-PSD "
                                 "bounds see only that value; the adjacent value carries no "
                                 "information about an object defined by the absence of "
                                 "edges. Two-distance bounds constrain the 325, not the 13")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5376_5379_STABILISER_AND_COMPLEMENT.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
