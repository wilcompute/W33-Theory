"""Exact CP transmission and protected-modulus soft response.

The scalar vacuum is prior Pass11953; added gauge protection is11958.
This extends their diagnostics, not a derived W33 or full E6 vacuum.
"""
from pathlib import Path
import json
import sys
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))


def cp_transmission():
    from w33_pass11952_11955_threshold_vacuum_loop_leptons import cp_vacuum
    prior=cp_vacuum()
    m=sp.Matrix([[1,1,0],[0,2,1],[1,0,3]])/10
    r=sp.Matrix([[1,2,1]])/10;t=sp.Matrix([[1,-1,2]])/10
    mu=sp.Rational(1,5); Hu=sp.diag(1,4,9)
    records=[]
    for sign in (1,-1):
        B=r+sign*sp.I*t
        Hd=m*(sp.eye(3)-B.conjugate().T*B/(mu**2+(B*B.conjugate().T)[0]))*m.T
        comm=Hu*Hd-Hd*Hu
        invariant=sp.simplify(sp.im(sp.trace(comm**3)))
        assert invariant!=0
        full=m.row_join(sp.zeros(3,1)).col_join(B.row_join(sp.Matrix([[mu]])))
        det=sp.factor(full.det());assert det==sp.Rational(7,5000)
        # Independent decoupling check using the actual4x4 left mass matrix.
        numeric=[]
        eff=np.asarray(Hd,complex); _,ue=np.linalg.eigh(eff)
        J_eff=float(np.imag(ue[0,0]*ue[1,1]*ue[0,1].conjugate()*ue[1,0].conjugate()))
        for scale in (10.,100.,1000.):
            M=np.asarray(full,complex);M[3,:]*=scale
            ev,U=np.linalg.eigh(M@M.conj().T)
            W=U[:3,:3]
            J=float(np.imag(W[0,0]*W[1,1]*W[0,1].conjugate()*W[1,0].conjugate()))
            numeric.append(dict(heavy_scale=scale,J_quartet=J,
                                unitarity_error=float(np.linalg.norm(W@W.conj().T-np.eye(3))),
                                error_vs_decoupling=abs(J-J_eff)))
        assert numeric[-1]['error_vs_decoupling']<1e-7
        records.append(dict(cp_sign=sign,scalar_gauge_invariant_Im_S1T2=-sign,
                            weak_basis_Im_trace_commutator_cubed=str(invariant),
                            tree_full_determinant=str(det),J_decoupling=J_eff,
                            heavy_decoupling_checks=numeric))
    assert sp.sympify(records[0]['weak_basis_Im_trace_commutator_cubed'])==-sp.sympify(records[1]['weak_basis_Im_trace_commutator_cubed'])
    return dict(status='PASS',prior_vacuum=prior,records=records,
                exact_argument='Nonzero ImTr[Hu,Hd]^3 forbids any quark weak-basis transformation restoring CP. Real supplied Yukawa rows couple the prior gauge-inequivalent S,T vacua to this observable; conjugation reverses it while det fullM stays positive.',
                scope='Prior11953 singlet F/D-flat scalar vacuum and supplied rational real Yukawa couplings; controlled vectorlike decoupling. No fitted physical masses, full E6 stabilization, radiatively safe strong CP or new scalar-vacuum priority claim.')


def high_norm(p):
    d=(2*p+p*p)/12
    return (np.sqrt(d*d+4)+d)/2


def normalized_radial(x,rho):
    p=rho*x;u=high_norm(p);u0=high_norm(rho)
    du=(1+p)/(6*(1+1/u**2))
    ratio=np.sqrt(u/u0)*x**12
    derivative=np.sqrt(u/u0)*(12*x**11+rho*du*x**12/(2*u))
    return ratio,derivative


def radial_minima(kappa,rho=1/32):
    # Exactly F/D flat for the first four constraints, all multipliers zero.
    # Only f_U and the supplied positive P soft mass vary on this curve.
    def derivative(x):
        a,da=normalized_radial(x,rho)
        return (a-1)*da+kappa*kappa*x
    grid=np.geomspace(1e-8,2,1600)
    roots=[]
    for a,b in zip(grid,grid[1:]):
        if derivative(a)*derivative(b)<0:
            x=brentq(derivative,a,b,xtol=1e-14)
            step=1e-5
            curvature=(derivative(x+step)-derivative(x-step))/(2*step)
            if curvature>0:
                z,_=normalized_radial(x,rho)
                roots.append(dict(x=x,V_over_F0_squared=(z-1)**2+kappa*kappa*x*x,
                                  derivative_curvature=curvature))
    return roots


def soft_modulus():
    mp.mp.dps=90
    rho=mp.mpf(1)/32;d=(2*rho+rho*rho)/12
    u=(mp.sqrt(d*d+4)+d)/2;pm=mp.sqrt(u);pp=1/pm;v=mp.sqrt(rho)
    J=mp.matrix([[v,0,v,0,-1,0,0],
                 [0,-2j*v,0,2j*v,-2,0,0],
                 [-3j*v,3*v,3j*v,3*v,0,0,0],
                 [0,0,0,0,0,pp,pm],
                 [0,0,0,0,12*pm*rho**11,rho**12,0]])
    eigen,_=mp.eighe(J*J.H)
    singular=[mp.sqrt(x) for x in eigen]
    assert all(x>0 for x in eigen)
    # Repeat at independent precision to detect fake zero eigenvalues.
    with mp.workdps(120):
        eig2,_=mp.eighe(J*J.H)
        relative=abs(mp.sqrt(eig2[0])/singular[0]-1)
    assert relative<mp.mpf('1e-45')
    kcrit2=12*(mp.mpf(10)/11)**(mp.mpf(5)/6)/11
    kspin2=72*(mp.mpf(5)/11)**(mp.mpf(5)/6)/11
    scale=mp.mpf('1e16')
    radial_scale=pm*rho**11*scale
    rows=[]
    for soft in (mp.mpf('1e-8'),mp.mpf('.1'),mp.mpf('1'),mp.mpf('1000')):
        k=float(soft/radial_scale)
        minima=radial_minima(k)
        rows.append(dict(soft_GeV=float(soft),kappa=k,nonzero_local_minima=minima,
                         restricted_global_minimum='nonzero' if minima and min(z['V_over_F0_squared'] for z in minima)<1 else 'origin'))
    assert rows[0]['restricted_global_minimum']=='nonzero'
    assert rows[-1]['nonzero_local_minima']==[]
    F=4*np.pi/.1*1000*1e6
    gravitino=F/(np.sqrt(3)*2.435e18)
    # Every Abelian charge assignment preserving the five constraint
    # polynomials on these seven condensates is already X/Z. Constraint
    # multipliers may carry the opposite charge of the first three rows.
    charges=sp.Matrix([[1,0,1,0,-1,0,0],
                       [0,1,0,1,-1,0,0],
                       [1,-1,-1,1,0,0,0],
                       [0,0,0,0,0,1,1],
                       [0,0,0,0,12,1,0]])
    X=sp.Matrix([-1,-1,1,1,0,0,0]);Z=sp.Matrix([0,0,1,1,1,-12,12])
    assert charges.rank()==5 and charges*X==charges*Z==sp.zeros(5,1)
    assert sp.Matrix.hstack(X,Z).rank()==2
    return dict(status='PASS',rho='1/32',constraint_J_singular_values=[mp.nstr(x,60) for x in singular],
                canonical_light_mass_GeV_if_Lambda_1e16=float(singular[0]*scale),
                precision_recheck_relative_error=float(relative),
                exact_restricted_curve='P=p real; S=(sqrt(p),i sqrt(p)); T=(sqrt(p),-i sqrt(p)); PhiMinus=sqrt(u(p)), PhiPlus=1/PhiMinus, u-1/u=(2p+p²)/12. Multipliers and spectator VEVs zero.',
                exact_restricted_potential='V/Lambda^4=|sqrt(u(p))*p^12-sqrt(u(rho))*rho^12|²+(msoft/Lambda)²*p²',
                leading_constant_high_norm_theorems={'degenerate_nonzero_minimum_x12':'10/11','spinodal_x12':'5/11',
                    'critical_kappa_squared':mp.nstr(kcrit2,40),'spinodal_kappa_squared':mp.nstr(kspin2,40)},
                exact_curve_soft_sweep=rows,
                no_new_Abelian_D_direction={'charge_constraint_rank':5,'charge_kernel_dimension':2,
                    'basis_X':list(map(int,X)),'basis_Z':list(map(int,Z)),
                    'theorem':'Any additional Abelian gauge charge preserving the stated constraint polynomials on these seven condensates is a linear combination of X,Z. At the same F/D-flat branch its D-term Hessian adds no independent radial gauge direction and cannot lift the gauge-orthogonal light F mode. New fields or changed stabilization operators are required; shifted FI vacua are not excluded.'},
                conditional_gauge_mediation={'alpha':.1,'visible_soft_GeV':1000,'messenger_GeV':1e6,
                    'F_GeV_squared':F,'F_over_messenger_squared':F/1e12,'gravitino_GeV':gravitino,
                    'radial_minima_if_only_gravity_scale_reaches_P':radial_minima(gravitino/float(radial_scale)),
                    'gate':'No direct high-sector gauge/kinetic-mixing transmission, A terms, tadpoles or supergravity vacuum computed. This is a necessary scale window, not an actual mediation model.'},
                scope='Canonical-K SUSY singlet constraint spectrum and an exact restricted D-flat soft-response curve, not a full softly broken E6 vacuum. Lowest F singular mode is orthogonal to both complex gauge kernels; D terms lift only their radial partners. Positive P soft mass alone erases the nearby selected minimum at TeV scales on this curve; other soft patterns are not excluded.',
                prior='analysis/w33_pass11957_11959_color_threshold_and_cp_quality.py:11958',
                primary='https://arxiv.org/abs/hep-ph/9801271')


def payload():
    return {'status':'PASS','11965':cp_transmission(),'11966':soft_modulus()}


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11965_11966_cp_transmission_soft_modulus.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['11965']['records'][0]['weak_basis_Im_trace_commutator_cubed'],d['11966']['canonical_light_mass_GeV_if_Lambda_1e16'],d['11966']['exact_curve_soft_sweep'],flush=True)
