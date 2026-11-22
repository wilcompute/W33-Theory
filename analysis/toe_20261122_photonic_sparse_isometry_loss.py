#!/usr/bin/env python3
"""Constructive adjacent-two-mode Witting Naimark networks; rail-local loss & order control.

Unlike full MxM completion meshes, synthesizes only Mx4 isometry with QR
Givens; losses are inserted on affected two output rails of each gate.
"""
from pathlib import Path
import json
import numpy as np
import toe_20261122_povm30_nai_mark_shot_cost as P
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_photonic_sparse_isometry_loss.json'

def qr_network(V,tol=1e-12):
    nrows,ncols=V.shape;A=V.copy();gates=[]
    for j in range(ncols):
        for k in range(nrows-1,j,-1):
            a,b=A[k-1,j],A[k,j]
            r=np.hypot(abs(a),abs(b))
            if r<tol:continue
            G=np.array([[np.conj(a)/r,np.conj(b)/r],[-b/r,a/r]],complex)
            A[[k-1,k],:]=G@A[[k-1,k],:]
            assert abs(A[k,j])<3e-12
            gates.append((k-1,k,G))
    top=A[:ncols,:]
    assert np.max(abs(top-np.diag(np.diag(top))))<2e-10
    assert np.max(abs(A[ncols:,:]))<2e-10
    assert np.max(abs(np.abs(np.diag(top))-1))<2e-10
    return gates,np.diag(top)

def reconstruct(m,n,gates,phase,eta):
    output=np.zeros((m,n),complex);output[np.arange(n),np.arange(n)]=phase
    for i,j,G in reversed(gates):
        output[[i,j],:]=G.conj().T@output[[i,j],:]
        output[[i,j],:]*=np.sqrt(eta)
    return output

def stats(V,eta,seed):
    gates,phase=qr_network(V)
    m,n=V.shape;assert len(gates)<=4*m-10
    U=reconstruct(m,n,gates,phase,eta=1.)
    resid=float(np.max(abs(U-V)))
    assert resid<2e-10,resid
    out=reconstruct(m,n,gates,phase,eta)
    eff=out.conj().T@out
    vals=np.linalg.eigvalsh(eff)
    assert max(vals)<=1+1e-10
    return dict(output_modes=m,gate_count=len(gates),naive_rectangular_Givens_limit=4*m-10,
      total_adjacent_gate_depth=len(gates),reconstruction_error=resid,
      per_hit_two_rail_intensity_transmission=eta,
      maximally_mixed_input_detection_probability=float(np.trace(eff).real/n),
      input_dependent_detection_eigenvalues=vals.tolist(),
      loss_no_click_effect_min_eigenvalue=float(1-max(vals)),
      loss_no_click_effect_max_eigenvalue=float(1-min(vals)),
      theoretical_all_gates_loss_floor=eta**len(gates))

def verify():
    rays,specs=P.frames();eta=.995
    rows=[]
    for i,(name,choice,weights) in enumerate(specs):
        V=np.array([np.sqrt(w)*rays[j].conj() for j,w in zip(choice,weights)])
        base=stats(V,eta,seed=20261122)
        rng=np.random.default_rng(20261122)
        candidate=[(base['gate_count'],base['maximally_mixed_input_detection_probability'],0)]
        for attempt in range(20):
            perm=rng.permutation(len(choice));s=stats(V[perm],eta,seed=attempt)
            candidate.append((s['gate_count'],s['maximally_mixed_input_detection_probability'],attempt+1))
        best=min(candidate,key=lambda x:(x[0],-x[1]))
        rows.append(dict(name=name,base=base,best_of_21_row_orders=dict(gates=best[0],detection_probability=best[1],seed_attempt=best[2]),
           gate_count_range=[min(x[0] for x in candidate),max(x[0] for x in candidate)],
           survival_range=[min(x[1] for x in candidate),max(x[1] for x in candidate)]))
    return dict(status='PASS_WITTING_30_39_ADJACENT_GIVENS_EXPLICIT_LOSS_MODEL',
       rows=rows,rank_one_measurement_architecture='Four input modes embedded into 30 or 39 output modes via row-local, QR-adjacent Givens couplers; each unitary reconstructed to <2e-10 max norm.',
       photon_survival_model='Every two-mode mixing multiplies amplitude on only its two affected modes by sqrt(0.995). No coupling, propagation, source/detector, phase drift, reflections or rail-dependent detector inefficiency included.',
       interpretation='Component count and survival are architecture/ordering dependent. No fabricated or measured device. The 30-effect vs 39-effect comparison must use both survival and detected-shot risk; count alone is not a performance guarantee.')

if __name__=='__main__':
    d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status']);print([(x['name'],x['base']['gate_count'],x['base']['maximally_mixed_input_detection_probability'],x['best_of_21_row_orders']) for x in d['rows']])
