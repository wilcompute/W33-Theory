"""Exact current-curvature variance in isotropic 78-mode Gaussian vacuum.

For C=i[Je,Jf]=b(Xe Yf-Xf Ye), b=Ue.Vf=Uf.Ve,
use exact Wick + Moyal:
Var(C)=b²/4 (||R||F²+tr(R²))+
       b²*a²/2 (||Ve-Vf||²+||Uf-Ue||²),
R=Ve Uf^T-Vf Ue^T; a²=1/20.
This is an isotropic TEST vector, NOT the actual Hamiltonian ground.
"""
from pathlib import Path
import sys,json
from fractions import Fraction as F
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as vac
def certificate():
    geom=vac.geometry()
    U=np.rint(40*geom['u']).astype('int64')
    V=np.rint(40*geom['v']).astype('int64')
    edges=vac.actual_edges()
    rec=[]
    def dot(x,y):return F(int(x@y),1600)
    for i in range(160):
        for j in range(i+1,160):
            b=dot(U[i],V[j])
            if b==0:continue
            assert b==dot(U[j],V[i])
            lu,lv=dot(U[i],U[j]),dot(V[i],V[j])
            l2=dot(U[i],U[i]);v2=dot(V[i],V[i])
            assert l2==v2==F(39,20)
            rnorm=2*l2*l2-2*lu*lv
            tracesq=2*b*b
            qterm=b*b*(rnorm+tracesq)/4
            linear=b*b*F(1,20)*(2*l2-2*lu+2*v2-2*lv)/2
            rec.append(dict(e=i,f=j,shared='point' if edges[i][0]==edges[j][0] else 'line',
                            b=str(b),variance=str(qterm+linear),
                            bilinear=str(qterm),linear=str(linear)))
    counts=Counter((r['shared'],r['variance']) for r in rec)
    assert len(rec)==480
    assert len(counts)==2,counts
    return dict(status='PASS',actual_current_pairs=480,
       pair_type_variance_counts={str(k):n for k,n in sorted(counts.items())},
       examples=[r for r in rec[:5]],
       expectation='zero for all pairs in centered uncorrelated isotropic pure Gaussian',
       theorem='Nonzero exact curvature fluctuations even when first moment vanishes. The Wick variance includes the Moyal/ordering correction tr(R²); omitting it gives incorrect quantum covariance.',
       boundary='This is a test Gaussian, not a certified ground-state curvature susceptibility or breaking.')
if __name__=='__main__':
    o=certificate()
    (ROOT/'data/w33_20261009_isotropic_curvature_fluctuations.json').write_text(json.dumps(o,indent=2)+'\n')
    print(o['pair_type_variance_counts'])
