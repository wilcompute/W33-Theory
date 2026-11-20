#!/usr/bin/env python3
"""A quantum-switch/SIC operational audit of W(3,3) projective symplectic geometry.

All observables are for programmable qutrit gates with a coherent control.
This is NOT a measurement of physical QCD colour, nor a gravity/TOE derivation.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import json, math
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"data/toe_20261120_projective_switch_sic_certificate.json"
OMEGA=np.exp(2j*np.pi/3)
X=np.roll(np.eye(3,dtype=complex),1,axis=0)
Z=np.diag([1,OMEGA,OMEGA**2])
I3=np.eye(3,dtype=complex)
I9=np.eye(9,dtype=complex)

def normalize(v):
    q=tuple(int(x)%3 for x in v)
    a=next((x for x in q if x),None)
    if a is None: raise ValueError("zero vector has no projective label")
    return tuple((x if a==1 else 2*x)%3 for x in q)

def points():
    return sorted({normalize(v) for v in product(range(3),repeat=4) if any(v)})

def symp(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def area_triangle(u,v,w):
    return (symp(u,v)*symp(v,w)*symp(w,u))%3

def pauli(u):
    # Convention chosen so W(u)W(v)=omega^symp(u,v) W(v)W(u).
    return np.kron(np.linalg.matrix_power(X,int(u[2]))@np.linalg.matrix_power(Z,int(u[0])),
                   np.linalg.matrix_power(X,int(u[3]))@np.linalg.matrix_power(Z,int(u[1])))

def geometry():
    P=points()
    assert len(P)==40
    z=n=0
    triangles=Counter()
    pair_profiles=Counter()
    noncomm=[]
    for i,j in combinations(range(40),2):
        s=symp(P[i],P[j])
        if s==0:
            z+=1
            continue
        n+=1
        noncomm.append((i,j))
        profile=Counter(area_triangle(P[i],P[j],P[k]) for k in range(40) if k!=i and k!=j)
        pair_profiles[(profile[0],profile[1],profile[2])]+=1
    assert (z,n)==(240,540)
    assert pair_profiles=={(20,9,9):540}
    for i,j,k in combinations(range(40),3):
        t=area_triangle(P[i],P[j],P[k])
        if t==0:continue
        u,v,w=P[i],P[j],P[k]
        span={normalize(tuple((a*u[h]+b*v[h])%3 for h in range(4)))
              for a,b in product(range(3),repeat=2) if a or b}
        dependent=w in span
        triangles[(bool(dependent),int(t))]+=1
    assert triangles=={(True,1):180,(True,2):180,(False,1):1440,(False,2):1440}
    rng=np.random.default_rng(502)
    flipped=[tuple((-x)%3 for x in p) if rng.integers(2) else p for p in P]
    for i,j,k in combinations(range(40),3):
        assert area_triangle(P[i],P[j],P[k])==area_triangle(flipped[i],flipped[j],flipped[k])
    # J -> -J under the anti-symplectic transformation diag(1,1,-1,-1).
    anti=[tuple((p[h] if h<2 else -p[h])%3 for h in range(4)) for p in P]
    anti_permutation=sorted(normalize(p) for p in anti)
    assert anti_permutation==P
    assert all(symp(anti[i],anti[j])==(-symp(P[i],P[j]))%3 for i,j in combinations(range(40),2))
    assert all(area_triangle(anti[i],anti[j],anti[k])==(-area_triangle(P[i],P[j],P[k]))%3
               for i,j,k in combinations(range(40),3))
    return {
      "points":40,"commuting_unordered_pairs":z,"noncommuting_unordered_pairs":n,
      "partners_per_noncommuting_pair":[20,9,9],
      "fully_noncommuting_triples":sum(triangles.values()),
      "projectively_dependent_triples":triangles[(True,1)]+triangles[(True,2)],
      "projectively_independent_triples":triangles[(False,1)]+triangles[(False,2)],
      "signed_dependent_counts":{"plus":triangles[(True,1)],"minus":triangles[(True,2)]},
      "signed_independent_counts":{"plus":triangles[(False,1)],"minus":triangles[(False,2)]},
      "triple_sign_invariant_under_independent_representative_flips":True,
      "triple_sign_reverses_under_anti_symplectic_map":True
    }

def switch(u,v,target):
    A=pauli(u)
    B=pauli(v)
    v0=A@B
    v1=B@A
    phase=np.trace(v0@target@v1.conj().T)
    # readout: <sigma_x>=Re phase; <-sigma_y>=Im phase.
    return phase,v0,v1

def operator_switch():
    P=points()
    rng=np.random.default_rng(25)
    psi=rng.normal(size=9)+1j*rng.normal(size=9)
    psi/=np.linalg.norm(psi)
    rho=np.outer(psi,psi.conj())
    residual=0.
    real_hist=Counter()
    imag_hist=Counter()
    for i,j in combinations(range(40),2):
        s=symp(P[i],P[j])
        phase,V0,V1=switch(P[i],P[j],rho)
        residual=max(residual,float(np.max(np.abs(V0-OMEGA**s*V1))))
        assert abs(phase-OMEGA**s)<1e-11
        real_hist[str(s)]+=1
        y=round(float(phase.imag),8)
        imag_hist[str(y)]+=1
    assert residual<2e-14
    # Arbitrary mixed target is equally valid: this measures the central phase.
    rho_mixed=np.diag(np.arange(1,10,dtype=float)/45.)
    for i,j in ((0,1),(3,17),(12,37),(0,39)):
        p,_,_=switch(P[i],P[j],rho_mixed)
        assert abs(p-OMEGA**symp(P[i],P[j]))<1e-11
    return {"tested_projective_pair_switches":780,
            "control_phase_residual_max":residual,
            "symplectic_form_counts_by_selected_projective_lifts":dict(real_hist),
            "target_independent_control_x_for_commuting":1.,
            "target_independent_control_x_for_noncommuting":-.5,
            "noncommuting_control_minus_y_magnitude":math.sqrt(3)/2,
            "quantum_switch_requires_two_order_coherent_paths":True}

def hesse_sic():
    fid=np.array([0,1,-1],complex)/math.sqrt(2)
    projectors=[]
    for a,b in product(range(3),repeat=2):
        state=np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,a)@fid
        projectors.append(np.outer(state,state.conj()))
    p=np.asarray(projectors)
    gram=np.einsum("aij,bji->ab",p,p)
    target=(np.ones((9,9))+3*np.eye(9))/4
    assert np.max(np.abs(gram-target))<1e-12
    assert np.max(np.abs(p.sum(axis=0)-3*I3))<1e-12
    return p

def sic_operator_frame():
    p=hesse_sic()
    q=np.asarray([np.kron(a,b) for a,b in product(p,repeat=2)])
    assert q.shape==(81,9,9)
    base=(np.ones((9,9))+3*np.eye(9))/4
    invbase=(4/3)*np.eye(9)-np.ones((9,9))/9
    gram=np.kron(base,base)
    invgram=np.kron(invbase,invbase)
    actual=np.einsum("aij,bji->ab",q,q)
    assert np.max(np.abs(actual-gram))<1e-12
    assert np.max(np.abs(gram@invgram-np.eye(81)))<1e-12
    assert np.max(np.abs(q.sum(axis=0)-9*I9))<1e-12
    rng=np.random.default_rng(240)
    H=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
    H=(H+H.conj().T)/2
    H-=np.trace(H).real/9*I9
    G=expm(.23j*H)
    P=points()
    A=G@pauli(P[0])
    B=pauli(P[1])
    K=(B@A).conj().T@(A@B)
    assert np.max(np.abs(K.conj().T@K-I9))<1e-12
    obs=np.einsum("aij,ji->a",q,K)
    coeff=invgram@obs
    recovered=np.einsum("a,aij->ij",coeff,q)
    assert np.max(np.abs(recovered-K))<1e-11
    average=np.mean(obs)
    delta=obs-average
    frob_noncentral=float(np.linalg.norm(K-average*I9))
    cert=float(np.real(np.vdot(delta,invgram@delta)))
    assert abs(cert-frob_noncentral**2)<1e-10
    # Global visibility and optical phase can multiply every SIC coherence.
    detector=.77*np.exp(.31j)
    measured=detector*obs
    corrected=measured/detector
    assert np.max(np.abs(corrected-obs))<1e-12
    # The normalized centrality ratio is unchanged without this calibration.
    defect_ratio=lambda a:float(
      np.real(np.vdot(a-a.mean(),invgram@(a-a.mean())))/np.real(np.vdot(a,invgram@a)))
    assert abs(defect_ratio(measured)-defect_ratio(obs))<1e-12
    # SU9 simultaneous frame gauge transformations preserve all expectations.
    H2=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
    H2=(H2+H2.conj().T)/2
    F=expm(.17j*H2)
    q2=F@q@F.conj().T
    obs2=np.einsum("aij,ji->a",q2,F@K@F.conj().T)
    assert np.max(abs(obs2-obs))<1e-11
    # Exact central case: the switch compares the two orderings of Pauli gates.
    u=P[0];v=next(t for t in P if symp(u,t)!=0)
    A=pauli(u);B=pauli(v)
    center=(B@A).conj().T@(A@B)
    assert np.max(abs(center-OMEGA**symp(u,v)*I9))<1e-12
    a0=np.einsum("aij,ji->a",q,center)
    assert max(abs(a0-np.mean(a0)))<1e-12
    return {
     "input_Hesse_SIC_states_each_factor":9,
     "tensor_product_informationally_complete_probes":81,
     "frame_Gram_eigenvalues":{"9":1,"2.25":16,"0.5625":64},
     "frame_Gram_condition_number":16.,
     "max_operator_reconstruction_error":float(np.max(np.abs(recovered-K))),
     "operator_noncentral_Frobenius_norm":frob_noncentral,
     "SIC_Gram_inverse_quadratic_certificate":cert,
     "noncentrality_visibility_phase_invariant_ratio":defect_ratio(obs),
     "uniform_phase_visibility_cancellation":True,
     "simultaneous_gauge_covariance":True,
     "ideal_center_81_probe_deviation_max":float(max(abs(a0-a0.mean()))),
     "limitation":"The qutrit SIC is established prior art. Any actual interferometer needs coherent reference, calibrated input-independent visibility and a physical gate implementation."
    }

def statistics(delta=.01,epsilon=.25):
    # 2m +/-1-valued control quadratures; each outcome is iid, N per quadrature.
    # Union-Hoeffding radius t = sqrt(2 log(4m/delta)/N).
    # With m=81 complex probe values, ||K-kI||_F <=
    # 4/3 ( sqrt(sum |a_hat - mean|²) + sqrt(2m)*t).
    m=81
    n=math.ceil(2*math.log(4*m/delta)*(((4/3)*math.sqrt(2*m))/epsilon)**2)
    bound=(4/3)*math.sqrt(2*m)*math.sqrt(2*math.log(4*m/delta)/n)
    assert bound<=epsilon+1e-12
    v=.8;drift=.1
    min_im=v*((math.sqrt(3)/2)*math.cos(drift)-.5*math.sin(drift))
    shots_sign=math.ceil(2*math.log(2/delta)/(min_im**2))
    return {
      "delta":delta,
      "noncentral_Frobenius_tolerance":epsilon,
      "conservative_individual_accepted_shots_per_each_of_162_quadrature_settings":n,
      "total_accepted_81_input_2_quadrature_shots":162*n,
      "central_Frobenius_sampling_bound_if_empirical_probe_spread_zero":bound,
      "minimum_quadrature_imag_signal_visibility_0p8_drift_0p1":min_im,
      "accepted_shots_to_resolve_chirality_sign_with_calibrated_frame":shots_sign,
      "shot_bound_scope":"IID +/-1 readout, 99% union guarantee, ideal preparation and visibility=1. Known visibility v<1 inflates the corrected amplitude error by 1/v and shot requirement by 1/v^2; phase/visibility calibration uncertainty excluded."
    }

def failure_controls():
    """Known finite counterexamples to overinterpreting the switch fringes."""
    P=points()
    u,v=next((a,b) for a in P for b in P if symp(a,b)==1)
    A,B=pauli(u),pauli(v)
    U0,U1=A@B,B@A
    state=np.diag(np.arange(1,10,dtype=float)/45.)
    control_blind=float(np.linalg.norm(U0@state@U0.conj().T -
                                      U1@state@U1.conj().T))
    assert control_blind<1e-12
    # A classical probabilistic mixture of definite orders removes relative
    # branch phase; only coherence between orders makes that phase observable.
    ordinary_mix=.5*(U0@state@U0.conj().T+U1@state@U1.conj().T)
    assert np.max(abs(ordinary_mix-U1@state@U1.conj().T))<1e-12
    z=OMEGA*np.ones(81,complex)
    vis=.80+.06*np.sin(np.arange(81)*.61)
    a=vis*z
    inv9=(4/3)*np.eye(9)-np.ones((9,9))/9
    inv81=np.kron(inv9,inv9)
    delta=a-a.mean()
    false_norm=float(np.sqrt(np.real(np.vdot(delta,inv81@delta))))
    assert false_norm>.01
    return {
       "definite_order_target_output_difference_for_central_commutator":control_blind,
       "classical_mixture_cannot_reveal_center_phase":True,
       "input_dependent_visibility_falsely_inferred_noncentral_norm":false_norm,
       "experimental_requirement":"A physical order-superposition control and per-input visibility/SPAM calibration, not merely a classical choice of order."
    }

def quadratic_character_extension():
    """Projective Maslov-type sign extends to odd prime fields via Legendre."""
    rng=np.random.default_rng(20261120)
    rows=[]
    for p in (3,5,7,11):
        legendre=lambda x:(0 if x%p==0 else
                           (1 if pow(int(x)%p,(p-1)//2,p)==1 else -1))
        sy=lambda u,v:(u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%p
        def maslov(u,v,w):
            return legendre(sy(u,v)*sy(v,w)*sy(w,u))
        accepted=0
        for attempt in range(500):
            v=[tuple(map(int,rng.integers(0,p,size=4))) for _ in range(3)]
            if any(not any(t) for t in v) or maslov(*v)==0:continue
            base=maslov(*v)
            scales=[int(rng.integers(1,p)) for _ in range(3)]
            rescaled=[tuple(s*x%p for x in vector) for s,vector in zip(scales,v)]
            assert maslov(*rescaled)==base
            anti=[tuple((x if i<2 else -x)%p for i,x in enumerate(z)) for z in v]
            assert maslov(*anti)==base*legendre(-1)
            accepted+=1
        assert accepted>=60
        rows.append({"prime_field":p,"random_nonorthogonal_triples_checked":accepted,
                     "chi_of_minus_one":legendre(-1),
                     "negative_symplectic_multiplier_reverses_Maslov_sign":legendre(-1)==-1})
    assert [r["chi_of_minus_one"] for r in rows]==[-1,1,-1,-1]
    return {"finite_field_projective_sign_formula":
            "Legendre(<u,v><v,w><w,u>), with value 0 for any commuting pair",
            "exact_projective_scaling_invariance":"Each point rescaling contributes its square to the triple pairing product.",
            "GSp_multiplier_rule":"M(g u,g v,g w)=Legendre(mu(g)) M(u,v,w) for symplectic multiplier mu(g).",
            "odd_prime_samples":rows,
            "physical_boundary":"A finite-field multiplier character is not a physical parity or chiral fermion index."}

def main(write=True):
    data={"status":"PASS_FINITE_SYMPLECTIC_SWITCH_SIC_RECONSTRUCTION",
          "prior_art":"Two-qutrit W(3,3) commutation, quantum switches and Hesse SIC states are established. The increment is their explicitly certified combined switch/probe/chirality protocol.",
          "geometry":geometry(),
          "quantum_switch":operator_switch(),
          "SIC_controlled_order_operator_tomography":sic_operator_frame(),
          "shot_planning":statistics(),
          "projective_quadratic_character_extension":quadratic_character_extension(),
          "failure_controls":failure_controls(),
          "physics_boundary":"An optical nine-mode qutrit algebra is not physical QCD colour. Chirality phase sign at a projective point requires a lift; a triple product cancels that lift. Physical SU3 gauge holonomy requires a genuinely charged gauge-invariant reference and observable. No emergence of spacetime, gravitational law or particle mass claimed."}
    if write:
        OUTPUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf8")
    return data

if __name__=="__main__":
    print(json.dumps(main(),indent=2))
