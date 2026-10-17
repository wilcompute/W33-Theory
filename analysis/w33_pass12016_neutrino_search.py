"""Portable local search from the earlier12007 Majorana witness, not a global scan."""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import least_squares
from w33_pass12007_shared_theta_leptons import NEUTRINO_FIT,NEUTRINO_TARGET
from w33_pass12016_12020_neutrino_vacuum_native_measure import neutrino_observables

def main():
    seed=NEUTRINO_FIT.copy();stages=[]
    for two_loop in (False,True):
        result=least_squares(lambda p:np.log(neutrino_observables(p,two_loop)[0]/NEUTRINO_TARGET),seed,max_nfev=500,xtol=1e-12,ftol=1e-12,gtol=1e-12)
        assert max(abs(result.fun))<1e-7
        stages.append(dict(two_loop_flavour_terms=two_loop,seed=seed.tolist(),parameters=result.x.tolist(),residual=result.fun.tolist(),function_evaluations=result.nfev))
        seed=result.x
    out=dict(status='PASS',initial_seed_source='Pass12007 NEUTRINO_FIT',stages=stages,scope='Local search on a one-dimensional fit fibre; coordinates need not equal frozen witness. No uniqueness or global optimum claim; same one-loop SM background as12011.')
    path=Path(__file__).resolve().parents[1]/'data/w33_pass12016_neutrino_search_record.json';path.write_text(json.dumps(out,indent=2)+'\n');print('PASS',max(abs(result.fun)),result.nfev)
if __name__=='__main__':main()
