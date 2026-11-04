#!/usr/bin/env python3
"""Ensemble-dependent Holevo upper bound and epsilon/no-click controls on 440 E8-derived ququart states.

Assumptions: all 440 root labels equiprobable, each independently prepares
a ququart density matrix rho_r(eps)=I4/4+eps/sqrt2*t_r.O, the 40-outcome
Witting POVM is a specified *fixed* decoder. The exact upper bound on
accessible information is chi=S(average state)-avg S(rho_r), NOT two bits
except as a coarse Hilbert dimension bound.

By antipodal root symmetry average state is I4/4, and mean POVM
probabilities are 1/40. Compute chi and Witting I per detected photon,
scan eps and independent heralded erasure eta, and Fano lower bound
on necessary repeated-copy count under fixed-measurement iid model.

This does NOT prove optimal POVM, nor sufficiency of Fano sample count.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
OUT=ROOT/"data/toe_20261104_two_e8_witting_holevo_capacity_scan.json"

def entropy(v):
    y=np.asarray(v,dtype=float)
    assert np.min(y)>=-1e-10
    y=y[y>0]
    return float(-np.sum(y*np.log2(y)))
def fano_need(bits,eta=1):
    h=.05
    minimum=math.log2(440)-entropy([h,1-h])-h*math.log2(439)
    assert bits>0
    return math.ceil(minimum/(eta*bits))
def main():
    j=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
    k=json.loads((ROOT/"data/toe_20261104_two_e8_root_to_witting_density_codebook.json").read_text())
    C=j["A5_classes"][1]
    E=np.array(C["explicit_W33_40x8_observable_coefficient_map"])
    Ops=np.array(C["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(C["explicit_8_Hermitian_ququart_observables_imag"])
    theta01=np.array(k["eight_real_parameters_for_440_states"])
    assert theta01.shape==(440,8)
    assert E.shape==(40,8) and Ops.shape==(8,4,4)
    assert np.max(abs(theta01.mean(axis=0)))<1e-10
    assert np.max(abs(E.T@E-np.eye(8)))<1e-10
    assert np.max(abs(np.real(np.einsum("iab,jba->ij",Ops,Ops))-2*np.eye(8)))<1e-9
    records=[]
    for eps in (.02,.05,.1,.15,.2,.225):
        theta=theta01*(eps/.1)
        rho=np.eye(4)[None,:,:]/4 + np.einsum("ij,jab->iab",theta,Ops)
        eig=np.linalg.eigvalsh(rho)
        mi=float(np.min(eig))
        positive=mi>=-1e-12
        if not positive:
            records.append(dict(epsilon=eps,all_440_PSD=False,minimum_eigenvalue=mi))
            continue
        rbar=rho.mean(axis=0)
        assert np.max(abs(rbar-np.eye(4)/4))<1e-10
        vv=np.array([entropy(x) for x in eig])
        chi=entropy(np.linalg.eigvalsh(rbar))-float(vv.mean())
        probs=np.ones((440,40))/40+theta@E.T/5
        assert probs.min()>0 and np.max(abs(probs.sum(axis=1)-1))<1e-10
        marginal=probs.mean(axis=0)
        assert np.max(abs(marginal-1/40))<1e-10
        I=float(np.mean(np.sum(probs*np.log2(probs/marginal),axis=1)))
        assert 0<I<chi<2
        n1=fano_need(I)
        n85=fano_need(I,.85)
        records.append(dict(epsilon=eps,all_440_PSD=True,
           minimum_eigenvalue=mi,
           minimum_probability=float(probs.min()),
           average_state_is_exact_maximally_mixed=True,
           ensemble_average_von_Neumann_entropy_bits=float(vv.mean()),
           holevo_bound_bits_per_ququart=chi,
           fixed_Witting_POVM_information_bits_per_detected_photon=I,
           Witting_fraction_of_Holevo_upper_bound=I/chi,
           upper_bound_to_actual_Witting_information_ratio=chi/I,
           Fano_necessary_detected_photons_for_5pct_error=n1,
           Fano_necessary_incident_photons_for_5pct_error_eta085=n85,
           total_information_per_incident_photon_eta085=.85*I))
    baseline=next(z for z in records if z["epsilon"]==.1)
    assert baseline["all_440_PSD"]
    assert abs(baseline["fixed_Witting_POVM_information_bits_per_detected_photon"]-.011617757280846361)<1e-10
    assert baseline["Fano_necessary_detected_photons_for_5pct_error"]==694
    assert baseline["Fano_necessary_incident_photons_for_5pct_error_eta085"]==816
    assert any(z["epsilon"]==.2 and z["all_440_PSD"] for z in records)
    # The source codebook epsilon=.1 is weak. Doubling it quadruples
    # information to leading order; the entropy yields the sharper
    # ensemble-specific cap (beyond 2-bit dimension cap).
    strong=next(z for z in records if z["epsilon"]==.2)
    assert strong["fixed_Witting_POVM_information_bits_per_detected_photon"]>baseline["fixed_Witting_POVM_information_bits_per_detected_photon"]*3.9
    result=dict(status="PASS_440_WITTING_STATE_HOLEVO_VS_ACTUAL_MEASUREMENT_INFORMATION",
       uniform_prior_root_labels=440,
       exact_uniform_average_density="I4/4 (antipodal 440-root symmetry)",
       coarse_Hilbert_dimension_Holevo_ceiling_bits=2,
       experiment_assumptions="IID known mixed ququart preparations, uniform prior, specified fixed Witting40 POVM, optional independent heralded no-click with eta=.85.",
       epsilon_scan=records,
       baseline_epsilon_point_one_Holevo_upper_bound_bits=baseline["holevo_bound_bits_per_ququart"],
       baseline_epsilon_point_one_Witting_information_bits=baseline["fixed_Witting_POVM_information_bits_per_detected_photon"],
       baseline_Witting_information_fraction_of_Holevo=baseline["Witting_fraction_of_Holevo_upper_bound"],
       epsilon_point_two_Holevo_upper_bound_bits=strong["holevo_bound_bits_per_ququart"],
       epsilon_point_two_Witting_information_bits=strong["fixed_Witting_POVM_information_bits_per_detected_photon"],
       epsilon_point_two_Fano_necessary_detected_photons=strong["Fano_necessary_detected_photons_for_5pct_error"],
       one_copy_Holevo_not_optimal_measurement="chi is an UPPER bound; the optimal POVM may attain less. E8 root codebook is a preparable family of nonorthogonal states, not 440 orthogonal quantum messages.",
       sample_count_warning="Fano gives NECESSARY, never sufficient, repetition budget; N repeated preparations of one unknown label and iid Witting measurements. The information per incident photon with independent no-click erasure eta is eta times the detected-photon value.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"Holevo",baseline["holevo_bound_bits_per_ququart"],"fraction",baseline["Witting_fraction_of_Holevo_upper_bound"],"eps02",strong["fixed_Witting_POVM_information_bits_per_detected_photon"],"needed",strong["Fano_necessary_detected_photons_for_5pct_error"],flush=True)
    return result
if __name__=="__main__":main()
