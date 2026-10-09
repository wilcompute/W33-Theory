"""T-odd current curvature in the W33 incidence algebra.

Two-level real symmetric control checks the no-Kramers/thermal logic;
it is not a truncation of the 78-coordinate W33 Hamiltonian.
"""
from pathlib import Path
import json,sys
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11769_quantized_current_vacuum import actual_edges
def certificate():
    edges=actual_edges()
    assert len(edges)==160
    adjacent=sum(bool(set(edges[i]) & set(edges[j]))
                 for i in range(160) for j in range(i+1,160))
    assert adjacent==480
    X=sp.Matrix([[0,1],[1,0]])
    Z=sp.diag(1,-1)
    c=sp.Rational(1,3)
    J1=X+c*sp.eye(2);J2=Z+c*sp.eye(2)
    H=J1*J1+J2*J2
    C=sp.I*(J1*J2-J2*J1)
    assert H==H.conjugate()
    assert C==-C.conjugate()
    eig=H.eigenvals()
    assert len(eig)==2 and list(eig.values())==[1,1]
    assert sp.trace(C)==0 and sp.trace(H*C)==0
    return dict(status='PASS',incidences=160,noncommuting_edge_pairs=adjacent,
       commuting_edge_pairs=160*159//2-adjacent,
       ground_doublet_control='Nondegenerate real 2x2 toy Hamiltonian',
       real_control_eigenvalues=[str(x) for x in eig],
       antiunitary_square='+1',
       selection='T-fixed vector or faithful T-invariant Gibbs state has vanishing expectation for i[J_e,J_f].',
       boundary='No classification of all antiunitaries; no physical CP or chirality identification.')
if __name__=='__main__':
    r=certificate()
    (ROOT/'data/w33_20261008_current_curvature_thermal.json').write_text(json.dumps(r,indent=2)+'\n')
    print(r)
