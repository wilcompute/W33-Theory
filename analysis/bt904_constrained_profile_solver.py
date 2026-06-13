#!/usr/bin/env python3
"""BT904 - constrained 9x9 multiplicity-profile solver.

Constructs a single S3-equivariant profile model in the BT901 commutant:

    V_profile = C^9 tensor Std(S3).

The 9x9 multiplicity space carries four disjoint rotation planes:
Cabibbo, PMNS solar, PMNS reactor, PMNS atmospheric.  Koide is recorded as
the equal-norm S3 singlet/doublet condition in signed sqrt-mass space.
This is a constrained scaffold, not a fitted fermion spectrum.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np

q=3; lam=2; mu=4; Phi3=13; Phi6=7
N=9

def plane(n:int,i:int,j:int,c:float,s:float)->np.ndarray:
    r=np.eye(n)
    r[i,i]=c; r[i,j]=s; r[j,i]=-s; r[j,j]=c
    return r

def frob(a:np.ndarray)->float: return float(np.linalg.norm(a,"fro"))
def rot_from_sin2(s2:float):
    return math.sqrt(1-s2), math.sqrt(s2)

def main()->None:
    specs=[
        ("Cabibbo",0,1,Phi3/math.sqrt(Phi3*Phi3+q*q),q/math.sqrt(Phi3*Phi3+q*q),"3/sqrt(178)"),
        ("PMNS_solar",2,3,*rot_from_sin2(mu/Phi3),"sqrt(4/13)"),
        ("PMNS_reactor",4,5,*rot_from_sin2(lam/(Phi6*Phi3)),"sqrt(2/91)"),
        ("PMNS_atmospheric",6,7,*rot_from_sin2(Phi6/Phi3),"sqrt(7/13)")]
    U=np.eye(N)
    for _,i,j,c,s,_ in specs:
        U=plane(N,i,j,c,s)@U
    assert frob(U.T@U-np.eye(N))<1e-10
    Du=np.diag(np.arange(1,N+1,dtype=float))
    Dd=U@Du@U.T
    comm=Du@Dd-Dd@Du
    assert frob(comm)>0

    # S3 standard representation and equivariant lift.
    rot=np.array([[-0.5,-math.sqrt(3)/2],[math.sqrt(3)/2,-0.5]])
    ref=np.array([[1.0,0.0],[0.0,-1.0]])
    A=np.kron(Du,np.eye(2)); B=np.kron(Dd,np.eye(2)); R=np.kron(np.eye(N),rot); C=np.kron(np.eye(N),ref)
    errors={"A_rot":frob(A@R-R@A),"B_rot":frob(B@R-R@B),"A_ref":frob(A@C-C@A),"B_ref":frob(B@C-C@B)}
    assert max(errors.values())<1e-10

    sing=np.ones(3)/math.sqrt(3)
    doub=np.array([1/math.sqrt(2),-1/math.sqrt(2),0.0])
    y=(sing+doub)/math.sqrt(2)
    koide=float(np.sum(y*y)/(np.sum(y)**2))
    assert abs(koide-2/3)<1e-12

    result={
        "theorem":"BT904 constrained 9x9 profile solver",
        "status":"constructive scaffold, not empirical mass fit",
        "profile_space":"C^9 multiplicity factor in C^9 tensor Std(S3)",
        "rotation_planes":[{"name":name,"plane":[i,j],"cos":c,"sin":s,"sin_exact":exact,"sin2":s*s} for name,i,j,c,s,exact in specs],
        "unitarity_error":frob(U.T@U-np.eye(N)),
        "profile_commutator_frobenius_norm":frob(comm),
        "s3_equivariance_errors":errors,
        "koide_condition":{"ratio":koide,"condition":"equal S3 singlet and standard-doublet norm in signed sqrt-mass space"},
        "exact_conclusion":"A single 9x9 multiplicity-space profile can house Cabibbo plus the PMNS archive scaffold on disjoint internal planes while lifting S3-equivariantly as profile tensor I_2. The numerical layer can therefore be searched without altering the shifted-reflection support skeleton.",
        "checks":{"T1_9x9_unitary_profile_built":True,"T2_four_disjoint_rotation_planes":True,"T3_up_down_profiles_noncommute":True,"T4_lift_commutes_with_S3":True,"T5_koide_equal_norm_condition_verified":True}}
    out=Path("data/PART_BT904_CONSTRAINED_PROFILE_SOLVER_results.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2))
    print("BT904 passed; commutator",frob(comm),"wrote",out)
if __name__=="__main__": main()
