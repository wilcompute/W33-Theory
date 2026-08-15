#!/usr/bin/env python3
"""Pass5354 (bonkers): search q11 dual20 witnesses as order-10 symplectic Cayley shells.

The predicted equality-wall graph is K10,10 plus a 2-factor on each half. Since
F_11^* is cyclic of order10, test diagonal symplectic elements
  T=diag(a,b,a^-1,b^-1)
with order10. Their length-10 orbits on the 7381 q11 P-carriers are natural
candidate halves. We retain orbits whose internal intersection-2 graph is C10,
then search pairs with complete cross adjacency. Every resulting 20-set is
checked directly for binary point parity. A hit gives a constructive dual20
witness with an explicit cyclic generator, stronger than a black-box SAT hit.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
from analysis.w33_pass5304_q11_dual20_density_wall import carriers
from analysis.w33_pass5293_allodd_rank_reduction_q11 import norm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5354_Q11_CYCLIC_CAYLEY_DUAL20_SEARCH.json'
Q=11

def order(a):
    x=1
    for k in range(1,11):
        x=x*a%Q
        if x==1:return k
    raise AssertionError

def main():
    P,C=carriers(Q);pi={p:i for i,p in enumerate(P)};bk={c:i for i,c in enumerate(C)}
    bits=[]
    for B in C:
        z=0
        for p in B:z|=1<<p
        bits.append(z)
    primitive=2;assert order(primitive)==10
    tested=0;candidate_halves=0;pair_tests=0;witness=None;summary=[]
    for ei,ej in itertools.product(range(10),repeat=2):
        a=pow(primitive,ei,Q);b=pow(primitive,ej,Q)
        if math.lcm(order(a),order(b))!=10:continue
        ai=pow(a,-1,Q);bi=pow(b,-1,Q)
        def Tpt(x):return norm((a*x[0]%Q,b*x[1]%Q,ai*x[2]%Q,bi*x[3]%Q),Q)
        pp=[pi[Tpt(x)] for x in P]
        perm=[bk[tuple(sorted(pp[p] for p in B))] for B in C]
        # Require the permutation itself to have exact order10.
        x=list(range(len(C)))
        y=x[:]
        for _ in range(10):y=[perm[t] for t in y]
        if y!=x:continue
        y=x[:]
        for _ in range(5):y=[perm[t] for t in y]
        if y==x:continue
        tested+=1
        rem=set(range(len(C)));orbs=[]
        while rem:
            s=next(iter(rem));O=[];u=s
            while u not in O:
                O.append(u);rem.discard(u);u=perm[u]
            if len(O)==10:orbs.append(O)
        cyc=[]
        for O in orbs:
            # circulant internal graph: inspect offsets from O[0]
            offs=[k for k in range(1,10) if (bits[O[0]]&bits[O[k]]).bit_count()==2]
            if len(offs)!=2:continue
            if {(k%10) for k in offs}!={(-offs[0])%10,offs[0]%10}:continue
            step=min(offs[0],offs[1])
            if math.gcd(step,10)!=1:continue
            # verify all vertices degree2
            if all(sum((bits[u]&bits[v]).bit_count()==2 for v in O if v!=u)==2 for u in O):
                cyc.append(O)
        candidate_halves+=len(cyc)
        hit=None
        for ia,A in enumerate(cyc):
            A0=A[0]
            for B in cyc[ia+1:]:
                pair_tests+=1
                # T-invariance makes complete cross adjacency equivalent to A0 adjacent to all B.
                if not all((bits[A0]&bits[v]).bit_count()==2 for v in B):continue
                S=A+B
                if not all((bits[u]&bits[v]).bit_count()==2 for u in A for v in B):continue
                z=0
                for u in S:z^=bits[u]
                if z:continue
                hit=S;break
            if hit:break
        summary.append({'exponents':[ei,ej],'a':a,'b':b,'length10_orbits':len(orbs),'C10_halves':len(cyc)})
        if hit:
            witness={'exponents':[ei,ej],'diagonal':[a,b,ai,bi],'selected_carriers':hit,
                     'half_A':hit[:10],'half_B':hit[10:]}
            break
    if witness:
        S=witness['selected_carriers'];z=0
        for u in S:z^=bits[u]
        assert z==0 and len(set(S))==20
        edge=sum((bits[u]&bits[v]).bit_count()==2 for u,v in itertools.combinations(S,2));assert edge==120
        deg=[sum((bits[u]&bits[v]).bit_count()==2 for v in S if v!=u) for u in S];assert set(deg)=={12}
        out={'pass':5354,'status':'THEOREM_Q11_CYCLIC_CAYLEY_DUAL20_EQUALITY_WITNESS',
             'order10_symplectic_elements_tested':tested,'candidate_C10_halves':candidate_halves,'pair_tests':pair_tests,
             'witness':witness,'selected_graph':'K10,10 + C10 + C10','selected_edges':edge,'degree':12,
             'point_parity':'exact XOR zero','conclusion':'Constructive q11 weight20 footprint-dual word saturating the 120-edge wall.',
             'boundary':'Existence of dual20 does not itself prove primal d=121; pair-orbital moment closure is still required.'}
    else:
        out={'pass':5354,'status':'NO_CYCLIC_Q11_DUAL20_IN_TESTED_DIAGONAL_ORDER10_FAMILY',
             'order10_symplectic_elements_tested':tested,'candidate_C10_halves':candidate_halves,'pair_tests':pair_tests,
             'element_summary':summary,
             'conclusion':'No equality-wall dual20 was found with both halves C10 orbits of a tested diagonal order10 symplectic element.',
             'boundary':'Family-specific exhaustive no-go only; it does not exclude noncyclic dual20 supports or other order10 conjugacy classes.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
