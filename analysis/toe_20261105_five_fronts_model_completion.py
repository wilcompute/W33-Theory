"""Concrete completion attempts; each retains its independent assumptions.

An anomaly-free two-scalar PQ variant, matrix-derived one-loop Yukawa
control, coupled step-threshold running of the original inventory, and
a warped gravity repair test. These are not one complete UV theory.
"""
import pathlib,json,math,itertools
import numpy as np
from fractions import Fraction as F
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
R=pathlib.Path(__file__).resolve().parents[1];K=1/(16*math.pi**2)
MQ=27279937181.61975;MU=3964835648946381.;MP=2.435e18

def complete_SU5_protection_obstruction():
    # Invariant traces on every SU5 irrep are proportional to these Cartans.
    Y=[F(-1,3)]*3+[F(1,2)]*2
    C=[F(1,2),F(-1,2),0,0,0];W=[0,0,0,F(1,2),F(-1,2)]
    reps={'5':[(i,)for i in range(5)],'10':list(itertools.combinations(range(5),2))}
    rows=[]
    for name,weights in reps.items():
        yy=sum(sum(Y[i]for i in weight)**2 for weight in weights)
        cc=sum(sum(C[i]for i in weight)**2 for weight in weights)
        ww=sum(sum(W[i]for i in weight)**2 for weight in weights)
        assert yy+ww-F(8,3)*cc==0
        rows.append(dict(irrep=name,TrY2=str(yy),SU3_index=str(cc),SU2_index=str(ww)))
    vals=[]
    for gen in [Y,C,W]:vals.append(sum((gen[i]-gen[j])**2 for i in range(5)for j in range(5)if i!=j))
    assert vals[0]+vals[2]-F(8,3)*vals[1]==0
    rows.append(dict(irrep='24',TrY2=str(vals[0]),SU3_index=str(vals[1]),SU2_index=str(vals[2])))
    return dict(exact_trace_controls=rows,old_candidate_C_per_qSigma=1,
        theorem='Define C=A_Y²X+A_SU2²X-(8/3)A_SU3²X. Any complete SU5 representation with a common X charge has C0: the unique invariant trace gives A_SU2=A_SU3 and A_Y²=(5/3)A_SU3. This holds for arbitrary representations, not just5,10,24. One-Higgs full-rank renormalizable SM Yukawas give C_SM0. For original D+Q+Q pair sums(d,a,b)=(-qSigma,-qSigma,+qSigma), C=-(d+a+b)=qSigma. Therefore any number of extra complete SU5 multiplets whose X commutes with SU5 cannot repair ordinary anomaly cancellation with qSigma nonzero under these hypotheses.',
        hypotheses='No GS/inflow. SM mass-sector assumptions unchanged; heavy original signs and renormalizable masses unchanged. Additional X is uniform across each complete SU5 representation. Split X charges, incomplete representations, changed mass operators or SM Yukawa sector evade the statement.',
        scope='A specific original-inventory repair obstruction, not a no-go for unification or protected axions. Invariant trace identities and complete-multiplet beta universality are established group theory. Connects the prior mixed-anomaly theorem to the incoming SU5/orbifold completion question.')

def protected_variant():
    rows=[]
    for n in range(2,41):
        # Integer charges: S2,T2n; n D pairs(-1,-1), one D(+n,+n).
        # 3n singlet pairs(+1,+1), three singlet pairs(-n,-n).
        fields=[(3,-1,n*2),(3,n,2),(1,1,6*n),(1,-n,6)]
        grav=sum(dim*q*count for dim,q,count in fields)
        cubic=sum(dim*q**3*count for dim,q,count in fields)
        assert grav==cubic==0
        assert -n+n==0 # SU3 and Y²X pair-sum, all colored reps identical.
        fa=1e11;F=fa*math.sqrt(n*n+1);dim=n+1
        r=math.exp(math.log(2)+dim*math.log(F/math.sqrt(2))-(dim-4)*math.log(MP)-4*math.log(.0756))
        # The gauge-invariant phase is psi=n thetaS-thetaT, not d theta.
        bound=r/(1-3*r)if r<1/3 else None
        db=np.array([4/15,0,2/3])*(n+1)
        ai=np.array([59.0,29.6,1/.118]);b=np.array([4.1,-19/6,-7.])
        threshold=F/math.sqrt(2);ix=ai-b/(2*math.pi)*math.log(threshold/91.19)
        t=2*math.pi*(ix[0]-ix[1])/((b+db)[0]-(b+db)[1])
        cross=ix-(b+db)*t/(2*math.pi)
        rows.append(dict(n=n,colored_Dirac_pairs=n+1,singlet_Dirac_pairs=3*n+3,
            scalar_X_charges=[2,2*n],gravitational_anomaly=grav,cubic_X_anomaly=cubic,
            fa_input_GeV=fa,equal_scalar_f_input_GeV=F,leading_scalar_operator_dimension=dim,
            leading_operator='S^n Tdag',phase_uniform_theta_bound=bound,
            sufficient_quality=bound is not None and bound<1e-10,
            gauge_delta_b=db.tolist(),one_loop_12_cross_scale_GeV=threshold*math.exp(t),
            third_inverse_coupling_mismatch_at_12=float(cross[2]-cross[0])))
    first=next(x for x in rows if x['sufficient_quality'])
    n=first['n'];bX=8*n*(n+1)+4*(1+n*n)/3
    first['X_gauge_beta_coefficient']=bX
    first['X_gauge_max_initial_coupling_for_no_formal_pole_before_MU']=math.sqrt(8*math.pi**2/(bX*math.log(MU/(first['equal_scalar_f_input_GeV']/math.sqrt(2)))))
    first['X_gauge_log10_pole_over_threshold']={str(g):8*math.pi**2/(bX*g*g)/math.log(10)for g in [.01,.03,.1]}
    return dict(rows=rows,first_quality_row=first,NDW=1,E_over_N='2/3',
        action='n copies S D Dbar + Tdag Dprime Dprimebar;3n copies Sdag N Nbar +3copies T Nprime Nprimebar. D=(3,1,-1/3). LH pair X charges(-1,-1),(n,n),(1,1),(-n,-n); scalars S2,T2n. SM fields X0. All listed mass terms renormalizable. Potential includes radial masses, self/portal quartics and gauge-allowed high-dimensional S^n Tdag; coefficients supplied.',
        anomaly_proof='Colored SU3²X and Y²X cancel between n and1 pairs; YX² cancels within each vectorlike SM pair; no new SU2 doublets. Singlet partners cancel X³ and gravity exactly. psi=n thetaS-thetaT is gauge invariant; QCD couples to psi once. After quotient by the gauge orbit the physical phase has period2pi, NDW1. Residual gauge Z2 acts trivially on scalar phases, not a second physical wall.',
        quality_scope='Equal vevs and coefficient1 are inputs. fa=FS FT/sqrt(n²FT²+FS²); for FS=FT=F, F=fa sqrt(n²+1). Leading pure scalar phase-breaking invariant has degree n+1. Mixed fermion operators, stable relics, cosmology and vacuum stability are NOT certified by this scalar check.',
        extra_relic_and_gauge_controls='With scalar charges2,2n a gauge Z2 survives. At odd n all new fermions are odd while SM fields are even: ordinary heavy-SM mixing is forbidden and the lightest odd state is stable. A gauge-invariant dimension6 operator (D N)(uc ec) has total X=-1+1=0 and Y=-1/3-2/3+1=0 and can permit colored decays only with appropriate spectrum and Wilson coefficient. No relic abundance/lifetime inferred. Tr(YX)=0 within the paired hypercharges, so one-loop kinetic mixing vanishes. The large positive bX=(2/3)sum_Weyl dim X²+(1/3)sum_complex X² is exported with a common-threshold formal Landau bound, not a full threshold evolution of the new protection model.',
        cost='This replaces D+2Q; it does not evade the unchanged-inventory theorem. The extra D multiplets do not reproduce its unification fit. The printed mismatch is a necessary one-loop screen with one common assumed Yukawa1 threshold, not a multi-threshold fit.',
        prior='Gauged two-scalar accidental PQ methods are established;2412.21157 and2609.01712. This specific transparent mirror-singlet variant is a control, no priority claim.')

def tensor_yukawa_control():
    dims=[3,6,6];ys=[.21,.32,.43];sign=[1,1,-1];N=2*sum(dims)
    Y=[np.zeros((N,N),complex)for _ in range(2)];off=0
    for d,y,sg in zip(dims,ys,sign):
        for j in range(d):
            a=off+2*j;b=a+1
            Y[0][a,b]=Y[0][b,a]=y/math.sqrt(2)
            Y[1][a,b]=Y[1][b,a]=1j*sg*y/math.sqrt(2)
        off+=2*d
    Y2=sum(z.conj().T@z for z in Y);beta=[]
    for A in Y:
        B=(Y2.T@A+A@Y2)/2+2*sum(z@A.conj().T@z for z in Y)
        B+=sum(z*np.trace((z.conj().T@A+A.conj().T@z)/2)for z in Y)
        beta.append(B)
    expected=[];observed=[];off=0;trace=sum(d*y*y for d,y in zip(dims,ys))
    for d,y in zip(dims,ys):
        expected.append(y*(y*y+trace));observed.append(float((math.sqrt(2)*beta[0][off,off+1]).real));off+=2*d
    assert np.max(abs(np.array(expected)-observed))<1e-14
    return dict(expected=expected,actual_real_scalar_tensor_beta=observed,
        common_y_cubic_coefficient_D15=16,old_parent_coefficient=18,single_color_triplet_coefficient=4,
        equation='16pi² beta_yi=yi[yi²+sum_j Dj yj²-6 sum_a Ca(i)ga²] for disjoint Dirac pairs coupled to one complex scalar. Real scalar Yukawa matrices explicitly implement sigma and sigma-dagger signs. Formula:1/2(Y2F^T Ya+Ya Y2F)+2Yb Ya†Yb+Yb Tr[(Yb†Ya+Ya†Yb)/2]-3g²{C,Ya}.',
        boundary='One-loop tensor identity for specified interactions, not all allowed SM-mixing Yukawas or higher-loop equations. Fermion wavefunction term gives1, scalar trace givesD; the parent D+3 is not inherited.')

def running(f,lamS,delta,split=(1.,1.,1.)):
    masses=MQ*np.array(split);mr=math.sqrt(2*lamS)*f;portal=math.sqrt(4*lamS*delta)
    if mr>=min(masses):
        return dict(f_input_GeV=f,lambdaS_at_radial_threshold=lamS,delta_lambdaH=delta,split=list(split),radial_mass_GeV=mr,
            reaches_MU=False,termination='UNSUPPORTED_RADIAL_FERMION_ORDER_NEEDS_BROKEN_PHASE_MATCHING',
            min_lambdaH_sampled=None,min_lambdaS_above_activation_sampled=None,final_state=None,threshold_events=[],
            reason='A colored fermion activates below the radial scalar. Full complex-scalar Yukawa beta functions are not a consistent EFT there. Broken-phase axion/mass operators and matching are required. This row is rejected before integration, not assigned a false stability result.')
    # gY,g2,g3,yt,lambdaH,lambdaS,lambdaHS,yD,yQ1,yQ2.
    v=np.array([.3583,.6478,1.1666,.936,.126,0.,0.,0.,0.,0.]);active=np.zeros(3,bool);scalar=False
    thresholds=sorted([(mr,'scalar',None)]+[(m,'fermion',i)for i,m in enumerate(masses)]+[(MU,'end',None)])
    allv=[];events=[];start=173.;success=True;reason='reached_MU'
    for stop,kind,i in thresholds:
        def beta(t,v):
            gY,g2,g3,yt,h,l,p=v[:7];y=v[7:];d=np.array([3,6,6]);T=float(np.dot(d,y*y))
            b=np.array([41/6,-19/6,-7.])+np.array([[4/9,0,2/3],[2/9,2,4/3],[2/9,2,4/3]]).T@active
            out=np.zeros(10);out[:3]=K*b*v[:3]**3
            out[3]=K*yt*(4.5*yt*yt-17/12*gY*gY-9/4*g2*g2-8*g3*g3)
            out[4]=K*(24*h*h+p*p+12*h*yt*yt-6*yt**4-h*(9*g2*g2+3*gY*gY)+3/8*(2*g2**4+(g2*g2+gY*gY)**2))
            if scalar:
                out[5]=K*(20*l*l+2*p*p+4*l*T-2*np.dot(d,y**4))
                out[6]=K*p*(12*h+8*l+4*p+6*yt*yt+2*T-4.5*g2*g2-1.5*gY*gY)
            gauge=8*g3*g3+np.array([0.,4.5,4.5])*g2*g2+np.array([2/3,1/6,1/6])*gY*gY
            out[7:]=K*y*(y*y+T-gauge)*active
            return out
        def cut(t,v):return 4*math.pi-max(np.max(v[:4]**2),np.max(abs(v[4:7])),np.max(v[7:]**2))
        cut.terminal=True;cut.direction=-1
        sol=solve_ivp(beta,(math.log(start),math.log(stop)),v,rtol=2e-8,atol=1e-11,max_step=.15,events=cut)
        allv.extend(sol.y.T.tolist());v=sol.y[:,-1]
        if not sol.success or sol.t[-1]<math.log(stop)-1e-8:success=False;reason='perturbativity_cut_or_solver_failure';break
        if kind=='scalar':
            scalar=True;v[4]+=delta;v[5]=lamS;v[6]=portal
        elif kind=='fermion':active[i]=True;v[7+i]=math.sqrt(2)*masses[i]/f
        events.append(dict(scale_GeV=float(stop),event=kind,species=i,state_after=v.tolist()));start=stop
    A=np.array(allv)
    return dict(f_input_GeV=f,lambdaS_at_radial_threshold=lamS,delta_lambdaH=delta,split=list(split),
        radial_mass_GeV=mr,tree_portal_at_threshold=portal,reaches_MU=success,termination=reason,
        min_lambdaH_sampled=float(A[:,4].min()),min_lambdaS_above_activation_sampled=float(A[A[:,5]!=0,5].min())if np.any(A[:,5]!=0)else None,
        final_state=v.tolist(),threshold_events=events)

def warped_gravity():
    out=[]
    for micron in [8.,10.,15.]:
        L=math.pi*micron*1e-6/1.973269804e-16
        M5=MU;k=M5**3/(2*MP**2);kl=k*L
        out.append(dict(radius_input_micron=micron,M5_target_input_GeV=M5,k_GeV=k,k_over_M5=k/M5,kL=kl,
            log10_IR_redshift=-kl/math.log(10),flat_KK_scale_GeV=1/L,
            log10_warped_KK_scale_GeV=math.log10(3.83*k)-kl/math.log(10),
            required_brane_EH_mass_squared_if_flat_GeV2=MP**2-M5**3*L))
    assert all(x['required_brane_EH_mass_squared_if_flat_GeV2']<0 for x in out)
    return dict(rows=out,
        action='5D Einstein-AdS interval with a(y)=exp(-ky), tuned RS brane tensions +/-6kM5³ in conventional normalization, and supplied stabilized L. M4²=M5³[1-exp(-2kL)]/(2k), using physical interval once. kL enormous, so exponent neglected with controlled bound. Positive brane EH terms in a flat interval only reduce the allowed M5: M4²=M5³L+Mbrane².',
        outcome='A weakly curved warped action can raise M5, but changes the KK spectrum exponentially and does not preserve the original approximately flat micron KK cosmology. Stabilization and vacuum selection not derived. Negative brane EH coefficient would be needed by the flat high-M5 attempt, not accepted as a healthy repair.',
        sources=['https://arxiv.org/abs/hep-ph/9905221','https://arxiv.org/abs/2409.01405'])

def build():
    rows=[running(f,l,.02,sp)for f,l,sp in itertools.product([5e10,1e11,2e11],[.003,.03,.3],[(1.,1.,1.),(1.,.7,1.4)])]
    return dict(status='PASS_EXPLICIT_PQ_VARIANT_TENSOR_RGE_AND_GRAVITY_REPAIR_ATTEMPTS',PQ=protected_variant(),complete_SU5_repair_obstruction=complete_SU5_protection_obstruction(),Yukawa=tensor_yukawa_control(),RG=rows,gravity=warped_gravity(),
        RG_action='SM top-only Yukawa truncation plus complex Sigma and original D+Q+Q inventory, potential lambdaH(HdagH)^2+lambdaS(SdagS)^2+lambdaHS HdagH SdagS. No sterile/mixing Yukawas. Piecewise one-loop gauge/top/scalar/three independent heavy Yukawa evolution. Tree matching lambdaH_high=lambdaH_low+lambdaHS²/(4lambdaS); new heavy yi(Mi)=sqrt2 Mi/f. All thresholds and boundary couplings are supplied.',
        RG_limits='A reproducible closed one-loop truncation for radial-before-all-heavy threshold ordering; other orderings explicitly rejected pending broken-phase EFT matching. Not complete SM flavor/sterile/mixing or two-loop finite matching. Higgs inputs illustrative. Sampled quartic minima are not a rigorous global vacuum-stability proof. This replaces the old common-y beta only within the stated model; no precise axion ceiling asserted.',
        sources=['https://arxiv.org/abs/1610.01639','https://arxiv.org/abs/2007.12700','https://arxiv.org/abs/2412.21157'],
        boundary='Three explicit independent construction attempts, not a common TOE action or a completed UV theory.')
if __name__=='__main__':
    d=build();(R/'data/toe_20261105_five_fronts_model_completion.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],'first_quality_n',d['PQ']['first_quality_row']['n'],'RG_reaches',sum(x['reaches_MU']for x in d['RG']),len(d['RG']),flush=True)
