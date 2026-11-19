"""Five connected TOE falsifiers and a causal-break qutrit control.

New relative to earlier work: H27 cannot be a free round-sphere deck group;
compact nearly-parallel G2 plus flat gauge twist has a universal Dirac gap;
the actual E8 Wilson centralizer's *parallel* adjoint Higgs cannot lift its
three central U1s; tensoring a 3-spatial-mode PW family by an INDEPENDENT
rank-3 H27 coefficient gives nine modes, not three; and an explicit noisy
qutrit SWAP/causal-break memory is tested with four local MUB readouts.

Prior art (already in the repo): H27 9x1D+2x3D reps, PW 3 L2 modes,
qutrit SWAP+break simulator, MUB Schmidt-number witness, E6 c=3 Wilson.
This adds independent cross-front obstructions and combined noise budgets,
not experimental apparatus or a solved higher-dimensional E8/G2 theory.
"""
from pathlib import Path
import json,math
from itertools import product
import numpy as np
import sympy as s
from scipy.stats import binom
import toe_20261118_E8_248_relative_Psi_G2_MUB as PREV

ROOT=Path(__file__).resolve().parents[1]
w=np.exp(2j*np.pi/3)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
Z=np.diag([1,w,w*w])

def hmul(g,h):
    a,b,c=g; A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C+a*B)%3)

def hinv(g):
    a,b,c=g
    return ((-a)%3,(-b)%3,(-c+a*b)%3)

def heisenberg_IR():
    G=list(product(range(3),repeat=3))
    identity=(0,0,0)
    center=[g for g in G if all(hmul(g,h)==hmul(h,g) for h in G)]
    assert center==[(0,0,0),(0,0,1),(0,0,2)]
    classes=[]
    remaining=set(G)
    while remaining:
        g=min(remaining)
        orbit={hmul(hmul(k,g),hinv(k)) for k in G}
        assert orbit.issubset(remaining)
        remaining-=orbit
        classes.append(sorted(orbit))
    assert len(classes)==11
    chars=[]
    for u,v in product(range(3),repeat=2):
        chars.append([w**(u*a+v*b) for a,b,c in G])
    for q in (1,2):
        chars.append([3*w**(q*c) if a==b==0 else 0 for a,b,c in G])
    gram=np.array(chars)@np.array(chars).conj().T/27
    assert np.max(abs(gram-np.eye(11)))<1e-12
    dims=[1]*9+[3,3]
    assert sum(x*x for x in dims)==27
    assert all(abs(chars[i][G.index((0,0,1))]-3*w**q)<1e-12
               for i,q in ((9,1),(10,2)))
    return dict(status="PASS",order=27,conjugacy_class_count=11,
        class_sizes=sorted(len(x) for x in classes),
        irreducible_dimensions=dims,sum_of_squares=27,
        all_one_dimensional_center_characters_trivial=True,
        two_nontrivial_center_characters=["omega","omega^2"],
        faithful_center_irreducible_dimension=3,
        irreducible_family_triplet_conditional=True,
        multiplication="(a,b,c)(A,B,C)=(a+A,b+B,c+C+aB) mod3",
        character_orthogonality_error=float(np.max(abs(gram-np.eye(11)))),
        prior_art="Irrep inventory is already proved in the repo (2026-09-22 address/operator H27 intertwiner). This PASS checks it independently and connects it to geometric obstructions.",
        caveat="A nontrivial H27 central character plus irreducibility implies rank3, but neither H27 dynamics nor physical irreducibility nor a choice between the two conjugate center characters is derived.")

def spherical_H27_obstruction():
    # H27 has abelian A=< (0,1,0),(0,0,1)> isomorphic C3 x C3.
    A=[(0,b,c) for b,c in product(range(3),repeat=2)]
    assert len(A)==9
    assert all(hmul(x,y)==hmul(y,x) for x,y in product(A,repeat=2))
    assert all(hmul(hmul(g,g),g)==(0,0,0) for g in A)
    assert all(not (hmul(g,g)==(0,0,0)) for g in A if g!=(0,0,0))
    ker=[]
    for u,v in product(range(3),repeat=2):
        zeros=[(b,c) for b,c in product(range(3),repeat=2)
               if (u*b+v*c)%3==0]
        ker.append(len(zeros))
        assert len(zeros)>=3
    assert ker==[9]+[3]*8
    # Every complex representation of the finite abelian subgroup A
    # diagonalizes into chars chi_(u,v). Each eigenline has a
    # nonidentity element in its kernel, fixing a nonzero vector.
    # Thus NO orthogonal (real) linear action of H27 on S^(n-1)
    # can be free, for any n. General free TOPOL sphere actions are
    # excluded by the periodic-cohomology criterion.
    return dict(status="PASS",
      abelian_subgroup="C3 x C3",subgroup_order=9,
      all_nine_character_kernel_sizes=ker,
      nontrivial_fixed_eigenline_for_every_linear_H27_rep=True,
      free_orthogonal_action_on_any_round_sphere_possible=False,
      free_topological_action_on_any_standard_sphere_possible=False,
      theorem="Finite groups acting freely on spheres have periodic group cohomology and all abelian subgroups cyclic. H27 contains C3xC3.",
      physical_scope="No smooth spherical space form S7/H27 with free deck action; NOT a no-go for H27 as gauge holonomy on a defect complement, finite quotient of pi1 on a DIFFERENT positive-Einstein manifold, or an orbifold with fixed points.")

def nearlyG2_gap():
    tau,L=s.symbols("tau L",positive=True)
    ric=s.Rational(3,8)*tau*tau
    scalar=s.simplify(7*ric)
    gap=s.simplify(scalar/4)
    myers_k=s.simplify(ric/6)
    diam=s.simplify(s.pi/s.sqrt(myers_k))
    assert scalar==s.Rational(21,8)*tau*tau
    assert gap==s.Rational(21,32)*tau*tau
    assert myers_k==tau*tau/16
    assert s.simplify(diam.subs(tau,2/L)-2*s.pi*L)==0
    assert s.simplify(gap.subs(tau,2/L)-s.Rational(21,8)/L**2)==0
    return dict(status="PASS",dimension=7,
       assumption="smooth closed spin nearly parallel G2, tau0 nonzero; ordinary geometric Dirac with a unitary FLAT Hermitian gauge bundle",
       Ricci_coefficient="3*tau0^2/8",
       scalar_curvature="21*tau0^2/8",
       twisted_Lichnerowicz="D_A^2=nabla_A^*nabla_A+Scal/4 for flat A",
       Dirac_squared_spectral_lower_bound="21*tau0^2/32",
       at_tau0_2_overL_Dirac_squared_L2_lower_bound="21/8",
       no_ordinary_flat_twisted_Dirac_zero_modes=True,
       Myers_diameter_upper_bound="4*pi/abs(tau0)",
       Myers_at_tau0_2_overL_diameter_upper_bound="2*pi*L",
       fundamental_group_finite=True,
       real_first_cohomology_zero=True,
       source_free_closed_harmonic_real_one_forms_zero=True,
       nonflat_gauge_curvature_Clifford_endomorphism_norm_necessary="operator norm K >= 21*tau0^2/32 somewhere for zero modes; otherwise Weitzenbock form remains strictly positive",
       caveat="No-go is for smooth closed positive-scalar geometry, ordinary gauge-Dirac with FLAT unitary twist and no boundary/singular contribution. Does not apply to charged 7D ADE defects, torsion/flux-modified supercovariant operators, nonflat curvature or spinors with physical boundary projectors.")

def centralizer_Higgs_and_overcount():
    e6w,wp,splits=PREV.weights_E6(3)
    assert len(e6w)==78
    assert splits["total_E6_78_fixed"]==14
    assert splits["E6_16minus3_fixed"]==0
    assert splits["E6_16barplus3_fixed"]==0
    assert splits["SU5_adjoint_24_fixed"]==12
    # E8 centralizer under the physical c3 combined Wilson and H27
    # is su3_color(8)+su2_weak(3)+u1^3(3)=14.
    # The CENTER of this lie algebra is a 3d u1^3. EVERY
    # covariantly constant adjoint Higgs is valued in h, hence
    # commutes with all three centers and cannot break them.
    assert 8+3+3==14
    # For the separate scalar PW 3-dimensional L2 kernel,
    # if an independent 3-dimensional H27 family fiber is
    # trivially tensored, the kernel is 9, not3.
    Q=s.diag(0,0,0,2,5)
    qt=s.kronecker_product(Q,s.eye(3))
    assert Q.nullspace().__len__()==3
    assert qt.nullspace().__len__()==9
    # Independently re-solve the previous three critical positions
    # for the tilted quartic f=Re(w^4)/4-|w|^2/2+z^2-x.
    # Their triangle is ISOSCELES but NOT equilateral, hence no
    # Euclidean order-three spatial rotation cycles the three sites.
    axis=[float(z.real) for z in np.roots([1,0,-1,-1])
          if abs(z.imag)<1e-10][0]
    side=[float(z.real) for z in np.roots([8,0,4,1])
          if abs(z.imag)<1e-10][0]
    height=float(np.sqrt(3*side*side+1))
    points=[(axis,0.),(side,height),(side,-height)]
    lengths=sorted(float(np.linalg.norm(np.array(points[i])-np.array(points[j])))
                   for i in range(3) for j in range(i+1,3))
    ratio=lengths[-1]/lengths[0]
    assert ratio>1.13 and ratio<1.15
    return dict(status="PASS",
       Wilson_E6_c3_unbroken_algebra="su3 + su2 + u1^3",
       Wilson_E6_c3_unbroken_dimension=14,
       residual_center_dimension=3,
       residual_extra_U1_beyond_SM=2,
       all_globally_covariantly_parallel_adjoint_VEVs_preserve_at_least_U1_cubed=True,
       reason="Any global parallel adjoint VEV lives in the holonomy centralizer h. The center z(h)=u1^3 commutes with EVERY VEV in h, even several noncommuting ones.",
       spatial_PW_scalar_L2_zero_modes=3,
       independent_H27_Schrodinger_family_fiber_dim=3,
       naive_commuting_tensored_L2_zero_modes=9,
       multiplicity_matrix_example="Q=diag(0,0,0,2,5); dim ker(Q tensor I3)=9",
       tilted_quartic_critical_points_xy=[list(v) for v in points],
       tilted_quartic_triangle_distances=lengths,
       tilted_quartic_triangle_longest_over_shortest=ratio,
       tilted_quartic_has_euclidean_C3_rotation_permuting_sites=False,
       non_double_count_option="Use the 3D spatial zero-mode space itself as the H27 triplet, or add non-Abelian mixing that removes unwanted degeneracy; cannot multiply two independently supplied triplets and still call result 3.",
       physics_limit="This does NOT prohibit nonparallel/charged Higgs sections, a nonflat gauge profile, source-localized Higgs, nonlinear index coupling or nontrivial global family-bundle gluing. The PW scalar kernel and H27 fiber were only tensored in a conditional product ansatz.")

def qutrit_causal_break():
    d=3
    I=np.eye(d)
    phi=np.zeros(d*d,complex)
    initial=np.zeros((d,d,d),complex)
    for k in range(d):
        phi[d*k+k]=1/np.sqrt(d)
        initial[k,k,0]=1/np.sqrt(d)
    v=initial.reshape(d**3)
    rho=np.outer(v,v.conj())
    P=np.outer(phi,phi.conj())
    def swapSE(a):
        return a.reshape((d,)*6).transpose(0,2,1,3,5,4).reshape(d**3,d**3)
    def traceE(a):
        return np.trace(a.reshape((d,)*6),axis1=2,axis2=5).reshape(d*d,d*d)
    def resetS(a,k):
        re=np.trace(a.reshape((d,)*6),axis1=1,axis2=4)
        sig=np.zeros((d,d));sig[k,k]=1
        return np.einsum("abcd,ij->aibcjd",re,sig).reshape(d**3,d**3)
    def depolE(a,t):
        rs=np.trace(a.reshape((d,)*6),axis1=2,axis2=5)
        return t*a+(1-t)*np.einsum("abcd,ef->abecdf",rs,I/d).reshape(d**3,d**3)
    def dephaseE(a):
        a=a.reshape((d,)*6).copy()
        for j in range(d):
            for k in range(d):
                if j!=k:a[:,:,j,:,:,k]=0
        return a.reshape(d**3,d**3)
    first=swapSE(rho)
    before_break=traceE(first)
    assert np.max(abs(before_break-np.kron(I/d,np.diag([1,0,0]))))<1e-12
    pure=[];classical=[];noisy={}
    for k in range(3):
        out=traceE(swapSE(resetS(first,k)))
        pure.append(out)
        outc=traceE(swapSE(resetS(dephaseE(first),k)))
        classical.append(outc)
        for t in (0.,.25,.5,.625,.75,1.):
            outt=traceE(swapSE(resetS(depolE(first,t),k)))
            expected=t*P+(1-t)*np.eye(9)/9
            assert np.max(abs(outt-expected))<1e-12
            noisy[t]=outt
    assert all(np.max(abs(out-P))<1e-12 for out in pure)
    F_classical=[float(np.real(phi.conj()@c@phi)) for c in classical]
    assert np.max(abs(np.array(F_classical)-1/3))<1e-12
    def witness(a):
        F=float(np.real(phi.conj()@a@phi))
        return F,(1+3*F)/4
    F2,p2=witness(noisy[.75])
    assert abs(F2-7/9)<1e-12 and abs(p2-5/6)<1e-12
    # The four MUB measurement identity has been verified in the
    # immediately preceding a3ec818a3 commit. Rebuild it here from
    # independent qutrit Weyl eigenbases as a control.
    omega=np.exp(2j*np.pi/3)
    X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    Z=np.diag([1,omega,omega**2])
    bases=[np.eye(3)]
    for U in (X,X@Z,X@Z@Z):
        vals,eig=np.linalg.eig(U)
        bases.append(eig)
    Match=np.zeros((9,9),complex)
    for U in bases:
        for j in range(3):
            x=U[:,j]
            v=np.kron(x,x.conj())
            Match+=np.outer(v,v.conj())
    identity_error=float(np.max(abs(Match-np.eye(9)-3*P)))
    assert identity_error<2e-12
    assert abs(float(np.real(np.trace(Match@noisy[.75])))/4-p2)<1e-12
    # One-sided exact binomial threshold for accepted independent
    # local-MUB trials under *declared* null p0, model alt p1.
    def design(p0,p1):
        for n in range(1,1800):
            k=int(binom.isf(.01,n,p0))+1
            while binom.sf(k-1,n,p0)>.01:k+=1
            while k>1 and binom.sf(k-2,n,p0)<=.01:k-=1
            power=float(binom.sf(k-1,n,p1))
            if power>=.90:
                return dict(accepted_trials=n,min_matches=k,
                            exact_typeI=float(binom.sf(k-1,n,p0)),
                            design_power=power)
        raise AssertionError("horizon")
    # Classical-memory channels produce separable R:S after a genuine
    # causal break, hence F<=1/3 and four-MUB match<=1/2. Intrinsic
    # qutrit Schmidt-number3 requires F>2/3, match>3/4.
    eb=design(.5,p2)
    sn3=design(.75,p2)
    assert sn3["accepted_trials"]==317 and sn3["min_matches"]==256
    readout=[]
    for eps in (0.,.01,.02):
        aa=(1-eps)**2+eps**2/2
        bb=eps*(1-eps)+eps**2/4
        def obs(p):return bb+(aa-bb)*p
        readout.append(dict(each_detector_symmetric_ternary_error=eps,
              expected_match=obs(p2),
              known_calibrated_classical_memory_null=obs(.5),
              known_calibrated_SN2_null=obs(.75),
              classical_memory_99pct_90pct_power=design(obs(.5),obs(p2)),
              intrinsic_SN3_99pct_90pct_power=design(obs(.75),obs(p2))))
    return dict(status="PASS",
       system="3 qutrit registers R reference, S input, E environment",
       circuit="prepare Bell R-S and E0; SWAP(S,E); channel noise on E; trace-reset S to arbitrary computational k; SWAP(S,E); measure R-S in four local MUBs",
       coherent_output_fidelity=1.,
       dephased_environment_classical_memory_fidelity=F_classical[0],
       no_memory_depolarized_environment_fidelity=1/9,
       visibility_t=.75,expected_return_fidelity=F2,
       expected_local_MUB_match=p2,
       four_MUB_2design_residual=identity_error,
       independently_prepared_middle_reset_values=[0,1,2],
       exact_CPTP_output_residual_max=max(float(np.max(abs(noisy[t]-(t*P+(1-t)*np.eye(9)/9)))) for t in noisy),
       entanglement_breaking_classical_memory_fidelity_bound=1/3,
       intrinsic_qutrit_SN2_fidelity_bound=2/3,
       classical_memory_fixed_n_99pct_typeI_90pct_power=eb,
       intrinsic_qutrit_fixed_n_99pct_typeI_90pct_power=sn3,
       detector_symmetric_ternary_error_designs=readout,
       status_of_2026_Beyer_genuine_three_time_only_target="NOT_PROVEN: restores two-time R-S entanglement across a causal break, but early-late effective channel is non-EB; stronger pairwise-classical triple incompatibility remains open",
       physical_limit="Ideal full density matrix control. No real photon circuit, calibrated detector, loss guarantee, event-ready reference, photonic causal-break exclusion, timing loophole, noise provenance or measured process tensor.")

def run():
    data=dict(status="PASS",date="2026-11-18",
      finite_H27_families=heisenberg_IR(),
      spherical_space_form_no_go=spherical_H27_obstruction(),
      smooth_nearlyG2_flat_Dirac_no_go=nearlyG2_gap(),
      E8_parallel_Higgs_and_family_multiplicity=centralizer_Higgs_and_overcount(),
      qutrit_controlled_memory=qutrit_causal_break(),
      no_TOE_claim=True)
    p=ROOT/"data/toe_20261118_H27_G2_flat_Higgs_qutrit_break.json"
    p.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("PASS: H27 irrep dimension3 iff nontrivial center and irreducible; no free H27 sphere; weakG2 flat spinor gap; E8 adjoint parallel Higgs leaves U1^3; 3x3=9 mode multiplicity; noisy causal-break local-MUB genuine qutrit memory model")
    return data
if __name__=="__main__":run()
