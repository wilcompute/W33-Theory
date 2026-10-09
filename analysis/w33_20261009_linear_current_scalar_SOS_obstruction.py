"""Numerical no-go for scalar-current Cauchy spectral lower bound.

The 160 bilinear symbols Ve(q) Ue(p) are linearly independent iff their
160x160 Gram [(Ve.Vf)(Ue.Uf)] is positive definite.
Then no weighted sum of currents cancels all principal symbols into a
positive scalar identity. This does NOT exclude nonlinear SOS bounds.
"""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as vac
def certificate():
    g=vac.geometry()
    U40=np.rint(40*g['u']).astype(np.int64)
    V40=np.rint(40*g['v']).astype(np.int64)
    gram=(U40@U40.T)*(V40@V40.T)
    edges=vac.actual_edges()
    adjacent=np.array([[int(i!=j and bool(set(e)&set(f))) for j,f in enumerate(edges)] for i,e in enumerate(edges)],dtype=np.int64)
    exact=6400*np.ones((160,160),dtype=np.int64)+2304000*adjacent+9728000*np.eye(160,dtype=np.int64)
    assert np.array_equal(gram,exact)
    levi=np.zeros((80,80),dtype=np.int64)
    for a,b in edges:levi[a,b]=levi[b,a]=1
    A2=levi@levi
    assert np.array_equal(levi@(A2-6*np.eye(80,dtype=np.int64))@
                          (A2-16*np.eye(80,dtype=np.int64)),
                          np.zeros((80,80),dtype=np.int64))
    from math import sqrt
    levi_expected=sorted([-4.,4.]+[-sqrt(6)]*24+[sqrt(6)]*24+[0.]*30)
    assert np.max(np.abs(np.linalg.eigvalsh(levi)-levi_expected))<1e-9
    ev=np.linalg.eigvalsh(gram.astype(float))
    rank=np.linalg.matrix_rank(gram)
    u=np.array(g['u']);v=np.array(g['v'])
    Q=v.T@u
    sym=Q+Q.T
    eig=np.linalg.eigvals(Q)
    assert rank==160 and abs(ev[0]-5120000)<1e-5
    assert np.max(np.abs(u.sum(axis=0)))<1e-12
    assert np.max(np.abs(v.sum(axis=0)))<1e-12
    assert abs(np.trace(Q))<1e-10
    assert np.max(np.abs(np.imag(eig)))<1e-8
    # Sum Je = Qbilinear(q,p)+8I; Q is real with nonzero eigs
    return dict(status='PASS',current_count=160,
        exact_Gram_identity='K = 6400*J + 2304000*A_linegraph + 9728000*I',
        exact_Gram_spectrum={'5120000':81,'14336000':30,'24576000':1,
          '14336000-2304000*sqrt6':24,'14336000+2304000*sqrt6':24},
        exact_min_eigenvalue=5120000,
        bilinear_symbol_gram_rank=int(rank),
        bilinear_symbol_gram_min_eigenvalue=float(ev[0]),
        bilinear_symbol_gram_max_eigenvalue=float(ev[-1]),
        Q_nonzero_eigenvalues_sorted=[float(a) for a in sorted(np.real(eig)) if abs(a)>1e-7],
        weighted_scalar_sum_impossible=True,
        theorem='The 160 bilinear principal symbols are linearly independent. Hence no nontrivial real weighted current sum is a scalar. In particular, scalar-Cauchy SOS cannot produce an H>=cI via an identity sum w_e J_e=cI.',
        extra='Equal-weight sum is a nontrivial dilation/linear symplectic generator plus constant 8; its spectrum is not bounded away from zero.',
        scope='Rules out this *linear-current* scalar lower-certificate tactic, not positive spectral lower bounds from nonlinear or representation-theoretic arguments; numeric Gram conditioning checked.')
if __name__=='__main__':
    o=certificate()
    (ROOT/'data/w33_20261009_linear_current_scalar_SOS_obstruction.json').write_text(json.dumps(o,indent=2)+'\n')
    print('rank',o['bilinear_symbol_gram_rank'],'mineig',o['bilinear_symbol_gram_min_eigenvalue'])
