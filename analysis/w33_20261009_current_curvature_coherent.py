"""Actual-current curvature in a deliberately T-breaking displaced coherent Gaussian.

Each J_e is a Weyl-ordered quadratic because U_e.V_e=0. Therefore
i[J_e,J_f]=-{J_e,J_f}_Poisson EXACTLY (no Moyal remainder).
For all W33 pairs Ve.Uf=Ue.Vf, so a CENTERED real Gaussian has zero
curvature. A momentum-displaced real Gaussian p0=a(Ue-Uf) yields
<Cef>=-a² (Ve.Uf) ||Ue-Uf||², a²=1/20.
This is an explicit nonzero witness without assuming it is a ground state.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as vac
def certificate():
    g=vac.geometry()
    edges=vac.actual_edges()
    U=np.rint(g['u']*40).astype(int);V=np.rint(g['v']*40).astype(int)
    assert np.max(np.abs(g['u']*40-U))<1e-9
    A=U@V.T
    # Disjoint edges commute; neighboring currents have integer symplectic brackets.
    neighboring=[]
    for i in range(160):
        for j in range(i+1,160):
            p=int(V[i]@U[j]);q=int(U[i]@V[j])
            if set(edges[i]).isdisjoint(edges[j]):assert p==q==0
            if p!=0 or q!=0:
                assert p==q
                # Prepare p0=a(Ue-Uf), q0=0; a^2=1/20.
                norm=int((U[i]-U[j])@(U[i]-U[j]))
                neighboring.append((i,j,p,q,F(-p*norm,20*1600*1600)))
    assert neighboring and len(neighboring)==480
    first=neighboring[0]
    differences=sorted(set(t[4] for t in neighboring))
    assert all(np.dot(U[i],V[i])==0 for i in range(160))
    chosen=[dict(e=int(i),f=int(j),edge_e=list(edges[i]),edge_f=list(edges[j]),
          symplectic_brackets_int=[int(p),int(q)],curvature_expectation=str(c))
        for i,j,p,q,c in neighboring[:8]]
    return dict(status='PASS',current_count=160,
        nonzero_current_curvature_pair_count=len(neighboring),
        distinct_centered_real_gaussian_curvature=[str(x) for x in differences],
        example=chosen,
        domain='Real Gaussian displaced in momentum p0=a(Ue-Uf) for each chosen adjacent pair, q0=0; finite-energy test vector, NOT T-fixed ground state.',
        theorem='Exactly quadratic Weyl currents imply i[J_e,J_f] = -{J_e,J_f}_Poisson. Centered real Gaussian curvature vanishes for all pairs because Ve.Uf=Ue.Vf. A shifted Gaussian can have nonzero curvature; not a ground-state result.')
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261009_current_curvature_coherent.json').write_text(json.dumps(d,indent=2)+'\n')
    print({k:v for k,v in d.items() if k!='example'});print(d['example'][:2])
