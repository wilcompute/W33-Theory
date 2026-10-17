"""Portable optional search behind the frozen common-scale witness."""
from pathlib import Path
import sys,json,argparse
import numpy as np
from scipy.optimize import least_squares
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12011_12015_scale_flavour_internal_index as p
from w33_pass12007_shared_theta_leptons import Y,EU,FIT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--search',action='store_true');parser.add_argument('--max-evaluations',type=int,default=500);args=parser.parse_args()
    if not args.search:
        print('Frozen maximum log residual:',max(abs(p.rg_residual(p.RG_FIT))));return
    initial=np.r_[np.log(Y),np.log(EU),FIT,10.]
    lo=np.r_[-1.5,-9,-2,-.2,-.2,np.full(5,-60),0];hi=np.r_[.5,-3,1,.2,.2,np.full(5,60),33]
    fit=least_squares(p.rg_residual,initial,bounds=(lo,hi),max_nfev=args.max_evaluations,xtol=1e-11,ftol=1e-11,gtol=1e-11,diff_step=1e-5)
    out=dict(status='PASS' if max(abs(fit.fun))<1e-7 else 'SEARCH_NOT_CONVERGED',method='bounded least_squares with supplied historical MZ data and one-loop SM running; start is12007 atlogscale10, not the new frozen answer',initial=initial.tolist(),coordinates=fit.x.tolist(),residual=fit.fun.tolist(),evaluations=int(fit.nfev),matching_scale_GeV=float(p.MZ*np.exp(fit.x[-1])),scope='Search replay, not a vacuum selection or independently predicted physical scale')
    (ROOT/'data/w33_pass12011_common_scale_search_record.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['matching_scale_GeV'],max(abs(fit.fun)))
if __name__=='__main__':main()
