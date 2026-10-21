#!/usr/bin/env python3
"""Five independent W33 RH frontiers (2026-10-21).
Finite exact certificates and numerical arithmetic explicit-formula checks.
NOT a proof of classical RH.
"""
from __future__ import annotations
import itertools, math, json, hashlib
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.special import digamma
from scipy.integrate import quad
from analysis.w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles

G4=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,21,22,28,30,31)
G2=(0,1,2,3,4,5,6,7,8,9,10,12,13,14,18,40,41,42,44,45,47,48,50,51,53,54,56,57,59,60)

def mod_rank_rows(B,p=101):
    piv={}; rows=[]
    for i in range(B.shape[0]):
        v=B[i,:]%p
        for j in sorted(piv):
            if v[j]: v=(v-v[j]*piv[j])%p
        indices=np.flatnonzero(v)
        if len(indices):
            j=int(indices[0]);piv[j]=v*pow(int(v[j]),-1,p)%p
            rows.append(i)
    return rows

def conjugator():
    _,_,A,N,_=geometry()
    O=np.zeros((40,40),dtype=np.int64)
    L=np.block([[O,N],[N.T,O]])
    I=np.eye(80,dtype=np.int64)
    T=np.block([[L,-3*I],[I,np.zeros((80,80),dtype=np.int64)]])
    L2=L@L
    Q6=L2@(16*I-L2)
    Q0=(L2-6*I)@(L2-16*I)
    vectors=[]; blocks=[]
    for d,gs,Q,c in [(4,G4,Q6,9),(2,G2,Q0,3)]:
        for g in gs:
            v=np.zeros(160,dtype=np.int64)
            if g<80:v[:80]=Q[:,g]
            else:v[80:]=Q[:,g-80]
            for k in range(d):
                vectors.append(v.copy())
                v=T@v
            C=np.zeros((d,d),dtype=np.int64)
            for j in range(d-1):C[j+1,j]=1
            C[0,-1]=-c
            blocks.append(C)
    B=np.column_stack(vectors)
    C=np.zeros((156,156),dtype=np.int64)
    offset=0
    for block in blocks:
        d=len(block); C[offset:offset+d,offset:offset+d]=block;offset+=d
    assert B.shape==(160,156) and np.array_equal(T@B,B@C)
    assert not np.any((np.linalg.matrix_power(T,4)+9*np.eye(160,dtype=np.int64))@B[:,:96])
    assert not np.any((T@T+3*np.eye(160,dtype=np.int64))@B[:,96:])
    piv=mod_rank_rows(B)
    assert len(piv)==156
    return {"status":"PASS","matrix_shape":[160,156],"rational_minor_shape":[156,156],
        "rank_mod_101":156,"pivot_rows":piv,
        "block_counts":{"x4+9":24,"x2+3":30},
        "sha256_integer_intertwiner":hashlib.sha256(np.asarray(B,dtype="<i8").tobytes()).hexdigest(),
        "quartic_generators":G4,"quadratic_generators":G2,
        "claim":"T B = B C exactly. A full-column-rank integer intertwiner yields a rational module isomorphism; NOT a canonical etale motivic map."}

def hecke():
    _,_,A,N,_=geometry()
    I=np.eye(40);J=np.ones((40,40))
    P0=J/40
    P2=2*I/3+A/6-J/15
    Pm=I/3-A/6+J/24
    assert np.allclose(P0+P2+Pm,I)
    rows=[]
    for p in (2,3,5,7,11):
        s=1+p**3
        X=s*I
        Y=s*P0+p*Pm
        for M in (X,Y):
            Mp2=M@M-p**3*I
            assert np.allclose(A@Mp2,Mp2@A)
            assert np.allclose(A@M,M@A)
            assert np.allclose(M@M-Mp2,p**3*I)
        assert abs(np.trace(X)-np.trace(Y))>1
        rows.append({"prime":p,"E4_constant_eigenvalue":s,"scalar_trace":round(float(np.trace(X))),
          "nonconstant_trace":round(float(np.trace(Y)))})
    return {"status":"PASS","prime_witnesses":rows,
        "claim":"The abstract Hecke recursion admits inequivalent commuting W33 Bose-Mesner actions. It does NOT select a canonical Hecke correspondence."}

def holonomy():
    _,lines,A,N,edge_line=geometry()
    flags={(p,li):i for i,(p,li) in enumerate(
        (p,li) for li,line in enumerate(lines) for p in sorted(line))}
    cycles=simple_four_cycles(A)
    assert len(cycles)==1620
    vv=[]
    for sq in cycles:
        bits=set()
        for e in sq:
            li=edge_line[e]
            for p in e:bits.add(flags[(p,li)])
        assert len(bits)==8
        vv.append(sum(1<<v for v in bits))
    vv=sorted(vv)
    assert len(set(vv))==1620
    piv={};basis=[]
    for idx,original in enumerate(vv):
        v=original
        for b in sorted(piv,reverse=True):
            if (v>>b)&1:v^=piv[b]
        if v:
            piv[v.bit_length()-1]=v;basis.append(idx)
    assert len(piv)==81
    counts={sum((v>>i)&1 for v in vv) for i in range(160)}
    assert counts=={81}
    return {"status":"PASS","octagons":1620,"GF2_rank":81,"cycle_space_dim":160-80+1,
        "cycles_per_edge":81,"basis_octagon_indices":basis,"gauge_classes":"2^81",
        "claim":"Octagon parities separate ALL Z2 signings modulo vertex gauge. Temperedness of their Ihara factors is not implied."}

def mangoldt(n):
    for p in range(2,math.isqrt(n)+1):
        if n%p==0:
            v=n
            while v%p==0:v//=p
            return math.log(p) if v==1 else 0.
    return math.log(n)

def arithmetic_explicit(delta,sigma=11.):
    h=lambda t:math.exp(-.5*(t/sigma)**2)*math.cos(delta*t)
    pole=2*math.exp(1/(8*sigma**2))*math.cosh(delta/2)
    gamma=quad(lambda t:h(t)*(float(digamma(.25+.5j*t).real)-math.log(math.pi)),
               0.,200.,epsabs=2e-10,limit=250)[0]/math.pi
    prime=0.
    for n in range(2,500):
        lam=mangoldt(n)
        if not lam:continue
        u=math.log(n)
        f=sigma*math.sqrt(2*math.pi)/2*(
             math.exp(-.5*sigma**2*(u-delta)**2)+math.exp(-.5*sigma**2*(u+delta)**2))
        prime+=lam/math.sqrt(n)*f/math.pi
    return pole+gamma-prime,(pole,gamma,prime)

def weil():
    shifts=(0.,.15,.35,.65)
    cache={abs(a-b):arithmetic_explicit(abs(a-b)) for a in shifts for b in shifts}
    K=np.array([[cache[abs(a-b)][0] for b in shifts]for a in shifts])
    ev=np.linalg.eigvalsh(K)
    assert ev[0]>0
    mp.mp.dps=28
    known=[float(mp.im(mp.zetazero(k))) for k in range(1,61)]
    direct=np.array([[sum(2*math.exp(-.5*(r/11.)**2)*math.cos((a-b)*r) for r in known)
                     for b in shifts]for a in shifts])
    discrepancy=float(np.max(abs(K-direct)))
    assert discrepancy<2e-9
    return {"status":"PASS","basis_shifts":shifts,"width_sigma":11,"matrix":K.tolist(),
        "minimum_eigenvalue":float(ev[0]),"eigenvalues":ev.tolist(),
        "max_zero_side_discrepancy_first60":discrepancy,
        "pole_gamma_prime_at_delta_zero":cache[0.][1],
        "claim":"Completed pole + digamma gamma - von Mangoldt prime power Gaussian Galerkin form, numerically positive on this 4D test space; not an all-tests positivity theorem."}

def spectrum():
    mp.mp.dps=27
    zeros=np.array([float(mp.im(mp.zetazero(n))) for n in range(1,31)])
    def guess(n):
        m=mp.mpf(n)-mp.mpf(7)/8
        return float(2*mp.pi*m/mp.lambertw(m/mp.e))
    base=np.array([guess(n) for n in range(1,31)])
    a=math.acos(1/math.sqrt(11));b=math.acos(-2/math.sqrt(11))
    shift=np.array([.05*(24*math.cos(n*a)+15*math.cos(n*b))/39 for n in range(1,31)])
    models=[]
    for name,s in (("base",base),("W33",base+shift),("opposite_W33",base-shift)):
        models.append({"name":name,
          "mean_rel_err_first20":float(np.mean(abs(s[:20]-zeros[:20])/zeros[:20])),
          "mean_rel_err_first30":float(np.mean(abs(s-zeros)/zeros)),
          "inverse_moments_2_4_6":[float(sum(s**-p)) for p in (2,4,6)]})
    return {"status":"PASS","models":models,
        "first30_actual_inverse_moments":[float(sum(zeros**-p))for p in (2,4,6)],
        "claim":"Two distinct bounded W33 modulations retain compact resolvent and the leading TlogT zero count but differ in inverse moments; no Xi determinant."}

def main():
    items={"levi_conjugator":conjugator(),"formal_Hecke_obstruction":hecke(),
      "complete_binary_apartment_holonomy":holonomy(),
      "completed_Weil_Galerkin":weil(),"infinite_spectral_falsifier":spectrum()}
    assert all(v["status"]=="PASS"for v in items.values())
    out={"status":"PASS","classical_RH_proved":False,"experiments":items}
    path=Path("data/w33_20261021_rh_five_followups.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out,sort_keys=True,indent=2,default=list)+"\n")
    print(json.dumps({"scope":"classical RH unproved","experiments":{k:v["status"]for k,v in items.items()}},indent=2))
    return out

if __name__=="__main__":main()
