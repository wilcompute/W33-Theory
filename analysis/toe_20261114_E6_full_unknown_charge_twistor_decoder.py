#!/usr/bin/env python3
"""Complete two-stage unknown-charge + hidden-qubit state reconstruction.

Stage 1: 21 of 27 even Pauli expectations identify any of 180 signed
E6 charge fibers without a supplied charge label.
Stage 2: after inference, three odd Pauli axes from a fixed global
12-axis menu reconstruct any pure state on that quaternionic CP1 fiber.
All formulas are independently checked against 8x8 Pauli matrices.
Includes noisy 21-axis charge-classification controls.
"""
from pathlib import Path
import json,sys
from itertools import product
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261114_exact_gaussian_us8_pauli_clock as E
import toe_20261114_E6_180charge_minimal_even_readout as O
OUT=ROOT/"data/toe_20261114_E6_full_unknown_charge_twistor_decoder.json"

def main():
    c=O.main()
    q=json.loads((ROOT/"data/toe_20261114_hidden_qubit_12_pauli_global_tomography.json").read_text())
    dic=json.loads((ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json").read_text())
    mp={int(i):int(v) for i,v in dic["coordinate_to_pauli_label"].items()}
    flips=set(dic["coordinate_negative_sign_indices"])
    pauli,quad,odd,_=E.pauli_data()
    P=[(-1 if i in flips else 1)*pauli[mp[i]] for i in range(27)]
    _,terms,_,_,_=R.load()
    charges=[]
    for tri,s in terms.items():
        for pat in product((-1,1),repeat=3):
            if pat[0]*pat[1]*pat[2]!=s:continue
            z=[0]*27
            for i,t in zip(tri,pat):z[i]=t
            charges.append(tuple(z))
    assert len(charges)==180
    chosen=c["selected_even_coordinates"]
    lookup={tuple(z[i] for i in chosen):z for z in charges}
    assert len(lookup)==180
    rng=np.random.default_rng(20261114)
    I=np.eye(8,dtype=complex)
    maximum_matrix_residual=0.
    min_fidelity=1.
    count=0
    for z in charges:
        X=sum((z[i]*P[i] for i in range(27)),np.zeros((8,8),complex))
        Pi=(I+X)/4
        assert np.max(abs(Pi@Pi-Pi))<1e-14
        eigenvectors=np.linalg.eigh(Pi)[1][:,-2:]
        logicalsupport=tuple(sorted(mp[i] for i,x in enumerate(z) if x))
        reps=q["orbit_local_three_axes"][",".join(map(str,logicalsupport))]
        assert len(reps)==3 and all(r in q["global_menu_labels"] for r in reps)
        for _ in range(4):
            psi=eigenvectors@(rng.normal(size=2)+1j*rng.normal(size=2))
            psi/=np.linalg.norm(psi)
            rho=np.outer(psi,psi.conj())
            measurement=[float(np.vdot(psi,P[i]@psi).real) for i in chosen]
            recovered=lookup[tuple(int(round(x)) for x in measurement)]
            assert recovered==z
            Pirecovered=(I+sum((recovered[i]*P[i] for i in range(27)),np.zeros((8,8),complex)))/4
            rs=[float(np.trace(rho@pauli[a]).real) for a in reps]
            Ln=[Pirecovered@pauli[a]@Pirecovered for a in reps]
            inferred=(Pirecovered+sum((r*L for r,L in zip(rs,Ln)),np.zeros((8,8),complex)))/2
            err=float(np.max(abs(inferred-rho)))
            maximum_matrix_residual=max(maximum_matrix_residual,err)
            fidelity=float(np.vdot(psi,inferred@psi).real)
            min_fidelity=min(min_fidelity,fidelity)
            assert err<1e-12
            count+=1
    # Simulated finite-shot charge reads under calibrated visibility.
    # Samples are independent copies of one state per charge and axis.
    noisy={}
    for visibility,nshots in ((1.,54),(.8,85)):
        success=0
        trials=0
        for z in charges:
            for _ in range(4):
                trinary=[]
                for i in chosen:
                    mu=visibility*z[i]
                    plus=rng.binomial(nshots,(1+mu)/2)
                    estimate=(2*plus/nshots-1)/visibility
                    trinary.append(-1 if estimate<-.5 else (1 if estimate>.5 else 0))
                trial=tuple(trinary)
                success+=int(trial in lookup and lookup[trial]==z)
                trials+=1
        noisy[str(visibility)]=dict(trials=trials,correct=success,
            empirical_accuracy=success/trials,per_even_axis_shots=nshots,
            total_even_copies_per_trial=nshots*21)
    out=dict(status="PASS_FULL_E6_UNKNOWN_CHARGE_PLUS_LOGICAL_QUBIT_RECONSTRUCTION",
        charge_fibers=180,random_pure_state_reconstructions=count,
        global_even_axis_menu=21,global_odd_axis_menu=12,
        per_state_even_axis_nonadaptive=21,
        per_state_odd_axis_adaptive=3,
        menu_total=33,per_state_nonadaptive_full_settings=24,
        ideal_greedy_per_state_expected_full_settings=c["adaptive_greedy_axis_queries_expected"]+3,
        ideal_greedy_per_state_worst_full_settings=c["adaptive_greedy_axis_queries_worst"]+3,
        pure_state_max_matrix_error=maximum_matrix_residual,
        pure_state_min_fidelity=min_fidelity,
        noisy_charge_classification=noisy,
        scope="This solves only state tomography conditioned on the known 180-charge ensemble. Requires repeated identical state preparations and charge-invariant even Pauli statistics. Finite-shot simulation does not propagate wrong charge hypotheses into odd tomography; no device experiment.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True),flush=True)
    return out

if __name__=="__main__":main()
