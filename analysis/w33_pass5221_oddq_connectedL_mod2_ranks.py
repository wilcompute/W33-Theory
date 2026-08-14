#!/usr/bin/env python3
"""Pass5221 (bonkers): exact GF(2) adjacency ranks of connected odd-q L graphs.

Pass5216 diagonalizes the q=3,5 connected L/opposite-line chart graphs over
characteristic zero.  This pass computes the binary ranks directly, rather than
reducing real eigenvalue multiplicities (which is invalid in modular
representation theory).  Rows are stored as Python integers and eliminated over
F2 exactly.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5221_ODDQ_CONNECTEDL_MOD2_RANKS.json'

def graph_rows(q,plus_I=False):
    G=build_W(q);L=[loc for t,loc in G['charts'] if t=='L'];own=[[] for _ in G['apartments']]
    for i,loc in enumerate(L):
        for a in loc.values():own[a].append(i)
    assert set(map(len,own))=={2}
    rows=[0]*len(L)
    for u,v in own:rows[u]|=1<<v;rows[v]|=1<<u
    if plus_I:
        for i in range(len(rows)):rows[i]^=1<<i
    return rows

def rank2(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def anchor(q):
    A=graph_rows(q,False);n=len(A);deg=A[0].bit_count();assert {x.bit_count() for x in A}=={deg}
    rA=rank2(A);rI=rank2([x^(1<<i) for i,x in enumerate(A)])
    return {'q':q,'vertices':n,'degree':deg,
      'rank_F2_A':rA,'nullity_F2_A':n-rA,
      'rank_F2_A_plus_I':rI,'nullity_F2_A_plus_I':n-rI,
      'kernel_intersection_dimension':0}

def main():
    A={'3':anchor(3),'5':anchor(5)}
    assert A['3']=={'q':3,'vertices':540,'degree':6,'rank_F2_A':440,'nullity_F2_A':100,
      'rank_F2_A_plus_I':360,'nullity_F2_A_plus_I':180,'kernel_intersection_dimension':0}
    assert A['5']=={'q':5,'vertices':9750,'degree':15,'rank_F2_A':7074,'nullity_F2_A':2676,
      'rank_F2_A_plus_I':6891,'nullity_F2_A_plus_I':2859,'kernel_intersection_dimension':0}
    out={'pass':5221,'status':'THEOREM_EXACT_CONNECTEDL_MOD2_RANKS_Q3_Q5',
      'definition':'A is the adjacency matrix of the connected L/opposite-line chart graph, with one edge per apartment.',
      'anchors':A,
      'direct_method':'Exact GF(2) row reduction on the binary adjacency rows; no inference from the characteristic-zero spectrum.',
      'modular_firewall':'The large kernels show that the characteristic-zero decomposition in Pass5216 is not semisimple after reduction mod2. Binary L-side equality/residual arguments must work with the actual modular modules, not parity-reduced real eigenvalue multiplicities.',
      'q5_targets':'ker(A_L) has dimension2676 and ker(A_L+I) dimension2859 inside F2^9750. These are concrete connected-L binary modules available for projecting or stratifying residual/equality-shell constraints.',
      'boundary':'Exact finite q3/q5 modular-rank theorem. No all-odd-q rank formula or direct q5 distance consequence is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
