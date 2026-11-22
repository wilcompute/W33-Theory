#!/usr/bin/env python3
"""F/D-flat E6 adjoint/vectorlike singlet truncation and accidental family moduli obstruction."""
import sympy as s

def verify():
    n=3;u=s.symbols('u0:3');v=s.symbols('v0:3');a=s.symbols('a');m,lam,M=s.symbols('m lam M',nonzero=True)
    # For E6 27 -> SO10 16_1+10_-2+1_4:
    qnorm=16*1**2+10*(-2)**2+1*4**2
    assert qnorm==72
    bilinear=sum(x*y for x,y in zip(u,v))
    W=(m+4*lam*a)*bilinear+s.Rational(1,2)*M*qnorm*a*a
    F=[s.diff(W,x) for x in (*u,*v,a)]
    root=s.solve([m+4*lam*a,s.diff(W,a)],[a,bilinear],dict=True)
    ar=-m/(4*lam);br=s.Rational(9,2)*M*m/(lam*lam)
    assert s.expand((m+4*lam*ar))==0
    assert s.expand(4*lam*br+72*M*ar)==0
    subs={m:1,lam:1,M:1,a:s.Rational(-1,4),u[0]:s.sqrt(s.Rational(9,2)),v[0]:s.sqrt(s.Rational(9,2)),u[1]:0,u[2]:0,v[1]:0,v[2]:0}
    assert all(s.simplify(f.subs(subs))==0 for f in F)
    J=s.Matrix(F).jacobian((*u,*v,a)).subs(subs)
    rank=int(J.rank()); assert rank==2
    complex_tangent=7-rank
    complex_gauge_orbit=1
    residual=complex_tangent-complex_gauge_orbit
    assert residual==4
    # Nonzero parameter and conjugate VEV select |u|=|v|, [A,A^dag]=0, hence D-flat.
    # For a fixed flavor direction the three-family singlet sector has 4 complex flat moduli
    # after the broken E6 U1 quotient, with accidental GL3 rotations.
    # The 27+27bar spectator chirality is vectorlike, independent of flavor orientation.
    return dict(status='PASS_E6_FD_FLAT_ADJOINT_SINGLET_BRANCH_AND_FAMILY_MODULI_OBSTRUCTION',
        E6_branching='27=16_1+10_-2+1_4',trace_Q_squared=qnorm,
        toy_superpotential='W=(m+4 lambda a) (sum_i v_i u_i)+(M/2)*72*a^2',
        adjoint_a=str(ar),holomorphic_pairing_s=str(br),
        illustrative_D_flat_point={'m':1,'lambda':1,'M':1,'a':'-1/4','u0':'sqrt(9/2)','v0':'sqrt(9/2)','others':0},
        F_gradient_all_zero=True,D_terms_zero_on_conjugate_singlet_ansatz=True,
        F_jacobian_rank=rank,complex_singlet_plus_adjoint_variables=7,
        complex_ungauged_flat_tangent=complex_tangent,broken_complex_U1_gauge_directions=complex_gauge_orbit,
        remaining_complex_flat_moduli=residual,
        limitations='Truncated SO10-singlet and E6-adjoint Cartan ansatz. This is a renormalizable supersymmetric E6 invariant W in a vectorlike model, assuming standard E6 contraction and invariant projection. It is not a fully isolated E6 vacuum or three chiral Standard Model families. Family uniformity produces an accidental GL3 and four complex moduli. A full nonsinglet Hessian and gauge Goldstone spectrum is NOT evaluated here.')
if __name__=='__main__':print(verify())
