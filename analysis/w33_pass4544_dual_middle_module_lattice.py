#!/usr/bin/env python3
"""Pass 4544 -- exact upper submodule lattice of the 364D apartment-dual middle.

Pass 4522 constructed a 364-dimensional F2 PSp(4,3)-module M and exhibited one
outer-stable 358D submodule with a faithful 6D O^-(6,2) quotient.  This pass
reopens the module rather than assuming that 358D submodule is unique.

Exact cyclic-span and subspace calculations show:

* standard basis cyclic dimensions are 284^2, 330^10, 358^49, 364^303;
* there is one 284D cyclic submodule S284 and one 330D cyclic submodule S330;
* there are THREE distinct 358D submodules T0,T1,T2;
* every Ti contains S330;
* every pair Ti,Tj intersects in the same 352D core K352 and sums to M;
* M/K352 is 12D and is U6 direct-sum U6.  Exhausting all 4095 nonzero quotient
  vectors gives exactly three proper nonzero invariant submodules, all 6D and
  irreducible.  They are the three lines in the F2^2 multiplicity space;
* the projective outer involution swaps two 358D submodules and fixes the third;
* K352/S330 is 22D and splits exactly as irreducible V8 direct-sum V14;
* S284 intersects S330 in a 256D submodule K256 and intersects K352 in 278D.
  The 22D layer between K256 and that 278D intersection is again V8+V14, and
  S284/(S284 cap K352) is a 6D irreducible;
* inside K256, standard cyclic spans expose a unique 186D submodule inside a
  unique 250D submodule.  The remaining quotient dimensions are 64 and 6.

The pass intentionally stops short of calling the entire Loewy lattice closed:
irreducibility/composition structure of the 186D submodule and the 64D quotient
are not certified here.  The exact upper lattice and every displayed 6/8/14
irreducibility statement are exhaustive finite calculations.
"""
from __future__ import annotations

import json
from collections import Counter,deque
from pathlib import Path

import numpy as np

import w33_pass4522_4525_4527_dual_orthogonal_schlafli as p4522
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4511_4514_dual_even_prism_ihara import build_groups,perm_mask

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4544_DUAL_MIDDLE_MODULE_LATTICE.json'


def apply_cols(cols,x):
    out=0;y=int(x)
    while y:
        b=y&-y;i=b.bit_length()-1;out^=cols[i];y-=b
    return out


def canonical(rows,n):
    R,_=p4522.rref_int_rows(rows,n)
    return tuple(R)


def rank_rows(rows,n):
    return len(p4522.rref_int_rows(rows,n)[0])


def intersect(A,B,n):
    aperp=p4522.nullspace_from_rows(A,n)
    bperp=p4522.nullspace_from_rows(B,n)
    return p4522.nullspace_from_rows(aperp+bperp,n)


def contains(B,x):
    C=p4522.CoordBasis()
    for y in B:C.add(int(y))
    return C.coords(int(x)) is not None


def cyclic(seed,gens):
    piv={};basis=[];q=deque()
    def add(x):
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;basis.append(int(x));q.append(int(x));return True
        return False
    add(seed)
    while q:
        x=q.popleft()
        for g in gens:add(apply_cols(g,x))
    return basis


def restrict_to_subspace(gens,S,n):
    C=p4522.CoordBasis()
    for x in S:C.add(int(x))
    assert len(C.orig)==len(S)
    out=[]
    for g in gens:
        cols=[]
        for x in C.orig:
            z=C.coords(apply_cols(g,x));assert z is not None;cols.append(z)
        out.append(cols)
    return out,C


def quotient_gens(gens,S,n):
    """Quotient an nD module by invariant subspace S; return quotient cols."""
    C=p4522.CoordBasis()
    for x in S:C.add(int(x))
    d=len(C.orig)
    for i in range(n):C.add(1<<i)
    assert len(C.orig)==n
    out=[]
    for g in gens:
        cols=[]
        for j in range(d,n):
            z=C.coords(apply_cols(g,C.orig[j]));assert z is not None;cols.append(z>>d)
        out.append(cols)
    return out,C


def quotient_inside(Sgens,Sdim,T_in_S):
    return quotient_gens(Sgens,T_in_S,Sdim)[0]


def exhaustive_irreducible(gens,d):
    dims=Counter();subs={}
    for x in range(1,1<<d):
        B=cyclic(x,gens);dims[len(B)]+=1;subs.setdefault(canonical(B,d),len(B))
    proper={k:v for k,v in subs.items() if v<d}
    return dims,proper


def reconstruct_middle():
    pts,pidx,lines,A,apartments,apmasks,H=geometry();n=1620
    Hrows=[]
    for row in H:
        x=0
        for j,b in enumerate(row):
            if b:x|=1<<j
        Hrows.append(x)
    Dnull=p4522.nullspace_from_rows(Hrows,n);assert len(Dnull)==1581
    apidx={m:i for i,m in enumerate(apmasks)}
    triples=[]
    for i in range(n):
        mi=apmasks[i]
        for j in range(i+1,n):
            k=apidx.get(mi^apmasks[j])
            if k is not None and j<k:triples.append((i,j,k))
    assert len(triples)==2160
    B=p4522.CoordBasis()
    for a,b,c in triples:B.add((1<<a)|(1<<b)|(1<<c))
    assert len(B.orig)==1215
    for x in Dnull:B.add(x)
    assert len(B.orig)==1581

    selected,psp,outer,pgsp=build_groups(pts,pidx,lines)
    linegens=[x[1] for x in selected]
    apgens=[]
    for lp in linegens+[outer]:apgens.append(tuple(apidx[perm_mask(m,lp)] for m in apmasks))
    def perm_coordmask(x,p):
        out=0;y=int(x)
        while y:
            b=y&-y;i=b.bit_length()-1;out|=1<<p[i];y-=b
        return out
    def quotient_cols(pg):
        cols=[]
        for j in range(1215,1581):
            c=B.coords(perm_coordmask(B.orig[j],pg));assert c is not None;cols.append(c>>1215)
        return cols
    Qgens=[quotient_cols(pg) for pg in apgens[:5]];Qouter=quotient_cols(apgens[5])
    Qm=[p4522.cols_to_np(c,366) for c in Qgens]
    fixed=p4522.nullspace2(np.vstack([g^np.eye(366,dtype=np.uint8) for g in Qm]));assert fixed.shape==(1,366)
    dualfixed=p4522.nullspace2(np.vstack([g.T^np.eye(366,dtype=np.uint8) for g in Qm]));assert dualfixed.shape==(1,366)
    assert int(fixed[0]@dualfixed[0]%2)==0
    Hb=p4522.nullspace2(dualfixed);C=p4522.CoordBasis();C.add(p4522.vecint(fixed[0]))
    for x in Hb:C.add(p4522.vecint(x))
    assert len(C.orig)==365
    Mgens=[]
    for qg in Qgens:
        cc=[]
        for j in range(1,365):
            z=C.coords(apply_cols(qg,C.orig[j]));assert z is not None;cc.append(z>>1)
        Mgens.append(cc)
    Mouter=[]
    for j in range(1,365):
        z=C.coords(apply_cols(Qouter,C.orig[j]));assert z is not None;Mouter.append(z>>1)
    return Mgens,Mouter


def main()->int:
    Mgens,Mouter=reconstruct_middle();n=364
    std=[];bydim=Counter();subkeys={}
    for i in range(n):
        B=cyclic(1<<i,Mgens);bydim[len(B)]+=1
        subkeys.setdefault(len(B),{}).setdefault(canonical(B,n),[]).append(i)
    assert bydim==Counter({364:303,358:49,330:10,284:2})
    assert len(subkeys[284])==1 and len(subkeys[330])==1 and len(subkeys[358])==3
    S284=list(next(iter(subkeys[284])));S330=list(next(iter(subkeys[330])))
    T=[list(k) for k in subkeys[358]]
    assert all(all(contains(t,x) for x in S330) for t in T)

    K=[intersect(T[i],T[j],n) for i in range(3) for j in range(i+1,3)]
    assert {len(x) for x in K}=={352} and len({canonical(x,n) for x in K})==1
    K352=K[0]
    assert all(rank_rows(T[i]+T[j],n)==364 for i in range(3) for j in range(i+1,3))

    # Outer permutation on the three 358D submodules.
    tkeys={canonical(t,n):i for i,t in enumerate(T)};op=[]
    for t in T:
        image=canonical([apply_cols(Mouter,x) for x in t],n);assert image in tkeys;op.append(tkeys[image])
    assert sorted(op)==[0,1,2] and Counter(op)==Counter({0:1,1:1,2:1})
    # Must have one fixed point and one transposition.
    assert sum(i==op[i] for i in range(3))==1

    Q12,_=quotient_gens(Mgens,K352,n)
    dims12,proper12=exhaustive_irreducible(Q12,12)
    proper6=[k for k,v in proper12.items() if v==6]
    assert len(proper6)==3 and set(proper12.values())=={6}
    assert dims12[6]==3*63 and dims12[12]==4095-3*63
    for k in proper6:
        g6,_=restrict_to_subspace(Q12,list(k),12)
        d6,p6=exhaustive_irreducible(g6,6);assert d6==Counter({6:63}) and not p6

    # K352 / S330 = V8 direct-sum V14.
    Kgens,Kcoord=restrict_to_subspace(Mgens,K352,n);kdim=352
    S330K=[]
    for x in S330:
        z=Kcoord.coords(x);assert z is not None;S330K.append(z)
    Q22,_=quotient_gens(Kgens,S330K,kdim);assert len(Q22[0])==22
    cyc22=Counter();subs22={}
    for i in range(22):
        b=cyclic(1<<i,Q22);cyc22[len(b)]+=1;subs22.setdefault(len(b),{}).setdefault(canonical(b,22),[]).append(i)
    assert cyc22==Counter({14:14,22:6,8:2})
    assert len(subs22[8])==len(subs22[14])==1
    V8=list(next(iter(subs22[8])));V14=list(next(iter(subs22[14])))
    assert len(intersect(V8,V14,22))==0 and rank_rows(V8+V14,22)==22
    for V,d in [(V8,8),(V14,14)]:
        vg,_=restrict_to_subspace(Q22,V,22);dd,pp=exhaustive_irreducible(vg,d);assert dd==Counter({d:(1<<d)-1}) and not pp

    # S284 branch.
    K256=intersect(S284,S330,n);I278=intersect(S284,K352,n)
    assert len(K256)==256 and len(I278)==278
    assert all(contains(I278,x) for x in K256)
    S284g,S284c=restrict_to_subspace(Mgens,S284,n)
    K256c=[S284c.coords(x) for x in K256];I278c=[S284c.coords(x) for x in I278]
    assert None not in K256c and None not in I278c
    Q28,_=quotient_gens(S284g,K256c,284);assert len(Q28[0])==28
    # I278/K256 is the invariant 22D subspace inside Q28; quotient is 6D.
    Ctmp=p4522.CoordBasis()
    for x in K256c:Ctmp.add(int(x))
    for i in range(284):Ctmp.add(1<<i)
    I22=[]
    for x in I278c:
        z=Ctmp.coords(int(x));assert z is not None;I22.append(z>>256)
    I22=list(canonical(I22,28));assert len(I22)==22
    I22g,_=restrict_to_subspace(Q28,I22,28)
    cycI=Counter(len(cyclic(1<<i,I22g)) for i in range(22));assert cycI==Counter({14:14,8:2,22:6})
    Q6,_=quotient_gens(Q28,I22,28);d6,p6=exhaustive_irreducible(Q6,6);assert d6==Counter({6:63}) and not p6

    # Exact deeper frontier inside K256: unique 186 < unique 250 < 256.
    K256g,K256coord=restrict_to_subspace(Mgens,K256,n)
    cyc256=Counter();u={}
    for i in range(256):
        b=cyclic(1<<i,K256g);cyc256[len(b)]+=1;u.setdefault(len(b),{}).setdefault(canonical(b,256),[]).append(i)
    assert cyc256==Counter({256:193,250:57,186:6})
    assert len(u[186])==len(u[250])==1
    S186=list(next(iter(u[186])));S250=list(next(iter(u[250])))
    assert all(contains(S250,x) for x in S186)
    S250g,S250c=restrict_to_subspace(K256g,S250,256)
    S186c=[S250c.coords(x) for x in S186];assert None not in S186c
    Q64,_=quotient_gens(S250g,S186c,250);assert len(Q64[0])==64
    Q6b,_=quotient_gens(K256g,S250,256);dd6,pp6=exhaustive_irreducible(Q6b,6);assert dd6==Counter({6:63}) and not pp6
    std64=Counter(len(cyclic(1<<i,Q64)) for i in range(64));assert std64==Counter({64:64})

    out={
      'pass':4544,
      'middle_module':{'dimension':364,'standard_basis_cyclic_dimensions':{str(k):v for k,v in sorted(bydim.items())}},
      'upper_lattice':{
        'unique_S284':284,'unique_S330':330,'number_of_S358':3,
        'common_K352':352,'pairwise_S358_sum_dimension':364,
        'all_S358_contain_S330':True,
        'outer_action_on_three_S358':op,
        'outer_action_shape':'one fixed 358D submodule plus a transposed pair'},
      'top_quotient':{
        'M_over_K352_dimension':12,'proper_nonzero_submodules':3,
        'proper_submodule_dimensions':[6,6,6],
        'all_three_6D_irreducible_exhaustive':True,
        'structure':'U6 direct-sum U6; the three 6D submodules are the three F2-lines in a 2D multiplicity space'},
      'K352_over_S330':{
        'dimension':22,'structure':'V8 direct-sum V14','V8_irreducible_exhaustive':True,'V14_irreducible_exhaustive':True},
      'S284_branch':{
        'S284_intersect_S330_dimension':256,'S284_intersect_K352_dimension':278,
        'I278_over_K256':'V8 direct-sum V14','S284_over_I278_dimension':6,'top_6D_irreducible_exhaustive':True},
      'K256_frontier':{
        'standard_basis_cyclic_dimensions':{str(k):v for k,v in sorted(cyc256.items())},
        'unique_S186_dimension':186,'unique_S250_dimension':250,
        'S250_over_S186_dimension':64,'K256_over_S250_dimension':6,
        'K256_over_S250_irreducible_exhaustive':True,
        'S250_over_S186_standard_basis_all_cyclic_dimension':64,
        'open':['irreducibility/composition structure of S186','irreducibility/composition structure of the 64D quotient']},
      'boundary':'This closes the upper lattice through K256 and proves every displayed 6D/8D/14D simple layer exhaustively. It does NOT claim the complete Loewy lattice below S186 or certify the 64D quotient irreducible.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
