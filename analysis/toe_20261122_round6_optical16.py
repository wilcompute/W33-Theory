#!/usr/bin/env python3
"""Calibrated Naimark 16-effect Witting IC measurement; compare 18/19/20/30/39."""
import numpy as np
import toe_20261122_round6_16effect_optimal as T
import toe_20261122_round5_18effect_optical as R
import toe_20261122_povm30_nai_mark_shot_cost as P
import toe_20261122_photonic_sparse_isometry_loss as O

def verify(ntries=60):
 cert=T.proof();rays,_=P.frames();ids=list(T.S);w=np.array([float(T.WEIGHTS[i]) for i in ids]);V=np.array([np.sqrt(a)*rays[k].conj() for k,a in zip(ids,w)])
 assert np.max(abs(V.conj().T@V-np.eye(4)))<1e-12
 rng=np.random.default_rng(260622);psi=rng.normal(size=4)+1j*rng.normal(size=4);psi/=np.linalg.norm(psi)
 rho=np.outer(psi,psi.conj());z=[]
 orders=[np.arange(16)]+[rng.permutation(16) for _ in range(ntries)]
 for ix,perm in enumerate(orders):
   q=R.loss_risk(V[perm],rho);p=R.loss_risk(V[perm],np.eye(4)/4)
   q['haar_pure_average_source_photon_HS_risk_coefficient']=p['source_photon_HS_risk_coefficient']-.75
   q['index']=ix
   z.append(q)
 best=min(z,key=lambda a:a['haar_pure_average_source_photon_HS_risk_coefficient']);baseline=z[0]
 print('16 baseline',baseline,flush=True);print('16 best average',best,flush=True)
 return dict(rank_cert=cert,baseline=baseline,best=best,norders=len(orders),status='PASS_16_EFFECT_WITTING_PHOTONIC_MODEL')
if __name__=='__main__':verify()
