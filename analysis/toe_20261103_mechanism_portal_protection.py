"""Global-SUSY protection, then an explicit supersymmetric portal with soft leakage.

The old meV result is a conditional subtraction/naturalness benchmark, not data.
Here the leakage is derived from declared one-loop RG equations, not asserted.
"""
import json, math, pathlib
import mpmath as mp
ROOT=pathlib.Path(__file__).resolve().parents[1]

def running_soft(y, log_ratio, visible_soft_squared):
    """W=y S D Dbar, all gauge-singlets, real constant y, A=0.

    16pi² d m_i²/d ln(mu)=2 y²(mS²+mD²+mDbar²).
    UV: (mS²,mD²,mDbar²)=(visible_soft_squared,0,0).
    These are the specified leading-order constant-Yukawa equations.
    """
    shift=visible_soft_squared*math.expm1(-6*y*y*log_ratio/(16*math.pi**2))/3
    return shift,visible_soft_squared+shift

def cw_curvature(mass, soft_squared, cp, Mpl):
    # A pair of complex scalars vs one Dirac fermion; mu=m(today).
    with mp.workdps(85):
        m,d,c,p=map(mp.mpf,map(str,(mass,soft_squared,cp,Mpl)))
        def V(x):
            u=m*m*mp.exp(-2*c*x); b=u+d
            return (b*b*(mp.log(b/(m*m))-mp.mpf('1.5'))-u*u*(mp.log(u/(m*m))-mp.mpf('1.5')))/(16*mp.pi**2)
        assert m*m+d>0
        return float(mp.diff(V,0,2)/(p*p))

def build():
    parent=json.loads((ROOT/'data/toe_20261103_dark_radiative_stability.json').read_text())
    # Read the actual fit, not a rounded cprime chosen to reproduce the old cap.
    fit=json.loads((ROOT/'analysis/toe_uv/fading_ds_dovekie.json').read_text())['free_c_neg']
    # Older fit JSON may wrap optimizer parameters; export its schema on error.
    if isinstance(fit,dict) and 'cp' not in fit:
        pars=fit.get('params',fit.get('best_fit',fit))
    else:pars=fit
    # Actual schema is inspected in the runner; names are never inferred silently.
    cp=float(pars['cp']) if isinstance(pars,dict) and 'cp'in pars else None
    if cp is None:
        raise ValueError('Unexpected fading fit schema: '+str(fit)[:700])
    h=float(pars['h']); H0=h*100*1000/3.08567758149e22*6.582119569e-16
    Mpl=2.435e27;mass=1e9; visible=1e12;L=10.
    allowed_delta=math.sqrt(2*math.pi**2)*H0*Mpl/(cp*mass)
    ymax=math.sqrt(8*math.pi**2/L)*allowed_delta/visible
    rows=[]
    for y in [0.,ymax/10,ymax,ymax*10,1e-8,1e-3]:
        dark,source=running_soft(y,L,visible**2)
        stable=mass**2+dark>0
        curve=cw_curvature(mass,dark,cp,Mpl) if stable else None
        rows.append(dict(y=y,dark_soft_squared_eV2=dark,source_soft_squared_eV2=source,
            scalar_non_tachyonic=stable,one_loop_curvature_eV2=curve,
            absolute_curvature_over_H0_squared=abs(curve)/H0**2 if stable else None))
    exact_control=[cw_curvature(mass,0,cp,Mpl),cw_curvature(1e3,0,cp,Mpl)]
    assert exact_control==[0.,0.]
    assert abs(rows[2]['absolute_curvature_over_H0_squared']-1)<1e-10
    return dict(status='PASS_EXPLICIT_PORTAL_LEAKAGE_AND_SUSY_CONTROL',
        source_parent_status=parent['status'],input_fit='analysis/toe_uv/fading_ds_dovekie.json:free_c_neg',
        prior_CW_owner='analysis/w33_pass12034_12038_joint_mechanisms.py:radiative_fibre already implements the same complete scalar/Dirac common-soft determinant and exact SUSY cancellation on a DIFFERENT flavor texture, citing11909 and11935. Those methods are prior controls. The new declared S-D-Dbar portal RG solution and derivative of the fading physical mass add a specific leakage calculation, not a new supertrace theorem.',
        cprime=cp,H0_eV=H0,Mpl_eV=Mpl,DM_mass_input_eV=mass,visible_soft_mass_input_eV=visible,
        log_UV_over_IR=L,soft_delta_benchmark_eV=allowed_delta,portal_y_benchmark=ymax,rows=rows,
        exact_SUSY_curvature_controls=exact_control,
        declared_model='Global N=1 SUSY with canonical K and W=m(Phi) D Dbar + M S^2/2 + y S D Dbar. D=Dbar=S=0 and F_Phi=0 define the supersymmetric flat background. A soft scalar mass for S explicitly breaks SUSY. RG runs above the S threshold; log(UV/M)=10 is input. No visible SM embedding is presumed.',
        exact_protection='In the unbroken global-SUSY background, all four bosonic and four fermionic degrees have the same |m(Phi)|: their one-loop determinants cancel pointwise. Perturbative Kahler corrections alone cannot lift an F-flat background. This requires F_Phi=0 and unbroken SUSY, unlike a rolling positive-energy universe.',
        leakage='The declared portal transmits the supplied S soft mass even with zero dark soft masses at the UV boundary. Exact integration of the constant-y one-loop soft RG equations gives mD^2=(mS_UV^2/3)[exp(-6 y^2 L/(16pi^2))-1]. The IR sign is negative; large leakage can be tachyonic. Small-y naturalness uses its absolute value.',
        curvature='At mu=m(today), the small-soft expansion is delta_mPhi^2=cp^2*m^2*mDsoft^2/(2*pi^2*Mpl^2); the high-precision calculation evaluates the full two-complex-scalar minus Dirac determinant rather than subtracting floating nearly equal numbers.',
        boundary='Leading one-loop, constant Yukawa, explicit global-SUSY portal and supplied soft threshold. Gauge effects, A/B terms, y running, anomaly mediation, thermal state and gravity mediation are not included. The portal cap is conditional naturalness, not an experimental limit. This exhibits a possible protection and a concrete failure mechanism; it does not construct realistic sequestering.',
        sources=['https://arxiv.org/abs/hep-ph/9709356','https://arxiv.org/abs/1605.00996','https://arxiv.org/abs/hep-th/0701023'])

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_mechanism_portal_protection.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['portal_y_benchmark'],flush=True)
