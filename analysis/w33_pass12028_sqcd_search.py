"""Replay the charged SQCD fit from the previous leading-threshold branch."""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import least_squares
import w33_pass12026_12033_theta_soft_threshold_connections as q

def main():
    seed=q.prior.MATCH.copy()
    fit=least_squares(q.residual,seed,max_nfev=200,xtol=1e-11,ftol=1e-11,gtol=1e-11,diff_step=1e-5)
    assert max(abs(fit.fun))<1e-7
    out=dict(status='PASS',seed_source='Pass12024 leading-onlySQCD MATCH',seed=seed.tolist(),parameters=fit.x.tolist(),residual=fit.fun.tolist(),function_evaluations=fit.nfev,matching_scale_GeV=float(q.p.MZ*np.exp(fit.x[-1])),scope='Localdiscoveryreplay; no globaluniquenessclaim. Physicalthresholds/flow are exactly the imported12028declaredp0SQCDmodel; completeMSSMmatchingremainsopen.')
    path=Path(__file__).resolve().parents[1]/'data/w33_pass12028_sqcd_search_record.json';path.write_text(json.dumps(out,indent=2)+'\n');print('PASS localSQCDsearch',fit.nfev,max(abs(fit.fun)))
if __name__=='__main__':main()
