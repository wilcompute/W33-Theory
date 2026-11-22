#!/usr/bin/env python3
"""Naimark completions and exact multinomial linear-tomography risk: Witting
30- versus 39-effect one-photon POVMs, with a simple SPAM bias floor.

All resource counts are architecture-dependent upper-bound style counts,
not measured optical energy or implemented hardware.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_witting_qutrit_sic_mub30 as GEO
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_povm30_nai_mark_shot_cost.json'


def frames():
    d=GEO.verify()
    roots=W.all_rays()
    cv=lambda q:complex(float(q[0])-float(q[1])/2,float(q[1])*np.sqrt(3)/2)
    R=np.array([[cv(x) for x in v] for v in roots]);R/=np.linalg.norm(R,axis=1)[:,None]
    O27=d['universal_ray_orbit'];O12=sorted(set(range(40))-set(O27)-{25})
    specs=[('39-effect',O27+O12,[1/9]*27+[1/12]*12)]
    specs += [('30-effect-'+str(k),O27+b,[1/9]*27+[1/3]*3)
              for k,b in enumerate(d['blocked_qutrit_MUB_basis_partition'])]
    return R,specs


def solve_frame(R,choice,weights):
    m=len(choice)
    V=np.array([np.sqrt(w)*R[j].conj() for j,w in zip(choice,weights)])
    assert np.max(abs(V.conj().T@V-np.eye(4)))<1e-12
    Q=null_space(V.conj().T)
    U=np.column_stack((V,Q))
    assert U.shape==(m,m)
    assert np.max(abs(U.conj().T@U-np.eye(m)))<1e-11
    # The first four columns define a 4-to-m isometry implementing all
    # POVM outcome amplitudes in one photon path multiplexing stage.
    E=np.column_stack([w*np.outer(R[j],R[j].conj()).reshape(16)
                       for j,w in zip(choice,weights)])
    F=E@E.conj().T
    vals=np.linalg.eigvalsh(F)
    assert vals[0]>1e-12
    dual=np.linalg.solve(F,E)
    assert np.max(abs(dual@E.conj().T-np.eye(16)))<1e-11
    return V,U,E,dual,vals


def risk(E,dual,rho):
    state=rho.reshape(16)
    p=(E.conj().T@state).real
    assert abs(np.sum(p)-1)<1e-12 and min(p)>-1e-12
    assert np.linalg.norm(dual@p-state)<1e-11
    # For N iid multinomial detections, rho_hat=sum(count_k/N)D_k;
    # exactly E ||rho_hat-rho||_HS^2 = [sum p_k ||D_k||² - Tr(rho²)]/N.
    norms=np.sum(abs(dual)**2,axis=0).real
    var=float(np.dot(p,norms)-np.trace(rho@rho).real)
    assert var>0
    return var


def verify():
    R,specs=frames();rng=np.random.default_rng(4281)
    psi=rng.normal(size=4)+1j*rng.normal(size=4);psi/=np.linalg.norm(psi)
    states={'maximally_mixed':np.eye(4)/4,
       'fixed_ray25':np.outer(R[25],R[25].conj()),
       'universal_ray36':np.outer(R[36],R[36].conj()),
       'blocked_ray1':np.outer(R[1],R[1].conj()),
       'seeded_generic_pure':np.outer(psi,psi.conj())}
    rows=[]
    for name,choice,weights in specs:
        V,U,E,dual,vals=solve_frame(R,choice,weights)
        samples={k:risk(E,dual,rho) for k,rho in states.items()}
        rows.append(dict(name=name,outcome_count=len(choice),
           direct_dilation_unitary_dimension=len(choice),
           generic_full_mesh_two_mode_cells=len(choice)*(len(choice)-1)//2,
           complex_rectangular_Stiefel_real_dimension=2*4*len(choice)-4*4,
           Naimark_isometry_deviation=float(np.max(abs(V.conj().T@V-np.eye(4)))),
           reconstruction_frame_min_eigenvalue=float(vals[0]),
           reconstruction_frame_condition_number=float(vals[-1]/vals[0]),
           expected_linear_inversion_HS_MSE_times_detected_shot_count=samples))
    assert rows[0]['generic_full_mesh_two_mode_cells']==741
    assert all(r['generic_full_mesh_two_mode_cells']==435 for r in rows[1:])
    assert rows[0]['outcome_count']==39
    assert all(r['outcome_count']==30 for r in rows[1:])
    # Simple phase-blind / depolarizing POVM calibration error model:
    # actual state rho'= (1-delta)rho + delta I4/4 but inverse ignores delta.
    # Even at infinite N, trace distance for input pure rho is 3delta/4.
    delta=0.01
    pure=states['seeded_generic_pure'];observed=(1-delta)*pure+delta*np.eye(4)/4
    trdist=np.linalg.svd(pure-observed,compute_uv=False).sum()/2
    assert abs(trdist-0.75*delta)<1e-12
    return dict(status='PASS_WITTING_30_EFFECT_NAIMARK_COMPLETION_AND_ANALYTIC_SHOT_RISK',
       four_mode_input_dimension=4,
       design_comparison=rows,
       full_mesh_cell_reduction_if_generic_30_vs39=(741-435)/741,
       algebraic_linear_inversion_risk_formula='E(||rhohat-rho||_HS^2) = (sum_k p_k ||F^-1(E_k)||_HS^2 - Tr(rho^2))/N, for N detected iid multinomial outcomes',
       calibration_model='Unknown uniform source/measurement depolarization delta=0.01: rho_observed=(1-delta)rho+delta I4/4',
       hypothetical_infinite_shot_pure_state_trace_distance_bias=trdist,
       physical_boundary='Specific isometries and unitary completions exist numerically. Full generic 30x30/39x39 meshes are not optimized, built or calibrated. Naimark 30 outputs does not imply 30 independent detectors with time multiplexing. Analytic variances ignore systematic SPAM and detector drift.')


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],[(x['outcome_count'],x['generic_full_mesh_two_mode_cells'],round(x['expected_linear_inversion_HS_MSE_times_detected_shot_count']['seeded_generic_pure'],3)) for x in d['design_comparison']])
if __name__=='__main__':main()
