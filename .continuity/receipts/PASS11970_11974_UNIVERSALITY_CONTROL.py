"""Executable non-W33 negative control for the11970 free Dirac mechanism.

Same harmonic-current/Wilson recipe, with a2-site4-multiedge unit cell.
This control forbids interpreting free Dirac existence as W33 uniqueness.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigvalsh

V=np.vstack([np.zeros(3,dtype=int),np.eye(3,dtype=int)])
J=np.vstack([-2*np.ones(3,dtype=int),2*np.eye(3,dtype=int)])
SIGMA=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
ALPHA=[np.kron([[0,1],[1,0]],s) for s in SIGMA]
BETA=np.diag([1,1,-1,-1])
assert np.array_equal(J.T@V,2*np.eye(3))
assert np.array_equal(J.sum(axis=0),np.zeros(3))


def Hamiltonian(k):
    phase=np.exp(1j*V@k)
    B=np.column_stack([-np.ones(4),phase]);C=np.column_stack([.5*np.ones(4),.5*phase])
    K=[-1j*C.conj().T@(J[:,i,None]*B) for i in range(3)]
    return sum(np.kron(a,d) for a,d in zip(ALPHA,K))+10*np.kron(BETA,B.conj().T@B)


def payload():
    ev=eigvalsh(Hamiltonian(np.zeros(3)))
    assert sum(abs(ev)<1e-10)==4
    p=np.array([2.,-1,3]);p/=np.linalg.norm(p)
    rows=[]
    for a in (.02,.01,.005,.0025):
        ev=eigvalsh(Hamiltonian(a*p));low=np.sort(ev[np.argsort(abs(ev))[:4]])/a
        rows.append(dict(spacing=a,low_scaled=low.tolist(),max_error=float(max(abs(low-[-1,-1,1,1])))))
    assert rows[-1]['max_error']<rows[0]['max_error']/8
    return dict(status='PASS',control_graph='Two vertices joined by4 multiedges with voltages0,e1,e2,e3: infinite cover is a two-sublattice four-neighbour graph, NOT W33.',
                spinor_bands=8,J=J.tolist(),origin_zero_modes=4,origin_heavy_gap=80.,refinement=rows,
                theorem_scope='The11970 argument extends to a connected finite voltage graph with positive3-period harmonic Gram and three unit holonomy generators; J=n h G^-1 normalizes the projected Dirac symbol. Positive Wilson block excludes other zeros. Generic Wilson technology, not a W33-specific selection theorem.',
                consequence='A single free3+1D Dirac species cannot identify W33 or derive3families/gravity/couplings. This much smaller graph realizes the same infrared free operator. W33-specific predictions require selected interactions/vacuum data or independently constrained irrelevant matching coefficients.',
                primary_context='https://arxiv.org/abs/2306.14180; two-sublattice four-neighbour3D models also occur in https://arxiv.org/abs/cond-mat/0607699 but that is a DIFFERENT Hamiltonian.')


if __name__=='__main__':
    d=payload();Path(__file__).with_suffix('.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS non-W33 control',d['spinor_bands'],[r['max_error'] for r in d['refinement']])
