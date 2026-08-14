#!/usr/bin/env python3
"""Pass5083: exact q=3 active-chart minimization contract.

Variables are apartment bits x, theta parity auxiliaries t, and one activity bit
per opposite-pair chart.  For a valid K4 cut restriction chart weight is 0,3,4,
so 3 z_O <= sum_{A in O} x_A <= 4 z_O.  Fixing x_0=1 is valid by apartment
transitivity for any nonzero word.  If HiGHS returns OPTIMAL=108 this certifies
the sharp q=3 inequality A(y)>=108=4q^3.
"""
from __future__ import annotations
import argparse,json,itertools
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.optimize import milp,Bounds,LinearConstraint
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5083_Q3_ACTIVE_CHART_MILP.json'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=600.0);args=ap.parse_args()
    G=build_W(3);n=len(G['apartments']);charts=G['charts'];assert (n,len(charts))==(1620,1080)
    theta=[]
    for _,loc in charts:
        for i,j,k in itertools.combinations(range(4),3):
            theta.append((loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))]))
    assert len(theta)==4320 and len(set(tuple(sorted(t)) for t in theta))==4320
    nt=len(theta);nz=len(charts);offt=n;offz=n+nt;nvar=n+nt+nz
    rr=[];cc=[];vv=[];lo=[];hi=[];r=0
    # theta parity x_i+x_j+x_k-2t=0
    for k,(i,j,l) in enumerate(theta):
        rr += [r]*4;cc += [i,j,l,offt+k];vv += [1.,1.,1.,-2.];lo.append(0.);hi.append(0.);r+=1
    # activity: sum local x -3z >=0 and sum local x -4z <=0
    for k,(_,loc) in enumerate(charts):
        ids=list(loc.values())
        rr += [r]*(len(ids)+1);cc += ids+[offz+k];vv += [1.]*len(ids)+[-3.];lo.append(0.);hi.append(np.inf);r+=1
        rr += [r]*(len(ids)+1);cc += ids+[offz+k];vv += [1.]*len(ids)+[-4.];lo.append(-np.inf);hi.append(0.);r+=1
    # x0=1
    rr.append(r);cc.append(0);vv.append(1.);lo.append(1.);hi.append(1.);r+=1
    A=sparse.coo_matrix((vv,(rr,cc)),shape=(r,nvar)).tocsr()
    c=np.zeros(nvar);c[offz:]=1.
    lb=np.zeros(nvar);ub=np.ones(nvar);integrality=np.ones(nvar,dtype=np.int8)
    res=milp(c=c,integrality=integrality,bounds=Bounds(lb,ub),constraints=LinearConstraint(A,np.array(lo),np.array(hi)),
             options={'time_limit':args.seconds,'mip_rel_gap':0.0})
    incumbent=getattr(res,'x',None) is not None
    objective=None if not incumbent else int(round(float(res.fun)))
    verdict='OPTIMAL' if res.success else ('TIME_LIMIT_WITH_INCUMBENT' if incumbent else 'TIME_LIMIT_NO_INCUMBENT')
    out={'pass':5083,'status':verdict,'q':3,'apartments':n,'theta_checks':nt,'charts':nz,
         'model_variables':nvar,'model_constraints':r,'objective_active_charts':objective,
         'target':108,'solver_status':int(res.status),'solver_message':str(res.message),
         'theorem_closed':bool(res.success and objective==108),
         'implication':'If theorem_closed, A(y)>=108 and wt>=3A/4>=81; chamber stars attain equality.',
         'boundary':'No all-q active-chart theorem is inferred. Non-optimal solver exits are UNKNOWN.'}
    if res.success: assert objective==108
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
