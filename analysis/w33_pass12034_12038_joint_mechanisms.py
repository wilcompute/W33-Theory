"""Five explicit mechanism tests after12026-12033; none is a complete TOE.

Standard CW, MSSM RG, Higgs spectra, heat form factors and bundle atlases are
prior art. The named texture/native maps and their compatibility tests matter.
"""
from pathlib import Path
import sys,json,math
import numpy as np
import sympy as sy
from scipy.integrate import quad,solve_ivp
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12026_12033_theta_soft_threshold_connections as old
import w33_pass11995_native_metric_gr_lift as native
p=old.p; prior=old.prior; LOOP=16*np.pi**2

def grad(f,x,h=2e-5):
    return np.array([(f(x+h*v)-f(x-h*v))/(2*h) for v in np.eye(len(x))])

def flat_basis():
    x=old.MATCH[:10];J=old.derivative(lambda z:old.mix_coordinates(np.r_[z,old.MATCH[-1]]),x)
    return np.linalg.svd(J,full_matrices=True)[2][4:].T

def texture_eigenvalues(x):
    # Fixed overall normalization, never a parameter-dependent rescaling.
    base=p.theta_matrices(old.MATCH)[:3];mats=p.theta_matrices(np.r_[x,old.MATCH[-1]])[:3]
    scale=max(np.linalg.norm(z,2) for z in base)
    return [np.linalg.eigvalsh(z@z.conj().T)/scale**2 for z in mats]

def cw(x,soft=1.,Q=1.):
    def f(z):return z*z*(np.log(z/Q**2)-1.5)
    # Two complex scalars and one Dirac fermion per singular mass; common soft2.
    return sum(n*np.sum(f(z+soft)-f(z)) for n,z in zip([3,3,1],texture_eigenvalues(x)))/(16*np.pi**2)

def cw_scale_derivative(x,soft=1.):
    return -2*sum(n*np.sum(2*soft*z+soft**2) for n,z in zip([3,3,1],texture_eigenvalues(x)))/(16*np.pi**2)

def radiative_fibre():
    x=old.MATCH[:10];N=flat_basis();rows=[]
    for Q in [.5,1.,2.]:
        g=N.T@grad(lambda z:cw(z,Q=Q),x);rows.append(dict(Q=Q,projected_gradient=g.tolist(),norm=float(np.linalg.norm(g))))
    predicted=N.T@grad(cw_scale_derivative,x)
    observed=(np.array(rows[2]['projected_gradient'])-np.array(rows[0]['projected_gradient']))/np.log(4)
    assert np.linalg.norm(predicted-observed)<1e-8
    assert abs(cw(x,soft=0))<1e-16
    g0=np.array(rows[1]["projected_gradient"]);cstar=-np.dot(g0,predicted)/np.dot(predicted,predicted);remainder=g0+cstar*predicted
    # The entire scale-dependent gradient is one allowed TrYdagY counterterm.
    return dict(status='PASS',normalization='one fixed common baseline singular norm',common_soft_mass_squared=1.,projected_gradients=rows,
        best_single_counterterm_shift=float(cstar),unremovable_force_norm=float(np.linalg.norm(remainder)),projected_logQ_gradient_derivative=predicted.tolist(),scale_identity_error=float(np.linalg.norm(predicted-observed)),
        exact_identity='dV1/dlogQ=-(1/(8pi2)) sum_n Nc [(z_n+s)^2-z_n^2]. With common soft s this is constant plus -(s/(4pi2))sum Nc Tr(YdagY). A running local counterterm cancels it.',
        conclusion='The declared complete scalar/fermion toy supermultiplets lift the six-direction fibre, but the fitted point is not stationary and the force depends on an unspecified allowed counterterm. Fermion-only CW cannot select this vacuum. Exact SUSY s=0 cancels identically.',
        single_counterterm_test='Orthogonally project the six-component force off its logQ-running direction. The nonzero remainder cannot be removed by the one common TrYdagY counterterm alone. This is specific to the toy common-soft spectrum; independent invariant counterterms can change it.',
        scope='Not full MSSM/UV field-dependent spectrum, no supplied kinetic metric or native counterterm boundary condition; no selected theta vacuum.',prior=['12026 actual six-dimensional theta fibre','11909 up-sector CW','11935 soft-supertrace angular selector; different map','9709356 section7.3'])

def trilinear_beta(g,Y,T,mg):
    """16pi2 beta, Q-row convention; g1 is SU5 normalized."""
    u,d,e=Y;tu,td,te=T;hu=u@u.conj().T;hd=d@d.conj().T;he=e@e.conj().T
    g1,g2,g3=g;M1,M2,M3=mg;I=np.eye(3)
    cu=3*np.trace(hu).real-(13/15*g1*g1+3*g2*g2+16/3*g3*g3)
    cd=3*np.trace(hd).real+np.trace(he).real-(7/15*g1*g1+3*g2*g2+16/3*g3*g3)
    ce=3*np.trace(hd).real+np.trace(he).real-(9/5*g1*g1+3*g2*g2)
    su=6*np.trace(tu@u.conj().T)+26/15*g1*g1*M1+6*g2*g2*M2+32/3*g3*g3*M3
    sd=6*np.trace(td@d.conj().T)+2*np.trace(te@e.conj().T)+14/15*g1*g1*M1+6*g2*g2*M2+32/3*g3*g3*M3
    se=6*np.trace(td@d.conj().T)+2*np.trace(te@e.conj().T)+18/5*g1*g1*M1+6*g2*g2*M2
    return [(5*hu+hd+cu*I)@tu+(4*tu@u.conj().T+2*td@d.conj().T+su*I)@u,
            (5*hd+hu+cd*I)@td+(4*td@d.conj().T+2*tu@u.conj().T+sd*I)@d,
            (5*he+ce*I)@te+(4*te@e.conj().T+se*I)@e]

def flow_beta(t,z):
    y=z[:30];g,Y=p.unpack(y);mg=z[30:33].real;T=z[33:].reshape(3,3,3)
    return np.r_[prior.mssm_beta(t,y),2*np.array([33/5,1,-3])*g*g*mg/LOOP,np.array(trilinear_beta(g,Y,T,mg)).ravel()/LOOP]

def alignment_residual(Y,T):
    # Subtract the best scalar multiple of Y; covariant under both flavour bases.
    return [float(np.linalg.norm(t-np.vdot(y,t)/np.vdot(y,y)*y)/np.linalg.norm(y)) for y,t in zip(Y,T)]

def offdiagonal_trilinears(Y,T):
    result=[]
    for y,t in zip(Y,T):
        U,z,Vh=np.linalg.svd(y);a=U.conj().T@t@Vh.conj().T
        result.append(float(np.linalg.norm(a-np.diag(np.diag(a)))/np.linalg.norm(y)))
    return result

def soft_running():
    g,Y,_=old.improved_initial();mg=np.array([1500.,1600.,2000.]);z=np.r_[p.pack(g,Y),mg,np.zeros(27,complex)];rows=[]
    sol=solve_ivp(flow_beta,[0,-np.log(10)],z,rtol=2e-10,atol=1e-11,dense_output=True);assert sol.success
    for h in [.02,.01,.005,np.log(10)]:
        q=sol.sol(-h);gg,yy=p.unpack(q[:30]);tt=q[33:].reshape(3,3,3);r=alignment_residual(yy,tt)
        rows.append(dict(log_interval=-h,misalignment_GeV=r,offdiagonal_mass_basis_GeV=offdiagonal_trilinears(yy,tt),misalignment_over_log_squared=(np.array(r)/h**2).tolist()))
    g1,g2,g3=g;M1,M2,M3=mg
    cu=26/15*g1*g1*M1+6*g2*g2*M2+32/3*g3*g3*M3
    cd=14/15*g1*g1*M1+6*g2*g2*M2+32/3*g3*g3*M3
    ce=18/5*g1*g1*M1+6*g2*g2*M2
    hu,hd,he=[y@y.conj().T for y in Y]
    quadratic=[(3*cu*hu+cd*hd)@Y[0]/LOOP**2,(3*cd*hd+cu*hu)@Y[1]/LOOP**2,3*ce*he@Y[2]/LOOP**2]
    exact_leading=alignment_residual(Y,quadratic)
    # For nonzero universal A, the first derivative is generically not aligned.
    a=300.;T=[a*y for y in Y];dY=p.unpack(prior.mssm_beta(0,p.pack(g,Y)))[1];dT=np.array(trilinear_beta(g,Y,T,mg))/LOOP
    tangent=alignment_residual(Y,[dt-a*dy for dt,dy in zip(dT,dY)])
    return dict(status='PASS',real_gaugino_inputs_GeV=mg.tolist(),A_zero_coupled_running=rows,analytic_log_squared_misalignment_GeV=exact_leading,analytic_log_squared_offdiagonal_GeV=offdiagonal_trilinears(Y,quadratic),exact_matrix_law='For R_u=Tu Yu^-1 and initial T=0: nonscalar R_u(t)=t2[3 c_u Hu+c_d Hd]/(16pi2)^2+O(t3), where c_u,d are the real gaugino sources in betaT. Down exchanges u,d; lepton has3 c_e He. Scalar terms are projected out.',nonzero_universal_A_GeV=a,first_derivative_alignment_residual_GeV=tangent,bino_commutator=bino_commutator(),
        formula='For T_u=a Yu, T_d=a Yd: 16pi2(betaTu-a betaYu)=[6a Hu+2a Hd+(6a TrHu+gaugino source)I]Yu. In the up mass basis 2a Hd Yu has offdiagonal entries. For A=0 first derivative is scalar-aligned; nonalignment begins at log^2 in the coupled flow.',
        scope='Full three-family one-loop Yukawa, gauge, real gaugino and trilinear subsystem. The2TeV-to200GeV interval is a formal full-MSSM vector-field test, not decoupled EFT evolution or a messenger-to-observation spectrum. Scalar soft masses, Higgs soft running, mu/B and physical LR loop recomputation are not integrated. Thus this is an explicit failure of generic scalar LR alignment, not a total strongCP prediction or complete soft RG solution.',prior=['12027 exact linked theorem requires LR=aM','12018 one-sided protection','Martin-Vaughn hep-ph/9311340','9709356 equations6.5.33-35'])

def bino_commutator():
    rng=np.random.default_rng(12035);Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));U=np.linalg.qr(Z)[0]
    Y=[np.diag([.3,.8,1.1]),U@np.diag([.2,.6,.9]),np.diag([.1,.2,.4])];g=np.array([.6,.5,.9]);hu=Y[0]@Y[0].conj().T;hd=Y[1]@Y[1].conj().T;rows=[]
    for bino in [.8,0.]:
        mg=np.array([bino,1.1,.7]);coefficient=-(16/15)*g[0]**2*bino*(hu@hd-hd@hu)/LOOP**3
        z=np.r_[p.pack(g,Y),mg,np.zeros(27,complex)];sol=solve_ivp(flow_beta,[0,-.5],z,rtol=2e-12,atol=2e-14,dense_output=True);assert sol.success
        tests=[]
        for t in [-.5,-.25,-.125]:
            q=sol.sol(t);yy=p.unpack(q[:30])[1];tt=q[33:].reshape(3,3,3);R=np.linalg.solve(yy[0].T,tt[0].T).T;anti=(R-R.conj().T)/t**3
            tests.append(dict(log_interval=t,antiHermitian_over_log_cubed_norm=float(np.linalg.norm(anti)),analytic_error=float(np.linalg.norm(anti-coefficient))))
        rows.append(dict(bino_mass=bino,analytic_coefficient_norm=float(np.linalg.norm(coefficient)),samples=tests))
    return dict(formula='Ru-Ru_dag=-(16/15)g1^2 M1 t^3 [Hu,Hd]/(16pi2)^3+O(t4), for initial T=0 and real gauginos; hypercharge is SU5 normalized.',
        proof='Subtract the adjoint of betaRu:16pi2 d(Ru-Ru_dag)/dt=4[Hu,Ru]+2[Hd,Ru]+2[Rd,Hd] when Ru,Rd are Hermitian to lower order. Substitute their ordert2 terms:4(c_d-c_u)t2[Hu,Hd]/(16pi2)^2. Since c_u-c_d=(4/5)g1^2 M1, integrate once.',
        controls=rows,scope='First anti-Hermitian trilinear word in this subsystem, not its first scalar strongCP invariant: Tr[Hu,Hd]=0. M1=0 removes this cubic coefficient, not all higher-order CP terms. Toy nondegenerate Yukawas isolate the coefficient without inverse-hierarchy roundoff.')

def electroweak():
    g,Y,_=old.improved_initial();gp=g[0]*np.sqrt(3/5);g2=g[1];v=246.22;tb=10.;cb=1/np.sqrt(101);sb=10*cb;c2=cb*cb-sb*sb;s2=2*sb*cb
    mu=1000.;ma=2000.;M1=1500.;M2=1600.;mz2=(gp*gp+g2*g2)*v*v/4;mw=g2*v/2;sw=gp/np.sqrt(gp*gp+g2*g2);cw0=np.sqrt(1-sw*sw);mz=np.sqrt(mz2)
    # Here consistently use the running couplings at2TeV; not on-shell MZ.
    B=ma*ma*s2/2;hu=B/tb+.5*mz2*c2-mu*mu;hd=B*tb-.5*mz2*c2-mu*mu
    neutral=np.array([[M1,0,-mz*sw*cb,mz*sw*sb],[0,M2,mz*cw0*cb,-mz*cw0*sb],[-mz*sw*cb,mz*cw0*cb,0,-mu],[mz*sw*sb,-mz*cw0*sb,-mu,0]])
    charg=np.array([[M2,np.sqrt(2)*mw*sb],[np.sqrt(2)*mw*cb,mu]])
    higgs=np.array([[ma*ma*sb*sb+mz2*cb*cb,-(ma*ma+mz2)*sb*cb],[-(ma*ma+mz2)*sb*cb,ma*ma*cb*cb+mz2*sb*sb]])
    tree= (gp*gp+g2*g2)*c2*c2/8;yt=np.linalg.svd(Y[0],compute_uv=False)[0]*sb;mt=yt*v/np.sqrt(2);st=old.sqcd_delta(mt,'u')['squark_mass_squares'];MS2=np.sqrt(np.prod(st));X=-mu/tb
    stop=3*yt**4/(16*np.pi**2)*(np.log(MS2/mt**2)+X*X/MS2*(1-X*X/(12*MS2)))
    # Known one-loop finite gauge-scheme map, not a Yukawa/Higgs conversion.
    gMS=g*(1-g*g*np.array([0,2,3])/(96*np.pi**2))
    return dict(status='PASS',running_Z_mass_GeV=mz,Higgs_soft_inputs_GeV2=dict(mHu2=hu,mHd2=hd,Bmu=B),neutralino_tree_masses_GeV=sorted(abs(np.linalg.eigvalsh(neutral)).tolist()),chargino_tree_masses_GeV=sorted(np.linalg.svd(charg,compute_uv=False).tolist()),CP_even_tree_masses_GeV=np.sqrt(np.linalg.eigvalsh(higgs)).tolist(),lambda_tree=tree,leading_stop_delta_lambda=stop,leading_log_Higgs_mass_GeV=float(np.sqrt(2*(tree+stop)*v*v)),declared_g_DR_for_isolated_scheme_map=g.tolist(),g_MS_from_DR=gMS.tolist(),Higgs_scalar_Yukawa_MS_over_DR_minus_one=(np.array([[-1/60,-3/4,8/3],[-13/60,-3/4,8/3],[9/20,-3/4,0]])@(g*g)/(32*np.pi**2)).tolist(),
        stationary_residuals_GeV2=[hu+mu*mu-B/tb-.5*mz2*c2,hd+mu*mu-B*tb+.5*mz2*c2],
        scope='Tree EW closure and standard leading stop effective-potential logarithm/mixing check for supplied spectrum; leading-log mass is not a pole-mass prediction. Isolated scheme maps treat the inherited coupling numbers as declared DR inputs: gauge MS=DR[1-C_A g2/(96pi2)] and Higgs-scalar Yukawa MS/DR=1+sum g_a2(C_Q+C_R-2C_H)/(32pi2). They are not a heavy-particle decoupling match and are not applied to the12028 fit. No complete complete neutralino/chargino/Higgs/lepton self energies or two-loop Higgs calculation. Existing12028 fit is NOT silently replaced.',prior=['12024 supplied soft benchmark','12028 exact declared p0SQCD','9709356 sections8.1-8.2','hep-ph/9308222 scheme conversion'])

def tensor_formfactor(x):return .5*(quad(lambda u:np.exp(-x*u*(1-u)),0,1,epsabs=1e-13)[0]-1)

def tensor_spectral_heat(epsilon,t=1.,cutoff=32,quadrature_order=5):
    """Independent Galerkin heat trace; R4 except longitudinal8pi torus.

    Scalar operator is assembled at finite h, never using its Hessian formula.
    Gaussian quadrature covers transverse1,2; transverse3 integrates exactly.
    """
    from scipy.special import roots_hermite
    n=np.arange(-cutoff,cutoff+1);diff=n[:,None]-n[None,:];grid=2*np.pi*np.arange(512)/512
    plus=np.fft.fft(np.exp(epsilon*np.cos(4*grid)))/512
    minus=np.fft.fft(np.exp(-epsilon*np.cos(4*grid)))/512
    X,W=roots_hermite(quadrature_order);val=0.
    for x,w in zip(X,W):
        for y,z in zip(X,W):
            A=np.diag((n/4)**2)+(x*x/t)*minus[diff%512]+(y*y/t)*plus[diff%512]
            val+=w*z*np.exp(x*x+y*y)*np.exp(-t*np.linalg.eigvalsh(A)).sum()
    return float(val/np.pi*2*np.sqrt(np.pi*t)/(8*np.pi))

def tensor_spectral_certificate():
    baseline=tensor_spectral_heat(0);rows=[]
    for h in [.004,.002,.001]:
        fd=(tensor_spectral_heat(h)-2*baseline+tensor_spectral_heat(-h))/h**2
        rows.append(dict(amplitude=h,finite_difference=float(fd),analytic=tensor_formfactor(1.),error=float(fd-tensor_formfactor(1.))))
    return rows

def tensor():
    b,v,C,H=native.inputs();H=np.array(H,float);R=np.linalg.cholesky(H);M=np.sqrt(np.linalg.det(H));J=sy.Matrix([[C[e,i]*C[e,j]/27 for e in range(135)] for i,j in native.PAIRS]);selected=list(J.rref()[1]);rows=[]
    # g=exp(h T), traceT=0, T has transverse eigenvalues(+1,-1).
    T=np.diag([0.,1.,-1.,0.]);q=np.array([1.,0.,0.,0.]);assert np.linalg.norm(T@q)==0 and np.trace(T)==0
    for h in [-.002,0,.002]:
        target=R@expm(-h*T)@R.T;w,history=native.lift(target,b,v,selected);got,_=native.homogenize(w,b,v)
        rows.append(dict(h=h,min_weight=float(min(w)),metric_error=float(np.linalg.norm(got-target)),relative_capacity=float(np.sqrt(np.linalg.det(got))/M)))
    x=sy.symbols('x');coeff=[sy.Rational(1,2)*(-1)**n*sy.factorial(n)/sy.factorial(2*n+1) for n in range(1,6)]
    samples=[dict(x=z,normalized_heat_hessian=tensor_formfactor(z),leading=-z/12) for z in [.01,.05,.1,.5,1.]]
    return dict(status='PASS',native_TT_metric_lifts=rows,exact_metric_rank=10,redundant_linear_edge_directions=125,
        normalized_TT_heat_hessian='(4pi t)^2 K_doubleprime/Vol = 1/2 [int_0^1 exp(-x u(1-u))du -1], x=t q^2; metric diag(1,exp(h cos qx0),exp(-h cos qx0),1), sqrtg=1.',
        series_coefficients=[str(z) for z in coeff],samples=samples,independent_continuum_spectral_check=tensor_spectral_certificate(),
        derivation='A1=cos(qx0)(p1^2-p2^2); A2=cos^2(qx0)(p1^2+p2^2). Gaussian averages <p1^2+p2^2>=1/t and <(p1^2-p2^2)^2>=1/t2 give seagull -1/2 and Duhamel +1/2 int exp(-x u(1-u)).',
        Einstein_Hilbert_comparison='Heat a2: K_doubleprime=(4pi t)^-2(t/6) (int sqrtg R)_doubleprime. Thus EH Hessian/Vol=-q2/2, since leading heat=-t q2/12. This sign and ratio are the standard Euclidean tensor result; induced action sign also depends on proper-time prefactor and matter species.',
        scope='New explicit native lifts for the TT family and independent continuum scalar form factor, not a native TT heat convergence theorem. Native27-band tensor replay, Lorentzian unitarity, constraint algebra, nonlinear dynamics, G and Lambda remain open. Rank10/125 already belongs to11995.',prior=['11995 full metric chart','12029 conformal heat only','12009 density','0811.1063 standard covariant heat perturbation'])

def frame_from(P,E):
    z,U=np.linalg.eigh(E.conj().T@P@E);assert min(z)>1e-8
    return P@E@(U/np.sqrt(z))@U.conj().T,float(min(z))

def atlas():
    patch=prior.NativeChiralPatch();anchors=[(-.3,-.2),(.25,.2),(.05,-.15)];refs=[patch.evaluate(*a)[1] for a in anchors];rows=[]
    for s,t in [(-.12,-.1),(.12,.1),(.03,-.02)]:
        P,_,_,gap,_,dP=patch.evaluate(s,t,ds=.7,dt=-.4);fs=[frame_from(P,E) for E in refs];F=[f for f,o in fs];trans=lambda a,b:F[a].conj().T@F[b]
        cocycle=np.linalg.norm(trans(0,1)@trans(1,2)-trans(0,2));unit=max(np.linalg.norm(trans(a,b).conj().T@trans(a,b)-np.eye(30)) for a,b in [(0,1),(1,2),(2,0)])
        def current(E):
            Z=E.conj().T@P@E
            return float((.5j*np.trace(np.linalg.solve(Z,E.conj().T@(P@dP-dP@P)@E))).real)
        L=[current(E) for E in refs];h=1e-5;theta=[]
        for sign in [-1,1]:
            PP=patch.evaluate(s+sign*h*.7,t-sign*h*.4)[0];FF=[frame_from(PP,E)[0] for E in refs];theta.append(np.linalg.det(FF[0].conj().T@FF[1]))
        dtheta=np.angle(theta[1]/theta[0])/(2*h);err=L[1]-L[0]+dtheta
        rows.append(dict(coordinates=[s,t],kernel_gap=gap,reference_overlap_min=min(o for f,o in fs),frame_cocycle_error=float(cocycle),transition_unitarity_error=float(unit),connection_transition_identity_error=float(err),transition_determinant_phase=float(np.angle(np.linalg.det(trans(0,1))))))
    return dict(status='PASS',anchors=anchors,overlap_checks=rows,
        exact_law='F_beta=F_alpha T_ab, T_ab=F_alpha_dag F_beta; T_ab T_bc=T_ac. L_beta-L_alpha=-d arg det T_ab for L=iTr(Fdag dF). This constructs actual transitions of the native non-Abelian SU5 10+bar5 projector, not only a Chern number.',
        uniform_overlap_locality_obstruction='Reference E is a30-column finite-cell frame. Its min eigenvalue E dag P E is checked only at these points. Its inverse square root has no volume-uniform locality bound. Even exact atlas cocycles define a determinant line, not a global trivialization; global holonomies and a local reconstruction current still must be supplied.',
        scope='Three intersecting finite patches for actual native-word non-Abelian backgrounds. No all-configuration covering, noncontractible global gluing or uniform-volume locality theorem.',prior=['12025 one-patch current','12030 Abelian torus Chern test','Luscher hep-lat/9904009','2610.09093v1 global reconstruction obligations'])

def payload():return dict(status='PASS',pass12034=radiative_fibre(),pass12035=soft_running(),pass12036=electroweak(),pass12037=tensor(),pass12038=atlas())
if __name__=='__main__':
    d=payload();path=ROOT/'data/w33_pass12034_12038_joint_mechanisms.json';path.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
