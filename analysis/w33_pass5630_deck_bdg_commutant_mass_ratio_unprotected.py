#!/usr/bin/env python3
"""Pass5630: classify symmetry-allowed perturbations of the signed deck16 Hamiltonian.

Using the exact 96-element vector stabilizer from Pass5627, the deck-odd magnetic
module splits over C as 2A + 2Abar, where A and Abar are non-isomorphic conjugate
irreducible 4-dimensional modules.  Hence the equivariant complex commutant has
dimension 2^2+2^2=8.

For Hermitian Hamiltonians with K H K^{-1}=-H (K=complex conjugation), the
stabilizer-equivariant perturbation space is the purely imaginary Hermitian part,
i times the real skew-symmetric commutant.  Its real dimension is 4.  Therefore
the Pass5622 ratio 6/3=2 is not protected by deck parity + K + carrier symmetry
alone.  This verifier constructs an explicit allowed perturbation that moves it.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
import w33_pass5627_deck_stabilizer_spinor_no_go as core

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5630_DECK_BDG_COMMUTANT_MASS_RATIO.json'

def signed_matrix(pair):
    p,s=pair; R=np.zeros((16,16),float)
    for i,j in enumerate(p): R[j,i]=s[i]
    return R

def pair_comp(a,b):
    p,s=a;q,t=b
    return (tuple(p[q[i]] for i in range(16)),tuple(t[i]*s[q[i]] for i in range(16)))
def pair_closure(gs):
    e=(tuple(range(16)),tuple([1]*16));G={e};front=[e]
    while front:
        x=front.pop()
        for g in gs:
            y=pair_comp(g,x)
            if y not in G:G.add(y);front.append(y)
    return G

def build():
    P=core.p1(); S=[core.segre(u,v) for u in P for v in P]; si={v:i for i,v in enumerate(S)}
    seed=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0)]
    SG=core.closure_mat([core.trans_mat(v) for v in seed]); assert len(SG)==51840
    Sset=set(S); vst=[M for M in SG if {core.norm(core.apply(M,v)) for v in S}==Sset]; assert len(vst)==96
    def action(M):
        p=[];sg=[]
        for v in S:
            y=core.apply(M,v);ny=core.norm(y);p.append(si[ny]);k=next(i for i,z in enumerate(ny) if z)
            a=(y[k]*pow(ny[k],-1,3))%3;sg.append(1 if a==1 else -1)
        return tuple(p),tuple(sg)
    pairs=[action(M) for M in vst]; Rs=[signed_matrix(x) for x in pairs]
    # intrinsic 32 lift and deck-odd compression
    w=np.exp(2j*np.pi/3);vecs=[];base=[]
    for i,v in enumerate(S):
        for a in (1,2):vecs.append(tuple(a*x%3 for x in v));base.append(i)
    L=np.zeros((32,32),complex)
    for i in range(32):
        ri,ci=divmod(base[i],4)
        for j in range(i+1,32):
            rj,cj=divmod(base[j],4)
            if ri!=rj and ci!=cj:
                z=w**((2*core.B(vecs[i],vecs[j]))%3);L[i,j]=z;L[j,i]=np.conj(z)
    Q=np.zeros((32,16),complex)
    for i in range(16):Q[2*i,i]=1/np.sqrt(2);Q[2*i+1,i]=-1/np.sqrt(2)
    H=Q.conj().T@L@Q
    return pairs,Rs,H

def main():
    pairs,Rs,H=build(); assert max(np.max(abs(R@H-H@R)) for R in Rs)<1e-9
    ev,V=np.linalg.eigh(H); levels=(-6,-3,3,6)
    chars={}
    for lam in levels:
        I=np.where(abs(ev-lam)<1e-8)[0]; W=V[:,I]; assert len(I)==4
        chars[lam]=[np.trace(W.conj().T@R@W) for R in Rs]
        inn=sum(abs(z)**2 for z in chars[lam])/96; assert abs(inn-1)<1e-7
    same=lambda a,b: max(abs(chars[a][i]-chars[b][i]) for i in range(96))<1e-7
    conj=lambda a,b: max(abs(chars[a][i]-np.conj(chars[b][i])) for i in range(96))<1e-7
    assert same(-6,3) and same(-3,6) and conj(-6,6) and conj(-3,3) and not same(-6,6)

    # Greedily obtain a small generating set for the signed group.
    gens=[];cur={(tuple(range(16)),tuple([1]*16))}
    for c in pairs:
        if c not in cur:
            test=pair_closure(gens+[c])
            if len(test)>len(cur):gens.append(c);cur=test
            if len(cur)==96:break
    assert len(cur)==96
    GR=[signed_matrix(x) for x in gens]
    A=np.vstack([np.kron(R.T,np.eye(16))-np.kron(np.eye(16),R) for R in GR])
    u,s,vh=np.linalg.svd(A); nullity=int(np.sum(s<1e-9)); assert nullity==8
    N=vh[-nullity:].T
    Bs=[N[:,i].reshape(16,16,order='F') for i in range(nullity)]
    sym=np.column_stack([((X+X.T)/2).reshape(-1,order='F') for X in Bs])
    skw=np.column_stack([((X-X.T)/2).reshape(-1,order='F') for X in Bs])
    symdim=int(np.linalg.matrix_rank(sym,1e-8)); skwdim=int(np.linalg.matrix_rank(skw,1e-8))
    assert (symdim,skwdim)==(4,4)

    # Explicit independent K-odd equivariant perturbation by Reynolds averaging.
    E=np.zeros((16,16),float);E[0,4]=1;E[4,0]=-1
    S1=sum(R@E@R.T for R in Rs); assert np.linalg.norm(S1)>1e-9
    assert max(np.max(abs(R@S1-S1@R)) for R in Rs)<1e-9 and np.max(abs(S1+S1.T))<1e-9
    S0=(-1j*H).real
    corr=abs(np.vdot(S0.ravel(),S1.ravel()))/(np.linalg.norm(S0)*np.linalg.norm(S1)); assert corr<1e-9
    eps=.1; Hp=H+1j*eps*S1
    pev=np.linalg.eigvalsh(Hp); pos=[x for x in pev if x>1e-8]
    vals=[]
    for x in pos:
        if not vals or abs(x-vals[-1])>1e-6:vals.append(float(x))
    assert len(vals)==2
    ratio=vals[1]/vals[0]; assert abs(ratio-2)>1e-3

    out={
      'pass':5630,'status':'DECK16_COMMUTANT_IS_2A_PLUS_2ABAR_AND_MASS_RATIO_TWO_IS_UNPROTECTED',
      'module_decomposition':'2 A + 2 Abar, dim(A)=4, A irreducible and non-real',
      'eigenspace_module_pattern':{'-6':'A','-3':'Abar','3':'A','6':'Abar'},
      'complex_commutant_dimension':nullity,'real_symmetric_commutant_dimension':symdim,'real_skew_commutant_dimension':skwdim,
      'PHS_compatible_equivariant_Hamiltonians':'i times the 4-real-dimensional skew commutant',
      'explicit_perturbation':{'epsilon':eps,'positive_levels':vals,'mass_ratio':ratio,'unperturbed_ratio':2.0},
      'theorem':'Deck parity, K particle-hole symmetry and the full 96-element vector carrier stabilizer do not uniquely select H_mag. Four real equivariant K-odd directions exist, and an explicit one moves the 6/3 ratio away from 2.',
      'physics_boundary':'Pass5622 remains a property of the chosen intrinsic magnetic operator, not a symmetry-protected Standard Model mass prediction.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
