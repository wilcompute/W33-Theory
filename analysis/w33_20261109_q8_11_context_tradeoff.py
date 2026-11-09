#!/usr/bin/env python3
"""Explore 10/11/12 context precision-resource tradeoff for W33 Q8 tomography."""
import json,sys
from pathlib import Path
import numpy as np
from w33_20261109_q8_ten_context_tomography import select, random_unitary, projection_design
from w33_20261109_q8_12setting_completion import main as twelve

def main(path=None):
    ten,(B,U,V,op,_)=select(return_components=True)
    Mb=projection_design(B,op)
    M10=np.vstack([Mb,projection_design(U,op),projection_design(V,op)])
    rng=np.random.default_rng(2026110944)
    best=None
    for idx in range(300):
        Q=random_unitary(rng)
        M=np.vstack([M10,projection_design(Q,op)])
        # Optimize actual full frame conditioning, not merely its 16D projection.
        sv=np.linalg.svd(M,compute_uv=False)
        condition=float(max(sv)/min(sv))
        if best is None or condition<best[0]:
            best=(condition,idx,Q,M,sv)
    c,idx,Q,M11,sv=best
    assert np.linalg.matrix_rank(M11,tol=1e-10)==80
    pseudo=np.linalg.pinv(M11,rcond=1e-14)
    errs=[];r=np.random.default_rng(2026110945)
    for rank in (1,2,3,9):
        for _ in range(8):
            x=r.normal(size=(9,rank))+1j*r.normal(size=(9,rank))
            rho=x@x.conj().T;rho/=np.trace(rho)
            p=np.concatenate([np.einsum("ij,ik,kj->j",e.conj(),rho,e).real
                              for e in (B,U,V,Q)])
            theta=pseudo@(p-1/9)
            re=np.eye(9)/9+np.einsum("i,ijk->jk",theta,op)
            errs.append(np.max(abs(re-rho)))
    assert max(errs)<3e-12
    twelve_data=twelve()
    out={"status":"PASS_11_SETTING_ADAPTIVE_EXTRA_FRAME_TRADEOFF",
         "ten":{"settings":10,"rank":80,"condition":ten["combined_condition_number"],"generic_9mode_contexts":2},
         "eleven":{"settings":11,"rank":80,"condition":c,"generic_9mode_contexts":3,
                   "third_context_optimizations":300,"third_context_index":idx,
                   "min_singular":float(min(sv)),
                   "max_reconstruction_error":float(max(errs))},
         "twelve":{"settings":12,"rank":80,
                   "condition":twelve_data["combined_condition_number"],
                   "matched_product_contexts":4},
         "scope":"11-setting design adds a third generic non-MUB nine-mode basis. 300 seeded candidates; not proven globally optimal. A local 3mode product protocol in 12 contexts is much better conditioned."}
    assert ten["combined_condition_number"]>c>twelve_data["combined_condition_number"]
    if path:Path(path).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("PASS tomography context tradeoff",json.dumps({
       "10":out["ten"]["condition"],"11":c,"12":out["twelve"]["condition"],
       "11_reconstruction_error":max(errs)}))
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
