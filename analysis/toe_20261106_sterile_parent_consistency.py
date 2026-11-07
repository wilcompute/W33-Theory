"""Apply prior CW benchmarks to the current sterile window; test an explicit parent.

Generic CW, subtractions and SUSY controls are already owned by Nov3 packets.
The added hypothesis is canonical real S with V=lambda/4*(S^2-w(phi)^2)^2,
w(phi)=w0 exp(-b phi/Mpl), w=v_S/sqrt2. This is not forced by freeze-in.
"""
import hashlib
import json
import math
import pathlib

import mpmath as mp
import sympy as sy

ROOT = pathlib.Path(__file__).resolve().parents[1]
MPL = 2.435e27  # reduced, eV
H0 = 1.4466703e-33  # declared reference, not a new fit
RHO_DE = 3 * H0**2 * MPL**2 * .69
B = .053
INPUTS = ['analysis/toe_uv/sterile_window.py', 'analysis/toe_uv/sterile_window.json',
          'analysis/toe_uv/sterile_lya.py', 'analysis/toe_uv/sterile_lya.json',
          'analysis/toe_uv/line_drift.json', 'data/toe_20261103_dark_radiative_stability.json',
          'analysis/toe_20261103_dark_radiative_stability.py',
          'analysis/toe_20261103_mechanism_portal_protection.py']


def omega_per_y_squared(mass_GeV, parent_GeV):
    """Replay the existing MB equilibrium-parent approximation, 2 daughters."""
    return (2.744e8 * mass_GeV * 2 * 135 / (8 * math.pi**3 * 1.66 * 106.75**1.5)
            * 1.22e19 / (16 * math.pi * parent_GeV))


def parent_point(mass_keV, parent_GeV):
    mass_GeV = mass_keV * 1e-6
    y = math.sqrt(.12 / omega_per_y_squared(mass_GeV, parent_GeV))
    v = math.sqrt(2) * mass_GeV / y
    floor = math.sqrt(32 * math.pi * 1.66 * math.sqrt(106.75) * parent_GeV / 1.22e19)
    cap = 2.2e-6 * 125.25**2 / (B * v*v)
    w = v/math.sqrt(2)  # mN=y*w and Gamma=y^2*mS/(16pi), canonical real S
    lam = parent_GeV**2 / (2*w*w)
    log_pole = 16 * math.pi**2 / (18*lam)
    return dict(M_keV=mass_keV, m_S_GeV=parent_GeV, y=y, v_S_GeV=v,canonical_real_scalar_vev_GeV=w,
                portal_floor=floor, portal_clock_cap=cap, portal_open=floor < cap,
                lambda_S=lam, beta_lambda_over_lambda=18*lam/(16*math.pi**2),
                scalar_only_one_loop_log_pole_over_mS=log_pole,
                scalar_only_one_loop_pole_over_mS=math.exp(log_pole) if log_pole < 700 else None,
                pole_ratio_exceeds_float_range=log_pole >= 700,
                one_loop_fractional_beta_below_one=18*lam/(16*math.pi**2) < 1,
                radial_CW_absolute_curvature_over_H0_squared=B*B*(parent_GeV*1e9)**4/(8*math.pi**2*MPL**2*H0**2),
                induced_valley_metric_correction=(B*w*1e9/MPL)**2)


def portal_boundary(mass_keV):
    # v^2=A*M_keV^3/mS from the actual source; portal floor=L sqrt(mS).
    # Thus mS_min=(L*A/Bclock)^2*M_keV^6 and lambda_min scales as M_keV^15.
    v = parent_point(mass_keV, 1000)
    threshold = 1000*(v['portal_floor']/v['portal_clock_cap'])**2
    row = parent_point(mass_keV, threshold)
    assert math.isclose(row['portal_floor'], row['portal_clock_cap'], rel_tol=2e-14)
    row['portal_open'] = False  # equality; suppress roundoff-dependent True
    row['on_portal_boundary'] = True
    return row


def symbolic_checks():
    p, S, b, M, v0, lam = sy.symbols('p S b M v0 lam', positive=True)
    v = v0*sy.exp(-b*p/M)
    V = lam*(S*S-v*v)**2/4
    H = sy.hessian(V, (p,S)).subs(S,v)
    dv = sy.diff(v,p)
    target = 2*lam*v*v*sy.Matrix([[dv*dv,-dv],[-dv,1]])
    assert sy.simplify(H-target) == sy.zeros(2)
    assert sy.simplify(H.det()) == 0
    assert sy.simplify(H*sy.Matrix([1,dv])) == sy.zeros(2,1)
    x, a = sy.symbols('x a', real=True)
    z = sy.exp(-2*b*x)
    # One Majorana, fixed mu/m0=exp(a), dimensionless CW shape.
    F = -z*z*(sy.log(z)-2*a-sy.Rational(3,2))
    assert sy.simplify(sy.diff(F,x,2).subs(x,0)-8*b*b*(1+4*a)) == 0
    return dict(valley_hessian='2 lambda w^2 [[wprime^2,-wprime],[-wprime,1]], w=vS/sqrt2',
                eigenvalues=['0','2 lambda w^2 (1+wprime^2)'],
                light_metric='1+wprime^2',
                scalar_curvature_leading='-b^2 mS^4/(8 pi^2 Mpl^2), mu=mS(today)',
                Majorana_curvature='b^2 mN^4/(4 pi^2 Mpl^2)*(1+4 ln(mu/mN0))',
                scheme_control='mu/mN0=exp(-1/4) makes this local curvature zero; not protection along history',
                canonical_scope='Radial CW uses leading wprime^2<<1. Exact Hessian and induced metric are certified; full two-field renormalization is not computed.')


def build():
    parent = json.loads((ROOT/'data/toe_20261103_dark_radiative_stability.json').read_text())
    incoming = json.loads((ROOT/'analysis/toe_uv/sterile_lya.json').read_text())
    original = json.loads((ROOT/'analysis/toe_uv/sterile_window.json').read_text())
    drift = json.loads((ROOT/'analysis/toe_uv/line_drift.json').read_text())
    # Replay every numerical portal row, without endorsing the Ly-alpha criterion.
    for row in incoming['window'] + original['rows']:
        r = parent_point(row['M_keV'],row['m_S'])
        for ours,theirs in [('v_S_GeV','v_S')]:
            assert math.isclose(r[ours], row[theirs], rel_tol=2e-13)
    open_rows = [parent_point(m,s) for m,s in incoming['open_points']]
    fermion = []
    with mp.workdps(80):
        for mass in [7.1, 15, 16, 18, 20, 30]:
            m = mass*1000
            curve = B*B*m**4/(4*math.pi**2*MPL**2)
            delta = 2*math.pi*H0*MPL/(B*m)
            fermion.append(dict(M_keV=mass, Majorana_CW_curvature_over_H0_squared=curve/H0**2,
                                soft_mass_parameter_cap_eV=delta,
                                physical_small_soft_partner_splitting_eV=delta**2/(2*m)))
        history = []
        for label, dat in drift.items():
            for zz, row in dat['rows'].items():
                if zz == '0.0':
                    continue
                x = -mp.mpf(str(dat['cp']))*mp.mpf(str(row['dphi']))
                assert abs(float(mp.exp(x))-row['M_over_M0']) < 5e-15
                residual = -mp.exp(4*x)*(2*x-mp.mpf('1.5'))-(mp.mpf('1.5')+4*x+4*x*x)
                history.append(dict(branch=label,z=float(zz),log_mass_ratio=float(x),
                                    dimensionless_twice_subtracted_residual=str(residual),
                                    residual_over_reference_rho_DE_by_mass_keV={str(m):float(abs(residual)*(m*1000)**4/(32*mp.pi**2*RHO_DE)) for m in [7.1,16,18,20]}))
    # Maximum M admitting portal and supplied scalar perturbativity cuts, analytically.
    base = portal_boundary(16)
    cuts = []
    for limit in [1., 4*math.pi, 16*math.pi**2/18]:
        maximum = 16*(limit/base['lambda_S'])**(1/15)
        cuts.append(dict(lambda_S_cut_input=limit, maximum_M_keV=maximum,
                         boundary_parent_mS_GeV=portal_boundary(maximum)['m_S_GeV']))
    return dict(status='PASS_STERILE_PARENT_CONDITIONAL_CONSISTENCY_AUDIT',
                input_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS},
                ownership='Nov3 dark_radiative_stability owns CW/subtracted-shape/soft/phase controls. This applies those controls to current Nov6 sterile points and adds a specified radial parent and portal-quartic scaling. No generic CW novelty claimed.',
                reference=dict(Mpl_reduced_eV=MPL,H0_eV=H0,rho_DE_eV4=RHO_DE,b=B,background='Declared numerical reference, not a refit; actual line-drift cp and histories used separately.'),
                parent_hypothesis='Canonical real S, V=lambda_S/4 [S^2-w(phi)^2]^2, w=w0 exp(-b phi/Mpl), mN=y w=y vS/sqrt2. Canonical w=vS/sqrt2 preserves the incoming Majorana width Gamma=y^2*mS/(16pi), as in1609.01289 AppA. Tiny portal and Yukawa corrections ignored. Additional cubic/tadpole potentials or phi-dependent lambda_S can change the radial conclusions.',
                symbolic=symbolic_checks(),incoming_open_points_under_parent_hypothesis=open_rows,
                portal_boundary=[portal_boundary(m) for m in [7.1,15,16,18,20,30]],
                scaling=dict(v_squared='M_N^3/mS',portal_floor='mS^(1/2)',portal_cap='mS/M_N^3',
                             parent_mass_at_portal_boundary='M_N^6',quartic_at_portal_boundary='M_N^15'),
                supplied_perturbativity_cuts=cuts,Majorana_benchmarks=fermion,actual_line_history_subtracted_benchmarks=history,
                prior_Dirac_status=parent['status'],
                RG_scope='Scalar-only one-loop beta_lambda=18 lambda^2/(16pi^2) in V=lambda S^4/4 convention. Pole is a breakdown diagnostic; where beta/lambda >=1 its numerical location is uncontrolled. No actual nonperturbative pole or full UV cutoff is established.',
                Lyalpha_scope='Incoming 15.2/16.8keV numbers match mean momentum to a thermal relic. They are proxies, not a computed transfer function or data likelihood. Koenig-Merle-Totzauer1609.01289 AppC explicitly shows failure of mean/free-streaming classification for nonthermal scalar-decay spectra. Neither a universal7.1keV exclusion nor a precise16-20keV allowed corridor follows.',
                protection_scope='Soft caps reuse equal boson/Majorana determinant cancellation with constant soft mass-squared shift. No common supersymmetric thermal-parent/Higgs-portal/SUGRA completion is supplied. Fine tuning or new symmetries can evade the benchmarks.',
                sources=['https://arxiv.org/abs/hep-ph/0606120','https://arxiv.org/abs/1609.01289',
                         'https://arxiv.org/abs/0911.1120','https://www.damtp.cam.ac.uk/user/tong/sft/sfthtml/S3.html'],
                boundary='Conditional EFT consistency and inherited-method application. No observational exclusion, new data fit, full thermal history or solved TOE.')


if __name__ == '__main__':
    out = build()
    (ROOT/'data/toe_20261106_sterile_parent_consistency.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],flush=True)
    print('open-grid quartics',[(x['M_keV'],x['m_S_GeV'],x['lambda_S']) for x in out['incoming_open_points_under_parent_hypothesis']],flush=True)
    print('conditional cuts',out['supplied_perturbativity_cuts'],flush=True)
