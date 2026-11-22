#!/usr/bin/env python3
"""An explicit 18-effect informationally complete Witting POVM and lossy QR circuit.

Two independent 12-ray tight frames with six-ray overlap; each sums P/3 = I.
Mixture yields 18 effects, weights 1/3 or 1/6. This is a constructive
upper bound, NOT a proof of optimality among Witting-supported POVMs.
Loss-calibrated tomography includes a no-click effect for launched photons.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json
import numpy as np
import toe_20261122_witting_qutrit_sic_mub30 as GEO
import toe_20261122_witting_minimal_lie_control as L
import toe_20261122_povm30_nai_mark_shot_cost as P
import toe_20261122_photonic_sparse_isometry_loss as O
import toe_20261122_20effect_Witting_context_POVM as T20
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261122_round5_18effect_optical.json'
A=(1,3,5,7,12,13,18,19,27,29,33,39)
B=(5,6,7,8,10,15,16,18,27,29,33,36)
C=(1,5,6,13,15,16,17,29,30,31,32,33)
D=(1,3,5,7,12,13,18,19,27,29,33,39)

def rank_certificates(ids,ids19):
    rows=[]
    for prime in L.PRIMES:
        mats=[]
        for v,vc in L.all_witting_rays(prime):
            norm=sum(int(a)*int(b) for a,b in zip(v,vc))%prime
            mats.append((np.array(L.outer(v,vc,prime),dtype=np.int64)*pow(norm,-1,prime)%prime).ravel().tolist())
        ranks={name:L.modular_rank([mats[k] for k in seq],prime) for name,seq in [('A',A),('B',B),('union18',ids),('C',C),('D',D),('union19',ids19)]}
        assert ranks=={'A':12,'B':12,'union18':16,'C':12,'D':12,'union19':16},(prime,ranks)
        rows.append({'prime':prime,**ranks})
    return rows

def exact_identities():
    rays=GEO.W.all_rays();M=[GEO.P_of(v) for v in rays]
    I=tuple(tuple(GEO.ONE if i==j else GEO.ZERO for j in range(4)) for i in range(4))
    for subset in (A,B,C,D):
        assert GEO.mat_scaled(GEO.qmatrix_sum(M,subset),GEO.F(1,3))==I
    return True

def loss_risk(V,rho,eta=.995):
    gates,phase=O.qr_network(V)
    Aphys=O.reconstruct(V.shape[0],4,gates,phase,eta)
    E=[np.outer(row.conj(),row) for row in Aphys]
    Enoclick=np.eye(4)-Aphys.conj().T@Aphys
    assert np.linalg.eigvalsh(Enoclick).min()>-1e-11
    E.append(Enoclick)
    assert np.max(abs(sum(E)-np.eye(4)))<5e-11
    mat=np.stack([m.reshape(16) for m in E],axis=1)
    frame=mat@mat.conj().T
    assert np.linalg.eigvalsh(frame).min()>1e-11
    dual=np.linalg.solve(frame,mat)
    p=(mat.conj().T@rho.reshape(16)).real
    assert np.min(p)>-1e-10 and abs(np.sum(p)-1)<1e-9
    var=float(np.dot(p,np.sum(abs(dual)**2,axis=0))-np.trace(rho@rho).real)
    assert var>0
    return dict(source_photon_HS_risk_coefficient=var,detected_probability=float(1-p[-1]),
                no_click_probability=float(p[-1]),gate_count=len(gates),
                lossy_frame_condition=float(np.linalg.cond(frame)))

def verify():
    assert len(A)==len(B)==12 and len(set(A)&set(B))==6
    exact_identities()
    ids=sorted(set(A)|set(B));assert len(ids)==18
    weights=np.array([(int(i in A)+int(i in B))/6 for i in ids],float)
    assert Counter((int(i in A)+int(i in B)) for i in ids)=={1:12,2:6}
    ids19=sorted(set(C)|set(D));assert len(ids19)==19 and len(set(C)&set(D))==5
    modular=rank_certificates(ids,ids19)
    rays,specs=P.frames()
    rng=np.random.default_rng(4281);psi=rng.normal(size=4)+1j*rng.normal(size=4);psi/=np.linalg.norm(psi)
    rho=np.outer(psi,psi.conj())
    w19=np.array([(int(i in C)+int(i in D))/6 for i in ids19],float)
    cases=[('18-effect',ids,weights),('19-effect',ids19,w19)]
    cases += [('20-effect',list(sum([list(x) for x in T20.BASES],[])),[.2]*20),specs[1],specs[0]]
    output=[]
    for name,selection,coeffs in cases:
        V=np.array([np.sqrt(w)*rays[i].conj() for i,w in zip(selection,coeffs)])
        assert np.max(abs(V.conj().T@V-np.eye(4)))<5e-12
        E=np.column_stack([w*np.outer(rays[i],rays[i].conj()).reshape(16) for i,w in zip(selection,coeffs)])
        dual=np.linalg.solve(E@E.conj().T,E)
        detected_risk=P.risk(E,dual,rho)
        loss=loss_risk(V,rho)
        # Exact Haar-pure expected linear-inversion variance: E[rho]=I/4,
        # E[Tr(rho^2)]=1. Mixed-state benchmark subtracts 3/4.
        haar_pure=loss_risk(V,np.eye(4)/4)['source_photon_HS_risk_coefficient']-.75
        condition=float(np.linalg.cond(E@E.conj().T))
        output.append(dict(design=name,outcomes=len(selection),
                           ideal_frame_condition=condition,
                           ideal_detected_photon_HS_risk_coefficient=detected_risk,
                           exact_Haar_pure_average_source_photon_HS_risk_coefficient=haar_pure,
                           **loss))
    assert [x['outcomes'] for x in output]==[18,19,20,30,39]
    best=output[0];assert best['gate_count']<=4*18-10
    # The mixture of the two tight frames can be reweighted continuously.
    # t=1/2 is the exact equal-weight construction; other t need not share
    # the same optimal tomography risk.
    rs=[]
    for t in np.linspace(.2,.8,13):
        ww=np.array([(t/3 if i in A else 0)+((1-t)/3 if i in B else 0) for i in ids])
        V=np.array([np.sqrt(w)*rays[i].conj() for i,w in zip(ids,ww)])
        E=np.column_stack([w*np.outer(rays[i],rays[i].conj()).reshape(16) for i,w in zip(ids,ww)])
        dual=np.linalg.solve(E@E.conj().T,E)
        rs.append(dict(t=round(float(t),4),ideal_risk=float(P.risk(E,dual,rho)),
                       loss_calibrated=loss_risk(V,rho)))
    choice=min(rs,key=lambda x:x['loss_calibrated']['source_photon_HS_risk_coefficient'])
    return dict(status='PASS_EXACT_18_EFFECT_WITTING_IC_AND_LOSS_AWARE_OPTICAL_BENCHMARK',
       exact_cyclotomic_identities=True,source_tight_frame_A=list(A),source_tight_frame_B=list(B),
       nineteen_source_frames=[list(C),list(D)],nineteen_ray_indices=ids19,
       overlap_six_rays=sorted(set(A)&set(B)),final_ray_indices=ids,
       final_weight_by_ray={str(i):round(float(w),12) for i,w in zip(ids,weights)},
       six_finite_field_projector_ranks=modular,
       optical_designs=output,mixture_weight_scan=rs,
       best_tested_mixture=choice,
       limitations='18 and 19 are explicit support upper bounds, not proven minima. Statistical risk is for one seeded pure state and calibrated finite-dimensional source/detector model; QR coupler losses are illustrative and exclude multiphoton imperfections, drift, source/detector efficiencies. Count is not evidence of hardware energy advantage.')
if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
 print(d['status'])
 for z in d['optical_designs']:print(z['design'],z['gate_count'],z['source_photon_HS_risk_coefficient'],z['detected_probability'])
 print('best_t',d['best_tested_mixture']['t'])
