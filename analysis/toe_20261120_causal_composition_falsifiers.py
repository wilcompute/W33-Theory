#!/usr/bin/env python3
"""Quantum-order/causal and nonlinear physical address-map falsifiers.

The central W33 quantum switch is operationally equivalent to a definite
ordered target unitary plus a known control phase. This cannot by itself
certify causal nonseparability or emergent time.
"""
import json,math
from itertools import combinations,product
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from toe_20261120_symplectic_order_sic_switch import OMEGA,pauli,symp
from toe_20261120_one_ensemble_centrality import trial_operators, noncentrality

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_causal_composition_falsifiers.json"
I9=np.eye(9,dtype=complex)
E=np.eye(4,dtype=int)

def vec(*v):return tuple(int(x)%3 for x in v)
def plus(u,v):return vec(*(int(a)+int(b) for a,b in zip(u,v)))
def shear(u):
    return vec(int(u[0])+int(u[1])*int(u[3]),u[1],u[2],u[3])
def shift_phase(c):
    return int(np.argmin([abs(c-OMEGA**s) for s in range(3)]))

def nonlinear_physical_address():
    P=[vec(*x) for x in product(range(3),repeat=4)]
    assert len(set(map(shear,P)))==81
    assert all(shear(tuple(E[:,i]))==tuple(E[:,i]) for i in range(4))
    six={}
    for i,j in combinations(range(4),2):
        u,v=tuple(E[:,i]),tuple(E[:,j])
        A,B=pauli(shear(u)),pauli(shear(v))
        measured=np.trace((A@B)@(B@A).conj().T)/9
        assert shift_phase(measured)==symp(u,v)
        six[f"{i}{j}"]=shift_phase(measured)
    u=plus(tuple(E[:,1]),tuple(E[:,3]))
    v=tuple(E[:,2])
    A,B=pauli(shear(u)),pauli(shear(v))
    measured=np.trace((A@B)@(B@A).conj().T)/9
    predicted=symp(u,v)
    actual=shift_phase(measured)
    assert predicted==0 and actual==1
    Uu=pauli(shear(tuple(E[:,1])))
    Uv=pauli(shear(tuple(E[:,3])))
    Uuv=pauli(shear(u))
    residual=Uu@Uv@Uuv.conj().T
    trace_abs=float(abs(np.trace(residual)/9))
    assert trace_abs<1e-12
    # Honest additive-label rep yields scalar residual for every address pair.
    good=pauli(tuple(E[:,1]))@pauli(tuple(E[:,3]))@pauli(u).conj().T
    assert abs(abs(np.trace(good)/9)-1)<1e-12
    mismatch=sum(symp(u,v)!=symp(shear(u),shear(v))
                 for u,v in combinations(P,2))
    assert mismatch==1512
    return {"physical_gate_address_map_is_bijective":True,
            "basis_generator_gates_unchanged":True,
            "six_basis_phases_pass":six,
            "all_81_address_pairs_that_fail_bilinear_prediction":mismatch,
            "holdout_pair":"u=e1+e3, v=e2",
            "linear_prediction":int(predicted),"measured_distorted_phase":int(actual),
            "composition_residual_normalized_trace_abs":trace_abs,
            "honest_composition_residual_normalized_trace_abs":float(abs(np.trace(good)/9)),
            "point":"A legitimate set of 81 Weyl unitary gates with nonlinear command address can fake all six basis-pair calibrations. A two-displacement composition holdout detects it."}

def cocycle_and_associativity():
    rng=np.random.default_rng(513)
    P=[tuple(int(x) for x in p) for p in product(range(3),repeat=4)]
    phi=lambda u,v:(u[0]*v[2]+u[1]*v[3])%3
    for u,v in product(P,repeat=2):
        assert (phi(u,v)-phi(v,u))%3==symp(u,v)
    triples=30000
    for _ in range(triples):
        u,v,w=[P[int(rng.integers(81))] for _ in range(3)]
        assert (phi(u,v)+phi(plus(u,v),w)-phi(v,w)-phi(u,plus(v,w)))%3==0
    return {"exact_sesquilinear_commutator_address_pairs_checked":81**2,
            "random_cocycle_associativity_triplets_checked":triples,
            "projective_representation_law":"W(u)W(v)=omega^phi(u,v) W(u+v), phi=z(u) dot x(v).",
            "prediction_no_go":"If an associative projective representation of additive F3^4 is exact, its central commutator is necessarily an alternating bicharacter with values in cube roots of unity. An independent nonbilinear pair phase would violate a premise, not demonstrate a new law with the same representation."}

def branch_equivalence():
    u,v=vec(1,0,0,0),vec(0,0,1,0)
    A,B=pauli(u),pauli(v)
    U0=A@B; U1=B@A
    c=OMEGA**symp(u,v)
    total=np.block([[U0,np.zeros((9,9))],[np.zeros((9,9)),U1]])
    fixed_order=np.kron(np.diag([c,1]),U1)
    err=float(np.max(abs(total-fixed_order)))
    assert err<1e-12
    # For central K the control cannot become entangled with a pure target
    # through this ideal switched unitary. For a perturbed noncentral K it can.
    _,K=trial_operators()
    mag=noncentrality(K)["trace_abs"]
    ent=lambda c:(0. if abs(c)>1-1e-13 else
        -sum(p*math.log2(p) for p in ((1+abs(c))/2,(1-abs(c))/2)))
    noncentral_entropy=ent(mag)
    assert .1<noncentral_entropy<1
    assert ent(c)==0
    return {
       "central_W33_switch_equals_definite_target_order_plus_control_phase_error_max":err,
       "central_switch_control_target_purification_entanglement_bits":0.,
       "noncentral_seeded_control_vs_purified_target_entropy_bits":noncentral_entropy,
       "formula":"For pure control |+> and purification of I_d/d, control entropy is h2((1+|Tr(K)/d|)/2).",
       "formal_boundary":"A central-pair switch output can be reproduced exactly by a known definite-target-order unitary with an extra control phase. It does not certify causal nonseparability. Independent trusted-operation/process-matrix or suitably extended causal witness is mandatory.",
       "literature":"Araújo et al. New J. Phys. 17 102001 (2015); quantum switch does not violate standard bipartite causal inequalities without extra trust or spacetime conditions."
       }

def noisy_six_and_holdout():
    honest=[0,1,2]
    rng=np.random.default_rng(20261121)
    vis=.9; drift=.05;N=160
    def read_class(k):
        ph=rng.uniform(-drift,drift)
        c=vis*np.exp(1j*ph)*OMEGA**k
        nx=rng.binomial(N,(1+c.real)/2)
        ny=rng.binomial(N,(1+c.imag)/2)
        est=complex(2*nx/N-1,2*ny/N-1)
        return shift_phase(est)
    reps=1500
    honest_ok=0
    trap_caught=0
    for _ in range(reps):
        six=[read_class(k) for k in (0,1,0,0,1,0)]
        if six==[0,1,0,0,1,0]:honest_ok+=1
        if six==[0,1,0,0,1,0] and read_class(1)!=0:trap_caught+=1
    assert honest_ok>1480 and trap_caught>1460
    return {"model":"IID Bernoulli two-quadrature switch phase; v=0.9, drift uniform [-.05,.05], N=160 per quadrature per setting.",
            "six_basis_and_one_holdout_accepted_control_shots_per_run":7*2*N,
            "seeded_replications":reps,"six_basis_pass_reps":honest_ok,
            "distorted_address_detected_given_six_basis_pass_reps":trap_caught,
            "no_hardware_measured":True}

def main(write=True):
    result={"status":"PASS_CAUSAL_SWITCH_EQUIVALENCE_AND_PHYSICAL_ADDRESS_HOLDOUT",
            "physical_address":nonlinear_physical_address(),
            "cocycle_consistency":cocycle_and_associativity(),
            "causal_order_ambiguity":branch_equivalence(),
            "noisy_holdout_planning":noisy_six_and_holdout(),
            "boundary":"Ordinary quantum circuit simulation and W33 algebra tests cannot by themselves constitute a parameter-free prediction beyond standard quantum mechanics or prove emergent Lorentzian spacetime."}
    if write:OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result
if __name__=="__main__":print(json.dumps(main(),indent=2))
