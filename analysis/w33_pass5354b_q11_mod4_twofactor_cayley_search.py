#!/usr/bin/env python3
"""Pass5354b: correct the q11 cyclic shell target using the q mod 4 two-factor pattern.

Known equality-wall dual supports:
 q=5: C4 | C4,
 q=7: C6 | (C3+C3),
 q=9: C8 | C8.
Thus the congruence pattern predicts q=11 (3 mod4) should use
 C10 | (C5+C5), not C10 | C10.

As in Pass5354, enumerate diagonal order-10 symplectic elements
T=diag(a,b,a^-1,b^-1), classify every length-10 carrier orbit whose internal
intersection-2 graph has degree2. An offset step coprime to10 gives C10; step of
gcd2 gives two C5 cycles. Search cross-type pairs for complete cross adjacency
and exact XOR-zero parity. A hit is a constructive dual20 equality-wall witness.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
from analysis.w33_pass5304_q11_dual20_density_wall import carriers
from analysis.w33_pass5293_allodd_rank_reduction_q11 import norm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5354B_Q11_MOD4_TWOFACTOR_CAYLEY_SEARCH.json'
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
    tested=pair_tests=0;counts={'C10':0,'2C5':0};witness=None;summary=[]
    for ei,ej in itertools.product(range(10),repeat=2):
        a=pow(primitive,ei,Q);b=pow(primitive,ej,Q)
        if math.lcm(order(a),order(b))!=10:continue
        ai=pow(a,-1,Q);bi=pow(b,-1,Q)
        def Tpt(x):return norm((a*x[0]%Q,b*x[1]%Q,ai*x[2]%Q,bi*x[3]%Q),Q)
        pp=[pi[Tpt(x)] for x in P]
        perm=[bk[tuple(sorted(pp[p] for p in B))] for B in C]
        y=list(range(len(C)))
        for _ in range(10):y=[perm[t] for t in y]
        if y!=list(range(len(C))):continue
        y=list(range(len(C)))
        for _ in range(5):y=[perm[t] for t in y]
        if y==list(range(len(C))):continue
        tested+=1
        rem=set(range(len(C)));orbs=[]
        while rem:
            s=next(iter(rem));O=[];u=s
            while u not in O:
                O.append(u);rem.discard(u);u=perm[u]
            if len(O)==10:orbs.append(O)
        typ={'C10':[],'2C5':[]}
        for O in orbs:
            offs=[k for k in range(1,10) if (bits[O[0]]&bits[O[k]]).bit_count()==2]
            if len(offs)!=2 or offs[1]!=(10-offs[0])%10:continue
            step=min(offs)
            if not all(sum((bits[u]&bits[v]).bit_count()==2 for v in O if v!=u)==2 for u in O):continue
            d=math.gcd(step,10)
            if d==1:typ['C10'].append(O)
            elif d==2:typ['2C5'].append(O)
        counts['C10']+=len(typ['C10']);counts['2C5']+=len(typ['2C5'])
        hit=None
        for A in typ['C10']:
            A0=A[0]
            for B in typ['2C5']:
                if set(A)&set(B):continue
                pair_tests+=1
                if not all((bits[A0]&bits[v]).bit_count()==2 for v in B):continue
                if not all((bits[u]&bits[v]).bit_count()==2 for u in A for v in B):continue
                S=A+B;z=0
                for u in S:z^=bits[u]
                if z:continue
                hit=(A,B);break
            if hit:break
        summary.append({'exponents':[ei,ej],'C10_halves':len(typ['C10']),'2C5_halves':len(typ['2C5'])})
        if hit:
            A,B=hit;witness={'exponents':[ei,ej],'diagonal':[a,b,ai,bi],
              'half_C10':A,'half_2C5':B,'selected_carriers':A+B};break
    if witness:
        S=witness['selected_carriers'];z=0
        for u in S:z^=bits[u]
        assert z==0 and len(set(S))==20
        e=sum((bits[u]&bits[v]).bit_count()==2 for u,v in itertools.combinations(S,2));assert e==120
        deg=[sum((bits[u]&bits[v]).bit_count()==2 for v in S if v!=u) for u in S];assert set(deg)=={12}
        out={'pass':'5354b','status':'THEOREM_Q11_MOD4_CAYLEY_DUAL20_EQUALITY_WITNESS',
          'order10_elements_tested':tested,'candidate_halves':counts,'pair_tests':pair_tests,
          'witness':witness,'selected_graph':'K10,10 + C10 + (C5+C5)','selected_edges':120,'degree':12,
          'conclusion':'A constructive q11 weight20 footprint-dual word exists in the congruence-predicted two-factor family.',
          'boundary':'Witness existence alone does not prove primal d=121; a dual-orbit moment certificate is still required.'}
    else:
        out={'pass':'5354b','status':'NO_Q11_MOD4_CAYLEY_DUAL20_IN_DIAGONAL_ORDER10_FAMILY',
          'order10_elements_tested':tested,'candidate_halves':counts,'pair_tests':pair_tests,
          'element_summary':summary,
          'conclusion':'No C10 | (C5+C5) XOR-zero equality-wall support occurs in the full tested diagonal order10 family.',
          'boundary':'Family-specific no-go only; other order10 conjugacy classes or noncyclic supports remain open.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
