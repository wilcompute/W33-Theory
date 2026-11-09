#!/usr/bin/env python3
"""Single-photon internal DoF entanglement vs genuine spatial Bell locality.

A two-qutrit factorization of ONE photon can yield abstract CHSH=2sqrt2
for compatible internal observables, but does not establish two distant
independent measurement parties. Passive optics cannot create two clicks
in disjoint detectors from one photon with photon counting alone.
A global instrument conjugation makes entangled and separable sources
statistically indistinguishable if full POVM calibration is untrusted.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from w33_20261109_q8_ten_context_optimize import main as optimize

Z=np.diag([1.,-1.,1.])
X=np.array([[0,1,0],[1,0,0],[0,0,1]],complex)
B0=(Z+X)/np.sqrt(2)
B1=(Z-X)/np.sqrt(2)
# The third-level extension in B0/B1 need not have ±1 spectrum because
# target states use only |0>,|1>; choose third eigenvalue +1 explicitly.
B0[2,2]=1.
B1[2,2]=1.

def internal_chsh():
    q=np.zeros(9,complex)
    q[0]=q[4]=1/np.sqrt(2)
    A=[Z,X];B=[B0,B1]
    es=[[float(np.vdot(q,np.kron(a,b)@q).real) for b in B] for a in A]
    S=es[0][0]+es[0][1]+es[1][0]-es[1][1]
    assert abs(S-2*np.sqrt(2))<5e-14
    assert all(abs(np.linalg.eigvalsh(x)).max()<1+1e-12 for x in A+B)
    return {"embedded_qutrit_state":"(|00>+|11>)/sqrt(2) inside C3 tensor C3, one photon internal degrees of freedom",
            "correlators":es,"CHSH_abs":abs(S),"local_realist_bound":2,
            "Tsirelson_bound":2*math.sqrt(2),
            "spatial_nonlocality_certified":False,
            "meaning":"If the two qutrit subsystems are both degrees of freedom of a single photon at one laboratory, CHSH algebra violates the abstract local-hidden-variable factorability inequality but no spacelike separation or independent-party locality is established."}

def passive_spatial_clicks():
    rng=np.random.default_rng(20261109299)
    norm_errors=[];samples=[]
    for _ in range(16):
        v=rng.normal(size=18)+1j*rng.normal(size=18)
        v/=np.linalg.norm(v)
        A=float(sum(abs(v[:9])**2))
        B=float(sum(abs(v[9:])**2))
        # In a one-photon Fock sector, P(click A) P(click B) == 0.
        joint=float(0.)
        norm_errors.append(abs(A+B-1))
        samples.append([A,B,joint])
    assert max(norm_errors)<1e-13
    return {"independent_detector_regions":["A modes 0..8","B modes 9..17"],
            "single_photon_number_constraint":"N_A+N_B=1, so P(N_A>=1 and N_B>=1)=0 for photon-number-resolving or ideal threshold counters",
            "single_photon_two_party_coincidence_probability":0.,
            "random_optical_wavefunction_controls":len(samples),
            "max_normalization_error":max(norm_errors),
            "example_distribution":samples[0],
            "no_go_scope":"Vacuum ancillas, passive photon-number preserving interferometry and photon counting; NOT a prohibition on single-photon spatial mode entanglement, homodyne measurements with local oscillators, heralding, or multi-photon resource protocols."}

def untrusted_measurement_gauge():
    _,(Bell,U,V,ops)=optimize(return_components=True)
    bases=[Bell[:,9*j:9*(j+1)] for j in range(8)]+[U,V]
    product=np.zeros(9,complex);product[0]=1.
    W=np.eye(9,dtype=complex)
    c=1/np.sqrt(2)
    W[np.ix_([0,4],[0,4])]=np.array([[c,-c],[c,c]])
    ent=W@product
    assert abs(np.vdot(ent,ent)-1)<1e-12
    rho0=np.outer(product,product.conj())
    rho1=np.outer(ent,ent.conj())
    assert np.max(abs(rho0-rho1))>.1
    diffs=[]
    for basis in bases:
        for j in range(9):
            projector=np.outer(basis[:,j],basis[:,j].conj())
            changed=W.conj().T@projector@W
            p_ent=float(np.trace(rho1@projector).real)
            p_sep=float(np.trace(rho0@changed).real)
            diffs.append(abs(p_ent-p_sep))
    assert max(diffs)<1e-12
    sv_ent=np.linalg.svd(ent.reshape(3,3),compute_uv=False)
    sv_sep=np.linalg.svd(product.reshape(3,3),compute_uv=False)
    assert sv_ent[1]>.7 and sv_sep[1]<1e-12
    return {"contexts":10,"outcome_probabilities":90,
            "untrusted_POVM_global_unitary":"E_sep= W^dag E_ent W with rho_ent=W rho_sep W^dag",
            "max_indistinguishability_error":max(diffs),
            "entangled_schmidt_coefficients":sv_ent.tolist(),
            "separable_schmidt_coefficients":sv_sep.tolist(),
            "physical_effects_all_projective":True,
            "consequence":"If all measurement POVMs and subsystem-local operations are untrusted, the same 90 observed probabilities are compatible with a maximally entangled internal state OR a pure product state and a globally rotated measurement instrument. Operational tensor-local calibration is essential."}

def main(path=None):
    data={"status":"PASS_SINGLE_PHOTON_INTERNAL_CHSH_VERSUS_SPATIAL_CAUSAL_NO_GO",
          "internal_degree_of_freedom":internal_chsh(),
          "passive_spatial_detection":passive_spatial_clicks(),
          "untrusted_POVM_ambiguity":untrusted_measurement_gauge(),
          "prior_art":"Single-photon contextuality/nonseparability and Bell network locality are distinct. PRL 134 010203 (2025) studies conversion of contextuality into NONLOCALITY using two-photon OAM entanglement. Nonlocality cannot be certified merely by formal C3 tensor C3 decomposition.",
          "scope":"Symbolic finite-state algebra plus numerical controls; no spacelike-separated Bell apparatus implemented or loophole-free experimental Bell score asserted."}
    if path:Path(path).write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS photonic causal control",json.dumps({
        "CHSH":data["internal_degree_of_freedom"]["CHSH_abs"],
        "two_click_probability":data["passive_spatial_detection"]["single_photon_two_party_coincidence_probability"],
        "instrument_ambiguity":data["untrusted_POVM_ambiguity"]["max_indistinguishability_error"]}))
    return data
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
