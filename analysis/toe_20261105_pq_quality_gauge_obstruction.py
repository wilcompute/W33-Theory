"""Quality and ordinary gauge-protection tests of the actual PQ-unification A.

Established anomaly/axion methods applied to the declared D+Q+Q inventory.
No general no-go for high-quality N_DW=1 axions: GS, extra matter, new
scalars/nonrenormalizable masses and gauge-origin Wilson lines can evade it.
"""
import itertools,json,math,pathlib
import mpmath as mp
import sympy as s
ROOT=pathlib.Path(__file__).resolve().parents[1]
MPL=2.435e18;CHI=(.0756)**4;THETA=1e-10

def ratio(fa,dimension,canonical=True,coefficient=1.):
    vev=fa/math.sqrt(2)if canonical else fa
    return math.exp(math.log(2*abs(coefficient))+dimension*math.log(vev)-(dimension-4)*math.log(MPL)-math.log(CHI))

def uniform_shift_bound(r,d):
    # U=1-cos(theta)-r*cos(d theta+delta). A global minimum obeys
    # 1-cos(theta)<=2r. Inside that neighborhood U''>=1-(d²+2)r.
    lower=1-(d*d+2)*r
    return d*r/lower if lower>0 and r<.5 else None

def exact_shift(r,d,phase):
    with mp.workdps(75):
        rr=mp.mpf(str(r));dd=mp.mpf(d);p=mp.mpf(str(phase))
        assert rr*(dd*dd+2)<mp.mpf('.5')
        x=mp.findroot(lambda x:mp.sin(x)+dd*rr*mp.sin(dd*x+p),0)
        residual=mp.sin(x)+dd*rr*mp.sin(dd*x+p)
        assert abs(residual)<mp.mpf('1e-65')
        return dict(theta=float(x),stationarity_residual=float(abs(residual)),curvature=float(mp.cos(x)+dd*dd*rr*mp.cos(dd*x+p)))

def anomaly_system():
    d,a,b,z=s.symbols('d a b z')
    matrix=s.Matrix([[s.Rational(1,2),1,1,0],[0,s.Rational(3,2),s.Rational(3,2),1],
                     [s.Rational(1,3),s.Rational(1,6),s.Rational(1,6),-1]])
    ns=matrix.nullspace();assert ns==[s.Matrix([0,-1,1,0])]
    # All SM quark/lepton Yukawa charges under one Higgs, in LH notation.
    q,l,h=s.symbols('q l h');u=-q-h;dc=-q+h;ec=-l+h
    SM3=s.expand((2*q+u+dc)/2);SM2=(3*q+l)/2
    SMYY=s.expand(q/6+4*u/3+dc/3+l/2+ec)
    assert SM3==0 and s.expand(SMYY+SM2)==0
    return matrix,ns,dict(SM_SU3=str(SM3),SM_SU2=str(SM2),SM_Y2=str(SMYY))

def build():
    parents=json.loads((ROOT/'analysis/toe_uv/pq_full_scan.json').read_text())
    rows=parents['rows'];model=[r for r in rows if sorted(tuple(x)for x in r['reps'])==sorted([(3,1,'-1/3'),(3,2,'1/6'),(3,2,'1/6')])]
    assert len(model)==1;signrow=next(x for x in model[0]['signs']if x['q']==[1,1,-1]);assert signrow['NDW']==1
    dw=1+2-2;E=s.Rational(2,3)+s.Rational(10,3)-s.Rational(10,3)
    assert dw==1 and E/dw==s.Rational(2,3)
    quality=[]
    for fa in [2.7e10,5.7e12/60,1e11,2e11,5.7e12/25,1e12]:
        by_convention=[]
        for canonical in [True,False]:
            rr=[]
            for dim in range(5,20):
                r=ratio(fa,dim,canonical);bound=uniform_shift_bound(r,dim)
                checks=[]
                if r*(dim*dim+2)<.5:
                    checks=[dict(phase=phase,**exact_shift(r,dim,phase))for phase in [.7,1.4]]
                    assert all(abs(x['theta'])<=bound*(1+1e-12)for x in checks)
                rr.append(dict(operator_dimension=dim,amplitude_over_QCD=r,uniform_theta_bound=bound,phase_controls=checks))
            allowed=[x['operator_dimension']for x in rr if x['uniform_theta_bound']is not None and x['uniform_theta_bound']<THETA]
            assert allowed
            by_convention.append(dict(canonical_sigma_f_over_sqrt2=canonical,first_sufficient_dimension=min(allowed),rows=rr))
        quality.append(dict(fa_input_GeV=fa,axion_mass_input_relation_ueV=5.7e12/fa,conventions=by_convention))
    # Ordinary exact non-R Z_N, no GS/inflow. Instanton2T normalization is
    # integral: heavy A3_integer=-(s_D+2s_Q1+2s_Q2)*q_sigma=-q_sigma.
    scans=[]
    for N in range(2,65):
        allowed=[qS for qS in range(N)if(-dw*qS)%N==0]
        assert allowed==[0]
        scans.append(dict(N=N,allowed_sigma_charges=allowed))
    M,ns,sm=anomaly_system()
    # Tempting two-scalar assignment: D and Q1 use S(q=2), Q2 uses Tdag(q=-3).
    axial=s.Matrix([-2,-2,3,0]);anoms=M*axial
    assert anoms==s.Matrix([0,s.Rational(3,2),-s.Rational(1,2)])
    return dict(status='PASS_PQ_QUALITY_AND_MINIMAL_GAUGE_PROTECTION_OBSTRUCTIONS',
        model_representation_source='analysis/toe_uv/pq_full_scan.json',left_handed_mass_signs=[1,1,-1],integer_color_anomaly=dw,E_over_N=str(E/dw),
        theta_tolerance_input=THETA,Planck_scale_input_GeV=MPL,QCD_susceptibility_input_GeV4=CHI,
        quality_scan=quality,discrete_modular_controls=scans,continuous_mixed_anomaly_matrix=[[str(x)for x in row]for row in M.tolist()],
        continuous_kernel_basis=[list(map(str,x))for x in ns],SM_one_Higgs_identities=sm,
        two_scalar_attempt=dict(scalar_gauge_charges=[2,3],axial_pair_charges=list(map(int,axial[:3])),SU3_squared_U1=0,SU2_squared_U1='3/2',Y_squared_U1='-1/2',lowest_interlocking_scalar_operator='S^3 (Tdag)^2',operator_dimension=5),
        quality_action='Sigma=(fa+rho)/sqrt(2)*exp(i theta), N_DW=1. DeltaV=-[c Sigma^d/Mpl^(d-4)+h.c.], |c|=1 input. U/chi=1-cos(theta)-r cos(d theta+delta), r=2(fa/sqrt2)^d/[Mpl^(d-4) chi]. Phase delta is generic. Canonical and bare-vev=fa conventions are exported separately; neither coefficient nor operator absence is predicted.',
        exact_bound='Every global minimum satisfies1-cos(theta)<=2r by comparison with theta=0. On that interval Usecond>=1-(d²+2)r. If positive the root is unique there and |theta_min|<=d*r/[1-(d²+2)r], uniformly in delta. Finite high-precision root controls verify two phases. Large-r rows are not assigned a false perturbative small-angle answer.',
        discrete_theorem='With full-rank renormalizable SM quark Yukawas and one Higgs, their determinant charge equations imply2 sum Q+sum uc+sum dc=0 modN. The three heavy Dirac mass terms from Sigma,Sigma,Sigma-dagger imply the integer SU3-instanton Jacobian charge A3=-(1+2-2)qSigma=-qSigma modN. Ordinary anomaly-free non-R ZN therefore requires qSigma=0. Sigma is neutral, so no power Sigma^d is forbidden. This algebra holds for everyN; the2..64 scan is only a control, not the proof.',
        continuous_theorem='Let d,a,b be LH pair-charge sums for D,Q1,Q2 and z the full SM SU2²U1 anomaly. The necessary SU3²,SU2²,Y² anomaly equations have only kernel(d,a,b,z)=(0,-t,t,0). Consequently an ordinary continuous U1 with just this colored inventory and renormalizable single-Higgs SM Yukawas cannot give D an axial charge. If D mass is renormalizably generated by Sigma, Sigma must be neutral. Arbitrarily many SM-singlet neutrinos cannot repair these mixed anomalies.',
        escapes='Green-Schwarz axions or higher-dimensional inflow, extra EW/colored chiral matter, multiple-Higgs or nonrenormalizable SM mass sectors, differently generated heavy masses, and Wilson-line gauge-origin axions change the hypotheses. Explicit high-quality N_DW=1 models exist in the literature, so this is NOT a universal obstruction to axions, discrete gauge protection or strong-CP solutions.',
        prior='Pass12603-12608 owns the unification inventory/signs and flags PQ quality open. Its pq_gates.py uses an order-of-magnitude quality proxy omitting the derivative factor and canonical vev in that proxy; this calculation retains both, without changing its stored results. Pass11949 concerns a different axiflavon loop obstruction. General quality/discrete anomaly methods are established prior physics.',
        sources=['https://arxiv.org/abs/1705.05370','https://arxiv.org/abs/hep-ph/0212339','https://arxiv.org/abs/2412.21157','https://arxiv.org/abs/2607.08814'],
        boundary='Declared operator coefficient/phase and necessary mixed-gauge anomaly tests, not a quantum-gravity prediction, full discrete anomaly classification, experimental exclusion or complete UV model.')

if __name__=='__main__':
    d=build();(ROOT/'data/toe_20261105_pq_quality_gauge_obstruction.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],[(r['axion_mass_input_relation_ueV'],r['conventions'][0]['first_sufficient_dimension'])for r in d['quality_scan']],flush=True)
