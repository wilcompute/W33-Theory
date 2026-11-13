#!/usr/bin/env python3
"""Exact qutrit chiral-gate Clifford-dressed compiler and conditional noise/action.

The unitaries are checked numerically to tolerance; the integer gate and
rational noise formulas are exact. The Landau model is phenomenological,
not derived Standard Model dynamics or physical symmetry breaking.
"""
from __future__ import annotations
import itertools, json, math, sys
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_chiral_null_order3_gate as G
OUT=ROOT/"data/toe_20261113_chiral_action_compiler_noise.json"
F=tuple(tuple(v) for v in G.FUTURE)
I=np.eye(27)
T,A,D=G.build()
TAU=2*math.pi/(9*math.sqrt(3))

def perm_add(v):
    P=np.zeros((27,27),dtype=int)
    for j,x in enumerate(G.V):
        target=tuple((x[k]-v[k])%3 for k in range(3))
        P[G.VID[target],j]=1
    return P

def cmult(k):
    """SUM(0->2) and SUM(0->1)^k; maps e0 to (1,k,1)."""
    P=np.zeros((27,27),dtype=int)
    for j,(a,b,c) in enumerate(G.V):
        target=(a,(b+k*a)%3,(c+a)%3)
        P[G.VID[target],j]=1
    return P

def compiler():
    Ts=[perm_add(v) for v in F]
    assert np.array_equal(sum((X-X.T for X in Ts)),D)
    assert all(np.array_equal(x@y,y@x) for x in Ts for y in Ts)
    C1,C2=cmult(1),cmult(2)
    x0=perm_add((1,0,0))
    assert np.array_equal(C1@x0@C1.T,Ts[2])
    assert np.array_equal(C2@x0@C2.T,Ts[3])
    R0=expm(TAU*(x0-x0.T))
    R2=expm(TAU*(Ts[1]-Ts[1].T))
    composed=R0@R2@(C1@R0@C1.T)@(C2@R0@C2.T)
    U=(18*I+3*D+D@D)/18
    delta=float(np.max(abs(composed-U)))
    assert delta<2e-13
    assert np.max(abs(np.linalg.matrix_power(R0,9)-I))<1e-12
    assert np.max(abs(np.linalg.matrix_power(R0,3)-I))>0.9
    assert np.max(abs(U.T@U-I))<1e-12
    return {"exact_product":"exp(t(X0-X0^-1))*exp(t(X2-X2^-1))*C111 exp(t(X0-X0^-1)) C111^-1 * C121 exp(t(X0-X0^-1)) C121^-1",
     "t":"2pi/(9sqrt(3))",
     "primitive_gates":{"one_qutrit_rotations":4,"qutrit_SUM":8},
     "single_rotation_order":9,"global_gate_order":3,
     "max_absolute_matrix_error":delta,
     "optimization_status":"constructive, not demonstrated gate-count optimality",
     "physical_scope":"requires coherent, accurately calibrated three-mode qutrit rotations and SUMs"}

def single_shot(p:Fraction):
    one=Fraction(1)
    pf=(one-p)*Fraction(4,81)+p*Fraction(1,27)
    pb=(one-p)*Fraction(1,81)+p*Fraction(1,27)
    contrast=pf-pb
    negativity=max(Fraction(0),Fraction(16,27)*(3-4*p))
    l1=one+2*negativity
    if contrast:
        # Hoeffding, Y=+1 forward/-1 reverse/0 other, |Y|<=1.
        # P(|mean(Y)-E Y|>=contrast) <=2 exp(-N contrast^2/2).
        n=math.ceil(2*math.log(200)/float(contrast*contrast))
    else:n=None
    return {"p":str(p),"forward_probability":str(pf),
            "reverse_probability":str(pb),
            "contrast":str(contrast),
            "negative_wigner_mass":str(negativity),
            "wigner_l1":str(l1),"minimum_shots_hoeffding_two_sided_alpha_001":n}

def symmetry_action():
    # GL2 congruence images =24, each preserves the positive orbit.
    mats={}
    for z in itertools.product(range(3),repeat=4):
        B=np.array(z,dtype=int).reshape(2,2)
        if int(round(np.linalg.det(B)))%3==0:continue
        M=G.sym2(B)
        mats[tuple(M.reshape(-1))]=M
    assert len(mats)==24
    orbits={tuple(map(int,(M@np.array(F[0]))%3)) for M in mats.values()}
    assert orbits==set(F)
    # Therefore every translation-/S4-covariant nearest-null Hamiltonian
    # lies in span(I, A, iD) if scalar onsite terms are admitted.
    # The unique parity-odd Hermitian nearest-null direction is iD.
    inv_idx=[G.VID[tuple((-t)%3 for t in v)] for v in G.V]
    assert np.array_equal(D[np.ix_(inv_idx,inv_idx)],-D)
    return {"translation_and_S4_orbit_dimensions":{"positive_null":4,"negative_null":4},
            "all_null_shells_transitive":True,
            "null_hopping_Hermitian_real_dimension":2,
            "parity_even_hopping":"A=T+T^T",
            "parity_odd_hopping":"iD=i(T-T^T)",
            "parity_odd_nearest_null_direction_unique_up_to_real_scalar":True,
            "selection_limitation":"Symmetry permits iD; it does not fix its coefficient or choose a sign."}

def mean_field():
    # Z(b)=Tr exp(-beta*b*iD) = 19 + 8 cosh(beta*sqrt(27)*b).
    kappa=8.0; lam=32.0
    rows=[]
    def Ff(b,beta):
        return kappa*b*b/2+lam*b**4/4-math.log(19+8*math.cosh(beta*math.sqrt(27)*b))/beta
    for beta in (0.8,1.0,1.25,1.5):
        z=minimize_scalar(lambda x:Ff(x,beta),bounds=(0,2),method="bounded",
                          options={"xatol":1e-12})
        center=Ff(0,beta)
        if beta<=1.0:
            bstar=0.0
            gap=0.0
        else:
            bstar=float(z.x)
            gap=float(z.fun-center)
            assert bstar>0.1 and gap<0
            assert abs(Ff(-bstar,beta)-Ff(bstar,beta))<1e-12
        rows.append({"beta":beta,
                     "curvature_at_origin":kappa-8*beta,
                     "minima_at_b_pm":bstar,
                     "lower_than_b0":gap})
    return {"toy_partition":"Z(b)=19+8 cosh(beta*sqrt(27)*b)",
            "phenomenological_free_energy":"F(b)=kappa*b^2/2+lambda*b^4/4-(1/beta)*ln(Z(b))",
            "kappa":kappa,"lambda":lam,
            "exact_curvature":"F''(0)=kappa-8 beta",
            "local_instability_at":"beta>kappa/8",
            "examples":rows,
            "scope":"Landau mean-field double well, not microscopic Hamiltonian derivation, finite-system spontaneous symmetry breaking, or observed CP/weak chirality"}

def verify():
    assert G.verify()["status"].startswith("PASS")
    r={"schema":"toe.chiral_action_compiler_noise.v1",
       "status":"PASS_EXACT_COMPILER_CONDITIONAL_NOISE_AND_TOY_ACTION",
       "symmetry_classification":symmetry_action(),
       "dressed_compiler":compiler(),
       "global_depolarizing_channel":{
         "model":"rho_p=(1-p) U|000><000|U^dag + p I_27/27",
         "exact_wigner_negativity_threshold":"p<3/4",
         "negative_mass_for_p_below_threshold":"(16/27)(3-4p)",
         "contrast":"(1-p)/27",
         "noise_scenarios":[single_shot(p) for p in
             [Fraction(0),Fraction(1,100),Fraction(1,10),Fraction(1,4),
              Fraction(1,2),Fraction(3,4),Fraction(1)]],
         "scope":"output-global depolarization ONLY; not per-gate local noise, magic distillation or FT threshold"},
       "toy_chirality_selection":mean_field(),
       "physics_firewall":"No material parameters, detector loss or real quantum device verified."}
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return r
if __name__=="__main__":
    r=verify()
    print(json.dumps({"status":r["status"],
                      "compiler":r["dressed_compiler"],
                      "mean_field":r["toy_chirality_selection"]},indent=2))
