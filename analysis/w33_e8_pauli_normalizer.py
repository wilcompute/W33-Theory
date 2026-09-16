#!/usr/bin/env python3
"""Exact Weyl normalizer of the canonical order-3 E8 twist and its Pauli action."""
from __future__ import annotations
import json
from collections import deque
from pathlib import Path
import sympy as sp
from sympy.combinatorics import Permutation, PermutationGroup
import w33_e8_twisted_fibration_weld as base

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_e8_pauli_normalizer.json'
R=sorted(base.e8_roots()); ridx={r:i for i,r in enumerate(R)}

def refl_root(v,r):
    dot=sum(v[i]*r[i] for i in range(8)); assert dot%4==0; q=dot//4
    return tuple(v[i]-q*r[i] for i in range(8))
def perm_refl(r): return Permutation([ridx[refl_root(v,tuple(r))] for v in R])
def rank_mod(rows):
    A=[[x%3 for x in r] for r in rows]; rr=0
    for cc in range(4):
        p=next((i for i in range(rr,len(A)) if A[i][cc]),None)
        if p is None: continue
        A[rr],A[p]=A[p],A[rr]; inv=pow(A[rr][cc],-1,3); A[rr]=[(x*inv)%3 for x in A[rr]]
        for i in range(len(A)):
            if i!=rr and A[i][cc]:
                f=A[i][cc]; A[i]=[(A[i][j]-f*A[rr][j])%3 for j in range(4)]
        rr+=1
    return rr
def invmod(M):
    n=M.rows; aug=[[int(M[i,j])%3 for j in range(n)]+[int(i==j) for j in range(n)] for i in range(n)]
    r=0
    for cc in range(n):
        p=next(i for i in range(r,n) if aug[i][cc]%3); aug[r],aug[p]=aug[p],aug[r]
        iv=pow(aug[r][cc],-1,3); aug[r]=[(x*iv)%3 for x in aug[r]]
        for i in range(n):
            if i!=r and aug[i][cc]%3:
                f=aug[i][cc]; aug[i]=[(aug[i][j]-f*aug[r][j])%3 for j in range(2*n)]
        r+=1
    return sp.Matrix([row[n:] for row in aug])

def main(write=True):
    gens=[perm_refl(r) for r in base.SIMPLE_ROOTS]
    W=PermutationGroup(gens); assert W.order()==696729600
    c=gens[0]
    for s in gens[1:]: c=c*s
    assert c.order()==30
    g=c**10; assert g.order()==3 and len(g.cyclic_form)==80
    C=W.centralizer(g); assert C.order()==155520

    target=~g; dq=deque([g]); parent={g:(None,None)}
    while dq:
        x=dq.popleft()
        if x==target: break
        for j,s in enumerate(gens):
            y=(~s)*x*s
            if y not in parent: parent[y]=(x,j); dq.append(y)
    assert target in parent
    word=[]; x=target
    while parent[x][0] is not None:
        prev,j=parent[x]; word.append(j); x=prev
    word=word[::-1]
    h=Permutation(list(range(240)))
    for j in word: h=h*gens[j]
    assert h.order()==2 and (~h)*g*h==~g
    N=PermutationGroup(C.generators+[h]); assert N.order()==311040

    entries=[]
    for k in range(4):
        d=json.loads((ROOT/'data'/f'w33_e8_pauli_cocycle_lift_entries_{k:02d}.json').read_text())
        entries.extend(d['entries'])
    entries=sorted(entries,key=lambda e:e['orbit_index']); assert len(entries)==80
    orbits=[tuple(tuple(r) for r in e['root_cycle']) for e in entries]
    labels=[tuple(e['pauli_degree']) for e in entries]
    oid={r:i for i,o in enumerate(orbits) for r in o}; assert len(oid)==240
    def orbit_perm(x): return Permutation([oid[R[x(ridx[o[0]])]] for o in orbits])
    C80=PermutationGroup([orbit_perm(x) for x in C.generators])
    N80=PermutationGroup([orbit_perm(x) for x in C.generators]+[orbit_perm(h)])
    assert C80.order()==51840 and N80.order()==103680
    assert C.order()//C80.order()==3 and N.order()//N80.order()==3

    basis=[]
    for i,v in enumerate(labels):
        if rank_mod([labels[j] for j in basis]+[v])>len(basis): basis.append(i)
        if len(basis)==4: break
    B=sp.Matrix([labels[i] for i in basis]); Bi=invmod(B)
    J=sp.Matrix([[0,2,0,0],[1,0,0,0],[0,0,0,2],[0,0,1,0]])
    def matrix_of(x):
        pp=orbit_perm(x); images=sp.Matrix([labels[pp(i)] for i in basis]); A=(Bi*images).applyfunc(lambda z:int(z)%3)
        for i,v in enumerate(labels):
            assert tuple(int(z)%3 for z in (sp.Matrix([v])*A))==labels[pp(i)]
        return A
    Cmat=[matrix_of(x) for x in C.generators]
    assert all((A*J*A.T-J).applyfunc(lambda z:int(z)%3)==sp.zeros(4) for A in Cmat)
    H=matrix_of(h); assert (H*J*H.T+J).applyfunc(lambda z:int(z)%3)==sp.zeros(4)

    out={'schema':'w33.e8_pauli_normalizer.v1','status':'PASS',
      'headline':'The Weyl normalizer of the canonical order-3 E8 twist induces exactly the extended two-qutrit Pauli grading symmetry: C_W(E8)(g)/<g> ~= Sp(4,3) of order 51840, and adjoining an explicit involution h with hgh^-1=g^-1 doubles it to an anti-symplectic extension of order 103680.',
      'weyl':{'W_E8_order':int(W.order()),'coxeter_order':int(c.order()),'g':'c^10','g_order':int(g.order()),'g_root_orbits':80,'centralizer_order':int(C.order()),'normalizer_order':int(N.order()),'reverser_simple_reflection_word_zero_based':word,'reverser_word_length':len(word),'reverser_order':int(h.order())},
      'oriented_80_degree_action':{'centralizer_image_order':int(C80.order()),'normalizer_image_order':int(N80.order()),'kernel_order':3,'kernel':'<g>','centralizer_identification':'Sp(4,3)','normalizer_identification':'Sp(4,3).2 anti-symplectic extension'},
      'forms':{'pauli_coordinate_order':['x1','z1','x2','z2'],'symplectic_matrix_mod3':[list(map(int,J.row(i))) for i in range(4)],'centralizer_generators_symplectic':True,'reverser_matrix_mod3':[list(map(int,H.row(i))) for i in range(4)],'reverser_is_anti_symplectic':True},
      'checks':{'W_E8_order':int(W.order())==696729600,'centralizer_155520':C.order()==155520,'normalizer_311040':N.order()==311040,'explicit_involutory_reverser':h.order()==2 and (~h)*g*h==~g,'80_degree_centralizer_image_51840':C80.order()==51840,'80_degree_normalizer_image_103680':N80.order()==103680,'kernel_is_order3':C.order()//C80.order()==3 and N.order()//N80.order()==3,'all_centralizer_generators_symplectic':True,'reverser_anti_symplectic':True}}
    assert all(out['checks'].values())
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out
if __name__=='__main__': main(True)
