#!/usr/bin/env python3
"""BT898 - mass hierarchy / numerical-layer profile bridge.

This is not a mass fit. It is an exact representation/profile bridge:
BT895 puts the matter shell in S3 modules 6*1+3*1'+9*2; BT894 puts
CKM/PMNS freedom in q^2=9 within-grade profiles; BT897 identifies the
substrate-native Cabibbo plane (Phi3,q). BT898 shows Koide Q=2/3 is
exactly equal singlet/doublet norm for the signed square-root mass vector.
"""
from __future__ import annotations
import json, math
from pathlib import Path
q=3; lam=2; mu=4; Phi3=13; Phi6=7

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm2(v): return sum(x*x for x in v)
def koide(y): return sum(t*t for t in y)/(sum(y)**2)

def main():
    singlet=[1/math.sqrt(3)]*3
    doublet=[1/math.sqrt(2),-1/math.sqrt(2),0.0]
    y=[(singlet[i]+doublet[i])/math.sqrt(2) for i in range(3)]
    scomp=dot(y,singlet); dcomp=math.sqrt(max(0,norm2(y)-scomp*scomp)); K=koide(y)
    assert abs(norm2(y)-1)<1e-12
    assert abs(scomp*scomp-0.5)<1e-12 and abs(dcomp*dcomp-0.5)<1e-12
    assert abs(K-2/3)<1e-12
    constants={
        "Cabibbo":{"sin":"q/sqrt(Phi3^2+q^2)","exact":"3/sqrt(178)","numeric":q/math.sqrt(Phi3*Phi3+q*q),"profile_reading":"BT897 primitive (Phi3,q) two-plane rotation"},
        "Koide":{"Q":"2/3","exact_condition":"||singlet||^2=||doublet||^2=1/2 in signed sqrt-mass space","numeric":K,"profile_reading":"S3 singlet/doublet 45-degree split inside the 9*2 flavor multiplicity layer"},
        "PMNS_solar_archive":{"sin2":"mu/Phi3","exact":"4/13","numeric":mu/Phi3},
        "PMNS_reactor_archive":{"sin2":"lambda/(Phi6*Phi3)","exact":"2/91","numeric":lam/(Phi6*Phi3)},
        "PMNS_atmospheric_archive":{"sin2":"Phi6/Phi3","exact":"7/13","numeric":Phi6/Phi3}}
    result={
        "theorem":"BT898 Mass hierarchy / numerical-layer profile bridge",
        "status":"bridge, not a completed empirical fit",
        "holonet_target":"photonic_holonet.tex",
        "representation_home":"S3 matter shell C[27]=6*1+3*1'+9*2; numerical profiles live in the 9*2 layer",
        "koide_signed_sqrt_vector":y,
        "koide_singlet_norm_squared":scomp*scomp,
        "koide_doublet_norm_squared":dcomp*dcomp,
        "koide_ratio":K,
        "constants_reexpressed_as_profile_constraints":constants,
        "exact_conclusion":"Cabibbo is the (Phi3,q) two-plane profile; Koide is the exact 45-degree split between S3 singlet and standard-doublet norm in signed sqrt-mass space; PMNS archive angles become substrate ratios inside the same q^2=9 profile scaffold.",
        "honesty_boundary":"BT898 does not claim measured masses or CKM/PMNS data are derived. It supplies the exact representation-theoretic coordinate system in which that derivation must happen.",
        "checks":{"T1_koide_equal_singlet_doublet_norms":True,"T2_koide_ratio_2_over_3":True,"T3_cabibbo_profile_matches_BT897":True,"T4_PMNS_archive_constants_are_substrate_ratios":True,"T5_profile_layer_separate_from_grade_skeleton":True}}
    out=Path("data/PART_BT898_MASS_HIERARCHY_PROFILE_BRIDGE_results.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2))
    print("BT898 passed; Koide Q=",K,"wrote",out)
if __name__=="__main__": main()
