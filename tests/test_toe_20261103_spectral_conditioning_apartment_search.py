"""Recheck deterministic seed-33 Pareto improvement without rerunning the whole search."""
import importlib.util, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"toe_20261103_spectral_conditioning_apartment_search.json"
module=ROOT/"analysis"/"toe_20261103_spectral_conditioning_apartment_search.py"
spec=importlib.util.spec_from_file_location("search",module)
search=importlib.util.module_from_spec(spec);spec.loader.exec_module(search)

def test_seed_sweep_certificate_and_provenance():
    r=json.loads(P.read_text(encoding="utf8"))
    assert r["status"]=="PASS_SEED33_SAMPLED_SPECTRAL_PARETO_IMPROVEMENT"
    assert len(r["search_results"])==33
    assert r["best_seed"]==33
    assert r["improvement_factor"]>270
    assert r["best"]["max_flag_load"]==5
    assert r["best"]["nonzero_hoppings"]==1896
    assert r["best"]["pi_flux_triangles"]==752

def test_seed_33_rerun_cycle_and_spectrum():
    D,C,_=search.base.build()
    indices,load=search.base.choose(C,seed=33)
    B=C[:,indices]
    assert len(indices)==81 and max(load)==5 and not np.any(D@B)
    exact=json.loads(P.read_text(encoding="utf8"))
    assert indices==exact["best"]["selected_apartment_indices"]
    vals=np.linalg.eigvalsh((B.T@B).astype(float))
    assert math.isclose(float(vals[-1]/vals[0]),exact["best"]["condition_number"],rel_tol=1e-7)
