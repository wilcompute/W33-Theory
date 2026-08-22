#!/usr/bin/env python3
"""Pass7185: the 27 ten-D4 spreads are atlases of 40 unimodular E8 charts.

A spread contains ten selected D4 subsystems, grouped into five orthogonal pairs.
The 40 pairs drawn from different orthogonal pairs have W33 relation (0,4), and
Pass7182 showed each such pair generates the full E8 root lattice with index 1.
This pass turns that statement into explicit GL(8,Z) chart matrices and checks
the transition groupoid.  The raw coordinate-change groupoid is flat: any
closed product telescopes to I.  Thus a nontrivial integral holonomy would need
extra frame identifications, not ordinary lattice basis changes.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import sympy as sp
import w33_pass7163_7170_e8_hexagonal_lift as b
import w33_pass7182_d4_glue_spread_code as d

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7185_E8_D4_CHART_ATLAS.json'

def main():
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers();Q,partner=d.cqs(adj);P=d.pairs(partner)
    support=[frozenset(Q[i]|Q[j]) for i,j in P];packs=[]
    for C in itertools.combinations(range(45),5):
        U=set();ok=True
        for z in C:
            if U&support[z]:ok=False;break
            U|=support[z]
        if ok and len(U)==40:packs.append(C)
    assert len(packs)==27
    bases=[d.simple(q,R,fib) for q in Q];BE=sp.Matrix(b.SIMPLES);BEi=BE.inv();detE=abs(int(BE.det()));assert detE==256
    cross4=[];chart={};det_sign=Counter();max_entry=Counter()
    for a,c in itertools.combinations(range(90),2):
        if d.relation(Q,adj,a,c)!=(0,4):continue
        M=sp.Matrix([R[v] for v in bases[a]+bases[c]]);assert M.rank()==8 and abs(int(M.det()))==detE
        X=sp.simplify(M*BEi)
        assert all(x.q==1 for x in X)
        Xi=sp.Matrix([[int(x) for x in X.row(i)] for i in range(8)])
        assert abs(int(Xi.det()))==1
        key=tuple(int(x) for x in Xi);chart[(a,c)]=Xi;cross4.append((a,c));det_sign[int(Xi.det())]+=1
        max_entry[max(abs(int(x)) for x in Xi)]+=1
    assert len(cross4)==1080 and len(set(tuple(int(x) for x in chart[p]) for p in cross4))==1080
    # The 27 spreads partition the 1080 cross4 pairs, 40 per spread.
    seen=Counter();transition_max=Counter();spread_data=[]
    for C in packs:
        ten=[]
        for z in C:ten.extend(P[z])
        pairs40=[]
        for a,c in itertools.combinations(sorted(ten),2):
            if d.relation(Q,adj,a,c)==(0,4):pairs40.append((a,c));seen[(a,c)]+=1
        assert len(pairs40)==40
        X0=chart[pairs40[0]];X0i=X0.inv();local=[]
        for p in pairs40:
            T=sp.simplify(chart[p]*X0i);assert all(x.q==1 for x in T)
            Ti=sp.Matrix([[int(x) for x in T.row(i)] for i in range(8)]);assert abs(int(Ti.det()))==1
            local.append(Ti);transition_max[max(abs(int(x)) for x in Ti)]+=1
        # Exact path law: T(j<-i)=X_j X_i^-1, so T(k<-j)T(j<-i)=T(k<-i).
        # Check it on every ordered triple of a fixed 4-chart generating sample per spread.
        sample=range(min(4,len(local)))
        for i,j,k in itertools.product(sample,repeat=3):
            Tij=sp.simplify(local[j]*local[i].inv());Tjk=sp.simplify(local[k]*local[j].inv());Tik=sp.simplify(local[k]*local[i].inv())
            assert Tjk*Tij==Tik
        spread_data.append({'orthogonal_pair_supports':list(C),'unimodular_cross_charts':40})
    assert set(seen)==set(cross4) and set(seen.values())=={1}
    out={
      'schema':'w33.pass7185.e8_d4_chart_atlas.v1','status':'PASS',
      'selected_D4':90,'orthogonal_D4_pairs':45,'ten_D4_spreads':27,
      'cross4_D4_pairs':1080,'cross4_pairs_per_spread':40,'cross4_pair_spread_multiplicity':1,
      'theorem':'Every W33 relation-(0,4) selected-D4 pair gives an explicit unimodular E8 root-lattice basis. The 1080 such charts are partitioned by the 27 ten-D4 spreads into 40 charts each.',
      'chart_coordinate_basis':'rows are the two deterministic D4 simple-root bases, expressed relative to the fixed E8 simple-root basis; every 8x8 coordinate matrix lies in GL(8,Z)',
      'chart_determinant_sign_histogram':{str(k):v for k,v in sorted(det_sign.items())},
      'chart_max_abs_entry_histogram':{str(k):v for k,v in sorted(max_entry.items())},
      'transition_max_abs_entry_histogram':{str(k):v for k,v in sorted(transition_max.items())},
      'transition_groupoid':'T(j<-i)=X_j X_i^{-1}; exact composition T(k<-j)T(j<-i)=T(k<-i)',
      'closed_path_holonomy':'identity for ordinary coordinate transitions (flat/telescoping)',
      'holonomy_firewall':'A nontrivial GL(8,Z) or triality holonomy cannot come from honest basis changes alone; it requires additional quotient/frame identifications. This pass rejects the naive transition-holonomy interpretation rather than manufacturing one.',
      'index4_charts':'The five orthogonal D4+D4 pairs per spread remain index-4 sublattices with diagonal (Z2)^2 glue from Pass7182; they are not unimodular charts before gluing.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','charts':1080,'spreads':27,'flat':True}))
if __name__=='__main__':main()
