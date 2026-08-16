#!/usr/bin/env python3
"""Pass5628: build the horizontal cubic action and test whether gauge symmetry kills bad9.

Pass5620 separated the E6 cubics by bundle projection:
  36 horizontal covariantly-affine lifts over AG(2,3) lines;
   9 vertical complete Z3 fibers.

Here the local gauge group acts by independent translations t -> t+s_b on each
three-state fiber.  A connection is transformed together with the fields, so the
36 horizontal supports are carried bijectively to the 36 horizontal supports of
the transformed connection.  But a vertical support {(b,0),(b,1),(b,2)} is also
setwise invariant under every local translation.  Therefore ordinary bundle gauge
invariance permits BOTH a horizontal cubic coupling g_H and a vertical on-site
coupling g_V.  It does not force g_V=0.

This is the requested field-action test, and it closes the tempting statement
"bad9 are forbidden just because they are gauge fibers" in the negative.
"""
from __future__ import annotations
import itertools,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5628_E6_GAUGE_ACTION_TWO_COUPLING_NO_GO.json'
F=range(3)

def points(): return [(x,y) for x in F for y in F]
def lines():
    L=[]
    for c in F: L.append(tuple((c,y) for y in F))
    for m in F:
        for c in F: L.append(tuple((x,(m*x+c)%3) for x in F))
    assert len(set(L))==12
    return L

def canonical_horizontal():
    H=[]
    for ell in lines():
        # deterministic line parameter is the stored order; three parallel lifts k
        # are enough for the covariance theorem. lambda=1 is a gauge choice here.
        for k in F:
            H.append(frozenset((b,(k+i)%3) for i,b in enumerate(ell)))
    assert len(H)==36 and len(set(H))==36
    return set(H)
def vertical():
    V={frozenset((b,t) for t in F) for b in points()}; assert len(V)==9; return V

def gauge_image(S,s):
    return {frozenset((b,(t+s[b])%3) for b,t in tri) for tri in S}

def main():
    H=canonical_horizontal(); V=vertical()
    assert all(len({b for b,t in tri})==3 for tri in H)
    assert all(len({b for b,t in tri})==1 for tri in V)
    # Exhausting all 3^9 gauges is unnecessary for the set-theoretic theorem, but
    # deterministic probes include basis gauges and a mixed gauge.
    probes=[]
    zero={b:0 for b in points()}; probes.append(zero)
    for b0 in points():
        for a in (1,2):
            s={b:0 for b in points()};s[b0]=a;probes.append(s)
    probes.append({b:(b[0]+2*b[1])%3 for b in points()})
    for s in probes:
        Hg=gauge_image(H,s); Vg=gauge_image(V,s)
        assert len(Hg)==36 and all(len({b for b,t in tri})==3 for tri in Hg)
        assert Vg==V
    # The two support sums are linearly independent formal cubic functionals,
    # because no monomial support occurs in both classes.
    assert H.isdisjoint(V)
    out={
      'pass':5628,'status':'GAUGE_INVARIANT_CUBIC_ACTION_HAS_INDEPENDENT_HORIZONTAL_AND_VERTICAL_COUPLINGS',
      'base':'AG(2,3)','fiber':'Z3','horizontal_supports':36,'vertical_supports':9,
      'local_gauge_group':'Z3^9 acting by t_b -> t_b+s_b, with the connection transformed covariantly',
      'horizontal_covariance':'the 36 horizontal monomials are mapped bijectively to the 36 monomials of the gauge-transformed connection',
      'vertical_invariance':'each complete fiber support {(b,0),(b,1),(b,2)} is setwise fixed by local translation at b',
      'allowed_action':'S_cubic = g_H sum_horizontal C_T + g_V sum_vertical V_b',
      'no_go':'Gauge invariance and total Z3 neutrality do not imply g_V=0. An additional principle such as horizontality/locality, an L-infinity/Jacobi constraint, representation theory, or dynamics is required to suppress the vertical nine.',
      'physics_boundary':'This is a discrete bundle action/covariance theorem. It does not identify either coupling with a measured Yukawa coupling.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
