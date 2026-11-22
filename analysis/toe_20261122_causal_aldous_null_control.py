#!/usr/bin/env python3
"""Aldous interchange-process gap: causal gap decrease can be kinetic, not emergent gravity."""
from pathlib import Path
import json,math,itertools
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
import toe_20261122_causal_growth_finite_spectrum as G
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_causal_aldous_null_control.json'

def gap_free(n):
    orders=list(itertools.permutations(range(n)));ix={p:i for i,p in enumerate(orders)}
    rr=[];cc=[];vv=[]
    for i,o in enumerate(orders):
      for k in range(n-1):
        p=list(o);p[k],p[k+1]=p[k+1],p[k]
        rr.append(i);cc.append(ix[tuple(p)]);vv.append(-1/(n-1))
      rr.append(i);cc.append(i);vv.append(1.)
    M=coo_matrix((vv,(rr,cc)),shape=(len(orders),len(orders))).tocsr()
    eig=np.linalg.eigvalsh(M.toarray())[:3] if n<=5 else np.sort(eigsh(M,k=3,which='SA',tol=1e-12)[0])
    exact=2*(1-math.cos(math.pi/n))/(n-1)
    assert abs(eig[0])<1e-12 and abs(eig[1]-exact)<1e-10,(n,eig[1],exact)
    return float(exact)

def verify():
    orig=G.verify()['nested_W33_induced_graphs']
    rows=[]
    for x in orig:
        n=x['n_vertices'];g=gap_free(n); observed=x['first_excitation_gap']
        rows.append(dict(n=n,states=x['number_of_total_order_states'],
            W33_interval_action_gap=observed,
            zero_action_adjacent_swap_gap=g,ratio_W33_over_free=observed/g,
            absolute_gap_difference=observed-g))
    assert all(.85 <r['ratio_W33_over_free']<1.05 for r in rows)
    return dict(status='PASS_W33_CAUSAL_ALDOUS_INTERCHANGE_NULL_CONTROL',
      samples=rows,zero_action_formula='lambda_1(n)=2(1-cos(pi/n))/(n-1) for normalized adjacent-transposition interchange walk on S_n, by the proved Aldous spectral-gap theorem',
      literature='Caputo, Liggett, Richthammer (2010), Proof of Aldous spectral gap conjecture, JAMS 23 831-851, arXiv:0906.1238',
      inference='The entire n=4..7 decreasing-gap trend exists even with zero W33 interval action. It is thus not evidence for emergent Lorentzian dynamics or graviton.',
      physical_limit='Finite n=4-7 controls do not rule out another causal dynamics, and fitted gap ratios are not physical predictions.')
if __name__=='__main__':
    d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status']);print(d['samples'])
