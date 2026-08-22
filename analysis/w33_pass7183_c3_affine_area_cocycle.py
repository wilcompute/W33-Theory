#!/usr/bin/env python3
"""Pass7183: identify the E6 matter C3 voltage class with the AG(2,3) area cocycle.

Exact finite statement.  Starting from the Pass7164 E8/W33 C6 fibration and the
Pass7181 A2-charge construction, the 27 W33 distance-two fibres group into nine
3-fibre classes.  Their perfect-matchings give a Z3 voltage on K9.  This pass
proves, up to switching, affine relabelling and sign, that this voltage is the
standard alternating determinant cocycle on AG(2,3).
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import sympy as sp
import w33_pass7163_7170_e8_hexagonal_lift as b

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7183_C3_AFFINE_AREA_COCYCLE.json'

def build_voltage():
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers(); anchor=0
    A2=fib[anchor];alpha,beta=A2[0],A2[2]
    A=sp.Matrix.hstack(sp.Matrix(R[alpha]),sp.Matrix(R[beta]));Gi=(A.T*A).inv()
    def proj(v):
        x=sp.Matrix(R[v]);z=x-A*(Gi*(A.T*x));return tuple(sp.simplify(q) for q in z)
    def canonpm(x):return min(x,tuple(-q for q in x))
    nonN=[y for y in range(40) if y!=anchor and y not in adj[anchor]];assert len(nonN)==27
    ids={};sig={}
    for y in nonN:
        S=frozenset(canonpm(proj(v)) for v in fib[y]);assert len(S)==3
        for x in S:ids.setdefault(x,len(ids))
        sig[y]=S
    assert len(ids)==27
    classes={}
    for y,S in sig.items():classes.setdefault(tuple(sorted(ids[x] for x in S)),[]).append(y)
    C=sorted((sorted(v) for v in classes.values()),key=lambda z:tuple(z));assert len(C)==9 and all(len(x)==3 for x in C)
    perms={}
    for i,j in itertools.combinations(range(9),2):
        p=[]
        for a in C[i]:
            h=[c for c in C[j] if c in adj[a]];assert len(h)==1;p.append(C[j].index(h[0]))
        perms[i,j]=tuple(p);inv=[0]*3
        for x,y in enumerate(p):inv[y]=x
        perms[j,i]=tuple(inv)
    # Gauge-fix the star from class 0 to identity.
    labels={0:{i:i for i in range(3)}}
    for j in range(1,9):
        p=perms[0,j];labels[j]={old:new for new,old in enumerate(p)}
    def gauged(i,j):
        inv={new:old for old,new in labels[i].items()};p=perms[i,j]
        return tuple(labels[j][p[inv[x]]] for x in range(3))
    def shift(p):
        for s in range(3):
            if p==tuple((x+s)%3 for x in range(3)):return s
        raise AssertionError(p)
    sh={(i,j):shift(gauged(i,j)) for i in range(9) for j in range(9) if i!=j}
    assert all(sh[0,j]==0 for j in range(1,9))
    hol={};hist=Counter()
    for i,j,k in itertools.combinations(range(9),3):
        z=(sh[i,j]+sh[j,k]+sh[k,i])%3;hol[(i,j,k)]=z;hist[z]+=1
    assert hist==Counter({1:36,2:36,0:12})
    return C,sh,hol,hist

def det(u,v):return (u[0]*v[1]-u[1]*v[0])%3

def main():
    C,sh,hol,hist=build_voltage()
    # Canonical affine plane AG(2,3); oriented triangle area is
    # det(v-u,w-u)=det(u,v)+det(v,w)+det(w,u).
    pts=[(a,b) for a in range(3) for b in range(3)]
    canonical_zero=set()
    for tri in itertools.combinations(range(9),3):
        u,v,w=[pts[i] for i in tri]
        h=(det(u,v)+det(v,w)+det(w,u))%3
        if h==0:canonical_zero.add(frozenset(tri))
    assert len(canonical_zero)==12
    zero_triples={frozenset(t) for t,h in hol.items() if h==0};assert len(zero_triples)==12
    # Find all affine-plane isomorphisms fixing the chosen gauge origin 0.
    isos=[]
    for rest in itertools.permutations(range(1,9)):
        p=(0,)+rest
        if {frozenset(p[i] for i in L) for L in zero_triples}==canonical_zero:isos.append(p)
    assert len(isos)==48  # GL(2,3)
    matches=[]
    for p in isos:
        for eps in (1,2):
            if all(sh[i,j]==eps*det(pts[p[i]],pts[p[j]])%3 for i in range(9) for j in range(9) if i!=j):
                matches.append((p,eps))
    assert len(matches)==48
    assert Counter(e for _,e in matches)==Counter({1:24,2:24})
    # The zero-holonomy triangles therefore ARE the twelve affine lines.
    # Nonzero holonomy is the signed affine area of a noncollinear triple.
    area_hist=Counter()
    p,eps=matches[0]
    for i,j,k in itertools.combinations(range(9),3):
        u,v,w=[pts[p[x]] for x in (i,j,k)]
        area=eps*(det(u,v)+det(v,w)+det(w,u))%3
        assert area==hol[i,j,k];area_hist[area]+=1
    assert area_hist==hist
    out={
      'schema':'w33.pass7183.c3_affine_area_cocycle.v1','status':'PASS',
      'base':'K9 on the nine E6-weight-signature classes','cover':'regular C3 voltage cover on 27 W33 distance-two fibres',
      'gauge':'class-0 spanning star fixed to zero voltage','triangle_holonomy':{str(k):v for k,v in sorted(hist.items())},
      'zero_holonomy_triangles':12,'identification':'the 12 zero-holonomy triples are exactly the 12 affine lines of AG(2,3)',
      'affine_plane_isomorphisms_fixing_origin':48,
      'determinant_cocycle_matches':48,'match_signs':{'plus':24,'minus':24},
      'theorem':'Up to switching, affine relabelling of AG(2,3), and global sign, the K9 voltage is psi(u,v)=det(u,v) in F3. Triangle holonomy is the oriented affine area det(v-u,w-u).',
      'cohomology_firewall':'The voltage is not cohomologous to zero because 72 of the 84 K9 triangles have nonzero holonomy. This is a finite F3 covering cocycle; no physical gauge field is inferred.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','affine_isos':48,'holonomy':out['triangle_holonomy']}))
if __name__=='__main__':main()
