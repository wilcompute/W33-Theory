"""Actual lepton-branch spectral potential audit and orientation selection.

Standard trace-alignment theorem, applied to the stored11960 branches.
Not a potential derived from W33 or a new prediction of measured parameters.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]


def orientation_control():
    rng=np.random.default_rng(11967)
    A=np.diag([1.,4.,9.]);b=np.array([.2,1.,3.])
    X=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    U,_=np.linalg.qr(X);B=(U*b)@U.conj().T
    K=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));K=(K+K.conj().T)/2
    def V(t):
        R=expm(1j*t*K);C=R@B@R.conj().T
        return -float(np.trace(A@C).real)
    slope=-float(np.trace(A@(1j*(K@B-B@K))).real)
    numeric=(V(1e-5)-V(-1e-5))/2e-5
    assert abs(slope-numeric)<1e-8
    # Every polynomial spectral function of EACH sector separately is
    # constant on independent unitary orbits, so cannot select mixing.
    independent=[]
    for t in (0.,.3,.7):
        R=expm(1j*t*K);C=R@B@R.conj().T
        independent.append([float(np.trace(np.linalg.matrix_power(C,n)).real) for n in (1,2,3)])
    assert np.max(abs(np.array(independent)-independent[0]))<1e-12
    aligned=-float(np.dot(np.diag(A),b))
    reverse=-float(np.dot(np.diag(A),b[::-1]))
    assert aligned<V(0)<reverse
    return dict(spectral_orbit_traces=independent,mixed_potential_variation_analytic=slope,
                finite_difference_variation=numeric,random_mixed_potential=V(0),
                alignment_global_minimum=aligned,opposite_extremum=reverse,
                theorem='For simple spectra, stationarity of -Tr(A U B Udagger) gives [A,U B Udagger]=0. Global minimum pairs eigenvalues in the same order (trace rearrangement); all stationary orientations are permutations, with no mixing. Separate-sector spectral potentials leave all orientations flat.',
                implication='A spectral mass potential or a single linear mixed trace cannot select observed mixing. Competing orientation invariants are required; their coefficients must be derived rather than fitted.')


def lepton_branch_potential():
    d=json.loads((ROOT/'data/w33_pass11960_11961_clebsch_and_shared_cone.json').read_text())['11960']
    rows=[];spl=.0025;mu=1.
    for f in d['two_real_diagonal_45_coefficients_fits']:
        for r in f['two_real_offdiagonal_neutrino_roots']:
            # The absolute comparator scale is supplied, as in TOE51.
            # Singular values are reconstructed from the stored bare matrix
            # and the actual shared kinetic root, not inferred from delta.
            import sys
            sys.path.insert(0,str(ROOT/'analysis'))
            from w33_pass11960_11961_clebsch_and_shared_cone import quark_kernel
            _,A=quark_kernel()
            nu=A.T@np.array(r['real_bare_Majorana'])@A
            s=np.sort(np.linalg.svd(nu,compute_uv=False))
            s*=np.sqrt(spl/(s[-1]**2-s[0]**2))
            q4=float(np.sum(s**4))
            cw=-float(np.sum(s**4*(np.log(s*s/(mu*mu))-1.5)))/(32*np.pi**2)
            rows.append(dict(delta_deg=r['delta_deg'],masses_eV=s.tolist(),
                             Majorana_CW_eV_fourth=cw,quartic_invariant_eV_fourth=q4))
    crossings=[]
    for i in range(len(rows)):
        for j in range(i):
            dq=rows[i]['quartic_invariant_eV_fourth']-rows[j]['quartic_invariant_eV_fourth']
            if abs(dq)>1e-12:
                dc=rows[i]['Majorana_CW_eV_fourth']-rows[j]['Majorana_CW_eV_fourth']
                c=-dc/dq
                assert abs(dc+c*dq)<1e-20
                crossings.append(dict(branch_i=i,branch_j=j,allowed_counterterm_crossing=c))
    assert crossings
    c0=crossings[0]['allowed_counterterm_crossing']
    rankings=[]
    for c in (c0-1.,c0+1.):
        rankings.append(dict(coefficient=c,ordering=list(map(int,np.argsort([
            r['Majorana_CW_eV_fourth']+c*r['quartic_invariant_eV_fourth'] for r in rows])))))
    assert rankings[0]['ordering']!=rankings[1]['ordering']
    return dict(branches=rows,counterterm_crossings=crossings,rankings=rankings,
                supplied_scale='Delta m31²=.0025 eV², subtraction mu=1eV; not derived',
                allowed_counterterm='c Tr[(Mnu† Mnu)^2] is weak-basis invariant and CP even; its coefficient is an unspecified UV scalar-potential matching datum',
                conclusion='One-loop neutrino vacuum energy does not select a physical lepton phase from these fitted roots without fixing the allowed invariant counterterm. A chosen subtraction convention is not a dynamical prediction.',
                prior='TOE51 already owns branch-dependent masses and m_bb;11960 owns the fitted roots. This audits a proposed dynamical ranking.')


def majorana_orientation_positive_control():
    y1,y2=sp.Rational(1,3),sp.Rational(2,3)
    U=sp.Matrix([[1,sp.I],[1,-sp.I]])/sp.sqrt(2)
    Y=sp.diag(y1,y2)*U
    assert sp.simplify(U*U.T)==sp.Matrix([[0,1],[1,0]])
    mass=sp.simplify(Y*Y.T)
    invariant=sp.simplify(sp.trace(mass*mass.conjugate().T))
    assert invariant==2*y1*y1*y2*y2
    diagonal=y1**4+y2**4
    assert diagonal-invariant==(y1*y1-y2*y2)**2>0
    assert sp.simplify(U.T*mass*U)==sp.eye(2)*y1*y2
    return dict(Yukawa_singular_values=[str(y1),str(y2)],
                orthogonal_RH_invariant='I_R=Tr[(Ynu Ynu.T)(Ynu Ynu.T)dagger]',
                exact_orientation_potential='For S=U_R U_R.T, t=|S11|²=|S22|², I_R=2 y1² y2²+t(y1²-y2²)². Positive coefficient selects t=0 globally on the2D unitary orbit.',
                invariant_at_minimum=str(invariant),invariant_at_diagonal_orientation=str(diagonal),
                seesaw_matrix_unit_M=[[str(x) for x in row] for row in mass.tolist()],
                Takagi_mass_both=str(y1*y2),
                boundary='Known O2-right-handed Majorana orientation mechanism, not a newly discovered flavour theorem. Singular values and degenerate heavy mass are supplied. The exact light masses are degenerate, so the displayed45-degree Takagi basis does not predict an observable mixing angle;3-family splitting, coefficient selection and UV embedding remain open.',
                primary='https://arxiv.org/abs/1306.5922')


def payload():
    return dict(status='PASS',orientation=orientation_control(),lepton_branches=lepton_branch_potential(),
                Majorana_sensitive_positive_control=majorana_orientation_positive_control(),
                scope='Executed two concrete selector candidates and their obstructions. No unique flavour coefficients, mass scale or out-of-sample selected branch derived.')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11967_flavour_orientation_selector.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['lepton_branches']['rankings'],flush=True)
