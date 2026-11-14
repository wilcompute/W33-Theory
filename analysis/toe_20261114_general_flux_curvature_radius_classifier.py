#!/usr/bin/env python3
"""Exact Einstein-frame radius classifier for positive internal p-form flux.

This is a conditional unwarped Einstein-Hilbert + p-form truncation, not an
E6 ExFT solution, a physical vacuum, or a derivation of gravity.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261114_general_flux_curvature_radius_classifier.json"

def powers(d:int,n:int,p:int):
    if not (d>2 and n>=2 and 1<=p<=n):
        raise ValueError("requires d>2, n>=2, 1<=p<=n")
    # Metric: ds^2_D = g_d + R^2 h_n, Vol(h)=1.
    # Raw flux: sqrt(g_D)|F_p|^2 ~ R^(n-2p).
    # Einstein rescale g_E=R^(2n/(d-2)) g_d:
    # sqrt(g_d) ~ R^(-dn/(d-2))sqrt(g_E).
    raw=Q(n-2*p)
    weyl=-Q(d*n,d-2)
    exponent=raw+weyl
    assert exponent == -2*Q(p)-Q(2*n,d-2)
    # Positive internal curvature contributes -B R^(-c).
    a=-exponent
    c=Q(2)+Q(2*n,d-2)
    return dict(d=d,n=n,p=p,raw=raw,weyl=weyl,flux_power=exponent,
                flux_decay=a,curvature_decay=c)

def one_flux_balance(d:int,n:int,p:int,A=Q(1),B=Q(1)):
    x=powers(d,n,p)
    a,c=x["flux_decay"],x["curvature_decay"]
    A,B=Q(A),Q(B)
    if A<=0 or B<=0: raise ValueError("A,B must be positive")
    if p==1:
        return dict(branch="degenerate_same_radial_scaling",
                    coefficient=A-B,isolated_stationary=False)
    # V=A*R^-a - B*R^-c, a>c for p>1.
    r_power=a*A/(c*B)  # R_star**(a-c)
    assert a>c and a-c==2*(p-1)
    # At the stationary point:
    # V_star=(1-a/c)*A*R_star^-a <0.
    # d^2 V/d(logR)^2=a*(a-c)*A*R_star^-a >0.
    return dict(branch="unique_stable_radial_AdS_extremum",
                radius_power=a-c,
                radius_power_value=r_power,
                vacuum_energy_over_A_RminusA=Q(1)-a/c,
                log_radius_hessian_over_A_RminusA=a*(a-c),
                full_background_solution_certified=False)

def multi_flux_balance(d:int,n:int,terms,curvature_B):
    """A_p>0; curvature_B>=0; log-radius exact monotonicity certificate."""
    if not terms or curvature_B<0: raise ValueError
    spec=[(int(p),Q(A),powers(d,n,int(p))) for p,A in terms]
    if any(A<=0 for _,A,_ in spec): raise ValueError
    if curvature_B==0:
        return dict(exists=False,reason="positive flux terms are strictly decreasing",
                    stationarity_sum="sum(-a_p*A_p*R**-a_p)<0 for all R>0")
    c=spec[0][2]["curvature_decay"]
    assert all(t["curvature_decay"]==c for _,_,t in spec)
    # p=1 terms share exponent with curvature; combine their coefficients.
    B_eff=Q(curvature_B)-sum(A for p,A,_ in spec if p==1)
    higher=[(p,A,t["flux_decay"]) for p,A,t in spec if p>1]
    if B_eff<=0 or not higher:
        return dict(exists=False,reason="no negative slower-decaying curvature term")
    # Let x=log R. At a critical point:
    # sum_{p>1} a_p A_p exp(-(a_p-c)*x)=c B_eff.
    # LHS strictly falls from infinity to zero, giving exactly one root.
    # Hessian=sum a_p(a_p-c) A_p exp(-a_p x)>0,
    # V_star=sum (1-a_p/c) A_p exp(-a_p x)<0.
    return dict(exists=True,unique=True,radially_stable=True,
                vacuum_energy_negative=True,full_background_solution_certified=False,
                effective_curvature_coefficient=str(B_eff),
                stationarity="sum a_p*A_p*R**(-(a_p-c))=c*B_eff; LHS strictly decreasing",
                hessian="sum a_p*(a_p-c)*A_p*R**(-a_p)>0",
                vacuum_energy="sum (1-a_p/c)*A_p*R**-a_p<0")

def main():
    x=powers(5,4,3)
    assert x["raw"]==-2 and x["weyl"]==-Q(20,3)
    assert x["flux_power"]==-Q(26,3)
    s=one_flux_balance(5,4,3)
    assert s["radius_power"]==4
    assert s["radius_power_value"]==Q(13,7)
    assert s["vacuum_energy_over_A_RminusA"]==-Q(6,7)
    assert multi_flux_balance(5,4,[(2,1),(3,2)],1)["unique"]
    assert not multi_flux_balance(5,4,[(2,1),(3,2)],0)["exists"]
    assert not multi_flux_balance(5,4,[(1,2),(3,1)],1)["exists"]
    data={
      "status":"PASS_CONDITIONAL_EINSTEIN_FRAME_SCALING_CLASSIFIER",
      "formula":"V_p(R)=A_p R^(-2p-2n/(d-2)) for A_p>0",
      "torus_T4_flux_only_runaway":True,
      "torus_case":{k:str(v) for k,v in x.items()},
      "curvature_formula":"V_curv(R)=-B R^(-2-2n/(d-2)), B>0 if integrated internal scalar curvature positive",
      "positive_flux_only_no_critical_point":True,
      "one_p3_example":{k:str(v) for k,v in s.items()},
      "multiflux_p2_p3_example":multi_flux_balance(5,4,[(2,1),(3,2)],1),
      "topology_guard":"No curvature term in the specified fixed flat T4 model. T4 does not support an everywhere-positive-scalar-curvature metric; this does not by itself rule out positive integrated curvature for a sign-changing metric. A different full compactification needs flux cohomology and field equations.",
      "scope":"Unwarped, no warp factor, fixed normalized internal shape, one uniform radius, fixed internal quantized fluxes, d>2; no proof of full moduli stability, E6 section selector, consistent solution or TOE.",
      "prior":"analysis/toe_20261114_E6_flux_shape_volume_runaway_nogo.py"
    }
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("PASS",OUT)
    return data

if __name__=="__main__":main()
