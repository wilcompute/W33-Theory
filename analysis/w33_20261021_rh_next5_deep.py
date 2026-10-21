#!/usr/bin/env python3
"""2026-10-21 five RH frontiers: finite exact proofs and analytic falsifiers.
Run: PYTHONPATH=. python analysis/w33_20261021_rh_next5_deep.py
The classical Riemann hypothesis is NOT proved.
"""
import itertools, math, json
from pathlib import Path
from collections import Counter
import numpy as np
import mpmath as mp
from analysis.w33_pass4461_line_signing_apartment_trace import geometry

ROOT=Path(__file__).resolve().parents[1]

def insert(v,piv,mod=101):
    y=v.astype(np.int64)%mod
    for i,b in piv.items():
        if y[i]: y=(y-y[i]*b)%mod
    inds=np.flatnonzero(y)
    if len(inds)==0:return False
    j=int(inds[0]);piv[j]=y*pow(int(y[j]),-1,mod)%mod
    return True

def levi_conjugator():
    pts,lines,A,N,edge_line=geometry()
    I=np.eye(80,dtype=np.int64); Z=np.zeros((40,40),dtype=np.int64)
    L=np.block([[Z,N],[N.T,Z]]);D=L@L
    T=np.block([[L,-3*I],[I,np.zeros((80,80),dtype=np.int64)]])
    def blocks(Q,d,goal):
        piv={}; cols=[];gen=[]
        for r in range(160):
            v=np.zeros(160,dtype=np.int64)
            if r<80:v[:80]=Q[:,r]
            else:v[80:]=Q[:,r-80]
            cand=[]
            for _ in range(d):cand.append(v);v=T@v
            trial=dict(piv)
            if not all(insert(w,trial) for w in cand):continue
            piv=trial;cols+=cand;gen.append(r)
            if len(cols)==goal:break
        assert len(cols)==goal
        return np.column_stack(cols),gen
    S4,g4=blocks(D@(16*I-D),4,96)
    S2,g2=blocks((D-6*I)@(D-16*I),2,60)
    S=np.column_stack((S4,S2))
    C=np.zeros((156,156),dtype=np.int64)
    for k in range(0,96,4):
        C[k+1,k]=C[k+2,k+1]=C[k+3,k+2]=1;C[k,k+3]=-9
    for k in range(96,156,2):C[k+1,k]=1;C[k,k+1]=-3
    assert np.array_equal(T@S,S@C)
    # An actual W33 symplectic transvection generates an automorphism.
    def norm(v):
        f=next(x for x in v if x)
        return tuple(f*x%3 for x in v)
    pindex={x:i for i,x in enumerate(pts)}
    def trans(x):return norm(((x[0]-x[1])%3,x[1],x[2],x[3]))
    pp=[pindex[trans(x)] for x in pts]
    lindex={frozenset(ln):j for j,ln in enumerate(lines)}
    ll=[lindex[frozenset(pp[i] for i in ln)] for ln in lines]
    perm=pp+[40+i for i in ll]
    assert sorted(perm)==list(range(80))
    G=np.zeros((160,160),dtype=np.int64)
    for i,j in enumerate(perm):G[j,i]=G[j+80,i+80]=1
    assert np.array_equal(T@G,G@T)
    # Simultaneously solve S H = G S modulo 101 and ensure C H = H C.
    p=101;aug=np.column_stack((S%p,(G@S)%p));n=156
    for k in range(n):
        q=np.flatnonzero(aug[k:,k]); assert len(q)
        j=k+int(q[0]);aug[[j,k]]=aug[[k,j]]
        aug[k]=(aug[k]*pow(int(aug[k,k]),-1,p))%p
        rows=np.flatnonzero(aug[:,k]); rows=rows[rows!=k]
        aug[rows]=(aug[rows]-aug[rows,k,None]*aug[k,None,:])%p
    H=aug[:n,n:]
    assert not np.any(aug[n:,n:])
    assert np.array_equal((S@H)%p,(G@S)%p)
    assert np.array_equal((H@C)%p,(C@H)%p)
    return {"rank":156,"companion_blocks":{"x4_plus9":24,"x2_plus3":30},
       "generator_seeds":{"quartic":g4,"quadratic":g2},"integer_TS_equals_SC":True,
       "symplectic_transvection_intertwiner_mod101":True,
       "limitations":"Explicit rational module, not a canonical geometric/Galois-equivariant curve correspondence."}

def hecke_obstruction():
    _,_,A,_,_=geometry();I=np.eye(40);J=np.ones((40,40))
    P1=J/40;P2=2*I/3+A/6-J/15;Pm=I/3-A/6+J/24
    assert [round(np.trace(P)) for P in (P1,P2,Pm)]==[1,24,15]
    assert all(np.max(abs(P@P-P))<1.e-12 for P in (P1,P2,Pm))
    assert max(abs(P2@np.ones(40)))<1.e-12 and max(abs(Pm@np.ones(40)))<1.e-12
    return {"E4_Hecke_eigenvalues":{str(p):1+p**3 for p in (2,3,5,7,11)},
      "Hom_G_of_trivial_E4_line_into_W33_nonconstant":0,
      "limitations":"Only rules out a full-Sp(4,3)-equivariant map from the trivial E4 eigenline; nontrivial arithmetic coefficients could transform under a different representation."}

def apartment_holonomy():
    _,_,A,N,edge_line=geometry()
    flags=[(i,j) for i in range(40) for j in range(40) if N[i,j]]
    findex={f:i for i,f in enumerate(flags)}
    cycles=set()
    for a,b in itertools.combinations(range(40),2):
        if A[a,b]:continue
        common=[k for k in range(40) if A[a,k] and A[b,k]]
        for c,d in itertools.combinations(common,2):
            cycles.add(frozenset((frozenset((a,c)),frozenset((c,b)),
                                   frozenset((b,d)),frozenset((d,a)))))
    assert len(cycles)==1620
    basis={}; occ=Counter(); pairs=Counter()
    for cy in cycles:
        fi=set()
        for e in cy:
            p,q=tuple(e);j=edge_line[e]
            fi.add(findex[p,j]);fi.add(findex[q,j])
        assert len(fi)==8
        w=sorted(fi);occ.update(w);pairs.update(itertools.combinations(w,2))
        mask=sum(1<<i for i in w)
        while mask:
            lead=mask.bit_length()-1
            if lead in basis:mask^=basis[lead]
            else:basis[lead]=mask;break
    assert len(basis)==160-80+1==81
    assert set(occ.values())=={81}
    hist=Counter()
    for i,j in itertools.combinations(range(160),2):
        hist[162-2*pairs[i,j]]+=1
    assert sum(hist.values())==12720
    return {"octagons":1620,"cycle_space_GF2_rank":81,
       "octagon_linear_relations":1620-81,"every_incidence_edge_in_octagons":81,
       "single_sign_flip_frustrates":81,"two_edge_flip_histogram":dict(sorted(hist.items())),
       "conclusion":"Octagon holonomies determine every Z2 graph character up to vertex gauge, because they span H1."}

def spectral_determinant():
    mp.mp.dps=40;N=1200
    th2=float(mp.acos(1/mp.sqrt(11)));thm=float(mp.acos(-2/mp.sqrt(11)))
    t=lambda n:float(2*mp.pi*(mp.mpf(n)-mp.mpf(7)/8)/mp.lambertw((mp.mpf(n)-mp.mpf(7)/8)/mp.e))
    lam=np.array([t(i) for i in range(1,N+1)])
    delta=np.array([.05*(24*math.cos(i*th2)+15*math.cos(i*thm))/39 for i in range(1,N+1)])
    def xi(s):return mp.mpf('.5')*s*(s-1)*mp.pi**(-s/2)*mp.gamma(s/2)*mp.zeta(s)
    heights=[2,5,10,12]
    true=[float(mp.log(mp.re(xi(mp.mpf('.5')+1j*z)/xi(mp.mpf('.5'))))) for z in heights]
    def logs(a):return [float(np.log1p(-(z/a)**2).sum()) for z in heights]
    base=logs(lam);mod=logs(lam+delta)
    zeros=np.array([float(mp.im(mp.zetazero(i))) for i in range(1,61)])
    moments={str(k):{"baseline":float(sum(lam**(-k))),
             "modulated":float(sum((lam+delta)**(-k))),
             "actual_first60_lower_bound":float(sum(zeros**(-k)))} for k in (2,4,6)}
    return {"N":N,"test_z":heights,"log_Xi_ratio":true,"baseline_log_finite_products":base,
       "W33_log_finite_products":mod,"baseline_error":[abs(x-y) for x,y in zip(true,base)],
       "W33_error":[abs(x-y) for x,y in zip(true,mod)],
       "inverse_moments":moments,
       "limitations":"Finite product includes only 1200 positive ordinates; no Xi determinant equality or exact zero matching."}

def completed_weil_galerkin():
    # Real even Schwartz Fourier tests, h_ij(t)=F_i(t)F_j(t).
    # Evaluate FULL pole + prime + archimedean formula and compare with known zero side.
    mp.mp.dps=40;a=mp.mpf('.07');w=[mp.mpf(x) for x in (0,7,14)]
    F=lambda u,z:mp.exp(-a*(z-u)**2)+mp.exp(-a*(z+u)**2)
    def g(x,u,v):
        fac=mp.sqrt(mp.pi/(2*a))/(2*mp.pi)*mp.exp(-x*x/(8*a))
        return fac*sum(mp.exp(-a*(e*u-d*v)**2/2)*mp.cos((e*u+d*v)*x/2)
                       for e in (-1,1) for d in (-1,1))
    lim=1000;von=[0.]*(lim+1)
    for p in range(2,lim+1):
        if all(p%d for d in range(2,math.isqrt(p)+1)):
            n=p
            while n<=lim:von[n]=math.log(p);n*=p
    zeros=[mp.im(mp.zetazero(i)) for i in range(1,65)]
    B=np.zeros((3,3));Z=np.zeros((3,3))
    for i in range(3):
      for j in range(i+1):
        pole=2*mp.re(F(w[i],.5j)*F(w[j],.5j))
        prime=mp.fsum(mp.mpf(str(von[n]))/mp.sqrt(n)*g(mp.log(n),w[i],w[j])
                      for n in range(2,lim+1) if von[n])
        def integral(t):
            return F(w[i],t)*F(w[j],t)*(mp.re(mp.digamma(mp.mpf('.25')+.5j*t))-mp.log(mp.pi))/mp.pi
        arch=mp.quad(integral,[0,6,12,18,25,35,50,80])
        x=pole-2*prime+arch
        y=2*mp.fsum(F(w[i],v)*F(w[j],v) for v in zeros)
        B[i,j]=B[j,i]=float(x);Z[i,j]=Z[j,i]=float(y)
    discrepancy=float(max(abs((B-Z).flat)))
    assert discrepancy<1.e-9,discrepancy
    eigen=np.linalg.eigvalsh(B)
    assert eigen[0]>-1e-10
    return {"basis_Fourier_centers":[0,7,14],"gaussian_a":.07,
        "prime_power_cutoff":lim,"spectral_zero_side_count":64,
        "completed_Weil_matrix":B.tolist(),"known_zero_Gram_matrix":Z.tolist(),
        "max_difference":discrepancy,"eigenvalues":eigen.tolist(),
        "limitations":"Numerical finite-dimensional Schwartz test, not interval-certified or an arbitrary-test positivity theorem."}

def build():
    out={"classical_RH_proved":False,"five_frontiers":{
      "Levi_exact":levi_conjugator(),"Hecke_obstruction":hecke_obstruction(),
      "apartment_holonomy":apartment_holonomy(),"spectral_determinant":spectral_determinant(),
      "completed_Weil":completed_weil_galerkin()}}
    assert out["five_frontiers"]["Levi_exact"]["rank"]==156
    return out

if __name__=="__main__":
    payload=build()
    dest=ROOT/"data"/"w33_20261021_rh_next5_deep.json"
    dest.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print("PASS all five scoped RH experiments; classical RH unproved. Wrote",dest)
