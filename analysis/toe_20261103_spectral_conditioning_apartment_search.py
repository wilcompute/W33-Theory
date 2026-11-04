#!/usr/bin/env python3
"""Deterministic 81-cycle basis seed scan for condition and pi-flux tradeoffs.

All candidates satisfy the proven maximum load 5. The finite 33-seed
search is not a proof of global spectral optimality.
"""
from pathlib import Path
from collections import Counter
import importlib.util, json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/"analysis"/"2026_11_03_optimal_5load_apartment_hamiltonian.py"
spec=importlib.util.spec_from_file_location("base",MOD)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
OUT=ROOT/"data"/"toe_20261103_spectral_conditioning_apartment_search.json"

def run():
    D,C,flags=base.build()
    results=[]
    for seed in range(1,34):
        pick,loads=base.choose(C,seed=seed)
        B=C[:,pick]
        assert len(pick)==81 and int(max(loads))==5 and int(sum(loads))==648
        assert not np.any(D@B)
        Gram=B.T@B
        ev=np.linalg.eigvalsh(Gram.astype(float))
        assert ev[0]>0
        cond=float(ev[-1]/ev[0])
        # Cheap symmetric product avoids 160-mode Hermitian eigensolve.
        H=B@B.T
        S=np.sign(H).astype(np.int64);np.fill_diagonal(S,0)
        N=np.abs(S)
        triangles=int(np.trace(N@N@N)//6)
        signed_sum=int(np.trace(S@S@S)//6)
        negative=(triangles-signed_sum)//2
        edgecount=int(np.count_nonzero(np.triu(H,1)))
        results.append(dict(seed=seed,condition_number=cond,
            min_nonzero_eigenvalue=float(ev[0]),max_eigenvalue=float(ev[-1]),
            max_flag_load=int(max(loads)),nonzero_hoppings=edgecount,
            triangle_count=triangles,pi_flux_triangles=negative,
            load_histogram={str(k):int(v) for k,v in sorted(Counter(loads).items())},
            selected_apartment_indices=pick))
    best=min(results,key=lambda x:x["condition_number"])
    assert best["seed"]==33 and best["condition_number"]<1300
    control=results[0]
    assert control["pi_flux_triangles"]==780 and control["nonzero_hoppings"]==1883
    summary=dict(status="PASS_SEED33_SAMPLED_SPECTRAL_PARETO_IMPROVEMENT",
        experiment="33 deterministic basis seeds, all 81 cycles and GF2 independent, maximum load five",
        best_seed=33,original_seed=1,improvement_factor=control["condition_number"]/best["condition_number"],
        original=control,best=best,
        attempted_seeds=33,
        audit_boundary="Not a globally minimal condition number. Eigenspectra are floating calculations; cycle ranks and load checks are exact. Pi-flux counts are exact integers.",
        search_results=[{k:v for k,v in item.items() if k!="selected_apartment_indices"} for item in results])
    OUT.write_text(json.dumps(summary,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print(summary["status"],"condition",best["condition_number"],
          "gain",summary["improvement_factor"],"hoppings",best["nonzero_hoppings"])
    return summary

if __name__=="__main__":
    run()
