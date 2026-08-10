#!/usr/bin/env python3
"""Pass 4571 -- close the remaining 186D/64D composition frontier of Pass4544.

Pass4544 left two exact open questions inside the 364-dimensional apartment-dual
middle module: the composition structure of the unique 186D submodule S186 and
irreducibility of the 64D quotient S250/S186.

This verifier reconstructs the same module and uses deterministic MeatAxe-style
operations over GF(2):
  * spin standard and contragredient basis vectors to expose visible submodules;
  * use multiplicity-one factor kernels of deterministic group-algebra elements
    to expose hidden invariant subspaces;
  * exhaust all nonzero vectors for 6D/8D/14D terminal factors;
  * certify 40D/64D terminal factors by finding a group-algebra element whose
    characteristic polynomial is irreducible of the full module degree. Such an
    element has no proper invariant subspace, so neither can the full group.

The resulting composition factors are

    S186 : 40^3 + 14^2 + 8 + 6^5,
    S250/S186 : 64 (irreducible).

The pass closes composition factors, not every extension class / every node of
the complete Loewy lattice below S186.
"""
from __future__ import annotations

import json,random
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp

import w33_pass4544_dual_middle_module_lattice as p4544
import w33_pass4522_4525_4527_dual_orthogonal_schlafli as p4522

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4571_DUAL_MIDDLE_MODULE_COMPOSITION.json'
X=sp.Symbol('x')


def mat_from_cols(cols,d):return p4522.cols_to_np(cols,d).astype(np.uint8)


def cols_from_mat(M):
    M=np.asarray(M,dtype=np.uint8);d=M.shape[0];out=[]
    for j in range(d):out.append(sum(int(M[i,j])<<i for i in range(d) if M[i,j]))
    return out


def gf2_inv(M):
    M=np.asarray(M,dtype=np.uint8);n=len(M);A=np.concatenate([M.copy(),np.eye(n,dtype=np.uint8)],axis=1);r=0
    for c in range(n):
        z=np.flatnonzero(A[r:,c]);assert len(z)
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        r+=1
    assert np.array_equal(A[:,:n],np.eye(n,dtype=np.uint8));return A[:,n:]


def dual_gens(gens,d):
    return [cols_from_mat(gf2_inv(mat_from_cols(g,d)).T) for g in gens]


def standard_proper(gens,d):
    seen={}
    for i in range(d):
        B=p4544.cyclic(1<<i,gens);k=p4544.canonical(B,d);seen.setdefault(k,len(B))
    proper=[(n,list(k)) for k,n in seen.items() if 0<n<d]
    return min(proper,key=lambda z:z[0]) if proper else None


def dual_annihilator_proper(gens,d):
    D=standard_proper(dual_gens(gens,d),d)
    if D is None:return None
    dd,Db=D;S=p4522.nullspace_from_rows(Db,d)
    assert len(S)==d-dd and 0<len(S)<d
    return len(S),S,dd


def charpoly_mod2(A):
    cp=sp.Matrix(np.asarray(A,dtype=int).tolist()).charpoly(X).as_expr()
    return sp.Poly(cp,X,modulus=2)


def algebra_element(gens,d,rng):
    G=[mat_from_cols(g,d) for g in gens];I=np.eye(d,dtype=np.uint8);A=np.zeros((d,d),dtype=np.uint8)
    terms=rng.randint(2,8)
    for _ in range(terms):
        W=I.copy()
        for _ in range(rng.randint(1,12)):W=(G[rng.randrange(len(G))]@W)%2
        A^=W
    return A


def poly_eval_matrix(poly,A):
    d=len(A);R=np.zeros_like(A);I=np.eye(d,dtype=np.uint8)
    coeff=[int(c)%2 for c in poly.all_coeffs()]
    for c in coeff:R=(R@A)%2;R^=(I if c else 0)
    return R


def nullspace_np(M):
    M=np.asarray(M,dtype=np.uint8);rows=[]
    for r in M:rows.append(sum(int(r[i])<<i for i in range(M.shape[1]) if r[i]))
    return p4522.nullspace_from_rows(rows,M.shape[1])


def full_irreducible_witness(gens,d,seed,max_trials=2500):
    rng=random.Random(seed)
    for trial in range(1,max_trials+1):
        A=algebra_element(gens,d,rng);p=charpoly_mod2(A)
        if p.degree()==d and p.is_irreducible:
            return {'trial':trial,'degree':d,'polynomial_hex':hex(int(sum((int(c)%2)<<(d-i) for i,c in enumerate(p.all_coeffs()))))}
    return None


def hidden_proper(gens,d,seed,target_dims=None,max_trials=2500):
    rng=random.Random(seed)
    for trial in range(1,max_trials+1):
        A=algebra_element(gens,d,rng);p=charpoly_mod2(A)
        for f,mult in sp.factor_list(p,modulus=2)[1]:
            if mult!=1:continue
            K=nullspace_np(poly_eval_matrix(f,A))
            for v in K:
                B=p4544.cyclic(int(v),gens);b=len(B)
                if 0<b<d and (target_dims is None or b in target_dims):
                    return {'trial':trial,'factor_degree':f.degree(),'factor_hex':hex(int(sum((int(c)%2)<<(f.degree()-i) for i,c in enumerate(f.all_coeffs())))),
                            'submodule_dimension':b},p4544.canonical(B,d)
    return None


def terminal_simple(gens,d,seed):
    if d<=14:
        dims=Counter(len(p4544.cyclic(x,gens)) for x in range(1,1<<d))
        assert dims==Counter({d:(1<<d)-1})
        return {'method':'exhaustive_nonzero_vector_spin','vectors':(1<<d)-1,'dimension':d}
    w=full_irreducible_witness(gens,d,seed);assert w is not None,(d,seed)
    return {'method':'irreducible_full_degree_group_algebra_charpoly',**w}


def locate_frontier():
    Mgens,Mouter=p4544.reconstruct_middle();n=364
    subs={}
    for i in range(n):
        B=p4544.cyclic(1<<i,Mgens);subs.setdefault(len(B),{}).setdefault(p4544.canonical(B,n),[]).append(i)
    S284=list(next(iter(subs[284])));S330=list(next(iter(subs[330])))
    K256=p4544.intersect(S284,S330,n);assert len(K256)==256
    Kgens,Kc=p4544.restrict_to_subspace(Mgens,K256,n)
    u={}
    for i in range(256):
        B=p4544.cyclic(1<<i,Kgens);u.setdefault(len(B),{}).setdefault(p4544.canonical(B,256),[]).append(i)
    S186=list(next(iter(u[186])));S250=list(next(iter(u[250])))
    S250g,S250c=p4544.restrict_to_subspace(Kgens,S250,256)
    S186c=[S250c.coords(x) for x in S186];assert None not in S186c
    Q64,_=p4544.quotient_gens(S250g,S186c,250)
    S186g,_=p4544.restrict_to_subspace(Kgens,S186,256)
    return S186g,Q64


def main()->int:
    S186g,Q64=locate_frontier()
    # 64D frontier closes directly.
    w64=terminal_simple(Q64,64,457111)

    # S186 exposes a unique standard 120D submodule.
    std186=Counter(len(p4544.cyclic(1<<i,S186g)) for i in range(186))
    assert std186==Counter({186:185,120:1})
    S120=list(p4544.canonical(next(p4544.cyclic(1<<i,S186g) for i in range(186) if len(p4544.cyclic(1<<i,S186g))==120),186))
    S120g,S120c=p4544.restrict_to_subspace(S186g,S120,186)
    Q66,_=p4544.quotient_gens(S186g,S120,186)

    # S120: a dual 106D submodule gives a primal irreducible 14D bottom.
    a14=dual_annihilator_proper(S120g,120);assert a14 and a14[0]==14
    A14=a14[1];A14g,_=p4544.restrict_to_subspace(S120g,A14,120);w14a=terminal_simple(A14g,14,0)
    Q106,_=p4544.quotient_gens(S120g,A14,120)

    # Hidden 60D layer in Q106; quotient 46 then 6|40.
    h106=hidden_proper(Q106,106,457101,{60});assert h106
    S60=list(h106[1]);S60g,_=p4544.restrict_to_subspace(Q106,S60,106);Q46u,_=p4544.quotient_gens(Q106,S60,106)
    a6u=dual_annihilator_proper(Q46u,46);assert a6u and a6u[0]==6
    A6u=a6u[1];A6ug,_=p4544.restrict_to_subspace(Q46u,A6u,46);w6u=terminal_simple(A6ug,6,0)
    Q40u,_=p4544.quotient_gens(Q46u,A6u,46);w40u=terminal_simple(Q40u,40,457112)

    # S60: hidden irreducible 40, quotient20 then 6|14.
    h60=hidden_proper(S60g,60,457102,{40});assert h60
    S40=list(h60[1]);S40g,_=p4544.restrict_to_subspace(S60g,S40,60);w40s=terminal_simple(S40g,40,457114)
    Q20,_=p4544.quotient_gens(S60g,S40,60)
    a6v=dual_annihilator_proper(Q20,20);assert a6v and a6v[0]==6
    A6v=a6v[1];A6vg,_=p4544.restrict_to_subspace(Q20,A6v,20);w6v=terminal_simple(A6vg,6,0)
    Q14,_=p4544.quotient_gens(Q20,A6v,20);w14b=terminal_simple(Q14,14,0)

    # Q66: dual visible 6D bottom, quotient60; hidden 8; then 6|6|40.
    a6=dual_annihilator_proper(Q66,66);assert a6 and a6[0]==6
    A6=a6[1];A6g,_=p4544.restrict_to_subspace(Q66,A6,66);w6a=terminal_simple(A6g,6,0)
    Q60,_=p4544.quotient_gens(Q66,A6,66)
    h8=hidden_proper(Q60,60,457103,{8});assert h8
    B8=list(h8[1]);B8g,_=p4544.restrict_to_subspace(Q60,B8,60);w8=terminal_simple(B8g,8,0)
    Q52,_=p4544.quotient_gens(Q60,B8,60)
    a6b=dual_annihilator_proper(Q52,52);assert a6b and a6b[0]==6
    A6b=a6b[1];A6bg,_=p4544.restrict_to_subspace(Q52,A6b,52);w6b=terminal_simple(A6bg,6,0)
    Q46,_=p4544.quotient_gens(Q52,A6b,52)
    a6c=dual_annihilator_proper(Q46,46);assert a6c and a6c[0]==6
    A6c=a6c[1];A6cg,_=p4544.restrict_to_subspace(Q46,A6c,46);w6c=terminal_simple(A6cg,6,0)
    Q40,_=p4544.quotient_gens(Q46,A6c,46);w40=terminal_simple(Q40,40,457113)

    fac120=Counter({40:2,14:2,6:2});fac66=Counter({40:1,8:1,6:3});fac186=fac120+fac66
    assert sum(k*v for k,v in fac186.items())==186 and fac186==Counter({6:5,40:3,14:2,8:1})
    out={
      'pass':4571,
      'S250_over_S186':{'dimension':64,'irreducible':True,'witness':w64},
      'S186':{
        'dimension':186,'standard_basis_cyclic_dimensions':{str(k):v for k,v in sorted(std186.items())},
        'visible_S120_dimension':120,
        'composition_factors':{'40':3,'14':2,'8':1,'6':5},
        'composition_factor_dimension_check':186,
        'S120_factors':{'40':2,'14':2,'6':2},
        'Q66_factors':{'40':1,'8':1,'6':3}},
      'certification':{
        'small_terminal_factors':'all nonzero vectors exhausted for dimensions 6,8,14',
        'large_terminal_factors':'full-degree irreducible characteristic polynomial of a deterministic GF(2) group-algebra element for dimensions 40 and 64',
        'hidden_submodules':'multiplicity-one factor-kernel plus group spin, with dual-annihilator layers used when visible'},
      'boundary':'Composition factors of S186 and irreducibility of the 64D quotient are closed. This does not claim every extension class or the complete unlabeled Loewy lattice below S186 has been enumerated.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
