"""Conditional controls of the existing PQ benchmark, not a full RGE fit.

Keep the parent's simplified beta functions fixed to isolate its explicit
sigma=f/sqrt(2) mass-normalization inconsistency. Also test whether the
micron dark-dimension and high-scale unification proposals share a controlled
5D gravity EFT. No quantum-gravity completion is excluded.
"""
import json, math, pathlib
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT=pathlib.Path(__file__).resolve().parents[1]
MQ=27279937181.61975
MU=3964835648946381.
M4=2.435e18
HBARC=1.973269804e-16
K=1/(16*math.pi**2)

def inverse_y_squared(f,y,scale=MU):
    """Independent exact solution of the parent's Yukawa Riccati equation."""
    B=11/(6*math.pi);p=24/11
    A=1/.118+7*(math.log(MQ)-math.log(91.19))/(2*math.pi)
    a0=A+B*math.log(f/MQ);a1=A+B*math.log(scale/MQ)
    integral=(a1**(1-p)-a0**(1-p))/(B*(1-p))
    return (a1/a0)**p/y**2-36*K*a1**p*integral

def rhs(t,v):
    lam,y=v
    tx=math.log(MQ)
    ia=1/.118+7*(tx-math.log(91.19))/(2*math.pi)+(11/3)*(t-tx)/(2*math.pi)
    g3sq=4*math.pi/ia
    return [K*(20*lam*lam+60*lam*y*y-30*y**4),K*y*(18*y*y-8*g3sq)]

def trajectory(f,y,lam,rtol=2e-9):
    def negative(t,v): return v[0]
    negative.terminal=True;negative.direction=-1
    def perturbative(t,v): return min(4*math.pi-v[0],4*math.pi-v[1]**2)
    perturbative.terminal=True;perturbative.direction=-1
    if y*y>=4*math.pi or lam>=4*math.pi:
        return dict(classification='initial_perturbativity_cut',solver_success=True,reaches_MU=False)
    sol=solve_ivp(rhs,(math.log(f),math.log(MU)),[lam,y],events=[negative,perturbative],rtol=rtol,atol=1e-12,max_step=.12)
    reaches=bool(sol.success and abs(sol.t[-1]-math.log(MU))<1e-8)
    kind='full_positive_perturbative'if reaches else 'quartic_negative'if len(sol.t_events[0])else 'perturbativity_cut'if len(sol.t_events[1])else 'solver_failure'
    return dict(classification=kind,solver_success=bool(sol.success),reaches_MU=reaches,
                end_scale_GeV=math.exp(sol.t[-1]),end_lambda=float(sol.y[0,-1]),end_y=float(sol.y[1,-1]),steps=len(sol.t))

def critical(f,y):
    # A too-large lambda can hit a pole while staying positive: positivity of
    # the returned samples alone is NOT successful integration to M_U.
    lo,hi=1e-10,4*math.pi*(1-1e-10)
    initial=trajectory(f,y,lo)
    if initial['reaches_MU']:return dict(lambda_initial=lo,trajectory=initial,lower_floor=True)
    if initial['classification']!='quartic_negative':return dict(lambda_initial=None,reason=initial)
    for _ in range(48):
        mid=math.sqrt(lo*hi)
        out=trajectory(f,y,mid)
        if out['classification']=='quartic_negative':lo=mid
        else:hi=mid
    # Shift slightly above the numerical separatrix and validate independently
    # with tighter tolerance. A failure is retained, never called stability.
    lam=hi*(1+2e-6)+1e-10
    check=trajectory(f,y,lam,rtol=2e-10)
    return dict(lambda_initial=lam if check['reaches_MU']else None,
                tested_lambda_initial=lam,trajectory=check,lower_floor=False)

def cutoff_rows():
    rows=[]
    for Rmicron in [8.,10.,15.]:
        radius=Rmicron*1e-6/HBARC
        for factor,label in [(math.pi,'interval_pi_R'),(2*math.pi,'circle_2pi_R')]:
            length=factor*radius
            m5=(M4*M4/length)**(1/3)
            fa=1e11
            g4=1/(fa*length)
            rows.append(dict(radius_input_micron=Rmicron,length_convention=label,L_GeV_inverse=length,
                M5_GeV=m5,MQ_over_M5=MQ/m5,MU_over_M5=MU/m5,
                axion_fa_input_GeV=fa,Wilson_line_g4_required=g4,
                dimensional_reduction_residual=(m5**3*length/M4**2)-1))
    return rows

def stretched_string_controls():
    # Apply2409.01405's necessary order-of-magnitude inequalities to the
    # *repo* R and MU. Unknown tension factors are explicit, not hidden.
    rows=[]
    for c in cutoff_rows():
        for kk in [1e3,1e4]:
            m5=c['M5_GeV'];ratio=MU*kk/m5**2
            factor=math.pi if c['length_convention']=='interval_pi_R'else 2*math.pi
            max_radius=HBARC*M4**2/(MU*kk)**1.5/factor/1e-6
            rows.append(dict(radius_input_micron=c['radius_input_micron'],length_convention=c['length_convention'],
                gauge_KK_lower_bound_input_GeV=kk,MV_identified_with_MU_GeV=MU,
                MV_upper_if_tension_at_M5_squared_GeV=m5*m5/kk,
                required_tension_over_M5_squared=ratio,
                max_radius_micron_if_unit_tension_factor=max_radius,
                allowed_tension_factors={str(k):bool(k>=ratio)for k in [1,10,100,1000]}))
    return rows

def build():
    rows=[]
    for f in [1.5e10,2.7e10,5e10,1e11,2e11,5e11,1e12]:
        conventions=[]
        for canonical in [False,True]:
            y=MQ/f*(math.sqrt(2)if canonical else 1)
            c=critical(f,y)
            if c['lambda_initial']is not None:c['radial_mass_GeV']=math.sqrt(2*c['lambda_initial'])*f
            conventions.append(dict(canonical_sigma_f_over_sqrt2=canonical,y_initial=y,**c))
        rows.append(dict(f_input_GeV=f,ma_input_ueV=5.7e12/f,threshold_decoupling_uncontrolled=f<MQ,conventions=conventions))
    upper=trajectory(2.7e10,MQ/2.7e10,2.)
    assert upper['classification']=='perturbativity_cut'and not upper['reaches_MU']
    assert all(abs(x['dimensional_reduction_residual'])<1e-13 for x in cutoff_rows())
    yukawa_bounds=[]
    for canonical in [False,True]:
        factor=math.sqrt(2)if canonical else 1
        fcut=brentq(lambda f:inverse_y_squared(f,factor*MQ/f)-1/(4*math.pi),MQ,1e12,xtol=.001)
        yukawa_bounds.append(dict(canonical_sigma_f_over_sqrt2=canonical,
            minimum_f_for_y_squared_below_4pi_GeV=fcut,
            necessary_ma_upper_ueV=5.7e12/fcut,
            inverse_y_squared_at_MU=inverse_y_squared(fcut,factor*MQ/fcut)))
    for x in rows:
        for c in x['conventions']:
            if c['lambda_initial']is not None:
                exact=inverse_y_squared(x['f_input_GeV'],c['y_initial'])
                assert abs(1/c['trajectory']['end_y']**2-exact)<2e-6*max(1,abs(exact))
    return dict(status='PASS_CANONICAL_NORMALIZATION_AND_CONDITIONAL_CUTOFF_CONTROLS',
        physical_MQ_input_GeV=MQ,physical_MU_input_GeV=MU,stability=rows,
        positive_but_incomplete_flow_control=upper,gravity_cutoffs=cutoff_rows(),
        stretched_GUT_string_controls=stretched_string_controls(),
        stretched_string_hypotheses='Apply the order-of-magnitude proposal2409.01405: MV=T*LX, T<=cT*M5², LX<=Lg, and Lg<=1/KKmin. Then cT>=MV*KKmin/M5². Set MV=the repo fitted MU as an additional hypothesis, KKmin1or10TeV as illustrative localization-bound inputs, and export cT sensitivity. No exact black-string prefactor or experimental likelihood is computed; cT is not a measured number. This diagnoses the cost of this particular proposed UV repair, not a theorem excluding all high-scale gauge sectors.',
        exact_parent_Yukawa_perturbativity_bounds=yukawa_bounds,
        Yukawa_analytic_control='Set z=1/y². The supplied beta becomes zprime=16K*g3²*z-36K. With inverse alpha3=a(t)=a0+B(t-t0), B=11/(6pi), exact z(t)=[a(t)/a0]^(24/11)z0-36K*a(t)^(24/11)*integral(a(s)^(-24/11)ds). This independently checks numerical trajectories and exposes pole/perturbativity failure regardless of quartic. It is only the parent beta system, not a complete EW/Yukawa model or universal axion bound.',
        equations='Parent simplified one-loop beta functions retained: 16pi² beta_lambda=20lambda²+60lambda*y²-30y⁴, 16pi² beta_y=y(18y²-8g3²), portals and sterile Yukawas set0. Parent canonical Sigma=(f+rho)/sqrt2 exp(ia/f), M_Q=yf/sqrt2, m_rho=sqrt(2lambda)f. Therefore y=sqrt2*M_Q/f, not M_Q/f. Gauge threshold held at the same physical M_Q in both convention runs.',
        perturbativity='Declared diagnostic lambda<4pi and y²<4pi; stricter criteria change the domain. Integration must succeed and reach MU with positive lambda. A positive solver prefix ending at a pole/cut is not evidence of UV stability.',
        RGE_scope='Controlled normalization comparison within the parent approximate beta system, not a complete mass-dependent multi-loop SMASH calculation. Common y is a boundary input, not equality protected against EW running. f<MQ rows flag the missing decoupling treatment. No unique axion ceiling or measured instability scale inferred.',
        gravity_equations='For a flat factorizable five-dimensional Einstein term, M4_reduced²=M5³ L. R and interval/circle length conventions are exported. This is the characteristic 5D gravity scale up to UV factors, not a precision hard cutoff. The KK species scaling Lambda³~M4²/R agrees parametrically.',
        shared_EFT_boundary='If the micron dark dimension and high-scale PQ/unification benchmark inhabit this same ordinary 5D gravity EFT, their MQ and MU exceed its gravity scale. The existing 4D perturbative gauge calculation alone is not a controlled common UV completion. Brane localization does not prove gravitational UV corrections vanish. A separate compact dimension, modified Planck relation, or explicit UV completion changes this conditional conclusion.',
        Wilson_line_scope='For the gauge-origin interval axion in2607.08814, f=1/(g5 sqrtL) and g4=g5/sqrtL imply g4=1/(fL). Using the micron dimension therefore requires the exported very small g4, an additional input. Its Wilson-line axion has no scalar PQ radial mode; the old scalar threshold-stabilization model cannot be imported unchanged.',
        prior_owners=['analysis/toe_uv/pq_gates.py','analysis/toe_uv/pq_twoloop.json','analysis/PASS12603_12608_PQ_ASSISTED_UNIFICATION.md','analysis/PASS12609_12611_PQ_TESTS.md','analysis/PASS12563_12570_STABILISED_TOWER.md','analysis/toe_uv/hw_wall_radius.py','analysis/toe_uv/hw_wall_radius.json'],
        cutoff_priority='The hw_wall_radius producer/certificate in12593 already owns the M5 value265054293.94261003GeV for R10micron and L=2piR. This reproduces that value and tests its compatibility with the later12603 MQ/MU benchmark; it is not a new Planck-scale law.',
        literature=['https://arxiv.org/abs/2607.08814','https://arxiv.org/abs/1203.0237','https://arxiv.org/abs/hep-ph/9803315','https://arxiv.org/abs/2409.01405'],
        boundary='Neither an axion exclusion nor a general TOE no-go. This exposes extra protection/normalization/UV assumptions that need a shared action.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261105_pq_normalization_cutoff.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],flush=True)
    for x in d['stability']:print(x['f_input_GeV'],[(z['canonical_sigma_f_over_sqrt2'],z['lambda_initial'],z.get('radial_mass_GeV'))for z in x['conventions']],flush=True)
    print('M5_range',min(x['M5_GeV']for x in d['gravity_cutoffs']),max(x['M5_GeV']for x in d['gravity_cutoffs']),flush=True)
