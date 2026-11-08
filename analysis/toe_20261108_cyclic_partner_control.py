"""Declared cyclic-partner benchmark from2610.30253, not a W33 completion.

Independent high precision CW differentiation and frozen-population response.
Every dimensional scale is supplied. No conversion-rate or cosmology fit.
"""
import json
from pathlib import Path
import mpmath as mp
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
mp.mp.dps=100


def cw_second(N,eps,theta):
    """Exact dimensionless one-loop V''/M^4 at mu=M, Dirac partners."""
    terms=[]
    for k in range(N):
        t=theta+2*mp.pi*k/N
        z=1+eps**2+2*eps*mp.cos(t)
        dz=-2*eps*mp.sin(t);ddz=-2*eps*mp.cos(t)
        terms.append(2*mp.log(z)*dz**2+2*z*(mp.log(z)-1)*ddz)
    return -mp.fsum(terms)/(16*mp.pi**2)


def cw_potential(N,eps,theta):
    vals=[1+eps**2+2*eps*mp.cos(theta+2*mp.pi*k/N) for k in range(N)]
    return -mp.fsum(z*z*(mp.log(z)-mp.mpf('1.5'))for z in vals)/(16*mp.pi**2)


def leading_curvature(N,eps):
    return N*N*eps**N/(4*mp.pi**2*(N-1)*(N-2))


def population_control(N,eps,temperature,theta_i=.37,nodes=4096):
    """Freeze NR equilibrium weights at theta_i; differentiate only masses."""
    k=2*np.pi*np.arange(N)/N
    mi=np.sqrt(1+eps*eps+2*eps*np.cos(theta_i+k))
    logw=1.5*np.log(mi)-mi/temperature
    w=np.exp(logw-logw.max());w/=w.sum()
    theta=2*np.pi*np.arange(nodes)/nodes
    phase=theta[:,None]+k
    masses=np.sqrt(1+eps*eps+2*eps*np.cos(phase))
    dmass=-eps*np.sin(phase)/masses
    effective=masses@w
    beta=-(dmass@w)/effective
    uniform=masses.mean(axis=1)
    return dict(N=N,Td_over_M=temperature,formation_phase=theta_i,
                minimum_m_over_Td=float(mi.min()/temperature),
                frozen_weights=w.tolist(),population_first_fourier_abs=float(abs(w@np.exp(1j*k))),
                uniform_fractional_rms=float(np.std(uniform)/np.mean(uniform)),
                biased_fractional_rms=float(np.std(effective)/np.mean(effective)),
                max_abs_collective_beta_f_equals_MP=float(np.max(abs(beta))),
                angular_nodes=nodes,
                scope='Supplied instantaneous internal-equilibrium/freeze approximation; weights held fixed during subsequent field scan. No proof of efficient conversions, total relic abundance or realized field excursion.')


def build():
    b=mp.mpf('.053');eps=(1-mp.sqrt(1-4*b*b))/(2*b)
    M=mp.mpf(16000);f=mp.mpf('2.435e27');H0=mp.mpf('1.44667e-33')
    dimensional=M**4/(f*f*H0*H0)
    rows=[]
    for N in range(3,41):
        exact=abs(cw_second(N,eps,mp.mpf(0)))
        lead=leading_curvature(N,eps)
        rows.append(dict(N=N,leading_envelope_over_H0_squared=float(lead*dimensional),
                         exact_theta0_over_H0_squared=float(exact*dimensional),
                         theta0_exact_over_leading=float(exact/lead)))
    first=next(r['N']for r in rows if r['leading_envelope_over_H0_squared']<1)
    precise=[dict(N=N,theta=str(t),analytic=str(cw_second(N,eps,t)),
                  independent_mpmath_differentiation=str(mp.diff(lambda x:cw_potential(N,eps,x),t,2)))
             for N in [3,9,18,21,27]for t in [mp.mpf(0),mp.mpf('.37')]]
    out=dict(status='DECLARED_CYCLIC_PARTNER_SPECTRUM_AND_FROZEN_POPULATION_CONTROL_NOT_NATIVE_COMPLETION',
             reference='https://arxiv.org/abs/2610.30253',
             supplied=dict(individual_beta_at_pi_over2=float(b),eps=float(eps),mass_eV=float(M),f_eV=float(f),H0_eV=float(H0),arbitrary_precision_digits=mp.mp.dps),
             radiative_scan=rows,first_N_leading_envelope_below_H0_squared=first,
             high_precision_derivative_controls=precise,
             populations=[population_control(N,float(eps),T)for N in [12,18,first,27]for T in [.1,.03,.01,.003]],
             interpretation='N is a supplied field-replication parameter. Leading one-loop curvature at this benchmark does not establish full radiative stability or a physical vacuum. The maximal native Sp43 element order18, PSp43 order12 and PGSp43 order12 cannot supply an element of orderN>=first_N under the specific single-generator embedding requirement; added symmetries/extensions are not excluded.',
             scope='No shared W33 action, conversion collision terms, scalar background/perturbation solver, portal audit, Planck-suppressed operator audit or physical TOE. Uniform-population values below float precision are numerical floors, not measured tiny harmonics.')
    (ROOT/'data/toe_20261108_cyclic_partner_control.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('CYCLIC',first,'eps',float(eps),'N18',rows[15],flush=True)
    return out


if __name__=='__main__':build()
