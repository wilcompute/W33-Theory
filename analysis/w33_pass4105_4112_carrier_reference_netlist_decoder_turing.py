#!/usr/bin/env python3
"""Deterministic verifier for Passes 4105-4112."""
from __future__ import annotations
import hashlib, itertools, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data/PART_4105_4112_CARRIER_REFERENCE_NETLIST_DECODER_TURING_BONKERS.json"
NET = ROOT / "data/w33_pass4107_router_fabrication_netlist.json"
CARRIER = ROOT / "data/w33_pass4105_sector_faithful_carrier.json"

def canonical_hash(d):
    x=dict(d); x.pop("semantic_sha256",None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def points_f3():
    out=set()
    for v in itertools.product(range(3), repeat=4):
        if not any(v): continue
        i=next(i for i,x in enumerate(v) if x)
        inv=1 if v[i]==1 else 2
        out.add(tuple((inv*x)%3 for x in v))
    return sorted(out)

def symp(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def w33():
    pts=points_f3(); n=len(pts)
    A=np.zeros((n,n))
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if i!=j and symp(u,v)==0: A[i,j]=1
    return A

def anomaly_checks():
    su3sq = 2*Fraction(1,6)+Fraction(-2,3)+Fraction(1,3)
    su2sq = 3*Fraction(1,6)+Fraction(-1,2)
    grav = 6*Fraction(1,6)+3*Fraction(-2,3)+3*Fraction(1,3)+2*Fraction(-1,2)+1
    u1c = 6*Fraction(1,6)**3+3*Fraction(-2,3)**3+3*Fraction(1,3)**3+2*Fraction(-1,2)**3+1
    return su3sq,su2sq,grav,u1c

def phase_terms(K,m,phi):
    th=math.pi/(K+2)
    c=np.array([math.sqrt(2/(K+2))*math.sin((n+1)*th) for n in range(K+1)])
    C=float(np.dot(c[:K+1-m],c[m:]))
    B=float(sum(c[n]*c[m-1-n] for n in range(m)))
    z=np.exp(1j*m*phi)*C+np.exp(-1j*(K+1-m)*phi)*B
    closed=((K+1-m)*math.cos(m*th)+math.sin((m+1)*th)/math.sin(th))/(K+2)
    return C,B,z,closed

def nonlinear(A,J,T=500.0):
    L=12*np.eye(40)-A
    evals,Q=np.linalg.eigh(L)
    rng=np.random.default_rng(42)
    y0=1e-3*rng.normal(size=80)
    y0[:40]-=y0[:40].mean(); y0[40:]-=y0[40:].mean()
    a,b=J[0]; c,d=J[1]
    def rhs(t,y):
        u=y[:40]; v=y[40:]
        return np.r_[a*u+b*v-u**3-0.1*(L@u), c*u+d*v-v**3-10.0*(L@v)]
    sol=solve_ivp(rhs,(0,T),y0,method="BDF",rtol=1e-8,atol=1e-10)
    assert sol.success
    u=sol.y[:40,-1]; coeff=Q.T@u
    energies={lam:float(np.sum(coeff[np.isclose(evals,lam)]**2)) for lam in (0,10,16)}
    return energies,float(np.linalg.norm(rhs(T,sol.y[:,-1])))

def main():
    cert=json.loads(CERT.read_text(encoding="utf-8"))
    assert canonical_hash(cert)==cert["semantic_sha256"]
    carrier=json.loads(CARRIER.read_text(encoding="utf-8"))
    assert carrier["candidate_99"]["dimension"]==6+3*15+2*24==99
    assert carrier["corrected_145"]["dimension"]==7+6*15+2*24==145
    assert anomaly_checks()==(Fraction(0),Fraction(0),Fraction(0),Fraction(0))
    net=json.loads(NET.read_text(encoding="utf-8"))
    assert sum(b["parallel_swap_cells"] for b in net["branches"])==160
    assert net["recirculating_qsp"]["swap_cells"]==160
    assert net["spatially_unrolled_qsp"]["swap_cells"]==800
    phi=math.atan2(3,-4)
    for m in (1,5,10,20):
        C,B,z,closed=phase_terms(256,m,phi)
        assert abs(C-closed)<1e-13 and B>=0
        stored=cert["pass4106_multiuse_sine_reference"]["samples_K256"][f"N{m}"]
        assert abs(abs(z-np.exp(1j*m*phi))-stored)<2e-13
    assert abs(2*math.sin(math.pi/14)-0.4450418679126288)<1e-15
    assert 1+160+math.comb(160,2)+math.comb(160,3)==682641
    A=w33(); L=12*np.eye(40)-A
    assert np.allclose(A.sum(axis=1),12)
    vals=np.linalg.eigvalsh(L)
    assert sum(np.isclose(vals,0))==1 and sum(np.isclose(vals,10))==24 and sum(np.isclose(vals,16))==15
    P=np.eye(40)-float(Fraction(13,80))*L+float(Fraction(1,160))*(L@L)
    assert np.allclose(P,np.ones((40,40))/40)
    R_adj=Fraction(13,80); R_non=Fraction(7,40)
    assert 240*R_adj==39 and 240*R_non==42
    assert Fraction(24,1)/Fraction(5,6)+Fraction(15,1)/Fraction(4,3)==Fraction(801,20)
    assert math.comb(48,10)==6540715896
    assert abs((2-(-4))-6)<1e-15
    e24,r24=nonlinear(A,np.array([[2.,5.],[-21.,-20.]]))
    e15,r15=nonlinear(A,np.array([[3.2,12.],[-21.,-10.]]))
    assert e24[10]/sum(e24.values())>1-1e-12 and r24<1e-8
    assert e15[16]/sum(e15.values())>1-1e-12 and r15<1e-8
    print(json.dumps({"status":cert["status"],"semantic_sha256":cert["semantic_sha256"],"carrier_dimensions":[99,145],"phase_K256_N20_error":cert["pass4106_multiuse_sine_reference"]["samples_K256"]["N20"],"decoder_sigma6":2*math.sin(math.pi/14),"turing_purities":[e24[10]/sum(e24.values()),e15[16]/sum(e15.values())]},sort_keys=True))

if __name__=="__main__":
    main()
