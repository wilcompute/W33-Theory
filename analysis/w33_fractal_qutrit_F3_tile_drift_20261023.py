#!/usr/bin/env python3
"""Embodied 3-mixer F3 qutrit tile: mathematical layout and drift sensitivity.
Fourth optical mode auxiliary and deliberately held idle in the ideal gate.
Not a fabricated PIC or measured qutrit quantum process.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_all5_engineering_20261023 import qutrit_bridge

def reconstruct(eps=None):
    b=qutrit_bridge()
    gates=b['givens']
    phases=np.asarray(b['terminal_phase_rad'],float)
    if eps is None:eps=np.zeros(len(gates)+5)
    e=np.asarray(eps,float)
    assert e.shape==(len(gates)+5,)
    U=np.diag(np.exp(1j*(phases+e[:4])))
    for k,gate in reversed(list(enumerate(gates))):
        G=np.array(gate['G_real'])+1j*np.array(gate['G_imag'])
        delta=e[4+k]
        D=np.diag([np.exp(1j*delta/2),np.exp(-1j*delta/2)])
        indices=gate['modes']
        R=np.eye(4,dtype=complex)
        R[np.ix_(indices,indices)]=D@G
        U=R.conj().T@U
    # Even weak unintentional coupling to the auxiliary port harms the gate.
    delta=e[-1]
    S=np.eye(4,dtype=complex)
    S[2,2]=S[3,3]=math.cos(delta)
    S[2,3]=S[3,2]=1j*math.sin(delta)
    return S@U

def noise_sweep(seed=11,samples=180):
    b=qutrit_bridge()
    F=np.array(b['qutrit_F3_real'])+1j*np.array(b['qutrit_F3_imag'])
    assert np.linalg.norm(reconstruct()[:3,:3]-F)<1e-12
    rng=np.random.default_rng(seed);rows=[]
    for sigma in (0.,.01,.05,.1):
        fidelity=[];leakage=[]
        for i in range(samples):
            e=rng.normal(0,sigma,8)
            e[-1]*=.333
            U=reconstruct(e)
            sub=U[:3,:3]
            fid=abs(np.trace(F.conj().T@sub))**2/9
            survival=np.sum(np.abs(sub)**2,axis=0)
            fidelity.append(float(fid))
            leakage.append(float(max(0,1-min(survival))))
        rows.append({'phase_error_sigma_rad':sigma,
                     'mean_unconditional_process_overlap':float(np.mean(fidelity)),
                     'p05_unconditional_process_overlap':float(np.quantile(fidelity,.05)),
                     'mean_worst_basis_leakage':float(np.mean(leakage))})
    return {'schema':'w33.fractal.qutrit_F3_tile_drift.v1',
            'active_two_mode_gates':len(b['givens']),
            'device_port_pairs':[x['modes'] for x in b['givens']],
            'phase_bank':4,'auxiliary_input_mode':3,'auxiliary_output_mode':3,
            'ideal_reconstruction_error':float(np.linalg.norm(reconstruct()[:3,:3]-F)),
            'noise_sweep':rows,
            'physical_gate_status':'UNFABRICATED; stochastic coupling/phase errors hypothetical',
            'scope':'no GDS routing, coupler S-parameters or experimental fidelity'}
if __name__=='__main__':
    o=noise_sweep()
    p=ROOT/'data/w33_fractal_qutrit_F3_tile_drift_20261023.json'
    p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
    print('PASS F3',o['ideal_reconstruction_error'],o['noise_sweep'])
