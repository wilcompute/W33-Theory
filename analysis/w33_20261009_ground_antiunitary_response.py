"""Finite ground-sector antiunitary T^2=+1 response classification.

For every T-odd Hermitian form C, its compression to a finite-dimensional
T-real ground eigenspace has matrix i*A, A real skew. It has paired +/- real
eigenvalues and a zero if multiplicity is odd. Toy matrices check
linear cusp versus quadratic nondegenerate response exactly.
"""
from pathlib import Path
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
def certificate():
    eps=s.symbols('eps',real=True)
    A2=s.Matrix([[0,1],[-1,0]])
    K=s.I*A2
    assert K.conjugate()==-K and K.H==K
    assert sorted(K.eigenvals().keys())==[-1,1]
    E0=s.Integer(2)
    H2=E0*s.eye(2)+eps*K
    assert sorted(H2.eigenvals().keys(),key=str)==sorted([2-eps,2+eps],key=str)
    A3=s.Matrix([[0,1,0],[-1,0,0],[0,0,0]])
    K3=s.I*A3
    assert set(K3.eigenvals())=={-1,0,1}
    assert K3.rank()==2
    Hsimple=s.diag(2,5)+eps*K
    eig=Hsimple.eigenvals()
    low=(7-s.sqrt(9+4*eps*eps))/2
    assert s.simplify(Hsimple.charpoly().as_expr().subs(s.Symbol('lambda'),low))==0
    assert s.diff(low,eps).subs(eps,0)==0
    assert s.diff(low,eps,2).subs(eps,0)==-s.Rational(2,3)
    return dict(status='PASS',antiunitary='T^2=+1, TCT^-1=-C',
         finite_ground_matrix='P0 C P0 = i A, A real skew',
         pairs='all nonzero first-order shifts appear in +/- pairs, odd ground multiplicity forces a zero',
         degenerate_control='twofold E0=2 gives lowest eigenvalue 2-|eps| (linear cusp)',
         simple_control='E0(eps)=(7-sqrt(9+4eps^2))/2',
         simple_second_derivative='-2/3',
         scope='Finite compact ground sector, not its unknown W33 multiplicity or a thermodynamic spontaneous-symmetry-breaking proof.')
if __name__=='__main__':
    out=certificate()
    (ROOT/'data/w33_20261009_ground_antiunitary_response.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out)
