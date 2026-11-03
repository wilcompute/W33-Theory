"""Radiative-stability benchmarks for the recently fitted fading dark sector.

Coleman-Weinberg naturalness is standard (Garny0606120; D'Amico etal1605.00996).
These are declared subtraction/counterterm benchmarks, not data exclusions.
"""
import json,math,pathlib
import mpmath as mp
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]
MPL=2.435e27;HBAR=6.582119569e-16;MPC=3.085677581491367e22

def build():
    x,a=s.symbols('x a',real=True);F=s.exp(-4*a*x)*(2*a*x+s.Rational(3,2))
    deriv=[s.diff(F,x,n).subs(x,0)for n in range(5)]
    assert deriv==[s.Rational(3,2),-4*a,8*a*a,0,-128*a**4]
    # Equal boson/fermion dof; soft mass-squared offset Delta^2 independent of x.
    u,d,m=s.symbols('u d m',positive=True)
    f=lambda z:z*z*(s.log(z/m**2)-s.Rational(3,2))
    soft_linear=s.diff(f(u+d)-f(u),d).subs(d,0).subs(u,m*m*s.exp(-2*a*x))
    assert s.simplify(s.diff(soft_linear,x,2).subs(x,0))==8*a*a*m*m
    phase_mass=s.diag(2*s.exp(s.I*x),3*s.exp(-s.I*x))
    assert s.simplify(phase_mass.conjugate().T*phase_mass)==s.diag(4,9)
    mp.mp.dps=70;rows=[]
    for dataset in ['pantheon','dovekie','desy5']:
        old=json.loads((ROOT/f'analysis/toe_uv/fading_ds_{dataset}.json').read_text())
        for label in ['free_c_neg','free_c_pos']:
            p=old[label];cp=p['cp'];H0=100*p['h']*1000/MPC*HBAR;rho=3*H0**2*MPL**2*p['info']['Ophi0'];g=4
            coeff=g*cp**2/(8*math.pi**2*MPL**2)
            cap=(H0**2/coeff)**.25;treecap=(p['c']**2*rho/MPL**2/coeff)**.25
            excursion=p['info']['phi_rec']-p['info']['phi0'];aa=mp.mpf(str(cp));xx=mp.mpf(str(excursion))
            residual=mp.exp(-4*aa*xx)*(2*aa*xx+mp.mpf('1.5'))-(mp.mpf('1.5')-4*aa*xx+4*aa**2*xx**2)
            assert residual!=0
            subcap=(rho/(g/(64*math.pi**2)*float(abs(residual))))**.25
            scans=[]
            for mass in [1e-22,1e-3,.01,.1,1e3,1e6,1e9]:
                correction=coeff*mass**4
                softcap=math.sqrt(8*math.pi**2/g)*H0*MPL/(cp*mass)
                scans.append(dict(DM_mass_eV=mass,MS_curvature_over_H0_squared=correction/H0**2,
                    excursion_residual_over_dark_energy=g/(64*math.pi**2)*float(abs(residual))*mass**4/rho,
                    allowed_constant_soft_mass_Delta_eV=softcap,small_soft_physical_partner_mass_splitting_eV=softcap**2/(2*mass)))
            rows.append(dict(dataset=dataset,branch=label,c=p['c'],cp=cp,H0_eV=H0,rho_DE_eV4=rho,
                field_excursion_rec_to_present_in_Mpl= -excursion,Dirac_degrees_of_freedom=g,
                MS_no_curvature_cancellation_DM_mass_cap_eV=cap,MS_tree_curvature_comparison_DM_mass_cap_eV=treecap,
                twice_subtracted_excursion_dimensionless_residual=str(residual),twice_subtracted_excursion_DM_mass_cap_eV=subcap,mass_scan=scans))
    return dict(status='PASS_FADING_DARK_SECTOR_RADIATIVE_BENCHMARKS',rows=rows,
        particle_assumption='One4D Dirac dark particle with m(phi)=m0 exp[-cp*(phi-phi0)/Mpl]. Absolute DM mass is NOT specified by the background fit; it is scanned here.',
        scheme='MS-bar at renormalization scale mu=m0; fermion DeltaV=-g*m(phi)^4/(64pi^2)*(log[m(phi)^2/mu^2]-3/2). x=(phi-phi0)/Mpl.',
        shape='DeltaV=(g*m0^4/(64pi^2))*exp(-4cp*x)*(2cp*x+3/2)',
        exact_curvature='Delta m_phi^2=g*cp^2*m0^4/(8pi^2*Mpl^2) at x=0 in this prescription.',
        subtracted_benchmark='Remove DeltaV(0), its slope and curvature by three independent local matching counterterms. Residual starts at quartic here: derivative3(0)=0 and derivative4(0)=-128cp^4. This special cancellation depends on the chosen subtraction scale; it is not a physical symmetry.',
        soft_protected_control='Equal boson/fermion dof and identical masses/couplings cancel their CW functions exactly. If mB^2=mF^2+Delta^2 with constant small Delta^2, the leading curvature is g*cp^2*m0^2*Delta^2/(8pi^2*Mpl^2). Delta is a soft mass parameter; the actual partner splitting is approximately Delta^2/(2*m0).',
        phase_only_protection_tradeoff='For M(phi)=U(phi) M0 V(phi)^dagger with unitary U,V, every singular mass and Tr f(M^dagger M) is constant. The explicit diag(2 exp(ix),3 exp(-ix)) control has squared masses4,9 and no one-loop mass-determinant potential, but physical cprime=-d ln(mass)/dx is0. Rotating a mass phase alone cannot reproduce the fitted fading of a mass magnitude.',
        gravity_soft_connection='If an additional unsequestered supergravity model supplies Delta approximately m_gravitino, the displayed naturalness control requires mDM*m_gravitino <=sqrt(8pi^2/g)*H0*Mpl/cprime. This is conditional on that mediation law. An exact-SUSY cancellation proposal must quantify how its protection survives the SUSY breaking needed for a positive vacuum in ordinary N=1 supergravity.',
        covariance_scope='Uses already-published background parameter certificates only. No new data fit, cosmological likelihood, CMB perturbation calculation or observational mass exclusion.',
        naturalness_scope='Mass caps quantify required cancellation/protection under the declared benchmark. Arbitrary field-dependent counterterms or an explicit protecting UV mechanism can change them; these are not scheme-independent theorems excluding a DM mass.',
        ownership='Pass12547 owns the fading-background fits and Pass12548 the fifth-force/moduli constraints. Quantum radiative constraints are prior physics; this evaluates them on the actual stored branches and supplies exact residual/soft-cancellation controls.',
        source_general='https://arxiv.org/abs/hep-ph/0606120',source_dark='https://arxiv.org/abs/1605.00996',source_finetuning='https://arxiv.org/abs/1812.03184',
        boundary='Unprotected particle EFT benchmark; no derived dark-particle identity, completed string compactification or prediction of the cosmological constant.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261103_dark_radiative_stability.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],[(r['dataset'],r['branch'],round(r['MS_no_curvature_cancellation_DM_mass_cap_eV'],5))for r in d['rows']],flush=True)
