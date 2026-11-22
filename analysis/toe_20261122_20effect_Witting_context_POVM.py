#!/usr/bin/env python3
"""Five disjoint Witting orthonormal bases give a 20-effect informationally complete POVM.

Does not retain all 27 universal gate sites. Unlike a d=4 SIC, non-equiangular.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import svdvals
import toe_20261122_witting_qutrit_sic_mub30 as G
import toe_20261122_witting_minimal_lie_control as L
import toe_20261122_povm30_nai_mark_shot_cost as P
import toe_20261122_photonic_sparse_isometry_loss as O
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_20effect_Witting_context_POVM.json'
BASES=[(1,13,21,29),(3,7,27,35),(4,37,38,39),(8,23,25,26),(9,24,31,34)]

def verify():
    rays,specs=P.frames();ids=[i for b in BASES for i in b]
    assert len(ids)==20 and len(set(ids))==20
    Pmat=[np.outer(r,r.conj()) for r in rays]
    for b in BASES:
        assert np.max(abs(sum((Pmat[j] for j in b),np.zeros((4,4),complex))-np.eye(4)))<1e-13
        assert max(abs(np.vdot(rays[i],rays[j])) for i in b for j in b if i!=j)<1e-13
    V=np.array([np.sqrt(1/5)*rays[i].conj() for i in ids]);
    assert np.max(abs(V.conj().T@V-np.eye(4)))<1e-13
    mats=np.array([(Pmat[j]/5).reshape(16) for j in ids]);rank=np.linalg.matrix_rank(mats,tol=1e-10)
    assert rank==16
    eig=np.linalg.eigvalsh(mats.conj().T@mats);condition=float(eig[-1]/eig[0]);
    assert 50<condition<100
    ranks=[]
    for prime in L.PRIMES:
        roots=[]
        for a,ac in L.all_witting_rays(prime):
            norm=sum(int(x)*int(y) for x,y in zip(a,ac))%prime
            roots.append((np.array(L.outer(a,ac,prime),dtype=np.int64)*pow(norm,-1,prime)%prime).ravel().tolist())
        ranks.append((prime,L.modular_rank([roots[k] for k in ids],prime)))
    assert all(x[1]==16 for x in ranks)
    optical=O.stats(V,eta=.995,seed=20)
    # Fixed reference test state for unbiased linear inversion risk.
    r=np.random.default_rng(4281);v=r.normal(size=4)+1j*r.normal(size=4);v/=np.linalg.norm(v)
    rho=np.outer(v,v.conj())
    _,_,E,dual,_=P.solve_frame(rays,ids,[.2]*20)
    risk=P.risk(E,dual,rho)
    assert optical['gate_count']<=70
    return dict(status='PASS_EXPLICIT_20_EFFECT_WITTING_CONTEXT_IC_POVM',
      five_disjoint_orthonormal_contexts=[list(b) for b in BASES],
      effects='E_j=P_j/5, j in five disjoint Witting orthonormal tetrads',
      number_of_outcomes=20,
      six_finite_field_IC_ranks=ranks,
      frame_condition_number=condition,
      seeded_pure_state_HS_risk_coefficient=risk,
      optical_constructive_Givens=optical,
      optimality_scope='For a construction using exactly five orthonormal bases, 20 effects are required if the projector span is 16: each basis adds at most 3 traceless directions and overlap of bases reduces rank. This is NOT the globally minimal Witting-supported IC POVM; general d4 needs >=16 effects.',
      tradeoffs='Cuts output ports from 30 to 20, at cost of larger frame condition and losing universal control on all 27 positive effects. Not a d4 SIC, and no optical experiment performed.')
if __name__=='__main__':
    d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],d['frame_condition_number'],d['optical_constructive_Givens']['gate_count'],d['optical_constructive_Givens']['maximally_mixed_input_detection_probability'],d['seeded_pure_state_HS_risk_coefficient'])
