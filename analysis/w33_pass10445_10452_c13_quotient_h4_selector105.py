#!/usr/bin/env python3
"""Pass10445-10452 outside-box: a canonical 105-state selector from the C13 quotient of H(4).

Canonical V2 projectivizes to the split Cayley hexagon H(4), with 1365 points and 1365
lines, 5 incident lines/point and 5 points/line.  Fix the internal order-13 clock C13<G2(4).
It acts fixed-point-freely on H(4) points (Pass10405/10413).

It is also fixed-point-free on lines: if a nontrivial element of order 13 stabilized a line
setwise, its induced permutation on that five-point line would have order dividing both 13
and 5!, hence would be trivial; it would fix all five points, contradiction.  Hence flags are
free as well.

Therefore the Levi/incidence graph quotient by C13 is a canonical connected 13-fold regular
cover quotient with

  1365/13 = 105 point-orbits,
  1365/13 = 105 line-orbits,
  6825/13 = 525 flag/edge-orbits.

As a quotient multigraph it is bipartite and 5-regular on both sides counting incidence
multiplicity.  The normalizer N_G2(C13)=C13:C6 induces a canonical C6 action on the quotient;
in G2(4):2 the normalizer C13:C12 gives the full C12 clock.

A topological count worth freezing (but not overinterpreting): the connected H(4) Levi graph
has cycle rank 6825-2730+1=4096=|V2|.  The C13 quotient has cycle rank
525-210+1=316=315+1, where 315 is the number of nonzero-vector C13 cycles before F4
projectivization.  These are exact identities, not an asserted vector-space isomorphism.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10445_10452_C13_QUOTIENT_H4_SELECTOR105.json'
def main():
    q=4;pts=(q+1)*(q**4+q**2+1);lines=pts;flags=pts*(q+1)
    assert (pts,lines,flags)==(1365,1365,6825)
    assert math.gcd(13,math.factorial(5))==1
    qp,ql,qf=pts//13,lines//13,flags//13
    assert (qp,ql,qf)==(105,105,525)
    beta=flags-(pts+lines)+1;assert beta==4096==4**6
    qbeta=qf-(qp+ql)+1;assert qbeta==316 and qbeta-1==315
    assert qf==qp*5==ql*5
    out={
      'schema':'w33.pass10445_10452.c13_quotient_h4_selector105.v1','status':'PASS','passes':'10445-10452','outside_box':True,
      'H4_Levi_graph':{'points':pts,'lines':lines,'vertices':pts+lines,'flags_edges':flags,'biregular_degree':5,'connected':True,'cycle_rank':beta},
      'C13_freeness':{'points':'fixed-point-free by irreducible natural-module action','lines':'fixed-point-free because an order-13 permutation of a 5-point line must be trivial, which would fix points','flags':'fixed-point-free because a fixed flag fixes its point'},
      'quotient_selector':{'point_states':qp,'line_states':ql,'flag_orbits':qf,'total_vertices':qp+ql,'bipartite_degree_counting_multiplicity':5,'cycle_rank':qbeta,'cover_degree':13},
      'normalizer_clock':{'inside_G2_4':'N(C13)=C13:C6 -> C6 on quotient','inside_G2_4_colon_2':'N(C13)=C13:C12 -> C12 on quotient'},
      'identities':{'V2_cardinality':4096,'H4_Levi_cycle_rank':4096,'nonzero_vector_C13_cycles':315,'quotient_Levi_cycle_rank_minus_one':315},
      'theorem':'The internal C13 clock canonically produces a 105-state projective selector by quotienting the full H(4) incidence geometry: 105 point-orbits, 105 line-orbits and 525 flag-orbits. The quotient is a connected bipartite 5-regular incidence multigraph and inherits the torus-normalizer C6 (or outer C12) clock.',
      'boundary':'The quotient counts/freeness and cycle ranks are exact. Parallel edges in the orbit quotient are not excluded here, so the safe object is an incidence multigraph/graph quotient. The equalities beta1(H4)=4096=|V2| and beta1(quotient)-1=315 are recorded as exact numerical/topological identities; no canonical isomorphism between graph homology and V2 is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','selector105':[qp,ql,qf],'beta':[beta,qbeta],'clock':'C6/C12'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
