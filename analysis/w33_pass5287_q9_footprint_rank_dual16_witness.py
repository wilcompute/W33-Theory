#!/usr/bin/env python3
"""Pass5287: exact q=9 footprint rank and an explicit weight-16 dual witness.

Construct PG(3,9) over GF(9)=F3[t]/(t^2+1), the symplectic W(3,9) point set,
and the P-component carriers given by unordered polar pairs {H,H^perp} of
nonisotropic projective lines. The point/P-component incidence matrix F has
820 rows and 3321 columns. Exact binary elimination gives rank_2(F)=369,
which equals q(q^2+1)/2 at q=9 and extends the verified q=3,5,7 anchors.

An explicit 16-column dependence is also certified. Its carrier incidence covers
160 W-points exactly twice and the induced P-block graph is 10-regular on 16
vertices. The complement is two connected 8-vertex components; each component
is K8 minus an 8-cycle (equivalently its complement is C8).

This is NOT a q=9 distance-81 theorem: no complete minimum dual orbit, shell
replication, or maximum pair-codegree certificate is asserted here.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5287_Q9_FOOTPRINT_RANK_DUAL16_WITNESS.json'
Q=9
WIT=(97,102,223,528,543,657,789,804,963,1656,2070,2292,2621,2670,2801,2910)

# GF(9): a+bt encoded as a+3b, t^2=2 over F3.
def add(x,y): return ((x%3+y%3)%3)+3*(((x//3+y//3)%3))
def neg(x): return ((-x%3)%3)+3*((-(x//3)%3)%3)
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    a,b=x%3,x//3; c,d=y%3,y//3
    return ((a*c+2*b*d)%3)+3*((a*d+b*c)%3)
def inv(x):
    assert x
    for y in range(1,9):
        if mul(x,y)==1:return y
    raise AssertionError

def smul(a,v): return tuple(mul(a,x) for x in v)
def vadd(u,v): return tuple(add(a,b) for a,b in zip(u,v))
def norm(v):
    for x in v:
        if x:return smul(inv(x),v)
    raise ValueError('zero')
def sp(u,v):
    z=0
    z=add(z,mul(u[0],v[2])); z=sub(z,mul(u[2],v[0]))
    z=add(z,mul(u[1],v[3])); z=sub(z,mul(u[3],v[1]))
    return z

def gf2_rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def main():
    pts=sorted({norm(v) for v in itertools.product(range(9),repeat=4) if any(v)})
    assert len(pts)==820
    pi={p:i for i,p in enumerate(pts)}

    # Enumerate all projective lines from point pairs, retaining one basis pair.
    lines={}
    for i,u in enumerate(pts):
        for j in range(i+1,len(pts)):
            v=pts[j]
            S={norm(v)}
            for a in range(9): S.add(norm(vadd(u,smul(a,v))))
            if len(S)!=10: continue
            key=tuple(sorted(pi[x] for x in S))
            lines.setdefault(key,(u,v))
    assert len(lines)==7462
    noniso=[(L,uv) for L,uv in lines.items() if sp(*uv)!=0]
    assert len(noniso)==6642

    carriers={}
    for H,(u,v) in noniso:
        Hp=tuple(i for i,x in enumerate(pts) if sp(x,u)==0 and sp(x,v)==0)
        assert len(Hp)==10
        C=tuple(sorted(set(H)|set(Hp)))
        assert len(C)==20
        carriers[C]=1
    C=sorted(carriers); assert len(C)==3321

    row=[0]*820; col=[]
    for j,c in enumerate(C):
        z=0
        for p in c:
            row[p]|=1<<j; z|=1<<p
        col.append(z)
    assert {x.bit_count() for x in row}=={81}
    assert {x.bit_count() for x in col}=={20}
    r=gf2_rank(row); assert r==369

    z=0
    for j in WIT:z^=col[j]
    assert z==0
    deg=Counter()
    for p in range(820):
        d=sum((col[j]>>p)&1 for j in WIT)
        deg[d]+=1
    assert deg==Counter({0:660,2:160})

    n=len(WIT); adj=[set() for _ in range(n)]
    for a,b in itertools.combinations(range(n),2):
        if (col[WIT[a]]&col[WIT[b]]).bit_count()==2:
            adj[a].add(b);adj[b].add(a)
    assert {len(x) for x in adj}=={10}
    assert sum(map(len,adj))//2==80
    compadj=[set(range(n))-{i}-adj[i] for i in range(n)]
    assert {len(x) for x in compadj}=={5}
    seen=set(); comps=[]
    for s in range(n):
        if s in seen:continue
        X={s};Qq=[s];seen.add(s)
        while Qq:
            u=Qq.pop()
            for v in compadj[u]:
                if v not in seen:seen.add(v);X.add(v);Qq.append(v)
        comps.append(sorted(X))
    assert sorted(map(len,comps))==[8,8]
    for X in comps:
        # Within each complement component every vertex has degree 5, so the
        # graph-theoretic complement inside X has degree 2; certify it is C8.
        cyc={u:(set(X)-{u}-compadj[u]) for u in X}
        assert {len(cyc[u]) for u in X}=={2}
        S={X[0]};Qq=[X[0]]
        while Qq:
            u=Qq.pop()
            for v in cyc[u]:
                if v not in S:S.add(v);Qq.append(v)
        assert len(S)==8

    out={
      'pass':5287,
      'status':'THEOREM_Q9_FOOTPRINT_BINARY_RANK_AND_EXPLICIT_DUAL16_WITNESS',
      'field':'GF(9)=F3[t]/(t^2+1)',
      'W_points':820,
      'projective_lines':7462,
      'nonisotropic_projective_lines':6642,
      'P_components':3321,
      'carrier_size':20,
      'point_footprint_weight':81,
      'binary_rank_F':369,
      'rank_formula_value_q_q2plus1_over2':369,
      'dual_weight_upper_bound':16,
      'dual16_witness':list(WIT),
      'witness_point_degree_histogram':{'0':660,'2':160},
      'selected_block_graph':'16 vertices, 10-regular, 80 edges',
      'selected_graph_complement':'5-regular; two connected components of size 8, each K8 minus C8',
      'rank_anchor_chain':{'q3':15,'q5':65,'q7':175,'q9':369},
      'boundary':'Exact q9 rank and explicit dual dependence only. No q9 dual minimum, complete shell orbit, primal distance81, or all-odd-q rank theorem is claimed.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
