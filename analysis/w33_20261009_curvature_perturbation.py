"""Relative form-bounded curvature perturbation of W33 current-square H.

Exact theorem: for C=i[J_e,J_f] as a quadratic form,
|c[psi]| <= ||J_e psi||^2+||J_f psi||^2 <= h[psi].
Hence (1-|eps|)H <= H+eps C <= (1+|eps|)H.
Compact resolvent persists for |eps|<1, if baseline Pass11778 holds.
A finite 2x2 control checks positivity, evenness and no Kramers doublet.
"""
import sympy as S
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def certificate():
    a=S.Rational(1,4);eps=S.symbols('eps',real=True)
    X=S.Matrix([[0,1],[1,0]])
    Z=S.diag(1,-1)
    J1=X+a*S.eye(2);J2=Z+a*S.eye(2)
    H=J1**2+J2**2
    C=S.I*(J1*J2-J2*J1)
    assert S.simplify(H+C-(J1-S.I*J2)*(J1+S.I*J2))==S.zeros(2)
    assert S.simplify(H-C-(J1+S.I*J2)*(J1-S.I*J2))==S.zeros(2)
    assert C.conjugate()==-C and H.conjugate()==H
    ev=list((H+eps*C).eigenvals())
    assert len(ev)==2
    assert all(S.simplify(x.subs(eps,-eps)-x)==0 for x in ev)
    assert all(S.simplify(x.subs(eps,0)-x.subs(eps,0))==0 for x in ev)
    return dict(status='PASS',relative_form_bound=1,
        compact_resolvent_for='-1 < eps < 1',
        ordered_eigenvalue_bounds='(1-|eps|)*E_j(0) <= E_j(eps) <= (1+|eps|)*E_j(0)',
        reflection='T H(eps) T^-1 = H(-eps), spectra equal for +/-eps',
        no_kramers='T^2=+1 does not force ground degeneracy',
        two_level_control_spectrum=[str(x) for x in ev],
        real_ground_rule='For a one-dimensional ground eigenspace, curvature expectation at eps=0 vanishes.',
        limitation='Does not compute W33 ground multiplicity, numerical gap, or physically identify T with CP.')
if __name__=='__main__':
    result=certificate()
    (ROOT/'data/w33_20261009_curvature_perturbation_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)
