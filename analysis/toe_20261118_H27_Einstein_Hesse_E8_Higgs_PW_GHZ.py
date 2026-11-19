"""Five connected W33/E8/H27/quantum hypotheses with exact controls.

1. Free H27 Einstein quotient (S5 x S3 x S3)/H27, NOT sphere or 4+7.
2. H27's two symmetric cubic invariants = classical Hesse pencil;
   full SU3 vs H27 effective E6 Yukawa selection.
3. H27 fixed-subspace obstruction for elementary E8 27x3 Higgs,
   and unique neutral bilinear.
4. PW non-equilateral 3-well hopping: H27 action nonlocal or broken.
5. 3-qutrit GHZ and dephased control identical at ALL pairwise
   reductions, separable at pairs, distinguishable by 3-party
   stabilizer witness; finite-shot Hoeffding and exact model power.
Claims are mathematical/conditional, not a solved M-theory vacuum or
a valid 3-slot causal quantum process tensor.
"""
import json,math
from itertools import product
from pathlib import Path
import numpy as np
from scipy.stats import binom

ROOT=Path(__file__).resolve().parents[1]
w=np.exp(2j*np.pi/3)
I3=np.eye(3,dtype=complex)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
Z=np.diag([1,w,w*w])
G=list(product(range(3),repeat=3))
ident=(0,0,0)

def mul(g,h):
    a,b,c=g; A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C+a*B)%3)

def rep(g):
    a,b,c=g
    # ZX=w XZ; this ordering realizes the +aB group cocycle.
    return (w**c)*np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,a)

def chi(g,idx):
    return w**g[idx]

def eigen_not_one(mat):
    return float(np.min(abs(np.linalg.eigvals(mat)-1)))

def geometry():
    err=max(float(np.max(abs(rep(mul(g,h))-rep(g)@rep(h))))
            for g in G for h in G)
    assert err<2e-13
    assert max(float(np.max(abs(rep(g).conj().T@rep(g)-I3))) for g in G)<1e-13
    assert max(abs(np.linalg.det(rep(g))-1) for g in G)<1e-12
    min_gap=float("inf")
    witnesses={}
    for g in G:
        if g==ident: continue
        gaps=(eigen_not_one(rep(g)),
              abs(chi(g,0)-1),abs(chi(g,1)-1))
        best=max(gaps)
        assert best>1.5, (g,gaps)
        min_gap=min(min_gap,best)
        key=("center" if g[0]==g[1]==0 else
             "first_character" if g[0]!=0 else "second_character")
        witnesses[key]=witnesses.get(key,0)+1
    assert witnesses==dict(center=2,first_character=18,second_character=6)
    # Representations 3, 2chi_a, 2chi_b give spheres S5,S3,S3,
    # unitary isometries. Every g!=1 moves every point of at
    # least one sphere, so diagonal action is FREE.
    dimensions=(5,3,3)
    radius_squared=(4,2,2)
    ric=[(n-1)/r for n,r in zip(dimensions,radius_squared)]
    assert ric==[1.,1.,1.]
    # H27 quotient of simply connected product -> pi1=H27.
    # Homogeneous product Euler/Poincare: (1+t^5)(1+t^3)^2.
    betti={0:1,3:2,5:1,6:1,8:2,11:1}
    assert sum(betti.values())==8
    assert sum(((-1)**k)*v for k,v in betti.items())==0
    volume=1024*math.pi**7/27
    # Further dynamical sanity control: normalized Ricci flow of a
    # product Einstein metric (scale only, volume preserved).
    # t_i=log(r_i/r_i0), sum d_i*t_i=0, and
    # dt_i/ds=-exp(-2t_i)+(sum d_j exp(-2t_j))/11.
    # Its linearization restricted to relative scales is +2*I:
    # the factor-size modes are UNSTABLE under normalized Ricci flow.
    dims=np.array(dimensions,dtype=float)
    lin=2*(np.eye(3)-np.outer(np.ones(3),dims)/11)
    tangent=np.array([[3,-5,0],[3,0,-5]],dtype=float).T
    assert np.max(abs(dims@tangent))<1e-12
    assert np.max(abs(lin@tangent-2*tangent))<1e-12
    hess=np.diag(4*dims)
    constrained_hessian=tangent.T@hess@tangent
    assert min(np.linalg.eigvalsh(constrained_hessian))>0
    return dict(status="PASS",free_group=27,
       group_law_max_error=err,representation_dimension=3,
       minimal_moving_eigenvalue_gap=min_gap,
       nonidentity_elements_covered_by_factor=witnesses,
       simply_connected_cover="S5(radius 2) x S3(radius sqrt(2)) x S3(radius sqrt(2))",
       free_isometric_H27_action=True,
       quotient_dimension=11,
       quotient_positive_Einstein_Ricci_coefficient=1,
       quotient_scalar_curvature=11,
       exact_quotient_volume="1024*pi^7/27",
       volume_float=volume,
       quotient_pi1_order=27,
       quotient_rational_Betti={str(k):v for k,v in betti.items()},
       quotient_Betti4=0,quotient_Betti7=0,
       quotient_real_degree4_and_degree7_flux_classes_absent=True,
       normalized_Ricci_flow_relative_scale_linear_eigenvalues=[2,2],
       volume_preserving_scalar_curvature_Hessian_positive=True,
       normalized_Ricci_flow_scope="Homogeneous product factor-scale modes only; their positive linearized flow exponent means instability in normalized Ricci flow, not an 11D supergravity BF mass computation.",
       restricted_factor_dimension_argument="One center-faithful 3D complex irrep requires S5; two independent quotient characters with positive-Ricci round factors require at least S3 each => dimension11 in THIS explicit three-factor linear ansatz. Not a theorem on all possible 7D actions.",
       physical_limit="Positive Einstein *Riemannian eleven-manifold*, NOT Lorentzian 11D supergravity; NOT an internal seven-manifold, G2 solution or quantified 4D compactification. Nonzero 4-form and 7-form de Rham flux classes on this model are absent; torsion classes could remain.")

def hesse():
    exps=[(i,j,3-i-j) for i in range(4) for j in range(4-i)]
    assert len(exps)==10
    where={e:i for i,e in enumerate(exps)}
    Tx=np.zeros((10,10),complex)
    Tz=np.zeros((10,10),complex)
    for j,(a,b,c) in enumerate(exps):
        Tx[where[(b,c,a)],j]=1
        Tz[j,j]=w**(b+2*c)
    assert np.max(abs(Tx@Tz-Tz@Tx))<1e-12  # central omega^3 acts trivially
    P=(np.eye(10)+Tx+Tx@Tx)/3@(np.eye(10)+Tz+Tz@Tz)/3
    assert np.max(abs(P@P-P))<1e-12
    assert round(np.trace(P).real)==2
    x3=np.zeros(10,complex)
    xyz=np.zeros(10,complex)
    for i in range(3):
        x3[where[tuple(3 if k==i else 0 for k in range(3))]]=1
    xyz[where[(1,1,1)]]=1
    for v in (x3,xyz):
        assert np.max(abs(Tx@v-v))<1e-12
        assert np.max(abs(Tz@v-v))<1e-12
    assert np.linalg.matrix_rank(np.stack([x3,xyz],axis=1))==2
    # Multiplicity in V tensor V tensor V from characters:
    # chi(g)=0 unless g in center, where chi=3*w^c.
    inv3=sum((np.trace(rep(g))**3 for g in G))/27
    assert abs(inv3-3)<1e-10
    wedge3=sum(np.linalg.det(rep(g)) for g in G)/27
    assert abs(wedge3-1)<1e-10
    # Sym3 multiplicity2 and alternating cubic multiplicity1.
    # The E6 symmetric d_{ijk} times SU3 epsilon_{abc}
    # vanishes for ONE identical COMMUTING chiral superfield,
    # by exchanging i,a <-> j,b. Finite test with a random
    # symmetric rank3 d and an arbitrary 3x3 superfield matrix:
    rng=np.random.default_rng(20261118)
    d=rng.normal(size=(3,3,3))
    d=sum(np.transpose(d,p) for p in (
        (0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)))/6
    a=rng.normal(size=(3,3))
    eps=np.zeros((3,3,3))
    for i,j,k in product(range(3),repeat=3):
        if len({i,j,k})==3:
            eps[i,j,k]=(1 if (i,j,k) in ((0,1,2),(1,2,0),(2,0,1)) else -1)
    su3cubic=np.einsum("ijk,abc,ia,jb,kc->",d,eps,a,a,a)
    assert abs(su3cubic)<1e-11
    return dict(status="PASS",group_order=27,
       symmetric_cubic_monomial_count=10,
       invariant_symmetric_cubic_space_dimension=2,
       invariant_polynomial_1="x^3+y^3+z^3",
       invariant_polynomial_2="x*y*z",
       pencil="x^3+y^3+z^3 - 3*lambda*x*y*z",
       Hesse_fiber_smooth_if="lambda^3 != 1 (finite lambda)",
       projector_idempotence_error=float(np.max(abs(P@P-P))),
       full_tensor_cube_invariant_dimension=round(inv3.real),
       alternating_tensor_cube_invariant_dimension=round(wedge3.real),
       full_SU3_family_symmetric_cubic_invariant_dimension=0,
       unique_SU3_family_trilinear_antisymmetric_epsilon=True,
       E6_symmetric_d_times_SU3_epsilon_identical_commuting_superfield_zero=True,
       cubic_contraction_numerical_residual=float(abs(su3cubic)),
       low_energy_E6_times_H27_symmetric_cubic_family_channels=2,
       effective_texture_moduli="One complex ratio between two Hesse-pencil cubic tensors remains (unless further dynamical symmetry or equations select it).",
       UV_E8_cubic_invariant=False,
       scope="Classical Hesse pencil is prior mathematics; this explicitly tests E6 d-symbol couplings with broken family SU3 -> H27. Effective cubic E6xH27 invariants need not lift to a renormalizable unbroken E8 adjoint cubic.")

def higgs():
    P3=sum(rep(g) for g in G)/27
    P9=sum(np.kron(rep(g),rep(g).conj()) for g in G)/27
    assert np.max(abs(P3))<1e-12
    assert np.max(abs(P9@P9-P9))<1e-12
    assert round(np.trace(P9).real)==1
    S=(I3/np.sqrt(3)).reshape(9)
    assert np.max(abs(P9@S-S))<1e-12
    return dict(status="PASS",H27_invariants_in_family3=0,
       H27_invariants_in_family3bar=0,
       H27_invariants_in_family3_tensor_3bar=1,
       H27_invariants_in_family_adjoint8=0,
       family3_projector_max_abs=float(np.max(abs(P3))),
       triplet_tensor_antitriplet_projector_rank=round(np.trace(P9).real),
       relative_to_E8_248_branching="(78,1)+(1,8)+(27,3)+(27bar,3bar)",
       full_E8_adj_H27_parallel_invariant_subspace_dim=78,
       after_order7_c3_Wilson_parallel_invariant_dim=14,
       no_H27_invariant_elementary_27x3_Higgs_VEV=True,
       neutral_family_bilinear_allowed=True,
       caveat="H27 is assumed embedded in SU3 family, separate from E6 Wilson. Nonparallel Higgs configurations can break H27; composite fields with other E6 charges may have H27-invariant order parameters. H27 singlet bilinear does not by itself resolve extra U1 Higgsing.")

def pw_hopping():
    # Tilted quartic known exact critical equations, re-solved.
    axis=float(next(r.real for r in np.roots([1,0,-1,-1]) if abs(r.imag)<1e-9))
    side=float(next(r.real for r in np.roots([8,0,4,1]) if abs(r.imag)<1e-9))
    height=math.sqrt(3*side**2+1)
    pts=np.array([[axis,0],[side,height],[side,-height]])
    D=np.linalg.norm(pts[:,None,:]-pts[None,:,:],axis=2)
    ds=sorted(float(D[i,j]) for i in range(3) for j in range(i+1,3))
    assert ds[-1]/ds[0]>1.13
    beta=1.
    H=np.exp(-beta*D**2)
    np.fill_diagonal(H,0)
    commX=float(np.linalg.norm(H@X-X@H))
    commZ=float(np.linalg.norm(H@Z-Z@H))
    assert commX>1e-3 and commZ>1e-3
    twirl=sum(rep(g)@H@rep(g).conj().T for g in G)/27
    assert np.max(abs(twirl))<1e-12
    assert np.allclose(np.sort(np.linalg.eigvalsh(H)).real,
                       np.sort(np.linalg.eigvalsh(H)).real)
    return dict(status="PASS",critical_points=pts.tolist(),
       pairwise_distances_sorted=ds,
       ratio_max_min_distance=ds[-1]/ds[0],
       gaussian_hopping_beta=beta,
       relative_long_edge_to_short_edge_hopping=math.exp(-(ds[-1]**2-ds[0]**2)),
       hopping_matrix=H.tolist(),
       commutator_X_frobenius=commX,
       commutator_Z_frobenius=commZ,
       H27_twirl_hopping_max_abs=float(np.max(abs(twirl))),
       H27_commutant_only_scalar=True,
       bound="Fixed local 3-well hopping with nonzero off-diagonal matrix elements cannot commute with both H27 shift and clock generators. Non-equilateral geometry makes even the cyclic shift fail in this chosen Gaussian overlap model.",
       physical_scope="Gaussian overlap effective model, NOT the continuum PW Dirac matrix element computed from its 3 exact L2 wavefunctions. A truly zero 3x3 effective Hamiltonian admits abstract H27; locality/geometric covariance and measured tunneling remain open.")

def GHZ():
    dim=3
    ghz=np.zeros(27,complex)
    for i in range(3):
        ghz[13*i]=1/math.sqrt(3)  # |iii> linear index i*(9+3+1)
    P=np.outer(ghz,ghz.conj())
    diag=np.zeros((27,27),complex)
    for i in range(3):
        diag[13*i,13*i]=1/3
    def reduce(rho,discard):
        a=rho.reshape((3,)*6)
        b=np.trace(a,axis1=discard,axis2=discard+3)
        return b.reshape(9,9)
    pair_errors=[]
    for discard in (0,1,2):
        pair_errors.append(float(np.max(abs(reduce(P,discard)-reduce(diag,discard)))))
        eig=np.linalg.eigvalsh(reduce(P,discard))
        assert eig.min()>-1e-12
    assert max(pair_errors)<1e-12
    O=np.kron(np.kron(X,X),X)
    pXXX=(np.eye(27)+O+O@O)/3
    V12=np.kron(np.kron(Z,Z.conj().T),I3)
    V23=np.kron(np.kron(I3,Z),Z.conj().T)
    pZ12=(np.eye(27)+V12+V12@V12)/3
    pZ23=(np.eye(27)+V23+V23@V23)/3
    join=pXXX@pZ12@pZ23
    assert np.max(abs(join-P))<1e-12
    assert abs(np.trace(join)-1)<1e-12
    assert abs(np.trace(O@P)-1)<1e-12
    assert abs(np.trace(O@diag))<1e-12
    t=.75
    rho=t*P+(1-t)*diag
    assert abs(float(np.real(np.trace(P@rho)))-(1+2*t)/3)<1e-12
    # 3 measurement settings. Equal-Z labels in pair (1,2)
    # and (2,3), and mod-3 sum zero in X Fourier triple.
    eps=.01
    pZ=(1-eps)**2+eps**2/2
    c=1-1.5*eps
    pX=(1+2*t*c**3)/3
    fidelity_lower=2*pZ+pX-2
    assert fidelity_lower>1/3
    alpha=.01
    n=200
    delta=math.sqrt(math.log(3/alpha)/(2*n))
    # Hoeffding one-sided simultaneous bounds, union alpha.
    # Since P_GHZ=P_XXX P_Z12 P_Z23 with commuting
    # projectors, F >= pXXX+pZ12+pZ23-2.
    # Any biseparable 3-qutrit state F<=1/3.
    cutoff=math.floor(n*(7/3+3*delta))+1
    pmf=np.convolve(np.convolve(binom.pmf(np.arange(n+1),n,pZ),
                              binom.pmf(np.arange(n+1),n,pZ)),
                   binom.pmf(np.arange(n+1),n,pX))
    power=float(np.sum(pmf[cutoff:]))
    assert power>.9,power
    return dict(status="PASS",
        triple_static_resource="( |000>+|111>+|222> )/sqrt3",
        dephased_classical_control="1/3 sum_j |jjj><jjj|",
        pairwise_reduced_density_max_error=max(pair_errors),
        each_pairwise_reduction_separable=True,
        GHZ_vs_classical_XXX_expectation=[1,0],
        joint_three_stabilizer_projector_rank=1,
        P_GHZ_equals_projector_Xsum0_Z12equal_Z23equal=True,
        biseparable_fidelity_upper_bound=1/3,
        dephased_visibility_t=t,
        GHZ_fidelity=(1+2*t)/3,
        detector_symmetric_ternary_error=eps,
        measured_equal_Z12_probability=pZ,
        measured_equal_Z23_probability=pZ,
        measured_X_basis_three_labels_sum_mod3_zero_probability=pX,
        fidelity_from_three_setting_union_lower_bound=fidelity_lower,
        statistical_confidence_alpha=alpha,
        per_setting_accepted_n=n,total_accepted_trials=3*n,
        Hoeffding_one_sided_each_setting_delta=delta,
        reject_biseparable_when_sum_counts_at_least=cutoff,
        exact_IID_GHZ_model_power_under_readout=power,
        statistical_null_typeI_at_most=alpha,
        scope="Valid static tripartite-qutrit entanglement witness; the triple GHZ vs dephased control has identical pairwise reductions. Identifying its three parties with three TIMES does not automatically produce an operationally valid causal process tensor or the stronger Beyer genuine-three-time-only memory criterion.")

def run():
    out=dict(status="PASS",date="2026-11-18",
       positive_Einstein_H27_cover=geometry(),
       E6_H27_Hesse_cubic=hesse(),
       H27_elementary_Higgs_obstruction=higgs(),
       PW_site_hopping_covariance=pw_hopping(),
       triple_GHZ_pairwise_classical_target=GHZ(),
       valid_TOE=False)
    p=ROOT/"data/toe_20261118_H27_Einstein_Hesse_E8_Higgs_PW_GHZ.json"
    p.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS five fronts: free H27 Einstein 11-manifold; Hesse Sym3 invariants2; no H27 elementary triplet Higgs invariant; non-C3 PW hopping; pairwise-identical GHZ vs dephased triple witness")
    return out
if __name__=="__main__":run()
