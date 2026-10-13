"""Declared enhancement threshold and gauged operator-quality completion.

Generic SUSY matching/discrete protection are prior art. No compactification
or complete SUSY-breaking vacuum is inferred from these explicit models.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"analysis"))
import w33_pass11950_11951_strong_cp_divisor_and_vectorlike as masses
import w33_pass11952_11955_threshold_vacuum_loop_leptons as loop_prior


def enhancement_threshold():
    z, mu, v0, m0, q = s.symbols("z mu v0 m0 q", nonzero=True)
    # Each SU(N)->SU(N-1) Higgs flavor changes b by -2; decoupling
    # the remaining massive flavor changes b by +1.
    ratio = (m0*z/mu)/((v0*z/mu)**2*(v0*z/mu)**2)
    assert s.simplify(ratio*z**3-m0*mu**3/v0**4) == 0
    stages = []
    for light in (0, 3, 6):
        stages.append(dict(light_spectator_flavors=light,
            groups=["SU5_color", "SU4_color", "SU3_color", "SU3_color"],
            flavors=[light+3, light+2, light+1, light],
            beta_coefficients=[12-light, 10-light, 8-light, 9-light]))
    # Stabilizer of two linearly independent fundamental VEVs: T has
    # zero rows/columns4,5 and traceless3x3 block, dimension8.
    generators = []
    for i in range(5):
        for j in range(i+1, 5):
            a = s.zeros(5); a[i,j] = a[j,i] = 1; generators.append(a)
            a = s.zeros(5); a[i,j] = s.I; a[j,i] = -s.I; generators.append(a)
    for i in range(4):
        a = s.zeros(5); a[i,i] = 1; a[4,4] = -1; generators.append(a)
    constraint = s.Matrix.hstack(*[s.Matrix(list(a[:,3])+list(a[:,4])) for a in generators])
    # Hermitian generator coefficients are REAL. Complexifying only the
    # fundamental constraints would instead compute a parabolic stabilizer.
    real_constraint=constraint.applyfunc(s.re).col_join(constraint.applyfunc(s.im))
    assert real_constraint.rank() == 16
    Q = s.zeros(5, 2); Q[3,0] = z; Q[4,1] = z
    # Anti-fundamentals are holomorphic equal z, not conjugate z;
    # their moment maps cancel because absolute norms agree.
    assert Q.conjugate().T*Q == s.eye(2)*s.conjugate(z)*z
    return {"status":"PASS", "threshold_ratio":str(s.factor(ratio)),
            "stages":stages, "gauge_stabilizer_dimension":8,
            "broken_vector_count":16,
            "superpotential":"sum_ij Xij(Qtilde_i Q_j-v0^2 z^2 delta_ij)+m0 z Qtilde_3 Q_3; i,j=1,2",
            "home":"Q1=Qtilde1=v0 z e4, Q2=Qtilde2=v0 z e5, flavor3=0, Xij=0: classical F=D=W=0",
            "scale_matching":"Lambda3^(9-n)=m Lambda5^(12-n)/(v1^2 v2^2)",
            "f3":"f_UV+3 log(z)/(8pi^2)+regular for v1=v2=v0 z and m=m0 z",
            "minimal_balance":"3-2 n_Higgs+n_chiral=0 has minimal nonnegative solution n_Higgs=2,n_chiral=1",
            "scope":"SU5_color is an enlarged COLOR parent, not the conventional SM SU5 GUT. It is not an E6/string/W33 vacuum. Perturbative matching holds only where Higgs/mass thresholds exceed strong scales. Cubic pole matches11950 locally; coefficient phase and global modular law remain uncomputed.",
            "primary":"https://arxiv.org/abs/hep-th/9509066 section4.1"}


def gauged_quality():
    # (dimension,E6 Dynkin index,X,Z). E6 T27=3. Z is a continuous
    # gauge group first broken by charge+-12 VEVs, not an anomalous
    # global Z12. Added conjugate families have11953 family sign-1.
    fields = []
    def add(name, dim, index, x, z, number=1):
        for i in range(number): fields.append((name+str(i),dim,index,x,z))
    add("27A",27,3,1,0); add("bar27A",27,3,-1,0)
    add("27B",27,3,-1,0,2); add("bar27B",27,3,1,1,2)
    add("27C",27,3,-1,-1,2); add("bar27C",27,3,1,0,2)
    add("P",1,0,0,1); add("constraint",1,0,0,-1,3)
    add("spectator",1,0,0,1,2)
    add("PhiMinus",1,0,0,-12); add("PhiPlus",1,0,0,12)
    # Neutral multipliers for the two high-scale constraints omitted from
    # anomaly sums because every charge is zero.
    anomalies = dict(E6_E6_X=sum(i*x for _,d,i,x,z in fields),
        E6_E6_Z=sum(i*z for _,d,i,x,z in fields),
        gravitational_X=sum(d*x for _,d,i,x,z in fields),
        gravitational_Z=sum(d*z for _,d,i,x,z in fields),
        X_cubed=sum(d*x**3 for _,d,i,x,z in fields),
        Z_cubed=sum(d*z**3 for _,d,i,x,z in fields),
        X_squared_Z=sum(d*x*x*z for _,d,i,x,z in fields),
        X_Z_squared=sum(d*x*z*z for _,d,i,x,z in fields))
    assert set(anomalies.values()) == {0}
    # Essential messenger audit: without a spectator-only parity, the
    # bare E6 mass27B bar27C is allowed. Its F term would induce a
    # charge-Z=-1 condensate C=-Lambda B/P and defeat the claimed branch.
    # An unbroken spectator Z2 makes BOTH C and barC odd and all other
    # fields even. Every ordinary mixed anomaly coefficient is even.
    spectator_odd=[f for f in fields if f[0].startswith(('27C','bar27C'))]
    z2_anomalies=dict(E6_E6_Z2=sum(2*i for _,d,i,x,z in spectator_odd),
        gravitational_Z2=sum(d for _,d,i,x,z in spectator_odd),
        X_squared_Z2=sum(d*x*x for _,d,i,x,z in spectator_odd),
        Z_squared_Z2=sum(d*z*z for _,d,i,x,z in spectator_odd),
        X_Z_Z2=sum(d*x*z for _,d,i,x,z in spectator_odd),
        X_Z2_squared=sum(d*x for _,d,i,x,z in spectator_odd),
        Z_Z2_squared=sum(d*z for _,d,i,x,z in spectator_odd))
    assert all(v%2==0 for v in z2_anomalies.values())
    # Low condensates: S(-1,0), T(+1,+1), P(0,+1), Phi+- (0,+-12).
    # Q Hd Dc has X=-1,Z=0; a,b,c,d,e powers give a-b=1,
    # a+c=12(d-e). rho power is(a+b)/2+c=a+c-1/2.
    leading = []
    for a in range(1, 13):
        b = a-1; c = 12-a
        assert a-b == 1 and a+c-12 == 0
        exponent = s.Rational(a+b,2)+c
        assert exponent == s.Rational(23,2)
        leading.append(dict(T_power=a,S_power=b,P_power=c,
                            PhiMinus_power=1,rho_exponent=str(exponent)))
    rho = s.Rational(1,32)
    # D_Z cancellation needs a small difference of high-scale norms.
    difference = (2*rho+rho**2)/12
    uminus = (s.sqrt(difference**2+4)+difference)/2
    uplus = (s.sqrt(difference**2+4)-difference)/2
    assert s.simplify(uminus*uplus-1) == 0
    assert s.simplify(2*rho+rho**2+12*(uplus-uminus)) == 0
    # Isolated singlet branch: seven charged variables, five independent
    # holomorphic constraints, two complex gauge directions. The two
    # moment maps lift their real radial partners, leaving only gauge
    # phases. Tiny spectator masses are nonzero EXACTLY, not numerical
    # rank-zero decisions on rho^20 eigenvalues.
    S1,S2,T1,T2,P,pm,pp=s.symbols('S1 S2 T1 T2 P pm pp')
    constraints=s.Matrix([S1*T1-P,2*(S2*T2-P),3*(S1*T2+S2*T1),
                          pm*pp-1,pm*P**12])
    J=constraints.jacobian((S1,S2,T1,T2,P,pm,pp))
    vr=s.symbols('vr',positive=True)
    minor=s.factor(J[:,[0,1,2,4,6]].det().subs({S1:vr,S2:s.I*vr,T1:vr,T2:-s.I*vr}))
    assert minor!=0
    moment=s.Matrix([[4*rho,2*rho],[2*rho,2*rho+rho**2+144*(uminus+uplus)]])
    assert moment[0,0]>0 and moment.det()>0
    V, md = masses.ckm_target(); target=(V*md**2)@V.conj().T
    real, B, mu = masses.barr_realization(target)
    sensitivity = float(np.linalg.norm(B@np.linalg.inv(real)/mu))
    soft_ratio = 1e-13
    holomorphic = float(rho**s.Rational(23,2))
    kaehler = soft_ratio*float(rho**s.Rational(3,2))
    # Exact fixed-modulus response to a supplied F_P source. The aligned
    # vacuum makes the multiplier quadratic form diagonal except F_P.
    X,Y,F0,L,r=s.symbols('X Y F0 L r',real=True,positive=True)
    quadratic=(F0-L*(X+2*Y))**2+2*r*L**2*X**2+8*r*L**2*Y**2
    response=s.solve([s.diff(quadratic,X),s.diff(quadratic,Y)],(X,Y))
    assert s.simplify(response[X]-F0/(2*L*(1+r)))==0
    assert s.simplify(response[Y]-F0/(4*L*(1+r)))==0
    multiplier=kaehler*float(3/(4*(1+rho)))
    # The high-order phase/magnitude constraint necessarily leaves a
    # parametrically light singlet. The neutral-U real direction has no
    # D-term mass and supplies an upper Rayleigh bound on the smallest
    # physical scalar mass. Generic TeV soft terms cannot be assumed small.
    light_bound=s.sqrt(2*((12*s.sqrt(uminus)*rho**11)**2+rho**24))
    return {"status":"PASS","full_anomaly_inventory":[dict(name=n,dimension=d,index_E6=i,X=x,Z=z) for n,d,i,x,z in fields],
            "anomaly_sums":anomalies,"residual_group":"U1Z broken to gauged Z12 by Phi+-12; subsequently low P,T condensates break the residual group",
            "spectator_parity":{"C_and_barC":"odd under an additional unbroken spectator Z2; all other fields even",
                "ordinary_mixed_anomaly_coefficients":z2_anomalies,
                "negative_control":"Without the tag, Lambda27B bar27C+P27C bar27C induces27C=-Lambda27B/P, invalidating the all-positive-charge condensate assumption. With tag, every allowed spectator vertex is at least quadratic, so C=barC=0 has no tree source; perturbative superpotential nonrenormalization forbids loop-generated inverse-P light vertices. Nonperturbative effects/soft breaking remain separate gates."},
            "allowed_mixing":"d(27_native,27A,27B), charges X=Z=0; real mu 27A bar27A allowed",
            "vacuum_superpotential":"11953 with SiTj replaced by E6 contractions and v^2 replaced by Lambda P; plus R(PhiMinus PhiPlus-Lambda^2)+U(PhiMinus P^12/Lambda^11-f^2)",
            "singlet_home":"P=rho Lambda real, S=(v,i v), T=(v,-i v), v^2=rho Lambda^2; all multipliers0; Phi norms as stored, product Lambda^2. F=D=W=0. f^2 selected to satisfy high constraint, not predicted.",
            "singlet_stability":{"constraint_rank":5,"nonzero_constraint_minor":str(minor),
                "charged_complex_variables":7,"neutral_or_charged_constraint_multipliers":5,
                "additional_massive_complex_spectators":2,"complex_gauge_kernel_dimension":2,
                "positive_physical_real_scalar_directions":26,"gauge_phase_zero_directions":2,
                "proof":"Rank5 holomorphic constraint Jacobian gives only two complex gauge kernels; positive rank2 moment-map Gram lifts radial gauge partners. Two spectator superpotential masses pm P^10 are nonzero. Canonical-K SUSY Hessian is positive on all26 remaining real singlet directions, although some masses are parametrically tiny. Other E6 components are not included."},
            "rho":str(rho),"PhiMinus_norm_squared_over_Lambda_squared":str(uminus),
            "PhiPlus_norm_squared_over_Lambda_squared":str(uplus),
            "leading_upper_block_monomials":leading,
            "all_order_holomorphic_bound":"For analytic UV superpotential monomials on the stated condensate branch, with unbroken spectator parity and perturbative SUSY matching: upper-block rho exponent>=23/2; first complex m or mu corrections exponent>=12. This does not include nonperturbative or soft operators. Neutral high-scale factors are real at this home.",
            "colored_spectator_mass":"P 27C bar27C; two full pairs carry total SU3 threshold index12, so their mass phase is arg(P^12), real in the PhiMinus-real gauge at the stated F-flat home",
            "light_singlet_gate":{"smallest_physical_scalar_mass_over_Lambda_upper":float(light_bound),
                "mass_upper_GeV_if_Lambda_1e16":float(light_bound)*1e16,
                "proof":"Neutral U fluctuation has real mass-squared2 Lambda^2[(12 PhiMinus/Lambda rho^11)^2+rho^24]; the smallest physical eigenvalue cannot exceed this Rayleigh value.",
                "meaning":"Classical exact positivity does not justify generic TeV-soft stability. High-sector sequestering or a different stabilization mechanism must be computed before trusting the soft-floor envelope."},
            "positive_spectator_mass":"PhiMinus P^10 spectator^2/Lambda^10 is allowed; spectator VEV0 and positive supplied real mass, not a full E6 stability proof",
            "kaehler_floor":"K contains P^dag T Q Hd Dc/Lambda^3; assuming F_P~m_soft P gives DeltaY~(m_soft/Lambda) rho^(3/2), much less suppressed than holomorphic rho^(23/2)",
            "fixed_modulus_multiplier_response":{"potential":"|F0-Lambda(X+2Y)|^2+2rhoLambda^2|X|^2+8rhoLambda^2|Y|^2+36rhoLambda^2|Z|^2",
                "solution":"X=F0/[2 Lambda(1+rho)],Y=F0/[4 Lambda(1+rho)],Z=0",
                "upper_block_leak":"X T Q Hd Dc/Lambda^2 and Y T Q Hd Dc/Lambda^2 are allowed. With F0=m_soft rhoLambda, combined unit-coefficient envelope is 3/[4(1+rho)] times the Kahler floor.",
                "scope":"Exact multiplier response at fixed moduli only. Light P/high moduli cannot be assumed fixed under generic soft terms."},
            "quark_upper_block_linear_sensitivity":sensitivity,
            "single_unit_coefficient_envelope":{"holomorphic_Y":holomorphic,"kaehler_Y_for_msoft_over_Lambda_1e_minus13":kaehler,
                "theta_linear_norm_bound":sensitivity*np.sqrt(3)*(holomorphic+kaehler)},
            "including_two_multiplier_unit_coefficients_theta_envelope":float(sensitivity*np.sqrt(3)*(holomorphic+kaehler+multiplier)),
            "scope":"A declared anomaly-free added-field model and selected F/D-flat branch, not original W33 field content or a stable full E6/SM vacuum. Upper-block per-operator envelope assumes unit Wilson coefficients; other soft/gluino/tadpole effects and actual scales remain open.",
            "primary":"https://arxiv.org/abs/2002.04204 studies distinct discrete/R and SUSY-breaking protections; our Z12 charges are not its model"}


def scalar_at_scale(cp_scale, portals=(.1,.2)):
    # Fixed B,mu,light m while scalar VEV/mass grows: lambda_S~1/vCP.
    m=np.array([[1,1,0],[0,2,1],[1,0,3]],float)/10
    r=np.array([1,2,1],float)/10; t=np.array([1,-1,2],float)/10
    M=np.zeros((4,4),complex);M[:3,:3]=m;M[3,:3]=r+1j*t;M[3,3]=.2
    vertices=np.zeros((5,4,4),complex);vertices[0,:3,:3]=m
    for j,row in enumerate((r,1j*r,t,1j*t),1):vertices[j,3,:3]=row/cp_scale
    K=np.diag([1.,3*cp_scale**2,1.5*cp_scale**2,1.5*cp_scale**2,3*cp_scale**2])
    K[1,4]=K[4,1]=cp_scale**2;K[2,3]=K[3,2]=cp_scale**2/2
    K[0,1]=K[1,0]=portals[0]*cp_scale;K[0,4]=K[4,0]=portals[1]*cp_scale
    ev,O=np.linalg.eigh(K);assert min(ev)>0
    U,ms,Vh=np.linalg.svd(M);V=Vh.conj().T;delta=np.zeros_like(M)
    for a,mass2 in enumerate(ev):
        gamma=np.einsum('i,ijk->jk',O[:,a],vertices)
        delta+=gamma@((V*(ms*loop_prior.b0(ms**2,mass2)))@U.conj().T)@gamma/(16*np.pi**2)
    return float(np.trace(np.linalg.solve(M,delta)).imag)


def portal_running():
    m=s.Matrix([[1,1,0],[0,2,1],[1,0,3]])/10
    r=s.Matrix([1,2,1]).T/10;t=s.Matrix([1,-1,2]).T/10
    Y=s.Matrix.vstack(r,t); F=Y*(m.T*m)*Y.T
    assert F[0,0]!=F[1,1] and F[0,1]!=0
    # Exact field-dependent Dirac determinant trace: mixed term is
    # 2 h^2 S^dag F S. Its CW scale derivative sources a non-isotropic
    # portal even when the tree portal matrix is proportional to I.
    h,x,y,u,v=s.symbols('h x y u v',real=True)
    B=(x+s.I*y)*r+(u+s.I*v)*t
    M=(h*m).row_join(s.zeros(3,1)).col_join(B.row_join(s.Matrix([[s.Rational(1,5)]])))
    trace=s.expand(s.trace((M.conjugate().T*M)**2))
    mixed=s.expand(trace).coeff(h,2)
    expected=s.expand(2*(B*(m.T*m)*B.conjugate().T)[0])
    assert s.expand(mixed-expected)==0
    scales=[dict(vCP=z,scalar_loop_theta=scalar_at_scale(z)) for z in (1.,10.,100.,1000.)]
    assert abs(scales[0]['scalar_loop_theta']-loop_prior.scalar_loop()['theta'])<1e-14
    assert abs(scales[-1]['scalar_loop_theta'])<1e-10
    return {"status":"PASS","fermion_box_matrix": [[str(z) for z in row] for row in F.tolist()],
            "trace_h_squared_coefficient":str(mixed),
            "fixed_coupling_CW_source":"mu dV1/dmu=Nc Tr[(M^dag M)^2]/(8pi^2); its mixed coefficient is Nc S^dag F S/(4pi^2). The compensating potential counterterm has opposite sign.",
            "alignment_result":"Equal diagonal portals are not preserved by this fermion-box source: F11 != F22 and F12 !=0. This is a source term, not the complete beta function including scalar/wavefunction/gauge terms.",
            "fixed_tree_matrix_scale_sweep":scales,
            "scope":"Separate declared non-SUSY scalar model. Raising vCP at fixed B reduces scalar Yukawas and this actual one-loop contribution; it does not derive the scale or control all SUSY/soft contributions."}


def payload():
    d={"status":"PASS","11957":enhancement_threshold(),"11958":gauged_quality(),"11959":portal_running()}
    paths=["analysis/w33_pass11950_11951_strong_cp_divisor_and_vectorlike.py","analysis/w33_pass11952_11955_threshold_vacuum_loop_leptons.py"]
    d['input_sha256_lf']={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in paths}
    return d


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11957_11959_color_threshold_and_cp_quality.json').write_text(json.dumps(d,indent=2)+'\n')
    print(d['status'],d['11958']['single_unit_coefficient_envelope'],d['11959']['fixed_tree_matrix_scale_sweep'],flush=True)
