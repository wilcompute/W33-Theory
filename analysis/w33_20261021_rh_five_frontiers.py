#!/usr/bin/env python3
"""Five independent, falsifiable RH-adjacent W33 experiments (2026-10-21).

Exact finite graph/Hecke arithmetic plus toy negative controls and a bounded
infinite diagonal scaffold. NOT a proof of the classical Riemann hypothesis.
Run from the repository root: python analysis/w33_20261021_rh_five_frontiers.py
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis.w33_pass4461_line_signing_apartment_trace import geometry

def hecke():
    def s3(n):return sum(d**3 for d in range(1,n+1) if n%d==0)
    primes=(2,3,5,7,11)
    for p in primes:
        for n in range(1,241):
            assert s3(p*n)+(p**3*s3(n//p) if n%p==0 else 0)==(1+p**3)*s3(n)
    return {"status":"PASS","identities":1200,
            "normalized_E4_Hecke_eigenvalues":{str(p):1+p**3 for p in primes},
            "boundary":"E4's one-dimensional Hecke eigenline does not construct a nonconstant W33 intertwiner."}

def rank_certificate(T,Q,indices,degree,prime=101):
    """Integer Krylov columns independent modulo prime => independent over Q."""
    pivots={}
    for i in indices:
        v=np.zeros(160,dtype=np.int64)
        if i<80:v[:80]=Q[:,i]
        else:v[80:]=Q[:,i-80]
        for _ in range(degree):
            w=v.copy()%prime
            for p in sorted(pivots):
                if w[p]:w=(w-w[p]*pivots[p])%prime
            nz=np.flatnonzero(w)
            assert len(nz)>0,("Krylov rank failure",i)
            p=int(nz[0]);pivots[p]=(w*pow(int(w[p]),-1,prime))%prime
            v=T@v
    return len(pivots)

def levi():
    _,_,A,N,_=geometry()
    I=np.eye(80,dtype=np.int64)
    O=np.zeros((40,40),dtype=np.int64)
    L=np.block([[O,N],[N.T,O]])
    L2=L@L
    P16=(L2@(L2-6*I))/160.
    P6=(L2@(16*I-L2))/60.
    P0=((L2-6*I)@(L2-16*I))/96.
    assert np.allclose(P16+P6+P0,I)
    assert all(np.allclose(P@P,P) for P in (P16,P6,P0))
    ranks=[int(round(np.trace(P))) for P in (P16,P6,P0)]
    assert ranks==[2,48,30]
    T=np.block([[L,-3*I],[I,np.zeros((80,80),dtype=np.int64)]])
    T2=T@T;T4=T2@T2
    Q6=L2@(16*I-L2)
    Q0=(L2-6*I)@(L2-16*I)
    P6b=np.block([[P6,np.zeros_like(P6)],[np.zeros_like(P6),P6]])
    P0b=np.block([[P0,np.zeros_like(P0)],[np.zeros_like(P0),P0]])
    assert np.max(abs((T4+9*np.eye(160))@P6b))<1e-9
    assert np.max(abs((T2+3*np.eye(160))@P0b))<1e-9
    g4=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,21,22,28,30,31]
    g2=[0,1,2,3,4,5,6,7,8,9,10,12,13,14,18,40,41,42,44,45,47,48,50,51,53,54,56,57,59,60]
    assert rank_certificate(T,Q6,g4,4)==96
    assert rank_certificate(T,Q0,g2,2)==60
    return {"status":"PASS","vertex_projector_ranks":ranks,
            "nontrivial_transfer_dimension":156,
            "quartic_rational_companion_blocks":24,
            "quadratic_rational_companion_blocks":30,
            "rank_mod_101":[96,60],
            "krylov_generators_quartic":g4,"krylov_generators_quadratic":g2,
            "local_frobenius_models":["x^4+9 (C/F3 genus 2)","x^2+3 (E/F3 elliptic)"],
            "boundary":"Constructive rational companion equivalence, not a canonical geometric/Galois-equivariant map or global L-function equality."}

def weil_negative_control():
    _,_,A,N,_=geometry()
    gamma=14.;delta=.2;a=2*math.pi/gamma
    # Spectral-side finite quartet Q(f)=sum_{z=+-gamma+-i delta} f(z)f(-z).
    K=np.array([[4*math.cos((x-y)*gamma)*math.cosh((x-y)*delta)
                 for y in (0.,a)] for x in (0.,a)])
    ev=np.linalg.eigvalsh(K)
    assert ev[0]<0<ev[1]
    I=np.eye(40);J=np.ones((40,40))
    P2=(2/3)*I+(1/6)*A-(1/15)*J
    Pm4=(1/3)*I-(1/6)*A+(1/24)*J
    assert np.allclose(P2@P2,P2) and np.allclose(Pm4@Pm4,Pm4)
    assert [int(round(np.trace(x))) for x in (P2,Pm4)]==[24,15]
    return {"status":"PASS","toy_ordinate_quartet":"z=+-14 +-0.2i",
            "off_line_kernel_eigenvalues":ev.tolist(),"on_line_kernel_eigenvalues":[0,8],
            "negative_directions_after_tensor_projector":[24,15],
            "boundary":"Toy spectral quartet only; full Weil prime/gamma/pole terms are not evaluated."}

def signed_levi():
    _,_,_,N,_=geometry()
    O=np.zeros((40,40),dtype=np.int64)
    L=np.block([[O,N],[N.T,O]])
    C=L.copy()
    j=40+int(np.flatnonzero(N[0])[0])
    C[0,j]=C[j,0]=-1
    sig=np.ones(80,dtype=np.int64);sig[0]=-1
    gauge=sig[:,None]*L*sig[None,:]
    tr0=int(np.trace(np.linalg.matrix_power(L,8)))
    tr1=int(np.trace(np.linalg.matrix_power(C,8)))
    trg=int(np.trace(np.linalg.matrix_power(gauge,8)))
    assert (tr0,tr1,trg)==(193280,190688,193280)
    radius=float(np.abs(np.linalg.eigvalsh(C)).max())
    assert radius>2*math.sqrt(3)
    return {"status":"PASS","Levi_apartments":1620,
            "apartments_per_edge":81,"unsigned_trace_A8":tr0,
            "one_edge_flip_trace_A8":tr1,"exact_trace_defect":tr0-tr1,
            "gauge_trace_defect":tr0-trg,"signed_radius":radius,
            "pure_weight_1_bound":2*math.sqrt(3),
            "boundary":"A graph sign character need not be Weil-tempered or a geometric Frobenius sheaf."}

def infinite_scaffold():
    mp.mp.dps=30
    t=lambda n:float(2*mp.pi*(mp.mpf(n)-mp.mpf(7)/8)/mp.lambertw((mp.mpf(n)-mp.mpf(7)/8)/mp.e))
    nmax=5000
    base=np.array([t(n) for n in range(1,nmax+1)])
    th1=math.acos(1/math.sqrt(11))
    th2=math.acos(-2/math.sqrt(11))
    shift=np.array([.05*(24*math.cos(n*th1)+15*math.cos(n*th2))/39 for n in range(1,nmax+1)])
    pert=base+shift
    actual=np.array([float(mp.im(mp.zetazero(n))) for n in range(1,21)])
    # Monotonicity below n=5000 is a finite check, not a global theorem.
    assert np.all(np.diff(pert)>0)
    counts=[]
    for T in (30,100,500,1000):
        counts.append({"height":T,"baseline":int(np.searchsorted(base,T)),
                       "perturbed":int(np.searchsorted(pert,T))})
    return {"status":"PASS","bounded_shift_max":float(np.max(np.abs(shift))),
            "mean_first20_relative_error_unperturbed":float(np.mean(abs(base[:20]-actual)/actual)),
            "mean_first20_relative_error_perturbed":float(np.mean(abs(pert[:20]-actual)/actual)),
            "finite_counting_checks":counts,
            "theorem":"Real diagonal on l2(N); t_n -> infinity and shift bounded, hence compact resolvent and correct leading T log T counting asymptotics.",
            "boundary":"No exact zeta zero spectrum or Xi determinant. Chosen scalar phases must not be read as a proof."}

def build_certificate():
    fronts={"E8_Hecke":hecke(),"Levi_Frobenius":levi(),
            "Weil_negative_control":weil_negative_control(),
            "Artin_Ihara_signed":signed_levi(),
            "infinite_scaffold":infinite_scaffold()}
    assert all(x["status"]=="PASS" for x in fronts.values())
    return {"status":"PASS","date":"2026-10-21","classical_RH_proved":False,
            "note":"PASS means scoped finite tests only, not RH.",
            "frontiers":fronts}

if __name__=="__main__":
    result=build_certificate()
    dest=ROOT/"data"/"w33_20261021_rh_five_frontiers.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    print("wrote",dest)
