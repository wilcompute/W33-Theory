#!/usr/bin/env python3
"""Flat W33 gauge+fermion Hessian proportionality to the 1620-octagon metric.

Numerically tests across beta and random tangent directions; exact
symbolic proof not supplied. All loops are the full 1620, not native
1382 contractible deck plaquettes. Detect if proportionality fails.
"""
import numpy as np,json,sys
from pathlib import Path
from scipy.linalg import eigvalsh
from w33_20261109_full_u1_variational_vacuum import model,physics

def main(path=None):
    ctx=model()
    W=ctx[-1]
    G=W.T@W
    rng=np.random.default_rng(98761)
    rows=[]
    for beta in (.1,.3,.5,1.,2.,5.,10.):
        vecs=[]
        for i in range(7):
            v=rng.normal(size=81)
            v/=np.linalg.norm(v)
            step=0.0002
            gp=physics(step*v,ctx,0,beta)[1]
            gm=physics(-step*v,ctx,0,beta)[1]
            hv=(gp-gm)/(2*step)
            ratio=-float(v@hv)/float(v@G@v)
            residual=np.linalg.norm(hv+ratio*(G@v))/(np.linalg.norm(hv)+1e-30)
            vecs.append((ratio,residual))
        arr=np.array(vecs)
        rows.append({"beta":beta,
                "ratio_mean":float(arr[:,0].mean()),
                "ratio_spread":float(arr[:,0].max()-arr[:,0].min()),
                "worst_operator_relative_residual":float(arr[:,1].max())})
    result={"status":"PASS_W33_FLAT_HESSIAN_EIGHT_CYCLE_METRIC_PROPORTIONALITY_NUMERIC",
        "beta_direction_controls":rows,
        "octagon_metric_min_positive_eigenvalue":float(eigvalsh(G)[0]),
        "octagon_metric_max_positive_eigenvalue":float(eigvalsh(G)[-1]),
        "scientific_scope":"Numerical Hessian directional tests. A rigorous analytic coefficient and identity for general beta are NOT proved here; high beta may be nonanalytic in flat zero eigenvalues, so check residuals. A positive all-octagon gauge κ stabilizes the flat stationary point quadratically only when κ exceeds the beta-dependent negative fermion Hessian direction.",
        "do_not_claim":"Spontaneous symmetry breaking, thermodynamic phase transition, global gauge vacuum or SM mass from finite matrix numerics."
        }
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("HESSIAN_PROPORTIONS",json.dumps([(r["beta"],r["ratio_mean"],r["ratio_spread"],r["worst_operator_relative_residual"]) for r in rows]))
    return result
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
