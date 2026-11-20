#!/usr/bin/env python3
"""Six quantum-switch phase settings reconstruct an *assumed bilinear*
two-qutrit symplectic commutator, with explicit nonlinear holdout falsifier.
Not a certification of arbitrary black-box operators or a TOE.
"""
import json, math
from itertools import combinations,product
from pathlib import Path
import numpy as np
from toe_20261120_symplectic_order_sic_switch import (
    OMEGA,points,symp,pauli
)

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"data/toe_20261120_six_switch_symplectic_frame.json"
E=np.eye(4,dtype=int)
J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]],dtype=int)%3

def mod3det(A):
    M=np.array(A,dtype=int)%3
    n=M.shape[0];rank=0;det=1
    for col in range(n):
        pivot=next((r for r in range(rank,n) if M[r,col]),None)
        if pivot is None:return 0
        if pivot!=rank:
            M[[rank,pivot]]=M[[pivot,rank]]
            det=-det
        value=int(M[rank,col]);det*=value
        M[rank]=(M[rank]*pow(value,-1,3))%3
        for r in range(rank+1,n):
            factor=int(M[r,col])
            M[r]=(M[r]-factor*M[rank])%3
        rank+=1
    return det%3

def pfaffian(A):
    M=np.asarray(A,dtype=int)%3
    return int((M[0,1]*M[2,3]-M[0,2]*M[1,3]+M[0,3]*M[1,2])%3)

def count_all_forms():
    count={0:0,1:0,2:0}
    for a,b,c,d,e,f in product(range(3),repeat=6):
        p=(a*f-b*e+c*d)%3
        count[p]+=1
    assert count=={0:261,1:234,2:234}
    return {"all_alternating_forms":729,
            "singular":count[0],"nondegenerate":count[1]+count[2],
            "pfaffian_one":count[1],"pfaffian_two":count[2],
            "proof":"Pfaffian=a f-b e+c d. For (a,b,c)=0, all 27 (f,-e,d) vanish in dot; for each of 26 other vectors there are 9 zero-dot choices: 27+26*9=261."}

def frame_from_switch(basis):
    """Take the six central phases of four labeled generators."""
    labels=[tuple(int(x)%3 for x in np.asarray(basis)[:,j]) for j in range(4)]
    gram=np.zeros((4,4),dtype=int)
    phases={}
    for i,j in combinations(range(4),2):
        A,B=pauli(labels[i]),pauli(labels[j])
        a0,a1=A@B,B@A
        coherence=np.trace(a0@a1.conj().T)/9
        err=[abs(coherence-OMEGA**s) for s in range(3)]
        s=int(np.argmin(err))
        assert err[s]<1e-12
        gram[i,j]=s
        gram[j,i]=(-s)%3
        phases[f"{i}{j}"]=s
    assert np.array_equal(gram,(basis.T@J@basis)%3)
    return gram,phases

def verify_random_frames():
    rng=np.random.default_rng(2326)
    matrices=[np.eye(4,dtype=int)]
    while len(matrices)<24:
        a=rng.integers(0,3,size=(4,4))
        if mod3det(a):matrices.append(a)
    points40=points()
    max_err=0.
    for M in matrices:
        G,phases=frame_from_switch(M)
        assert pfaffian(G)!=0 and mod3det(G)==pfaffian(G)**2%3
        assert len(phases)==6
        for u,v in combinations(points40,2):
            val=int((np.array(u)@G@np.array(v))%3)
            vActual=tuple(int(x) for x in (M@np.array(v))%3)
            uActual=tuple(int(x) for x in (M@np.array(u))%3)
            assert val==symp(uActual,vActual)
            U,V=pauli(uActual),pauli(vActual)
            max_err=max(max_err,float(np.max(np.abs(U@V-OMEGA**val*V@U))))
    assert max_err<2e-14
    return {"random_GL4_frames_tested":len(matrices),
            "all_780_pair_predictions_per_frame":True,
            "predicted_pairs_checked":780*len(matrices),
            "max_Weyl_commutator_residual":max_err,
            "standard_basis_six_pair_phase_labels":frame_from_switch(np.eye(4,dtype=int))[1],
            "standard_basis_pfaffian":pfaffian(J)}

def phase_class(z):
    s=int(np.argmin([abs(math.atan2((z/(OMEGA**k)).imag,(z/(OMEGA**k)).real))
                     for k in range(3)]))
    return s

def finite_shot_demo(delta=.01,vmin=.8,drift=.1):
    m=6
    rho=vmin*math.sin(math.pi/3-drift)
    eps=.99*rho
    N=math.ceil(4*math.log(4*m/delta)/eps**2)
    assert N==76
    rng=np.random.default_rng(2424)
    truth=[symp(E[:,i],E[:,j]) for i,j in combinations(range(4),2)]
    fail=0;trials=2000
    for _ in range(trials):
        signs=[]
        for s in truth:
            vis=float(rng.uniform(vmin,1))
            phi=float(rng.uniform(-drift,drift))
            c=vis*np.exp(1j*phi)*(OMEGA**s)
            kx=rng.binomial(N,(1+c.real)/2)
            ky=rng.binomial(N,(1+c.imag)/2)
            estimate=(2*kx/N-1)+1j*(2*ky/N-1)
            signs.append(phase_class(estimate))
        if signs!=truth:fail+=1
    return {
      "settings_basis_pairs":6,"two_quadratures_per_pair":True,
      "accepted_shots_per_quadrature":N,
      "accepted_shots_total":12*N,
      "confidence_union_lower_bound":1-delta,
      "minimum_visibility":vmin,"maximum_phase_drift_radians":drift,
      "radial_angle_margin":rho,
      "independent_seeded_trials":trials,"simulation_any_six_phase_misclassifications":fail,
      "scope":"99% worst-case bound assumes independent +-1 quadrature samples, known basis labels, v>=0.8 and drift<=0.1 for each setting; it does not certify that physical black-box gates obey the Weyl product law."
    }

def nonlinear_holdout():
    """An adversarial antisymmetric phase table agrees on six basis pairs."""
    def fake(u,v):
        t=(int(u[0])*int(u[1])*int(v[2])-
           int(v[0])*int(v[1])*int(u[2]))%3
        return (symp(u,v)+t)%3
    for i,j in combinations(range(4),2):
        assert fake(E[:,i],E[:,j])==symp(E[:,i],E[:,j])
    u=(E[:,0]+E[:,1])%3
    v=E[:,2]
    predicted=symp(u,v)
    observed=fake(u,v)
    assert predicted==1 and observed==2
    assert fake(v,u)==(-observed)%3
    return {"passes_all_six_basis_calibrations":True,
            "composite_holdout_u":"e0+e1","composite_holdout_v":"e2",
            "bilinear_prediction":int(predicted),"adversarial_actual_phase":int(observed),
            "invalid_assumption":"Six settings identify an alternating bilinear form only under an independently tested Weyl/address linearity promise. Nonlinear word-dependent devices can fake all six."}

def main(write=True):
    data={"status":"PASS_SIX_SWITCH_BILINEAR_FRAME_WITH_HOLDOUT_FALSIFIER",
          "prior_art":"Alternating forms over F3 and quantum-switch phase readout are standard. This is a bounded design/testing reduction, not a new quantum-information primitive.",
          "alternating_form_count":count_all_forms(),
          "exact_frame_checks":verify_random_frames(),
          "finite_shot_conservative_planning":finite_shot_demo(),
          "adversarial_holdout":nonlinear_holdout(),
          "physical_boundary":"A six-parameter alternating form is not a dynamical TOE; its standard nondegenerate realizations are all isomorphic under GL4(F3). Physical gate address linearity and nonclassical order certification need additional measurements."}
    if write: OUTPUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf8")
    return data

if __name__=="__main__":print(json.dumps(main(),indent=2))
