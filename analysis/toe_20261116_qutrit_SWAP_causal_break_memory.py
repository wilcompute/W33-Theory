"""3-qutrit causal-break coherent memory SWAP and classical-memory controls.

Registers R, S, E each dimension3. Prepare Bell R:S with E=|0>.
Swap S-E. Reset S to an arbitrarily selected state |2> (erasing its
prior local information). Swap S-E again. Coherent E returns Bell R:S,
whereas dephasing E in the computational basis yields an entanglement
breaking measure-reprepare control saturating 4-MUB separable bound.
Skipping SWAP back leaves R:S uncorrelated.

Compute actual 27x27 density matrices and trace partial systems,
not merely inventing matched probabilities. This is an exact
circuit simulation, NOT a physical photon experiment or memory device.
"""
import json,importlib.util
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_qutrit_SWAP_causal_break_controls.json"
sp=importlib.util.spec_from_file_location("opt",ROOT/"analysis"/"toe_20261116_qutrit_F3_optical_budget.py")
opt=importlib.util.module_from_spec(sp);sp.loader.exec_module(opt)

def initial_density():
    v=np.zeros((3,3,3),complex)
    for n in range(3):v[n,n,0]=1/np.sqrt(3)
    vec=v.reshape(27)
    return np.outer(vec,vec.conj())

def swap_SE(rho):
    return rho.reshape((3,)*6).transpose(0,2,1,3,5,4).reshape(27,27)

def reset_S(rho,t=2):
    a=rho.reshape((3,)*6)
    # Trace out S, then prepare new S state |t>
    red=np.einsum("rseRsf->reRf",a)
    out=np.zeros((3,3,3,3,3,3),complex)
    out[:,t,:,:,t,:]=red
    return out.reshape(27,27)

def dephase_E(rho):
    a=rho.reshape((3,)*6).copy()
    for e in range(3):
        for f in range(3):
            if e!=f:a[:,:,e,:,:,f]=0
    return a.reshape(27,27)

def trace_E(rho):
    return np.einsum("rseRSe->rsRS",rho.reshape((3,)*6)).reshape(9,9)

def fidelity_and_witness(rho):
    phi=np.zeros(9,complex)
    for n in range(3):phi[3*n+n]=1/np.sqrt(3)
    F=float(np.vdot(phi,rho@phi).real)
    _,bases=opt.matrices()
    probabilities=[]
    for U in bases:
        p=0.
        for k in range(3):
            match=np.kron(U[:,k].conj(),U[:,k])
            p+=float(np.vdot(match,rho@match).real)
        probabilities.append(p)
    assert abs(sum(probabilities)-(1+3*F))<1e-12
    eig=np.linalg.eigvalsh(rho)
    assert eig.min()>-1e-12 and abs(np.trace(rho)-1)<1e-12
    return {"Bell_fidelity":F,"four_MUB_matched_probabilities":probabilities,
            "four_MUB_witness_sum":sum(probabilities),
            "mean_random_setting_matched_probability":sum(probabilities)/4,
            "minimum_rho_eigenvalue":float(eig.min())}

def verify():
    start=initial_density()
    after_swap=swap_SE(start)
    after_reset=reset_S(after_swap,t=2)
    coher=trace_E(swap_SE(after_reset))
    classical=trace_E(swap_SE(reset_S(dephase_E(after_swap),t=2)))
    no_return=trace_E(after_reset)
    c=fidelity_and_witness(coher)
    k=fidelity_and_witness(classical)
    n=fidelity_and_witness(no_return)
    assert abs(c["Bell_fidelity"]-1)<1e-12
    assert abs(k["Bell_fidelity"]-1/3)<1e-12
    assert abs(n["Bell_fidelity"]-1/9)<1e-12
    assert abs(c["four_MUB_witness_sum"]-4)<1e-12
    assert abs(k["four_MUB_witness_sum"]-2)<1e-12
    assert abs(n["four_MUB_witness_sum"]-4/3)<1e-12
    for t in (0,1,2):
        q=trace_E(swap_SE(reset_S(after_swap,t=t)))
        assert np.max(abs(q-coher))<1e-12
    return {"status":"PASS_FULL_27x27_CAUSAL_BREAK_QUTRIT_SWAP_BELL_RETENTION",
        "registers":"R(reference),S(system),E(environment) in d3",
        "causal_break":"SWAP S-E, discard and reprepare S in arbitrary |t>, SWAP S-E again",
        "coherent_memory":c,"dephased_classical_memory":k,"without_return_SWAP":n,
        "controls":"Classical E dephasing is entanglement-breaking, reaches the separable bound. Skipping return SWAP gives a product R:S output.",
        "hardware_unperformed":True,
        "eventready_interface":"Combine with four-MUB qutrit optical POVM, calibrated no-click handling and precommitted sequential e-process from prior scripts."}
if __name__=="__main__":
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(d["status"],d["coherent_memory"]["four_MUB_witness_sum"],d["dephased_classical_memory"]["four_MUB_witness_sum"])
