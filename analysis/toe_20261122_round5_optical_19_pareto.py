#!/usr/bin/env python3
"""Joint mixture-weight and output-order search for the explicit 19-outcome Witting POVM.

No global-optimum claims: 1D mixing parameter is optimized for a fixed
ordering and 80 reproducible permutations are tested. Includes a
loss-calibrated no-click effect and process error per launched photon.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import minimize_scalar
import toe_20261122_round5_18effect_optical as F
import toe_20261122_povm30_nai_mark_shot_cost as P
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round5_optical_19_pareto.json'

def verify():
    R,_=P.frames();ids=sorted(set(F.C)|set(F.D))
    rng=np.random.default_rng(4281);psi=rng.normal(size=4)+1j*rng.normal(size=4);psi/=np.linalg.norm(psi)
    rho=np.outer(psi,psi.conj())
    def construct(t):
        w=np.array([(t/3 if i in F.C else 0)+((1-t)/3 if i in F.D else 0) for i in ids])
        return np.array([np.sqrt(v)*R[i].conj() for i,v in zip(ids,w)])
    base=F.loss_risk(construct(.5),rho)
    opt=minimize_scalar(lambda t:F.loss_risk(construct(t),rho)['source_photon_HS_risk_coefficient'],bounds=(.15,.85),method='bounded',options={'xatol':1e-7})
    assert opt.success
    target=float(opt.x)
    optimized=F.loss_risk(construct(target),rho)
    assert optimized['source_photon_HS_risk_coefficient']<=base['source_photon_HS_risk_coefficient']+1e-10
    # Search only row order at fixed optimal t, deterministic and scoped.
    rng2=np.random.default_rng(1919)
    V=construct(target)
    permutations=[np.arange(len(V))]+[rng2.permutation(len(V)) for _ in range(80)]
    trials=[]
    for ix,p in enumerate(permutations):
        s=F.loss_risk(V[p],rho)
        trials.append(dict(trial=ix,permutation=p.tolist(),**s))
    best=min(trials,key=lambda z:z['source_photon_HS_risk_coefficient'])
    # Reproduce direct risk by replaying the stored output permutation.
    replay=F.loss_risk(V[np.array(best['permutation'])],rho)
    assert abs(replay['source_photon_HS_risk_coefficient']-best['source_photon_HS_risk_coefficient'])<1e-11
    return dict(status='PASS_19_EFFECT_WITTING_WEIGHT_AND_ROUTING_OPTIMIZATION',
      source_frames=[list(F.C),list(F.D)],outcomes=19,
      reference_half_half=base,
      bounded_weight_optimum_t=target,
      fixed_order_weight_optimized=optimized,
      tested_output_row_orders=len(trials),
      best_tested_order=best,
      source_state_seed=4281,
      limitations='One seeded pure input, eta=0.995 on affected rails. SciPy scalar weight optimization is numeric and local to one parameter. Random 80-permutation selection does NOT certify globally optimal optical routing. No measured hardware, detector saturation, dark counts, multi-photon indistinguishability, drift or design robustness over all input states.')
if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status'],d['bounded_weight_optimum_t'],d['best_tested_order']['gate_count'],d['best_tested_order']['source_photon_HS_risk_coefficient'])
