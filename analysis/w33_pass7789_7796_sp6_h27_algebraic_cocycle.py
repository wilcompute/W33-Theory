#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
import sys
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
OUT=ROOT/'data/PART_W33_PASS7789_7796_SP6_H27_ALGEBRAIC_COCYCLE.json'
def pkey(g,n=27):return tuple(int(g(i)) for i in range(n))
def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();I={r:i for i,r in enumerate(R)};ai={S:i for i,S in enumerate(A2)}
    plus=sorted(i for i,x in enumerate(parity) if x==0);r=E.SIMPLES[0]
    rp=tuple(I[E.refl(x,r)] for x in R);ap=tuple(ai[frozenset(rp[x] for x in S)] for S in A2);li={L:i for i,L in enumerate(leaves)}
    rleaf=tuple(li[frozenset(ap[x] for x in L)] for L in leaves);U=[frozenset(leaves[v]&leaves[rleaf[v]]) for v in plus];ui={S:i for i,S in enumerate(U)};assert len(U)==1120
    orth=[x for x in R if E.dot(x,r)==0];reps=[];seen=set()
    for q in orth:
        nq=tuple(-z for z in q);k=min(I[q],I[nq])
        if k not in seen:seen.add(k);reps.append(R[k])
    assert len(reps)==63;perms=[]
    for q in reps:
        qp=tuple(I[E.refl(x,q)] for x in R);aq=tuple(ai[frozenset(qp[x] for x in S)] for S in A2);perms.append(tuple(ui[frozenset(aq[x] for x in S)] for S in U))
    chosen=[];PG=PermutationGroup([Permutation(list(range(1120)))])
    for p in perms:
        H=PermutationGroup([Permutation(x) for x in chosen+[p]]);o=int(H.order())
        if o>int(PG.order()):chosen.append(p);PG=H
        if o==1451520:break
    assert int(PG.order())==1451520;stab=PG.stabilizer(0);orbs=sorted(stab.orbits(),key=lambda o:(len(o),min(o)));assert sorted(map(len,orbs))==[1,12,27,27,81,108,216,648]
    O81=sorted(next(o for o in orbs if len(o)==81));A=[set() for _ in range(81)]
    for i,j in itertools.combinations(range(81),2):
        if len(U[O81[i]]&U[O81[j]])==4:A[i].add(j);A[j].add(i)
    comps=[];seen=set()
    for i in range(81):
        if i in seen:continue
        C={i};q=[i];seen.add(i)
        while q:
            x=q.pop()
            for y in A[x]:
                if y not in seen:seen.add(y);C.add(y);q.append(y)
        comps.append(sorted(C))
    assert len(comps)==27 and set(map(len,comps))=={3};loc={v:i for i,v in enumerate(O81)};ind=[]
    for g in stab.generators:ind.append(tuple(loc[int(g(v))] for v in O81))
    sel=[];G81=PermutationGroup([Permutation(list(range(81)))])
    for p in ind:
        H=PermutationGroup([Permutation(x) for x in sel+[p]]);o=int(H.order())
        if o>int(G81.order()):sel.append(p);G81=H
        if o==1296:break
    block_of={i:b for b,C in enumerate(comps) for i in C};bp=[]
    for p in sel:
        arr=[]
        for C in comps:
            z={block_of[p[i]] for i in C};assert len(z)==1;arr.append(next(iter(z)))
        bp.append(tuple(arr))
    G27=PermutationGroup([Permutation(x) for x in bp]);assert int(G27.order())==1296;K=G27.stabilizer(0);assert int(K.order())==48
    H=G27
    for _ in range(4):H=H.derived_subgroup()
    assert int(H.order())==27 and not H.is_abelian and int(H.center().order())==3 and int(H.stabilizer(0).order())==1
    hels=list(H.generate_schreier_sims());byimage={int(g(0)):g for g in hels};Z=list(H.center().generate_schreier_sims());e=H.identity;z=next(g for g in Z if int(g.order())==3)
    o8=next(set(map(int,o)) for o in K.orbits() if len(o)==8);S=[byimage[y] for y in sorted(o8)]
    def coset(g):return frozenset(pkey(g*c) for c in Z)
    assert len({coset(s) for s in S})==8
    a,b=next((a,b) for a,b in itertools.permutations(S,2) if int(PermutationGroup([a,b]).order())==27)
    def pw(g,n):return e if n%3==0 else (g if n%3==1 else g*g)
    qcos={(u,v):coset(pw(a,u)*pw(b,v)) for u in range(3) for v in range(3)};assert len(set(qcos.values()))==9
    section={coset(e):e};section.update({coset(s):s for s in S});sigma={uv:section[C] for uv,C in qcos.items()};zp={pkey(e):0,pkey(z):1,pkey(z*z):2};coc={}
    for x in qcos:
        for y in qcos:
            xy=((x[0]+y[0])%3,(x[1]+y[1])%3);c=sigma[x]*sigma[y]*(~sigma[xy]);coc[(x,y)]=zp[pkey(c)]
    sign=next(s for s in (1,2) if all(coc[(x,y)]==(s*(x[0]*y[1]-x[1]*y[0]))%3 for x in qcos for y in qcos));assert sign==1
    invq={C:uv for uv,C in qcos.items()};mats=set();center_scalars=set()
    for k in K.generate_schreier_sims():
        ca=invq[coset((~k)*a*k)];cb=invq[coset((~k)*b*k)];M=(ca[0],cb[0],ca[1],cb[1]);mats.add(M);zz=(~k)*z*k;center_scalars.add((M,(1 if pkey(zz)==pkey(z) else 2)))
    GL={(A0,A1,A2,A3) for A0,A1,A2,A3 in itertools.product(range(3),repeat=4) if (A0*A3-A1*A2)%3};assert mats==GL and all(sc==(M[0]*M[3]-M[1]*M[2])%3 for M,sc in center_scalars)
    out={'schema':'w33.pass7789_7796.sp6_h27_algebraic_cocycle.v1','status':'PASS','passes':'7789-7796','Sp6_2_order':1451520,'point_stabilizer_order':1296,'suborbit81_internal_graph':'27 K3','triangle_quotient_order':1296,'regular_normal_subgroup':{'order':27,'nonabelian':True,'exponent':3,'center_order':3,'quotient':'F3^2'},'canonical_section':'The valency-8 point-stabilizer orbit gives one representative of every nonzero coset of H27/Z, plus identity for zero.','section_cocycle':'c(u,v)=det(u,v) for all 9x9 ordered pairs in the chosen central orientation; replacing z by z^{-1} gives the Pass7186 convention -det(u,v).','complement_action':{'order':48,'matrices_on_H27_mod_center':48,'equals_GL2_3':True,'center_action':'z -> z^det(M)'},'algebraic_bridge':'H27 : GL2(3) with the determinant cocycle is obtained directly from multiplication and conjugation in the Sp6(2) 81-suborbit triangle quotient. No graph-isomorphism search is used.','prior_art_boundary':'Pass7186 already owns the AG(2,3) determinant-voltage/H27 Cayley law. Pass7629-7644 additionally owns the Schlaefli/H27 common 9x3 and local 20D Gram scheme. This pass proves the Sp6-derived quotient carries the same extension law algebraically.','claim_boundary':'Exact finite-group/cocycle theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','cocycle':'det','GL2_3':len(mats),'graph_match_used':False}))
if __name__=='__main__':main()
