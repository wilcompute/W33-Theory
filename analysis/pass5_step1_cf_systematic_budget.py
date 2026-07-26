#!/usr/bin/env python3
"""
Pass5 Step 1: CF Systematic Budget + Full SRG Verification
Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>
"""
import numpy as np
from itertools import permutations

q, v, k, lam_p, mu_p = 3, 40, 12, 2, 4

def symp(u, w):
    return (u[0]*w[3] - u[3]*w[0] + u[1]*w[2] - u[2]*w[1]) % 3

vecs = []
for a in range(3):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                if (a,b,c,d)==(0,0,0,0): continue
                vv = (a,b,c,d)
                if symp(vv,vv) != 0: continue
                if not any(tuple(x*s%3 for x in vv)==w for w in vecs for s in [1,2]):
                    vecs.append(vv)
assert len(vecs)==40, f'{len(vecs)}'

adj = np.zeros((40,40),dtype=int)
for i,u in enumerate(vecs):
    for j,w in enumerate(vecs):
        if i!=j and symp(u,w)==0: adj[i,j]=1

assert all(adj.sum(1)==12)
lam_vals = set(int(adj[i]@adj[j]) for i in range(40) for j in range(40) if adj[i,j]==1 and i!=j)
mu_vals  = set(int(adj[i]@adj[j]) for i in range(40) for j in range(40) if adj[i,j]==0 and i!=j)
assert lam_vals=={2} and mu_vals=={4}
print('SRG(40,12,2,4) VERIFIED from GF(3)^4 symplectic form')

eigs = sorted(np.linalg.eigvals(adj.astype(float)).real.round())
from collections import Counter
print('Eigenvalues:', dict(Counter(int(e) for e in eigs)))

# Systematic budget
print()
print('Systematic error budget:')
bdg = [('Dark counts',0.001),('Tritter mismatch',0.0015),
       ('EOM phase',0.0008),('Photon contamination',0.0005),('Switching latency',0.0002)]
for nm,val in bdg:
    print(f'  {nm:30s}: dCF < {val:.4f}')
print(f'  TOTAL (quadrature):             dCF < {np.sqrt(sum(v**2 for _,v in bdg)):.4f}')

CF_null=0.005; CF_W33=0.1; N=120
mu0=N*CF_null; sig0=np.sqrt(N*CF_null*(1-CF_null))
T_crit=mu0+2.326*sig0
mu1=N*CF_W33; sig1=np.sqrt(N*CF_W33*(1-CF_W33))
print(f'\nSNR = {(mu1-T_crit)/sig1:.1f}sigma, T_crit={T_crit:.1f}')
print(f'Expected violated contexts: {mu1:.0f} (W33) vs {mu0:.1f} (null)')
