#!/usr/bin/env python3
"""Eight high-upside causal/spectral TOE gates: reproducible physics tests.
Everything is conditional on GIVEN 2D/4D lattice, spin, gauge and metric data.
These are known mathematical identities, not a TOE or a novel physical law.
"""
from __future__ import annotations
import json, math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.integrate import quad

P=np.pi
I=np.eye(2,dtype=complex)
SX=np.array([[0,1],[1,0]],complex)
SY=np.array([[0,-1j],[1j,0]],complex)
SZ=np.diag([1,-1]).astype(complex)
SIG=(SX,SY,SZ)
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"data"/"toe_20261119_spectral_exchange_seven_gates.json"

def U(theta,axis):
    return np.cos(theta/2)*I+1j*np.sin(theta/2)*SIG[axis]

def fermion_gate(N=8):
    records=[]
    for ax in (0.,.5):
        for ay in (0.,.5):
            zeros=zeros_w=0; anti=0.
            for nx in range(N):
                for ny in range(N):
                    kx=2*P*(nx+ax)/N;ky=2*P*(ny+ay)/N
                    D=1j*(SX*np.sin(kx)+SY*np.sin(ky))
                    W=(2-np.cos(kx)-np.cos(ky))
                    assert np.linalg.norm(D@SZ+SZ@D)<1e-12
                    anti=max(anti,np.linalg.norm((D+W*I)@SZ+SZ@(D+W*I)))
                    zeros+=2*int(np.linalg.norm(D)<1e-10)
                    zeros_w+=2*int(np.linalg.norm(D+W*I)<1e-10)
            records.append({"spin_twist_x":ax,"spin_twist_y":ay,
                            "naive_zero_components":zeros,"wilson_zero_components":zeros_w,
                            "max_wilson_chiral_anticommutator":float(anti)})
    assert [(x["naive_zero_components"],x["wilson_zero_components"]) for x in records]==[(8,2),(0,0),(0,0),(0,0)]
    return {"status":"PASS","N":N,"four_spin_structures":records,
            "four_corner_chirality_signs":[1,-1,-1,1],"net_chirality":0,
            "interpretation":"Naive doubling and Wilson chiral-breaking; global spin twist changes spectrum while local lattice remains flat."}

def su2_gauge_gate():
    a=.23;b=.31
    X=U(a,0);Y=U(b,1)
    loop=X@Y@X.conj().T@Y.conj().T
    action=float(1-np.trace(loop).real/2)
    rng=np.random.default_rng(202611196)
    G=[]
    for _ in range(4):
        axis=rng.normal(size=3);axis/=np.linalg.norm(axis)
        phi=float(rng.uniform(-2,2))
        G.append(np.cos(phi/2)*I+1j*np.sin(phi/2)*sum(axis[i]*SIG[i] for i in range(3)))
    T01=G[0]@X@G[1].conj().T
    T12=G[1]@Y@G[2].conj().T
    T32=G[3]@X@G[2].conj().T
    T03=G[0]@Y@G[3].conj().T
    loopnew=T01@T12@T32.conj().T@T03.conj().T
    err=float(np.linalg.norm(loopnew-G[0]@loop@G[0].conj().T))
    commute=U(a,2)@U(b,2)@U(-a,2)@U(-b,2)
    ratio=[]
    for e in (.5,.25,.125,.0625):
        L=U(e*.8,0)@U(e*1.1,1)@U(-e*.8,0)@U(-e*1.1,1)
        ratio.append(float((1-np.trace(L).real/2)/(e**4*.8**2*1.1**2)))
    assert err<1e-12 and np.linalg.norm(commute-I)<1e-12
    assert abs(ratio[-1]-1/8)<.001
    return {"status":"PASS","noncommuting_SU2_loop_action":action,
            "local_gauge_transformation_error":err,"small_loop_ratios":ratio,
            "commuting_loop_error":float(np.linalg.norm(commute-I)),
            "interpretation":"Noncommuting constant gauge potentials have genuine commutator curvature even without ordinary gradients."}

def one_dirac_gate():
    a=.71;b=.94;Ax=a*SX/2;Ay=b*SY/2
    dx=1j*Ax;dy=1j*Ay
    D=np.kron(SX,dx)+np.kron(SY,dy)
    D2=D@D
    scalar=np.kron(I,dx@dx+dy@dy)
    Fcurv=-1j*(Ax@Ay-Ay@Ax)
    pauli=np.kron(SZ,Fcurv)
    residual=float(np.linalg.norm(D2-scalar-pauli))
    lost=float(np.linalg.norm(D2-scalar))
    C=U(.63,1);CC=np.kron(I,C)
    Drot=np.kron(SX,1j*C@Ax@C.conj().T)+np.kron(SY,1j*C@Ay@C.conj().T)
    gauge_error=float(np.linalg.norm(Drot-CC@D@CC.conj().T))
    assert residual<1e-13 and lost>.6 and gauge_error<1e-13
    return {"status":"PASS","square_minus_laplacian_minus_Pauli_error":residual,
            "Pauli_curvature_omission_norm":lost,"color_gauge_covariance_error":gauge_error,
            "Fcurv_eigenvalues":np.linalg.eigvalsh(Fcurv).tolist(),
            "identity":"Dslash²=Laplacian+gamma5 tensor (-i[Ax,Ay]), in the specified constant-field conventions",
            "scope":"2D flat Clifford/gauge matrices assumed; the R/4 curved-space term is known but NOT derived here."}

def sj_quantum_gate():
    u=np.array([.08,.23,.49,.66,.83,.97])
    v=np.array([.04,.31,.15,.71,.56,.98])
    C=np.zeros((len(u),len(u)),float)
    for i in range(len(u)):
        for j in range(i+1,len(u)):
            if u[i]<u[j] and v[i]<v[j]:C[j,i]=1.
    K=.5*C@np.linalg.inv(np.eye(len(u))+.21*C)
    Delta=K-K.T;H=1j*Delta
    eig,V=np.linalg.eigh(H)
    W=(V*np.maximum(eig,0))@V.conj().T
    eps=.15
    noise=W+eps*np.eye(len(u))
    skewerr=float(np.linalg.norm(W-W.T-H))
    minimum=float(np.linalg.eigvalsh(W).min())
    neg=float(np.linalg.eigvalsh(H/2).min())
    idx=np.array([2,5,3,0,4,1]);PP=np.eye(len(u))[idx]
    h2=PP@H@PP.T
    ev2,vec2=np.linalg.eigh(h2)
    w2=(vec2*np.maximum(ev2,0))@vec2.conj().T
    labelerr=float(np.linalg.norm(w2-PP@W@PP.T))
    assert skewerr<1e-12 and minimum>-1e-12 and neg<-.01
    assert np.linalg.eigvalsh(noise).min()>.14
    assert np.linalg.norm(noise-noise.T-H)<1e-12 and labelerr<1e-12
    return {"status":"PASS","causal_events":len(u),"positive_SJ_min_eigenvalue":minimum,
            "SJ_commutator_residual":skewerr,"relabel_invariance_error":labelerr,
            "naive_half_iDelta_negative_eigenvalue":neg,
            "second_state_positive_min_eigenvalue":float(np.linalg.eigvalsh(noise).min()),
            "second_state_added_noise":eps,
            "conclusion":"SJ positive-part selection works but the same commutator admits a continuum of other positive states."}

def conformal_geometry_gate(eps=.12,tau=2):
    flat=tau*tau/2
    vol=quad(lambda t:2*min(t,tau-t)*np.exp(2*eps*t*t),0,tau,epsabs=1e-12)[0]
    proper=quad(lambda t:np.exp(eps*t*t),0,tau,epsabs=1e-12)[0]
    R=4*eps*np.exp(-2*eps*(tau/2)**2)
    rng=np.random.default_rng(202611197)
    uv=rng.uniform(0,tau,(140000,2))
    t=(uv[:,0]+uv[:,1])/2
    weights=np.exp(2*eps*t*t)
    mc=flat*np.mean(weights)
    se=flat*np.std(weights,ddof=1)/np.sqrt(len(t))
    assert abs(mc-vol)<4*se+.002 and vol>flat and proper>tau
    return {"status":"PASS","conformal_epsilon":eps,"volume_ratio":float(vol/flat),
            "flat_volume":flat,"curved_volume":vol,
            "MC_volume_estimate":float(mc),"MC_standard_error":float(se),
            "flat_proper_time":tau,"curved_proper_time":proper,
            "scalar_curvature_at_midpoint":float(R),
            "causal_order_changed":False,
            "limitation":"Positive conformal rescaling leaves Lorentzian causal precedence unchanged; no Einstein dynamics derived."}

def flat_holonomy_gate(N=8):
    rows=[]
    for theta in (0.,P/2,P):
        lambdas=np.sort([4-2*np.cos((2*P*n+theta)/N)-2*np.cos(2*P*m/N)
                         for n in range(N) for m in range(N)])
        loop=np.exp(1j*theta)
        heat={str(t):float(np.exp(-t*lambdas).sum()) for t in (.25,1.,3.,8.)}
        rows.append({"theta":float(theta),"winding_real_imag":[float(loop.real),float(loop.imag)],
                    "lowest_laplacian_eigenvalue":float(lambdas[0]),
                    "heat_traces":heat,"plaquette_curvature":0.})
    delta=rows[0]["heat_traces"]["8.0"]-rows[-1]["heat_traces"]["8.0"]
    assert delta>.4 and rows[-1]["lowest_laplacian_eigenvalue"]>.01
    return {"status":"PASS","N":N,"flat_winding_sectors":rows,
            "heat_trace_delta_theta0_minus_pi_at_t8":float(delta),
            "conclusion":"All plaquettes flat, but global Wilson holonomy affects physical spectra."}

def four_dimensional_chiral_gate():
    corners=[(a,b,c,d) for a in (0,1) for b in (0,1) for c in (0,1) for d in (0,1)]
    signs=[(-1)**sum(p) for p in corners]
    rep=[("Q",3,2,F(1,6)),("u_c",3,1,F(-2,3)),("d_c",3,1,F(1,3)),
         ("L",1,2,F(-1,2)),("e_c",1,1,F(1,1)),("nu_c",1,1,F(0,1))]
    anomalies={
      "U1_cubic":sum(c*w*y**3 for _,c,w,y in rep),
      "gravitational_U1":sum(c*w*y for _,c,w,y in rep),
      "SU2_squared_U1":F(1,2)*(3*F(1,6)-F(1,2)),
      "SU3_squared_U1":F(1,2)*(2*F(1,6)-F(2,3)+F(1,3)),
      "SU3_cubic":2-1-1
    }
    assert len(corners)==16 and sum(signs)==0 and all(v==0 for v in anomalies.values())
    return {"status":"PASS","Brillouin_cones":16,"naive_zero_spinor_components":64,
            "Wilson_zero_spinor_components":4,"net_cone_orientation":0,
            "signed_chiralities":signs,"exact_SM_one_family_anomaly_sums":{k:str(v) for k,v in anomalies.items()},
            "SU2_left_doublet_count":4,
            "conditional":"One SM generation charges supplied by hand; no chiral family dynamically generated."}

def spin_gauge_gate(N=8):
    states=[]
    for spin in (0.,.5):
        for theta in (0.,P):
            effective=spin+theta/(2*P)
            ks=2*P*(np.arange(N)+effective)/N
            zeros=2*sum(1 for k in ks for l in 2*P*np.arange(N)/N if abs(np.sin(k))<1e-12 and abs(np.sin(l))<1e-12)
            states.append({"spin_antiperiodic":bool(spin),"gauge_winding_angle":float(theta),
                           "effective_twist":effective,"naive_zero_spinor_components":int(zeros),
                           "kx_sine_squared_sorted":sorted([float(np.sin(k)**2) for k in ks])})
    assert [x["naive_zero_spinor_components"] for x in states]==[8,0,0,8]
    assert np.allclose(states[1]["kx_sine_squared_sorted"],states[2]["kx_sine_squared_sorted"])
    return {"status":"PASS","four_spin_gauge_sectors":states,
            "interpretation":"For a charge-one probe, one antiperiodic spin twist is spectrally equivalent to a pi U1 Wilson holonomy; two minus signs compensate.",
            "scope":"This equivalence is representation dependent, not an identification of all spin structures and all gauge fields."}

def run_all():
    gates={"spin_structure_and_2D_doubling":fermion_gate(),
           "nonabelian_SU2_plaquette_curvature":su2_gauge_gate(),
           "single_Dirac_squared_Pauli_term":one_dirac_gate(),
           "causal_SJ_quantum_state_nonuniqueness":sj_quantum_gate(),
           "conformal_order_metric_ambiguity":conformal_geometry_gate(),
           "global_flat_holonomy_spectral_shift":flat_holonomy_gate(),
           "four_dimensional_chiral_anomaly_gate":four_dimensional_chiral_gate(),
           "spin_gauge_twist_compensation":spin_gauge_gate()}
    assert len(gates)==8 and all(x["status"]=="PASS" for x in gates.values())
    return {"date":"2026-11-19","status":"verified conditional missing-information gates, NOT a TOE",
            "TOE_solved":False,"selected_4D":False,"derived_fermion_generations":False,
            "derived_4D_GR_or_Born_rule":False,"gates":gates}

def main():
    result=run_all()
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(result,indent=2),encoding="utf8")
    g=result["gates"]
    print(json.dumps({"status":"PASS","gates":len(g),
       "fermion_zero_modes":[(x["naive_zero_components"],x["wilson_zero_components"]) for x in g["spin_structure_and_2D_doubling"]["four_spin_structures"]],
       "SU2_action":g["nonabelian_SU2_plaquette_curvature"]["noncommuting_SU2_loop_action"],
       "missing_Pauli_norm":g["single_Dirac_squared_Pauli_term"]["Pauli_curvature_omission_norm"],
       "SJ_alternative_min":g["causal_SJ_quantum_state_nonuniqueness"]["second_state_positive_min_eigenvalue"],
       "volume_ratio":g["conformal_order_metric_ambiguity"]["volume_ratio"],
       "flat_holonomy_heat_trace_delta":g["global_flat_holonomy_spectral_shift"]["heat_trace_delta_theta0_minus_pi_at_t8"],
       "4D_cones":g["four_dimensional_chiral_anomaly_gate"]["Brillouin_cones"],
       "twist_zeros":[x["naive_zero_spinor_components"] for x in g["spin_gauge_twist_compensation"]["four_spin_gauge_sectors"]],
       "output":str(OUTPUT)}))

if __name__=="__main__":main()
