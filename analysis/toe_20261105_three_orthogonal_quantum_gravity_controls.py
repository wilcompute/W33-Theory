#!/usr/bin/env python3
"""Three physics-first outside-the-box control experiments.

A: A five-Weyl-fermion anomaly-free chiral U1 becomes UV-coupling
   sensitive because its large charges give a large positive beta.
B: Quantum clock redshift entangles a path with internal proper time;
   coordinate exchange ticks need branch-dependent conversion.
C: Exact Gaussian harmonic-chain vacuum entanglement distinguishes
   gapped area-law saturation from near-critical logarithmic scaling.
All three are standard physics controls, not newly discovered effects.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_three_independent_toe_controls.json"

def anomaly_landau():
    charges=(-9,-5,-1,7,8)
    assert sum(charges)==sum(q**3 for q in charges)==0
    assert len(charges)==5
    assert all(-q not in charges for q in charges)
    b=(2/3)*sum(q*q for q in charges)
    assert abs(b-440/3)<1e-12
    mu0=1e3
    results=[]
    for g0 in (.1,.15,.2):
        logpole=8*math.pi**2/(b*g0*g0)
        # Perturbativity convention: alpha_effective_max =
        # (qmax*g)^2/(4pi) < 1.
        qmax=max(map(abs,charges))
        g_limit=math.sqrt(4*math.pi)/qmax
        assert g0<g_limit
        logstrong=(1/g0**2 - 1/g_limit**2)*8*math.pi**2/b
        assert 0<logstrong<logpole
        results.append({"g_at_1TeV":g0,
            "max_abs_charge":qmax,
            "one_loop_beta_b":b,
            "first_max_charge_alpha_equals_one_energy_GeV":mu0*math.exp(logstrong),
            "one_loop_Landau_pole_GeV":mu0*math.exp(logpole),
            "log_pole_over_threshold":logpole,
            "perturbativity_convention":"max_q (q*g)^2/(4*pi) reaches 1"})
    assert results[-1]["one_loop_Landau_pole_GeV"]<1e9
    assert results[0]["one_loop_Landau_pole_GeV"]>1e19
    return {"status":"PASS","chiral_charge_spectrum":list(charges),
      "anomaly_free":True,"chiral_no_opposite_pairs":True,
      "one_loop_beta_positive":True,
      "one_loop_beta_coefficient_b":b,
      "illustrative_couplings":results,
      "scope":"Anomaly-free charge spectrum does not ensure perturbative UV completion. Charges have conventional normalization with fixed g. Higgs and full QFT completion omitted."}
def entropy_binary(p):
    if p<=0 or p>=1:return 0.
    return -p*math.log2(p)-(1-p)*math.log2(1-p)
def gravitational_clock():
    # Weak-field proper time dτ=(1+Phi/c²)dt. A path qubit controls
    # one internal clock phase. Tracing over path suppresses visibility.
    f0=1e15
    delta_phi_over_c2=1e-15
    rows=[]
    for t in (0.,.125,.25,.5,.75,1.):
        dtheta=2*math.pi*f0*t*delta_phi_over_c2
        vis=abs(math.cos(dtheta/2))
        prob=(1+vis)/2
        ebits=entropy_binary(prob)
        if t==.5:
            assert abs(vis)<1e-12 and abs(ebits-1)<1e-12
        if t==1:assert abs(vis-1)<1e-12 and ebits<1e-12
        rows.append({"coordinate_time_s":t,"relative_proper_time_s":t*delta_phi_over_c2,
             "Ramsey_phase_difference_rad":dtheta,"clock_Ramsey_visibility":vis,
             "internal_clock_path_entanglement_ebits":ebits})
    return {"status":"PASS","clock_frequency_Hz":f0,
       "weak_field_potential_difference_over_c_squared":delta_phi_over_c2,
       "path_internal_state":"(|0>path |+>clock + |1>path e^{-i theta sigma_z/2}|+>clock)/sqrt2",
       "relations":"Delta_phase=2pi*f0*t*DeltaPhi/c²; visibility=abs(cos(Delta_phase/2)); entropy=H2((1+visibility)/2)",
       "rows":rows,
       "interpretation":"One global coordinate exchange count is not identical to both local proper times; each branch accumulates different clock phase. Branch-time entanglement is a known quantum-clock effect.",
       "boundary":"Prescribed weak gravitational potentials and fixed metric, no graviton quantization, no derived redshift or fundamental time-flow law."}
def chain_entropy(N,m,lengths):
    frequencies=np.sqrt(m*m+4*np.sin(np.pi*np.arange(N)/N)**2)
    xrow=np.fft.ifft(1/frequencies).real/2
    prow=np.fft.ifft(frequencies).real/2
    samples=[]
    for l in lengths:
        idx=(np.arange(l)[:,None]-np.arange(l)[None,:])%N
        XA=xrow[idx];PA=prow[idx]
        eigen=np.linalg.eigvals(XA@PA).real
        assert min(eigen)>=.25-2e-9
        nu=np.sqrt(np.maximum(eigen,.25))
        z=np.maximum(nu-.5,0)
        entropy=float(np.sum((z+1)*np.log1p(z) -
                z*np.log(np.maximum(z,1e-300))))
        samples.append({"subsystem_length":l,"entropy_nats":entropy,
            "smallest_symplectic_eigenvalue":float(nu.min())})
    return samples
def gauss_area():
    N=128
    sizes=(4,8,16,32,48,64)
    records={}
    for mass in (.001,.01,.2,.5):
        rows=chain_entropy(N,mass,sizes)
        x=np.log((N/np.pi)*np.sin(np.pi*np.array(sizes)/N))
        y=np.array([t["entropy_nats"] for t in rows])
        slope=float(np.polyfit(x,y,1)[0])
        records[str(mass)]={"mass_gap":mass,"subsystem_entropies":rows,
          "finite_chord_log_slope":slope,
          "late_block_entropy_difference":float(y[-1]-y[-3])}
    assert .28<records["0.001"]["finite_chord_log_slope"]<.34
    assert records["0.5"]["finite_chord_log_slope"]<.001
    assert abs(records["0.5"]["late_block_entropy_difference"])<1e-6
    return {"status":"PASS","N_sites":N,"nearest_neighbor_spring_strength":1,
      "periodic_chain":True,"subsystem_sizes":list(sizes),
      "model":"One-dimensional harmonic chain, Gaussian ground state, X/P restricted covariance and symplectic entropy",
      "records":records,
      "interpretation":"A gapped local vacuum entangles mainly across interval boundaries; a nearly critical vacuum has approximate CFT logarithmic growth. Entanglement area laws alone do not yield Einstein equations.",
      "boundary":"1+1D nonrelativistic lattice regulator, not 3+1D horizon entropy, black-hole thermodynamics or emergent gravity. m=.001 has finite zero-mode finite-size effects."}
def main():
    result={"status":"PASS_THREE_ORTHOGONAL_TOE_PHYSICS_CONTROLS",
      "chiral_landau":anomaly_landau(),
      "proper_time_quantum_clock":gravitational_clock(),
      "vacuum_entanglement_area_critical":gauss_area(),
      "prior_art":"Perturbative Abelian Landau poles, weak-field gravitational redshift, quantum-clock controlled phases, Gaussian symplectic eigenvalue entropies and 1+1D CFT scaling are established.",
      "no_toe_claim":True}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("OUTSIDE_PHYSICS_PASS",result["chiral_landau"]["illustrative_couplings"],
       [(key,round(z["finite_chord_log_slope"],6))
        for key,z in result["vacuum_entanglement_area_critical"]["records"].items()],flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return result
if __name__=="__main__":main()
