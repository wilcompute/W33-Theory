#!/usr/bin/env python3
"""Pass5206: exact leader-36 diagnostic for the first full-cut aggregation.

Pass5185 proves full cut-coset minimality.  At q=5 a selected-degree d vertex
with k host neighbours of selected degree three and s selected edges to those
neighbours satisfies k<=2s+3-d.  Combining this with d_Y<=3 gives an upper
bound on the sum of selected degrees across the six host neighbours:

  d=1: <=16,  d=2: <=17,  d=3: <=15.

Hence one bipartition side with degree counts (n1,n2,n3) contributes at most

  x^T N y <= 16 n1 + 34 n2 + 45 n3.

The same bound holds from the opposite side; minimize the two side caps and
maximize over every bipartition split compatible with 36 selected edges.  This
is the strongest consequence obtainable from this degree-class aggregation of
the Pass5185 pair/star rules.

For all eleven Pass5205 critical profiles, the resulting N2 upper bounds are
381..405, whereas the Delsarte extremizers use N2=164..175.  Therefore these
small-shore/full-cut degree-class consequences are completely redundant at the
leader-36 wall.  Any successful full-cut attack must retain correlated host
incidences on larger shores (or use an independent quotient constraint).
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5206_Q5_LEADER36_FULLCUT_DEGREECLASS_DIAGNOSTIC.json'

CRIT={
54:((18,0,18),164),55:((16,1,18),165),56:((14,2,18),166),
57:((15,0,19),167),58:((13,1,19),168),59:((11,2,19),169),
60:((12,0,20),171),61:((10,1,20),172),62:((8,2,20),173),
63:((9,0,21),174),64:((7,1,21),175)}

def side_cap(p): return 16*p[0]+34*p[1]+45*p[2]

def splits(total,m=36):
    n1,n2,n3=total;out=[]
    for a1 in range(n1+1):
      for a2 in range(n2+1):
       for a3 in range(n3+1):
        if a1+2*a2+3*a3!=m:continue
        b=(n1-a1,n2-a2,n3-a3)
        if b[0]+2*b[1]+3*b[2]==m:out.append(((a1,a2,a3),b))
    return out

def main():
    rows={}
    for W,(p,delsarte_n2) in CRIT.items():
        ss=splits(p);assert ss
        best=max(min(side_cap(a),side_cap(b)) for a,b in ss)
        n2cap=best-(36+2*W) # Pass5172: N2=x^TNy-(m+2N1)
        rows[str(W)]={'degree_counts':list(p),'bipartition_splits':len(ss),
          'fullcut_degreeclass_xNy_upper':best,'derived_N2_upper':n2cap,
          'Pass5205_Delsarte_N2':delsarte_n2,'slack':n2cap-delsarte_n2}
        assert n2cap>delsarte_n2
    assert [rows[str(W)]['derived_N2_upper'] for W in range(54,65)]==[
      405,403,403,396,396,395,390,388,388,381,381]
    out={'pass':5206,'status':'EXACT_Q5_LEADER36_FULLCUT_DEGREECLASS_REDUNDANCY',
      'leader_size':36,'open_N1_window':[54,64],
      'Pass5185_local_consequences':{
        'degree1_neighbor_degree_sum_upper':16,
        'degree2_neighbor_degree_sum_upper':17,
        'degree3_neighbor_degree_sum_upper':15,
        'side_xNy_upper':'16 n1 + 34 n2 + 45 n3'},
      'rows':rows,
      'conclusion':'The complete degree-class aggregation of the two-vertex and 3-2-3 full-cut consequences does not tighten the Pass5205 Delsarte extremizers in any open leader-36 layer.',
      'required_next_structure':'Retain correlated host incidences on larger cut shores, or introduce an independent quotient/code constraint; another degree-profile-only refinement cannot use this information.',
      'boundary':'Diagnostic only. Pass5200 remains the strict barrier leader>=36; this pass does not close leader 36.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
