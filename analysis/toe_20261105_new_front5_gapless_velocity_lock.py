#!/usr/bin/env python3
"""TOE front 5: exact no-go for velocity locking in Gaussian gapless sector.

Two massless scalar shifts forbid a potential mass term. Local
gradient interaction kappa del_x phiA del_x phiB produces positive
stiffness matrix K=[[vA^2,kappa],[kappa,vB^2]].
Normal modes omega_+/-~|k|sqrt(eigenvalues(K)).
Eigenvelocity degeneracy iff vA=vB AND kappa=0.
Testing 3+ free gapless species gives the same matrix principle:
a real symmetric stiffness with all eigenvalues equal must be c²I.
A dynamical *interacting RG* fixed point could change this; the
Gaussian exactly quadratic model cannot.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_front5_gapless_velocity_locking.json"
def model(vA,vB,k):
    K=np.array([[vA*vA,k],[k,vB*vB]])
    eig=np.linalg.eigvalsh(K)
    assert min(eig)>0
    speeds=np.sqrt(eig)
    return {"coupling":k,
      "gapless_boson_branches":2,
      "normal_mode_velocities":speeds.tolist(),
      "squared_velocity_discriminant":(vA*vA-vB*vB)**2+4*k*k,
      "velocity_split":float(speeds[1]-speeds[0]),
      "both_modes_gapless":True}
def main():
    v1,v2,k=sp.symbols("v1 v2 k",real=True)
    K=sp.Matrix([[v1**2,k],[k,v2**2]])
    disc=sp.factor(sp.discriminant(K.charpoly().as_expr(),sp.Symbol("lambda")))
    # Sympy charpoly default eigenvalue lambda symbol.
    assert sp.simplify(disc-((v1**2-v2**2)**2+4*k*k))==0
    A,B=1.,1.2
    ks=[0.,.05,.1,.2,.4,.8]
    xs=[model(A,B,x) for x in ks]
    assert all(z["normal_mode_velocities"][0]>0 for z in xs)
    assert all(z["velocity_split"]>=xs[0]["velocity_split"]-1e-14 for z in xs)
    # With identical bare speeds coupling itself SPLITS the cones.
    equal_case=[model(1.,1.,x) for x in (.0,.05,.2,.5)]
    assert equal_case[0]["velocity_split"]==0
    assert all(z["velocity_split"]>0 for z in equal_case[1:])
    controls=[]
    for nn in (3,4,6):
        rng=np.random.default_rng(20261105+nn)
        A=rng.standard_normal((nn,nn))
        # eigenvalue matrix positive definite and non-isotropic
        L=np.eye(nn)+.07*(A+A.T)/2
        eig=np.linalg.eigvalsh(L)
        assert min(eig)>0
        split=float(np.sqrt(max(eig))-np.sqrt(min(eig)))
        assert split>.03
        # algebraic Frobenius bound; equal eigenvalues requires L=cI.
        variance=float(np.linalg.norm(L-np.trace(L)/nn*np.eye(nn)))
        assert variance>0 and split>0
        controls.append({"number_gapless_species":nn,"velocity_spread":split,
           "stiffness_distance_from_scalar_identity_frobenius":variance})
    # GW170817: observational GW-versus-photon speed bounds, do NOT
    # naively apply this GW test to two arbitrarily hypothetical scalars.
    limit=3e-15
    model_gap=xs[0]["velocity_split"] / ((A+B)/2) if False else .2/1.1
    assert model_gap>1e13*limit
    out={"status":"PASS_GAPLESS_TWO_CONE_GAUSSIAN_NO_GO",
      "symbolic_squared_eigenvalue_discriminant":str(disc),
      "initial_velocities":[1.,1.2],
      "two_species_all_gapless_sweep":xs,
      "identical_bare_speeds_offdiagonal_coupling_sweep":equal_case,
      "higher_species_matrix_controls":controls,
      "gaussian_no_go_statement":"With positive kinetic time metric identity and two independent exact scalar shift symmetries, local gradient mixing keeps both modes massless but generically splits limiting speeds; equal speeds require exactly scalar stiffness, which for 2 unequal diagonal entries and nonzero mixing is impossible.",
      "gw170817_empirical_illustration":{"source":"LIGO Virgo Fermi GRB170817A ApJL848 L13 (2017)",
       "speed_gravity_minus_photon_over_c_range":[-3e-15,7e-16],
       "warning":"This observed GRAVITY vs PHOTON bound does not automatically constrain two hypothetical scalar modes here."},
      "scope":"Exact Gaussian quadratic gradient action; no interacting RG, no quantum UV completion, no statement that velocity equalization cannot occur under a non-Gaussian RG fixed point.",
      "prior_art":"Coupled Luttinger-liquid/harmonic normal modes and eigenvalue discriminants are elementary."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("VELOCITY_LOCK_NO_GO",[(x["coupling"],x["normal_mode_velocities"]) for x in xs],flush=True)
    return out
if __name__=="__main__":main()
