"""All28 real modes of a specified softly broken11958 singlet model.

11973 owns the leading Higgsed matching. We solve off its D-flat curve,
include multipliers/spectators, and separately compute the linear
canonical-supergravity multiplier tadpole response. Full E6 is open.
"""
from pathlib import Path
import json
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]


def potential_core(z,soft,g=.1,f0=None):
    if f0 is None:
        rho=mp.mpf(1)/32;d=(2*rho+rho*rho)/12
        f0=mp.sqrt((mp.sqrt(d*d+4)+d)/2)*rho**12
    s1,s2,t1,t2,p,rm,rp=z
    f=[s1*t1-p,2*(s2*t2-p),3*(s1*t2+s2*t1),rm*rp-1,rm*p**12-f0]
    dx=-abs(s1)**2-abs(s2)**2+abs(t1)**2+abs(t2)**2
    dz=abs(t1)**2+abs(t2)**2+abs(p)**2-12*abs(rm)**2+12*abs(rp)**2
    return sum(abs(a)**2 for a in f)+g*g*(dx*dx+dz*dz)/2+sum(a*abs(b)**2 for a,b in zip(soft,z))


def home(r):
    s1,s2,t1,t2,p,rm,rp=r
    return [s1,mp.j*s2,t1,-mp.j*t2,p,rm,rp]


def sugra_potential(z,matched,mg,Lambda,f0,g,auxiliary=False):
    core=z[:7];lag=mp.matrix(z[7:12]);spec=z[12:]
    s1,s2,t1,t2,p,rm,rp=core
    f=mp.matrix([s1*t1-p,2*(s2*t2-p),3*(s1*t2+s2*t1),rm*rp-1,rm*p**12-f0])
    J=mp.matrix([[t1,0,s1,0,-1,0,0],[0,2*t2,0,2*s2,-2,0,0],
                 [3*t2,3*t1,3*s2,3*s1,0,0,0],[0,0,0,0,0,rp,rm],
                 [0,0,0,0,12*rm*p**11,p**12,0]])
    ss=sum(x*x for x in spec)
    ws=sum(lag[i]*f[i] for i in range(5))+rm*p**10*ss/2
    M=mp.mpf('2.435e18');mu2=(M/Lambda)**2;w0=mg*M*M/Lambda**3
    wc=J.T*lag;wc[4]+=5*rm*p**9*ss;wc[5]+=p**10*ss/2
    hol=list(wc)+list(f)+[rm*p**10*x for x in spec]
    cov=[hol[i]+mp.conj(z[i])*(ws+w0)/mu2 for i in range(14)]
    if auxiliary:
        return [-mp.exp(sum(abs(x)**2 for x in z)/(2*mu2))*mp.conj(x) for x in cov]
    # Pinned neutral hidden chiral source contributes3|w0|²/mu².
    # This tunes the constant at z=0 only. No observed CC is derived.
    VF=mp.exp(sum(abs(x)**2 for x in z)/mu2)*(sum(abs(x)**2 for x in cov)-3*(abs(ws+w0)**2-w0*w0)/mu2)
    qx=[-1,-1,1,1,0,0,0]+[0]*7
    qz=[0,0,1,1,1,-12,12]+[-1,-1,-1,0,0,1,1]
    dx=sum(q*abs(x)**2 for q,x in zip(qx,z));dz=sum(q*abs(x)**2 for q,x in zip(qz,z))
    return VF+g*g*(dx*dx+dz*dz)/2+sum(q*abs(x)**2 for q,x in zip(matched,z))


def sugra_home(r):
    return home(r[:7])+[r[7],r[8],mp.j*r[9],r[10],r[11],mp.mpc(0),mp.mpc(0)]


def sugra_solve(start,matched,mg,Lambda,f0,g):
    def V(*r):return sugra_potential(sugra_home(r),matched,mg,Lambda,f0,g)
    def grad(r):return mp.matrix([mp.diff(V,tuple(r),tuple(int(j==i) for j in range(12))) for i in range(12)])
    sol=mp.matrix(start)
    for iteration in range(12):
        gr=grad(sol)
        if max(abs(x) for x in gr)<mp.mpf('1e-85'):break
        Hess=mp.matrix(12)
        for i in range(12):
            for j in range(i,12):Hess[i,j]=Hess[j,i]=mp.diff(V,tuple(sol),tuple(int(k==i)+int(k==j) for k in range(12)))
        step=mp.lu_solve(Hess,-gr)
        assert max(abs(x) for x in step)<mp.mpf('.001')
        sol+=step
    assert max(abs(x) for x in grad(sol))<mp.mpf('1e-85')
    z=sugra_home(sol);point=tuple(mp.re(v) for v in z)+tuple(mp.im(v) for v in z)
    def allV(*x):return sugra_potential([x[i]+mp.j*x[i+14] for i in range(14)],matched,mg,Lambda,f0,g)
    gr=[mp.diff(allV,point,tuple(int(k==i) for k in range(28))) for i in range(28)]
    assert max(abs(x) for x in gr)<mp.mpf('1e-85')
    H=mp.matrix(28)
    for i in range(28):
        for j in range(i,28):H[i,j]=H[j,i]=mp.diff(allV,point,tuple(int(k==i)+int(k==j) for k in range(28)))
    ev,_=mp.eigsy(H);positive=[x for x in ev if x>mp.mpf('1e-60')]
    assert len(positive)==26 and sum(abs(x)<mp.mpf('1e-60') for x in ev)==2
    assert min(ev)>-mp.mpf('1e-60')
    aux=sugra_potential(z,matched,mg,Lambda,f0,g,auxiliary=True)
    ratios=[Lambda*aux[i]/z[i] for i in range(7)]
    phase_max=max(abs(mp.im(x)) for x in ratios);assert phase_max<mp.mpf('1e-80')
    spread=max(abs(ratios[i]-ratios[0]) for i in range(4))
    # Prior11965 transmission B=r*S1/v+i*t*S2/(i v), r.t=1/100.
    # Its soft mixing row has the actual auxiliary logarithmic derivatives.
    # This invariant diagnoses misalignment, not a total colored loop.
    barr_imag=(mp.re(ratios[0])-mp.re(ratios[1]))/100
    return dict(real_coordinates=[mp.nstr(x,60) for x in sol],gradient_max=mp.nstr(max(abs(x) for x in gr),15),
                Newton_iterations=iteration,positive_physical_real_modes=26,gauge_zero_modes=2,
                masses_GeV=[float(Lambda*mp.sqrt(x/2)) for x in positive],
                P_relative_shift=float(mp.re(z[4])/(mp.mpf(1)/32)-1),
                multiplier_VEV_GeV=[mp.nstr(x*Lambda,25) for x in z[7:12]],
                core_auxiliary_F_over_VEV_GeV=[mp.nstr(x,60) for x in ratios],auxiliary_phase_alignment_max=mp.nstr(phase_max,15),
                ST_auxiliary_ratio_spread_GeV=mp.nstr(spread,20),Barr_mixing_Im_B_A_dagger_GeV=mp.nstr(barr_imag,20),
                Barr_scope='Using11965 supplied real rationalr,t with r.t=1/100, B=r+i t and AB=aS1*r+i aS2*t. Im(B AB.dag)=(aS1-aS2)/100. Actual vacuum auxiliary ratios fix this soft misalignment diagnostic; no scalar/gluino loop function or totaltheta evaluated.',
                phase_scope='All7 condensate auxiliaryF/VEV ratios are real on this selected CP-conjugate branch with realW0. This is a tree-level singlet spurion alignment, not a calculation of total radiative theta or colored threshold phases.',
                V_GeV_fourth=mp.nstr(allV(*point)*Lambda**4,25),
                scope='Full canonical-K28-real-singlet SUGRA scalar potential with supplied W0 and a PINNED neutral hidden F source, plus11973 matched masses. All28 visible/singlet gradients and Hessian modes checked. Hidden-sector stabilization is an assumption, other E6 components/colored loops absent; no global vacuum or cosmological constant prediction.')


def payload():
    mp.mp.dps=110;rho=mp.mpf(1)/32;Lambda=mp.mpf('1e16');g=mp.mpf('.1')
    d=(2*rho+rho*rho)/12;u=(mp.sqrt(d*d+4)+d)/2;rm=mp.sqrt(u);rp=1/rm
    F0=rm*rho**12
    old=json.loads((ROOT/'data/w33_pass11973_mediation_transmission.json').read_text())
    mg=mp.mpf(str(old['gravity_scale_GeV']))
    soft=[(mp.mpf(str(m))**2+mg*mg)/Lambda**2 for m in old['soft_masses_GeV']]
    def value(*r):return potential_core(home(r),soft,g,F0)
    def gradient(*r):
        return tuple(mp.diff(value,r,tuple(int(j==i) for j in range(7))) for i in range(7))
    start=(mp.sqrt(rho),)*4+(rho,rm,rp)
    # A gradient-norm line search stalls here: the light displacement is
    # ~1e-9, but its harmless quadratic heavy residual overwhelms the
    # ~1e-42 initial soft gradient. Resolve the stiff normal corrections
    # with undamped high-precision Newton, checking every step is local.
    sol=mp.matrix(start);iterations=0
    for iterations in range(12):
        gr=mp.matrix(gradient(*sol))
        if max(abs(x) for x in gr)<mp.mpf('1e-90'):break
        Hess=mp.matrix(7)
        for i in range(7):
            for j in range(7):Hess[i,j]=mp.diff(lambda *r:gradient(*r)[i],tuple(sol),tuple(int(k==j) for k in range(7)))
        step=mp.lu_solve(Hess,-gr)
        assert max(abs(x) for x in step)<mp.mpf('.001')
        sol+=step
    residual=max(abs(x) for x in gradient(*sol));assert residual<mp.mpf('1e-90')
    z=home(sol);s1,s2,t1,t2,p,rm,rp=z
    point=tuple(mp.re(v) for v in z)+tuple(mp.im(v) for v in z)
    def vc(*x):return potential_core([x[i]+mp.j*x[i+7] for i in range(7)],soft,g,F0)
    full_gradient=[mp.diff(vc,point,tuple(int(k==i) for k in range(14))) for i in range(14)]
    assert max(abs(x) for x in full_gradient)<mp.mpf('1e-90')
    H=mp.matrix(14)
    for i in range(14):
        for j in range(i,14):
            order=tuple(int(k==i)+int(k==j) for k in range(14))
            H[i,j]=H[j,i]=mp.diff(vc,point,order)
    ev,_=mp.eigsy(H)
    positive=[x for x in ev if x>mp.mpf('1e-65')]
    zero=[x for x in ev if abs(x)<=mp.mpf('1e-65')]
    assert len(positive)==12 and len(zero)==2 and min(ev)>-mp.mpf('1e-65')
    J=mp.matrix([[t1,0,s1,0,-1,0,0],
                 [0,2*t2,0,2*s2,-2,0,0],
                 [3*t2,3*t1,3*s2,3*s1,0,0,0],
                 [0,0,0,0,0,rp,rm],
                 [0,0,0,0,12*rm*p**11,p**12,0]])
    dz=abs(t1)**2+abs(t2)**2+abs(p)**2-12*abs(rm)**2+12*abs(rp)**2
    dx=-abs(s1)**2-abs(s2)**2+abs(t1)**2+abs(t2)**2
    lag_soft=[soft[4]]*3+[(mg/Lambda)**2]*2
    K=J.conjugate()*J.T
    for i in range(5):K[i,i]+=lag_soft[i]+(-g*g*dz if i<3 else 0)
    el,_=mp.eighe(K);assert min(el)>0
    # Two chargeZ=+1 spectator superpotential masses rm*p^10.
    spectator2=abs(rm*p**10)**2+g*g*dz+soft[4]
    assert spectator2>0
    mass_core=[Lambda*mp.sqrt(x/2) for x in positive]
    mass_lag=[Lambda*mp.sqrt(x) for x in el]
    # Canonical SUGRA constant-W0 cross term is mg*(sum z dW-3W)+h.c.
    # At the SUSY home W=0. The coefficients below are not guessed
    # universal A terms: they are the degree-weighted actual polynomials.
    source=mp.matrix([rho,2*rho,0,2,13*F0])*mg*Lambda**2
    induced=-(K*Lambda**2)**-1*source.conjugate()
    ratios=[abs(x)/Lambda for x in induced]
    z0=mp.matrix(home(start));S1,S2,T1,T2,P,RM,RP=z0
    J0=mp.matrix([[T1,0,S1,0,-1,0,0],[0,2*T2,0,2*S2,-2,0,0],
                  [3*T2,3*T1,3*S2,3*S1,0,0,0],[0,0,0,0,0,RP,RM],
                  [0,0,0,0,12*RM*P**11,P**12,0]])
    for charge in ([-1,-1,1,1,0,0,0],[0,0,1,1,1,-12,12]):
        tangent=mp.matrix([q*x for q,x in zip(charge,z0)])
        assert max(abs(x) for x in J0*tangent)<mp.mpf('1e-100')
        assert abs(sum(q*abs(x)**2 for q,x in zip(charge,z0)))<mp.mpf('1e-100')
    linear_lambda=-(J0.conjugate()*J0.T)**-1*(J0*z0).conjugate()*mg
    linear_condensate_F=Lambda*(J0.T*linear_lambda+mg*z0.conjugate())
    shielding=max(abs(x) for x in linear_condensate_F)
    assert shielding<mp.mpf('1e-65')
    matched=[soft[i]-(mg/Lambda)**2 for i in range(7)]+[soft[4]-(mg/Lambda)**2]*3+[mp.mpf(0)]*2+[soft[4]-(mg/Lambda)**2]*2
    sugra=sugra_solve(list(sol)+[mp.re(induced[0]/Lambda),mp.re(induced[1]/Lambda),mp.im(induced[2]/Lambda),mp.re(induced[3]/Lambda),mp.re(induced[4]/Lambda)],matched,mg,Lambda,F0,g)
    # It is only linear response to this separate source; it was NOT
    # included in the pure mass-soft stationary point/Hessian above.
    return dict(status='PASS',precision_digits=110,fields='Seven charged condensates, five constraint multipliers, two charged spectators:14complex/28real. All masses below refer only to this declared singlet sector.',
        superpotential='sum_{A=1}^5 lambda_A f_A(z) +1/2 PhiMinus P^10 (spectator1²+spectator2²), in cutoff units. f=(S1T1-P,2(S2T2-P),3(S1T2+S2T1),PhiMinus PhiPlus-1,PhiMinus P^12-F0).',
        soft_model='11973 matched charge-dependent positive masses plus supplied universal positive mg², with mg=F/(sqrt3 MPlanck). A terms and tadpoles ZERO in this solved model. X/Z gauge couplings.1, canonical K. Multipliers/spectators0 is exact stationary by their parity/quadratic structure.',
        selected_real_coordinates=[mp.nstr(x,70) for x in sol],radial_P_relative_shift=float(mp.re(p)/rho-1),
        full_gradient_max_cutoff_units=mp.nstr(max(abs(x) for x in full_gradient),12),Newton_iterations=iterations,D_X=mp.nstr(dx,30),D_Z=mp.nstr(dz,30),
        positive_core_real_modes=12,gauge_phase_zero_modes=2,positive_multiplier_real_modes=10,positive_spectator_real_modes=4,
        total_positive_physical_real_modes=26,core_masses_GeV=[float(x) for x in mass_core],
        multiplier_complex_masses_GeV=[float(x) for x in mass_lag],spectator_mass_GeV=float(Lambda*mp.sqrt(spectator2)),
        SUGRA_linear_source_GeV_cubed=[mp.nstr(x,25) for x in source],
        SUGRA_linear_multiplier_VEV_GeV=[mp.nstr(x,25) for x in induced],max_linear_multiplier_VEV_over_cutoff=float(max(ratios)),
        first_order_condensate_F_shielding_GeV_squared=mp.nstr(shielding,20),
        first_order_shielding_argument='At the SUSY home, rankJ=5 and kerJ is the two gauge tangents q*z. Canonical-K W0 adds mg*z.conj to DWcore. Dflatness says z.conj is orthogonal to the conjugated gauge kernel, hence lies in Im(J.T). The multiplier solution cancels every condensate DWcore at FIRST ORDER in mg. Multiplier auxiliaryF and higher-order backreaction are not cancelled; the full SUGRA root above checks them. Standard heavy-field readjustment, applied to this named branch, not a general strongCP theorem.',
        canonical_pinned_hidden_SUGRA=sugra,
        SUGRA_boundary='The canonical W0 tadpole is NOT zero despite W=F=0 at the unperturbed home. After linear response, the separate canonical pinned-hidden SUGRA model is solved including these sources and all28-field backreaction. Hidden-sector stabilization/K and physical CC matching remain additional data.',
        strong_CP_boundary='Real parameters retain CP-conjugate branches; the solved home keeps P/Phi real. No total radiative theta computed: colored scalar/gaugino soft matrices and their threshold vertices are not specified by this singlet model. Do not infer loop safety from scalar Hessian positivity.',
        scope='Full28-real-mode local vacua of specified soft-mass-only and canonical pinned-hidden SUGRA singlet potentials. Not global minimum, full E6/hidden-sector vacuum, observed CC or radiative strongCP solution.',
        prior=['11958 exact singlet branch','11966 canonical small mass','11973 Higgsed matching'],
        primary='https://arxiv.org/abs/hep-ph/9709356')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11978_full_singlet_soft_vacuum.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['radial_P_relative_shift'],min(d['core_masses_GeV']),d['max_linear_multiplier_VEV_over_cutoff'])
