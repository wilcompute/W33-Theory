"""A declared circle Wilson line and complete one-Dirac KK loop.

Known extranatural mechanism; no radion stabilization, relic populations,
complete charged inventory or quantum-gravity completion is supplied.
"""
import json
import math
from pathlib import Path
import mpmath as mp
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
MP=2.435e27;H0=1.44667e-33;M=16000.


def harmonic_log(Mass,R,ell=1):
    x=2*math.pi*ell*Mass*R
    # One periodic5D Dirac field = one4D Dirac per integer KK mode.
    # V_nonlocal=sum A_l cos(q*l*theta), zero-winding constant subtracted.
    return math.log(3/(16*math.pi**6))-4*math.log(R)-5*math.log(ell)-x+math.log(1+x+x*x/3)


def curvature_log10(a,r=.01,q=1,Mass=M):
    R=a/Mass;f=r*MP
    if a==0:raise ValueError('Use massless_control at fixed radius')
    first=harmonic_log(Mass,R)+2*math.log(abs(q)/(f*H0))
    ratios=[math.exp(harmonic_log(Mass,R,l)-harmonic_log(Mass,R)+2*math.log(l))for l in range(1,65)]
    x=2*math.pi*a
    # Each curvature harmonic ratio <= exp[-x*(l-1)]/l for a>0.
    tail_bound=math.exp(-x*64)/(1-math.exp(-x))if x*64<745 else 0.
    return (first+math.log(sum(ratios)+tail_bound))/math.log(10)


def proper_time_harmonic(Mass,R,ell=1):
    """Independent positive Schwinger integral, scaled around its saddle."""
    with mp.workdps(65):
        mm=mp.mpf(str(Mass));rr=mp.mpf(str(R));ll=mp.mpf(ell)
        a=mm*rr;x=2*mp.pi*a*ll
        integrand=lambda u:mp.exp(-mp.mpf('2.5')*u-x*(mp.cosh(u)-1))
        # exp[-x(cosh(u)-1)] falls superexponentially; no cutoff subtraction.
        val=mp.quad(integrand,[-8,-2,0,2,8])
        pref=mm**mp.mpf('2.5')/(4*mp.pi**4*rr**mp.mpf('1.5')*ll**mp.mpf('2.5'))
        return pref*mp.exp(-x)*val


def branch(a,r=.01,q=1,beta=.053,excursion=.3):
    # beta=-q*x/[2pi*r*(a^2+x^2)], x=n+q*theta/(2pi).
    B=2*math.pi*r*abs(beta)/abs(q)
    if 2*B*a>1:return dict(a=a,r=r,q=q,status='LOCAL_BETA_UNAVAILABLE_ON_ANY_KK_BRANCH')
    x0=-2*B*a*a/(1+math.sqrt(1-4*B*B*a*a))
    theta0=2*math.pi*x0/q # n0=0, possibly not the lowest level.
    def mass(x):return M*math.sqrt(1+x*x/(a*a))
    rows=[]
    for delta in [.001,.01,.1,excursion]:
        x=x0+q*delta/(2*math.pi*r)
        rows.append(dict(delta_phi_over_MP=delta,x=x,mass_ratio=mass(x)/mass(x0),
                         beta=-q*x/(2*math.pi*r*(a*a+x*x))))
    return dict(a=a,r=r,q=q,initial_theta=theta0,initial_x=x0,initial_mode_n=0,
                initial_mode_is_ground=abs(x0)<=.5,initial_mass_eV=mass(x0),
                initial_beta=-q*x0/(2*math.pi*r*(a*a+x0*x0)),
                maximal_beta_any_branch=abs(q)/(4*math.pi*r*a),
                relaxed_ground_max_log_mass_ratio=.5*math.log1p(1/(4*a*a)),
                fixed_branch_excursions=rows,
                scope='Physical diagonal KK eigenbranches, not a held-coordinate curvature. Fixed mode occupation is distinct from instantaneous relaxation to the lightest KK band. No conversion rate, populated spectrum, realized field excursion or constant-beta fit is established.')


def benchmark(a=12.,r=.01,q=1,bulk_fields=2):
    R=a/M;f=r*MP;g4=1/(2*math.pi*R*f)
    return dict(a=a,r=r,q=q,bulk_Dirac_fields=bulk_fields,M_eV=M,R_eV_minus1=R,radius_m=R*1.973269804e-7,
                f_eV=f,g4=g4,KK_spacing_eV=1/R,
                M5_eV=(MP*MP/(2*math.pi*R))**(1/3),
                log10_loop_curvature_over_H0_squared=curvature_log10(a,r,q)+math.log10(bulk_fields),
                first_harmonic_phase_energy_over_3_MP_squared_H0_squared=bulk_fields*math.exp(harmonic_log(M,R))/(3*MP*MP*H0*H0),
                fixed_population_density_curvature_control=dict(supplied_Omega_DM=.26,
                    curvature_over_H0_squared=3*.26*(q/(2*math.pi*r))**2*a*a/(a*a+branch(a,r,q)['initial_x']**2)**2,
                    scope='One occupied fixedKKbranch, rho_DM=3*Omega_DM*H0^2*MP^2. Matter term n*m(phi) has positive curvature even when the vacuum loop is tiny. Not a solved homogeneous or perturbed cosmology.'),
                q_g4_MP_eV=abs(q)*g4*MP,g4_MP_eV=g4*MP,
                magnetic_scale_over_bulk_mass=g4*MP/M,
                branch=branch(a,r,q),
                caveat='M5 assumes flat circle Einstein reduction. q*g4*MP andg4*MP are reported weak-gravity diagnostic scales with order-one conventions, not measured cutoffs or proof of a UV completion. Radion, magnetic objects, extra charged states and gravitational nonlocal effects unbuilt.')


def build():
    b=benchmark();controls=[]
    for a in [1.,6.,12.]:
        R=a/M;exact=proper_time_harmonic(M,R)
        controls.append(dict(a=a,positive_proper_time_integral=str(exact),closed_harmonic=math.exp(harmonic_log(M,R)),
                             relative_integral_residual=float(exact/mp.mpf(str(math.exp(harmonic_log(M,R))))-1)))
    a_low=brentq(lambda a:curvature_log10(a,.01)+math.log10(2)-math.log10(.01),3.,20.)
    a_ground=math.sqrt((1/(4*math.pi*.01*.053))-.25)
    # The preceding equation solves beta at x=.5 exactly.
    extra=[]
    R=b['R_eV_minus1'];f=b['f_eV']
    with mp.workdps(40):
        massless=3*mp.zeta(3)/(16*mp.pi**6*mp.mpf(str(R))**4*mp.mpf(str(f*H0))**2)
    extra.append(dict(charged_bulk_mass_eV=0.,log10_curvature_over_H0_squared=float(mp.log10(massless))))
    for mass in [M/10,M/2,M]:
        extra.append(dict(charged_bulk_mass_eV=mass,log10_curvature_over_H0_squared=curvature_log10(mass*R,.01,1,mass)))
    result=dict(status='DECLARED_WILSON_LINE_KK_EIGENMASSES_AND_COMPLETE_ONE_DIRAC_LOOP_NOT_TOE',
      action='Flat5D U1 on a supplied circle: -F_MN^2/(4g5^2)+sum_s=+,- DiracBar_s(iGamma^M D_M-s*M)Dirac_s. Two same-charge periodic Dirac fields with opposite signed bulk masses are used as a parity-paired benchmark. theta=integral A5dy; f=1/(2pi Rg4), g4^2=g5^2/(2piR). Scalar/gravity/radion/other charged sectors not specified.',
      spectrum='m_n^2=M^2+(n+q*theta/(2pi))^2/R^2, n integer. theta->theta+2pi relabels n->n-q; complete spectrum and loop are gauge periodic.',
      potential='V_nonlocal=3/(16pi^6 R^4)*sum_l>=1 exp(-x_l)(1+x_l+x_l^2/3)*cos(q*l*theta)/l^5, x_l=2pi*l*M*R. One periodic5D Dirac, theta-independent local divergence subtracted. All positive coefficients make the absolute curvature envelope attained at theta0.',
      protection='5D local gauge invariance forbids a local potential forA5. A Wilson-loop potential is nonlocal and is generated by charged trajectories winding the circle. This is an established extranatural mechanism, not a prohibition on unknown nonlocal UV contributions.',
      benchmark=b,proper_time_controls=controls,
      parity_odd_boundary='Single-Dirac formulas refer to the parity-even determinant only. Five-dimensional fermions also induce parity-odd Chern-Simons terms with a mass-sign dependence. The benchmark pairs opposite signed masses so the mass-sign shifts cancel; an allowed integer CS counterterm/regulator convention is chosen to cancel a remaining integer offset. The parity-even potential doubles. No proof of every global/topological anomaly or microscopic regulator/UV completion is asserted.',
      conditional_window=dict(r=.01,required_local_beta=.053,loop_target=.01,
                              first_a_with_loop_envelope_below_target=a_low,
                              last_a_with_that_beta_on_initial_ground_band=a_ground,
                              window_exists=a_low<a_ground,
                              scope='Only these two diagnostics; no stable DE vacuum, actual relic population, full charged inventory or cosmological likelihood.'),
      charged_contamination=extra,
      ownership='Extranatural Wilson-line protection hep-th/0301218; gauge-origin axions1804.01112 and2607.08814. New declared keV benchmark and independent integral/spectrum controls, not discovery or complete realization of these mechanisms.',
      limits='No radius selection/stabilization, scalar background, production/conversions, observedSMparameters or gravity completion. Boundary sectors and truncating the KK tower may change protection. Light charged species can dominate the potential. No solved TOE.')
    (ROOT/'data/toe_20261108_wilson_line_mass_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('WILSON_BENCHMARK',b,'WINDOW',result['conditional_window'],'EXTRA',extra,flush=True)
    return result


if __name__=='__main__':build()
