"""Explicit F/D-flat existence and self-consistency stress of B alignment
for E6 two-adjoint mirror messenger effective sector.

W=S_A(Tr27 A²-vA²)+S_B(Tr27 B²-vB²)
  +sum_s,t Fbar_s,t(M+s*y*A+t*u*B)F_s,t.
At Fbar=F=S_A=S_B=0, Hermitian commuting Cartan A and B
with prescribed quadratic norms are F=0, D=0. This establishes
EXISTENCE of F/D-flat backgrounds, NOT their unique dynamical
selection. Soft messenger scalar mass² shifts preserve F=D=0
at messenger origin but induce a Coleman-Weinberg potential.

Parameterize all SU5-preserving B in U1psi/chi plane with
Tr27 B²=72 psi²+120 chi²=7.68. Scan angular CW(B) on
this circle for physical messenger masses at least .15M, plus
kappa4(B) signs. Compare benchmark B=(-.2,+.2) to actual
CW(B) extrema; no assumption that benchmark is B vacuum.
"""
import math,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_E6_two_adjoint_split_27_threshold import IRREPS,threshold
OUT=ROOT/"data"/"toe_20261117_E6_FDflat_Balignment_angle_scan.json"
def quad():
    p=sum(dim*qp*qp for _,dim,qp,qc,_,__ in IRREPS)
    c=sum(dim*qc*qc for _,dim,qp,qc,_,__ in IRREPS)
    cross=sum(dim*qp*qc for _,dim,qp,qc,_,__ in IRREPS)
    assert (p,c,cross)==(72,120,0)
    assert math.isclose(72*.2**2+120*.2**2,7.68)
    return {"trace27_B2":"72 psi²+120 chi²","cross_coefficient":0,
            "trace27_A2":"6 Tr5(A²) for SU5 adjoint A",
            "example_B_trace27_squared":7.68,
            "FD_flat_constructive_proof":"Set messenger Fbar,F=0 and singlets S_A=S_B=0; impose Tr27 A²=vA², Tr27 B²=vB². Then all holomorphic F-terms vanish. Hermitian commuting A and B lie in a common compact Cartan so adjoint D^a proportional to [A†,A]+[B†,B] vanishes.",
            "critical_missing":"These are moduli of F/D flat backgrounds, not a uniquely selected vacuum. Soft one-loop potential, full E6 gauge/Higgs quantum corrections and other adjoint invariants control their stability."}
def Bangle(theta):
    return math.sqrt(7.68/72)*math.cos(theta), math.sqrt(7.68/120)*math.sin(theta)
def f(a):
    if a<0:raise ValueError
    if a==0:return 0.
    return a*a*(math.log(a)-1.5)
def V0(psi,chi,delta=.25):
    total=0.
    for _,dim,qp,qc,_,__ in IRREPS:
        B=psi*qp+chi*qc
        for t in (-1,1):
            mass2=(1+t*B)**2
            total+=dim*2*(f(mass2+delta)-f(mass2))/(16*math.pi**2)
    return total
def verify():
    algebra=quad()
    theta_ref=math.atan2(.2/math.sqrt(7.68/120),-.2/math.sqrt(7.68/72))
    ref=Bangle(theta_ref)
    assert np.allclose(ref,(-.2,.2),atol=1e-14)
    entries=[]
    for theta in np.linspace(0,2*math.pi,721)[:-1]:
        psi,chi=Bangle(float(theta))
        result=threshold(psi,chi,.25)
        assert result is not None
        minm=min(x["min_fermion_mass_abs"] for x in result["irrep"])
        minscalar=min(x["min_scalar_mass2"] for x in result["irrep"])
        if minm<.15:continue
        entries.append({"theta":float(theta),"psi":psi,"chi":chi,
             "CW_B_vacuum_energy":V0(psi,chi),
             "kappa_A_SU5_TrA4":result["kappa_SU5_TrPhi4"],
             "smallest_fermion_mass_abs":minm,
             "smallest_scalar_mass2":minscalar})
    assert len(entries)>100
    best=min(entries,key=lambda x:x["CW_B_vacuum_energy"])
    refv=V0(*ref)
    positives=[z for z in entries if z["kappa_A_SU5_TrA4"]>0]
    assert positives
    preferred=min(positives,key=lambda x:x["CW_B_vacuum_energy"])
    refquartic=threshold(-.2,.2,.25)["kappa_SU5_TrPhi4"]
    assert refquartic>.0025
    return {"status":"PASS_E6_TWO_ADJOINT_FD_FLAT_MODULI_AND_B_CW_ANGLE_STRESS",
      "exact_Cartan_norms_and_FD":algebra,
      "B_trace27_norm_squared":7.68,
      "B_angle_CW_scan_grid_720_with_fermion_mass_threshold_0p15":len(entries),
      "benchmark_B":{"psi":-.2,"chi":.2,
          "theta_rad":theta_ref,"CW_B_energy":refv,
          "kappa_A_SU5_shape":refquartic},
      "lowest_CW_B_energy_grid":best,
      "lowest_CW_B_energy_among_positive_kappa":preferred,
      "positive_A_quartic_count_at_same_B_norm":len(positives),
      "benchmark_B_is_global_CW_grid_min":abs(refv-best["CW_B_vacuum_energy"])<1e-8,
      "physical_caveat":"Even the B-only 1-loop grid minimum is not a global vacuum: full potential includes SUSY-breaking counterterms, E6 gauge/higgs modes and all Cartan directions. Scan is 720 angles under fixed B norm, excluding messenger fermion masses below 0.15M. The benchmark can be metastable or unselected.",
      "benchmark_proton_scale_proxy":"analysis/toe_20261117_E6_proton_scale_proxy.py"}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["B_angle_CW_scan_grid_720_with_fermion_mass_threshold_0p15"],
      z["benchmark_B_is_global_CW_grid_min"],z["positive_A_quartic_count_at_same_B_norm"])
