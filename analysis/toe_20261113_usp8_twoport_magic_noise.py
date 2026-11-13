#!/usr/bin/env python3
"""One-photon 27-path compact-E6 replacement clock: exact qutrit
stabilizer-magic witness and reproducible noisy 6-twoport gate benchmark.

This is not deterministic inter-photon entangling or a threshold theorem.
"""
from pathlib import Path
from itertools import combinations
import sys,json,math
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261113_usp8_twoport_magic_optical_noise.json"

def packet_data():
    cert,terms,D,mapi,roots=R.load()
    packets,Ks=R.pack_roots(roots)
    null={(i,j) for i,j in combinations(range(27),2) if D[i,j]}
    chosen=next(z for z,p in enumerate(packets)
                if sum((i,j) not in null for i,j,s in p)==3)
    packet=packets[chosen];K=Ks[chosen]
    return chosen,packet,K

def exact_magic():
    # A qutrit state a|0>+b|1> is a product of the two-dimensional
    # support target after a Clifford linear relabeling of 3-qutrit
    # computational basis labels. Such support 2 is not possible for
    # an odd-prime stabilizer state (supports are p^k).
    a=-sp.Rational(1,2);b=sp.sqrt(3)/2
    psi={0:a,1:b,2:sp.Integer(0)}
    omega=sp.exp(2*sp.pi*sp.I/3)
    entries={}
    for q in range(3):
        for p in range(3):
            z=sp.simplify(sum(
                omega**(p*t)*psi[(q+2*t)%3]*sp.conjugate(psi[(q-2*t)%3])
                for t in range(3))/3)
            z=sp.simplify(sp.expand_complex(z))
            assert not z.has(sp.I)
            entries[f"{q},{p}"]=z
    total=sp.simplify(sum(abs(z) for z in entries.values()))
    neg=sp.simplify((total-1)/2)
    assert sp.simplify(neg-sp.sqrt(3)/6)==0
    assert sp.simplify(total-(1+sp.sqrt(3)/3))==0
    assert sp.simplify(sum(entries.values())-1)==0
    return {"active_basis_input_computational_support":2,
            "stabilizer_basis_support_cardinality_is_power_of_three":True,
            "active_basis_outputs_are_nonstabilizer_magic":True,
            "discrete_qutrit_Wigner_entries":{k:str(v) for k,v in entries.items()},
            "Wigner_one_norm":str(total),
            "Wigner_sum_negativity":str(neg),
            "Wigner_mana_natural_log":float(sp.log(total)),
            "note":"Any nonzero two-basis difference in F3^3 can be carried to a single-qutrit coordinate by invertible GL3(F3) Clifford permutation, so Wigner L1 is the same for any active pair. Inactive basis outputs are stabilizer basis states."}

def hardware_noise(packet,K,samples=700):
    I=np.eye(27,dtype=np.float64)
    V=I+math.sqrt(3)/2*K+1.5*(K@K)
    assert np.max(abs(V.T@V-I))<1e-13
    assert np.max(abs(V@V@V-I))<1e-13
    theta=2*math.pi/3
    eta=.95
    rng=np.random.default_rng(20261113)
    original_psi=np.ones(27,dtype=np.complex128)/math.sqrt(27)
    angular_sigma=.01
    phase_sigma=.02
    f_ent=[]
    f_uniform=[]
    surv=[]
    used={x for i,j,s in packet for x in (i,j)}
    assert len(used)==12
    for _ in range(samples):
        noisy=I.copy()
        for i,j,sgn in packet:
            angle=theta+rng.normal(0,angular_sigma)
            c=math.cos(angle);v=sgn*math.sin(angle)
            noisy[i,i]=c;noisy[j,j]=c
            noisy[i,j]=v;noisy[j,i]=-v
        phases=rng.normal(0,phase_sigma,27)
        phases[np.array(sorted(set(range(27))-used),dtype=int)]=0
        loss=np.ones(27,dtype=np.float64)
        loss[list(used)]=math.sqrt(eta)
        A=np.diag(loss*np.exp(1j*phases))@noisy
        survival=float(np.real(np.trace(A.conj().T@A))/27)
        overlap=np.trace(V.T@A)
        fE=float(abs(overlap)**2/(27*np.real(np.trace(A.conj().T@A))))
        target=V@original_psi
        obs=A@original_psi
        fU=float(abs(np.vdot(target,obs))**2/np.vdot(obs,obs).real)
        assert 0<=fE<=1+1e-12 and 0<=fU<=1+1e-12
        f_ent.append(fE);f_uniform.append(fU);surv.append(survival)
    x=(15+12*eta)/27
    y=(15+12*math.sqrt(eta))**2/(27*(15+12*eta))
    assert np.max(np.abs(np.array(surv)-x))<1e-12
    assert y>min(f_ent)-.01
    return {"hardware_model":"6 simultaneous two-port rotation gates with independent Gaussian angular jitter sigma_theta, 12 active output phases sigma_phi, active output arm power transmission eta, 15 idle ideal; no crosstalk, source/detector errors or interdevice loss",
            "mode_count":27,
            "beam_splitter_twoport_count":6,
            "active_paths":12,"idle_paths":15,
            "active_power_transmission":eta,
            "angular_sigma_rad":angular_sigma,"phase_sigma_rad":phase_sigma,
            "mc_samples":samples,
            "mean_photon_survival":float(np.mean(surv)),
            "ideal_angle_and_phase_conditional_process_fidelity":y,
            "noisy_conditional_entanglement_fidelity_mean":float(np.mean(f_ent)),
            "noisy_conditional_entanglement_fidelity_q05_q50_q95":list(map(float,np.quantile(f_ent,[.05,.50,.95]))),
            "noisy_conditional_uniform_input_fidelity_mean":float(np.mean(f_uniform)),
            "worst_sample_fidelity":float(min(f_ent)),
            "conditioned_process_formula":"|Tr(V† A)|²/[27 Tr(A† A)]",
            "performance_limit":"Illustrative numerical error model only, no laboratory calibration or fault-tolerance threshold. This elementary V is E6-preserving but NOT Clifford-conjugate to original CCZ U because order-three spectra differ."}

def main():
    index,packet,K=packet_data()
    magic=exact_magic()
    optics=hardware_noise(packet,K)
    out={"status":"PASS_6_TWO_PORT_REPLACEMENT_MAGIC_AND_NOISE","chosen_packet":index,
         "magic":magic,"optics":optics}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":out["status"],"mana":magic["Wigner_mana_natural_log"],
       "loss_survival":optics["mean_photon_survival"],
       "ideal_conditional_F":optics["ideal_angle_and_phase_conditional_process_fidelity"],
       "MC_conditional_F":optics["noisy_conditional_entanglement_fidelity_mean"],
       "MC_worst":optics["worst_sample_fidelity"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
