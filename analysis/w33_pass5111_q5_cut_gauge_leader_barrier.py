#!/usr/bin/env python3
"""Pass5111: q=5 cut-gauge + girth-8 pair bound.

By Pass5110 a minimum chamber-generator representative is a cut-minimal edge set
in the 6-regular W(3,5) Levi graph.  Toggling a vertex star cannot reduce its
size, so every selected-subgraph degree is <=3.  The Levi graph has girth 8.
For a subcubic girth-8 graph with at most 13 edges, the maximum number of
adjacent edge pairs (wedges) is bounded by the connected tree extremum; possible
8-cycle and 12-edge theta cores do not exceed it.  Combined with the exact
chamber-star pair intersections q^3 for gallery distance 1 and <=q^2 otherwise,
this yields an explicit low-leader weight barrier.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5111_Q5_CUT_GAUGE_LEADER_BARRIER.json'

def tree_bound(e):
    if e<=0:return 0
    return e+(e-1)//2-1

def connected_bound(e):
    # Tree.  If beta=1, girth>=8 gives an 8-cycle core and each added tree edge
    # increases wedge count by at most 2.  If beta=2 and e<=13, the only possible
    # subcubic core is a theta graph; girth>=8 forces three paths of length >=4,
    # so the 12-edge base has 15 wedges and one extra edge raises this by <=2.
    vals=[tree_bound(e)]
    if e>=8:vals.append(2*e-8)
    if e>=12:vals.append(15+2*(e-12))
    return max(vals)

def global_bound(m):
    # Additive over components; dynamic programming over edge partitions.
    dp=[0]+[-10**9]*m
    for s in range(1,m+1):
        dp[s]=connected_bound(s)
        for k in range(1,s):dp[s]=max(dp[s],dp[s-k]+connected_bound(k))
    return dp[m]

def weight_lb(m,wedge,q=5):
    pairs=math.comb(m,2)
    # pair intersections: adjacent chambers q^3; every other pair <=q^2.
    return m*q**4-2*(wedge*q**3+(pairs-wedge)*q**2)

def main():
    table={}
    for m in range(1,14):
        w=global_bound(m);lb=weight_lb(m,w)
        table[str(m)]={'max_adjacent_pairs':w,'weight_lower_bound':lb}
        assert lb>=5**4
    assert [table[str(m)]['max_adjacent_pairs'] for m in range(6,14)]==[7,9,10,12,13,15,16,18]
    assert [table[str(m)]['weight_lower_bound'] for m in range(6,14)]==[1600,1525,1600,1425,1400,1125,1000,625]
    out={'pass':5111,'status':'THEOREM_Q5_COUNTEREXAMPLE_LEADER_AT_LEAST_14',
         'q':5,'target_distance':625,'cut_minimal_degree_cap':3,'levi_girth':8,
         'table':table,
         'conclusion':'Every cut-minimal chamber-generator representative of size <=13 produces apartment weight >=625. Therefore any word of weight <625 would have minimum chamber-generator leader >=14.',
         'with_pass5102':'Pass5102 gave leader>=6 plus a heavy K6 chart; this pass strengthens the leader wall to >=14. The heavy-chart condition remains simultaneously necessary.',
         'boundary':'This does not exclude leaders >=14, so q=5 distance 625 remains open. At m=13 the lower bound is exactly 625; equality-shell classification is not claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
