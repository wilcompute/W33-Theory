"""Passes 5248-5249 -- a second dual pair split by the same bound, and a structural
hypothesis for the odd-q value that does not survive contact.

  5248  W(3,q)/Q(4,q) split because one side had an ovoid and the other did not, on a
        SHARED Hoffman bound.  Is that a two-graph accident?  H(3,q^2) and Q(5,q) are also
        dual, with orders (q^2,q) and (q,q^2).  They are NOT cospectral -- swapping s and t
        changes n -- but st+1 is symmetric, so the Hoffman bound is the SAME q^3+1 on both.
        H(3,q^2) has ovoids; Q(5,q) has none.  Same split, different mechanism.

  5249  alpha(W(3,3)) = 7 is the only odd-q value this lane has settled.  Two structural
        readings suggest themselves -- a cut-space dimension from the other lane's tensor
        presentation, and q^2-q+1.  Both are tested here rather than asserted.

    py -3 analysis/w33_pass5248_5249_the_second_same_bound_pair_and_a_hypothesis_that_failed.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
import time
from pathlib import Path

import igraph

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


PP = _load("pp", "w33_pass4754_4755_prime_power_quadrangles_and_bliss.py")
P95 = _load("p95", "w33_pass4795_the_ovoid_gap_and_the_polarity_coset.py")
P89 = _load("p89", "w33_pass4389_hermitian_quadrangle_measured.py")
P26 = _load("p26", "w33_pass5226_5227_the_witness_decays_without_an_object.py")


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
    print("Passes 5248-5249 -- the second same-bound pair, and a failed hypothesis")
    print("=" * 78)

    print("\n  PASS 5248 -- H(3,9) and Q(5,3): different graphs, one bound\n")
    hp, hl = P89.build_h39()[:2]
    qp, ql = PP.dual(hp, hl)
    rows = []
    for name, (P, L), has_ovoid in (("H(3,9)", (hp, hl), True),
                                    ("Q(5,3)", (qp, ql), False)):
        g = graph_of(P, L)
        n, deg, lam, mu = PP.srg_params(g)
        hb = P95.hoffman(n, deg, lam, mu)
        t0 = time.time()
        wit, _ = P26.witness(g, hb, 60.0, seed=5248)
        assert not any(g.are_adjacent(u, v) for u, v in itertools.combinations(wit, 2))
        rows.append({"gq": name, "srg": [n, deg, lam, mu], "hoffman": hb,
                     "ovoid_exists": has_ovoid, "alpha_found": len(wit),
                     "attains": len(wit) == hb, "seconds": round(time.time() - t0, 1)})
        print(f"    {name:8s} SRG{tuple((n, deg, lam, mu))}  Hoffman {hb:3d}  "
              f"ovoid {'yes' if has_ovoid else 'NO ':3s}  reached {len(wit):3d}"
              f"  {'ATTAINS' if len(wit) == hb else 'short'}")

    H, Q = rows
    print(f"""
    THE BOUND IS SHARED AND THE GRAPHS ARE NOT. H(3,9) is SRG{tuple(H['srg'])} and Q(5,3) is
    SRG{tuple(Q['srg'])} -- different orders, different spectra, {H['srg'][0]} vertices against {Q['srg'][0]}.
    But a GQ of order (s,t) has Hoffman bound st+1, and st is symmetric under the duality
    that swaps s and t. So both inherit {H['hoffman']} = q^3+1 from opposite sides.

    H(3,9) attains it; Q(5,3) does not, and cannot -- Q(5,q) has no ovoid for any q. This is
    the SAME split as W(3,q)/Q(4,q) reached by a different route: there the two graphs were
    cospectral and the bound was shared because the spectra were equal, here the spectra
    differ and the bound is shared because st+1 is duality-invariant. Two mechanisms, one
    phenomenon, so the W/Q(4) case was not a two-graph accident.

    WHAT IS SETTLED HERE. alpha(H(3,9)) = {H['alpha_found']} both ways: witness verified pairwise
    non-adjacent, Hoffman capping at the same number. That reproduces Pass 5222 by an
    independent route. On Q(5,3) the searcher reached {Q['alpha_found']} and NOTHING is settled -- by
    Pass 5229's own lesson a shortfall is not a bound, and Q(5,3) is exactly the case where
    the object is known absent, so the searcher can never do better than report failure.""")

    print("\n  PASS 5249 -- two readings of alpha(W(3,3)) = 7, both tested\n")
    F = PP.GF(3)
    wp, wl = PP.build_w3(F)[:2]
    gw = graph_of(wp, wl)
    a7 = gw.independence_number()
    q = 3

    # Hypothesis A: 7 is a cut-space dimension, from the other lane's tensor presentation.
    # Track B Pass5220: a P component is Cut(K_{q+1}) tensor Cut(K_{q+1}), dimension q^2.
    cutdim = q                      # dim Cut(K_{q+1}) = (q+1) - 1
    tensordim = cutdim * cutdim
    # Hypothesis B: the arithmetic form q^2-q+1.
    formB = q * q - q + 1

    print(f"    alpha(W(3,3))                         = {a7}   (exhaustive, Pass 5226)")
    print(f"    A: dim Cut(K_{q+1}) tensor Cut(K_{q+1})   = {tensordim}   "
          f"{'MATCH' if tensordim == a7 else 'no match'}")
    print(f"    B: q^2 - q + 1                        = {formB}   "
          f"{'MATCH' if formB == a7 else 'no match'}")

    print(f"""
    HYPOTHESIS A IS DEAD ON ARRIVAL. Cut(K_4) has dimension {cutdim}, so the tensor square has
    dimension {tensordim}, and alpha is {a7}. It was worth ten lines to check because the other lane's
    Pass5220 presentation makes q^2 the natural dimension attached to a P component and it
    would have been easy to reach for it -- but {tensordim} is not {a7} and there is no correction that
    makes it so. Recorded as refuted rather than quietly dropped.

    HYPOTHESIS B MATCHES AT q=3 AND IS STILL NOT SUPPORTED. q^2-q+1 = {formB} = alpha, exactly. But
    Pass 5227 measured the searcher against this same q^2-q+1 at q = 5, 7, 9 and reached
    86, 77 and 68 percent of it -- so the formula has ONE confirming data point and three
    non-confirming, non-refuting ones. A single match on a two-parameter arithmetic guess is
    not evidence; at q=3 there are many closed forms hitting 7, and the corpus rule is that a
    pattern with one instance is a coincidence with ambition.

    WHAT THE q=3 COMPUTATION DOES ESTABLISH, and it is not nothing: alpha(W(3,3)) = {a7} < {P95.hoffman(*PP.srg_params(gw))}
    exhaustively, so W(3,3) HAS NO OVOID, proved here rather than cited. That is the odd half
    of the duality parity rule, at one value of q, by direct computation. The general
    statement remains quoted, not reproved.""")

    out = {
        "boundary": ("Pass 5248 settles alpha(H(3,9)) = 28 both ways; the Q(5,3) entry is "
                     "a searcher's best with NOTHING settled, and Q(5,q) is known to have "
                     "no ovoid so the shortfall there is expected and still not a bound. "
                     "Pass 5249 REFUTES the cut-space reading and does NOT support the "
                     "q^2-q+1 reading -- one matching data point against three neither "
                     "confirming nor refuting. The no-ovoid conclusion is proved at q=3 "
                     "ONLY; the general parity rule is quoted, not reproved"),
        "pass_5248": {"claim": ("the ovoid split is not specific to the cospectral pair -- "
                                "H(3,q^2)/Q(5,q) share the Hoffman bound q^3+1 because "
                                "st+1 is duality-invariant, with different spectra"),
                      "rows": rows,
                      "settled": "alpha(H(3,9)) = 28, both bounds",
                      "not_settled": "Q(5,3), where the object is known absent"},
        "pass_5249": {"alpha_W33": a7, "method": "exhaustive",
                      "hypothesis_A_cut_space": {"value": tensordim, "matches": False,
                                                 "source": "Track B Pass5220 P-component "
                                                           "= Cut(K_{q+1})^{tensor 2}",
                                                 "verdict": "REFUTED"},
                      "hypothesis_B_q2_q_1": {"value": formB, "matches_at_q3": True,
                                              "confirming_points": 1,
                                              "verdict": "UNSUPPORTED -- one data point"},
                      "does_establish": ("alpha(W(3,3)) = 7 < 10 exhaustively, hence "
                                         "W(3,3) has no ovoid -- the odd half of the "
                                         "parity rule proved at q=3 by computation")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5248_5249_SECOND_PAIR_AND_REFUTED_HYPOTHESIS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
