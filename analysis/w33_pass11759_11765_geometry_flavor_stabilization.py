"""Seven exact/conditional probes continuing11742-11758.

The published rank5 alternative is Buchbinder--Constantin--Lukas1311.1941,
not a newly discovered standard model. Fivebrane reduction is9808101.
The4D racetrack is supplied EFT data, not a W33-derived compactification.
"""
from __future__ import annotations
from functools import lru_cache
import hashlib
import itertools as it
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11750_11757_integral_geometry_and_flux_dynamics as Q
N=Q.N;M=N.M
OUT=ROOT/'data/w33_pass11759_11765_geometry_flavor_stabilization.json'


def line_euler(k):
    # Tetraquadric RR, d_ijk=2 for distinct indices; c2_i=24.
    return 2*sum(s.prod(k[i] for i in ids) for ids in it.combinations(range(4),3))+2*sum(k)


def normal_representation():
    """Actual section pullbacks of D01, modulo its defining equation."""
    g=s.diag(1,-1,-1,1)
    h=s.zeros(4)
    for i in range(4):h[3-i,i]=1
    q=s.Matrix([1,0,0,1])
    # A quotient basis modulo q: first three coordinate vectors.
    B=s.Matrix.hstack(*[s.eye(4)[:,i] for i in range(3)],q)
    reps=[(B.inv()*a*B)[:3,:3] for a in (s.eye(4),g,h,g*h)]
    assert all(a*q==q for a in (g,h))
    return reps


@lru_cache(None)
def fivebrane_normal_certificate():
    reps=normal_representation();tr=[int(a.trace()) for a in reps]
    assert tr==[3,-1,-1,-1]
    invariant=sum(reps,s.zeros(3))/4;assert invariant==s.zeros(3)
    # C in S=P1xP1 of bidegree(6,2); N_C/X=O_C(2,0)^2.
    ambient=M.ambient_cohomology((2,0));shift=M.ambient_cohomology((-4,-2))
    assert ambient==[3,0,0] and shift==[0,0,3]
    # For the orbit-pair elliptic curve, only its free g-stabilizer matters.
    elliptic_g=-s.eye(2);assert (s.eye(2)+elliptic_g)/2==s.zeros(2)
    return dict(status='PASS',cover_curve_genus=5,quotient_curve_genus=2,
        cover_normal_bundle='O_C(2,0) + O_C(2,0)',cover_h0_normal=6,cover_h1_normal=6,
        each_summand_character=tr,each_summand_matrices=[a.tolist() for a in reps],
        quotient_h0_normal=0,quotient_h1_normal=0,
        elliptic_cover_normal='O_E + O_E',elliptic_cover_h0=2,elliptic_cover_h1=2,
        elliptic_stabilizer_on_normal=elliptic_g.tolist(),elliptic_quotient_h0_normal=0,elliptic_quotient_h1_normal=0,
        separated_brane_count=7,worldvolume_abelian_vector_rank=8,universal_chiral_multiplets=7,
        visible_opposite_X_fields_from_separated_bulk_brane_zero_modes=0,
        proof='H0(O_C(D01)) is H0(A,D01)/<q01>, with character regular minus trivial. The D02 summand is identical. Equivariant Serre duality on the CY gives H1(N)=H0(N)*. Each elliptic orbit quotient has translation g on E and -I on its two transverse coordinate directions. Thus every quotient component is infinitesimally rigid.',
        physical_reading='In the separated smooth bulk M5 regime, genus2 plus six genus1 branes give8 hidden U1 vector multiplets and7 universal interval/axion chirals, but no curve-deformation chirals. Multiplicities can be separated along the interval. Intersections, boundary collisions and nonabelian enhancements are outside this zero-mode calculation.',
        prior='11751 owns the effective cycle;11755 integral descent. Lukas--Ovrut--Waldram hep-th/9808101 section4.2 owns the genus-g worldvolume reduction.',
        scope='Exact equivariant normal cohomology for the generic smooth curves in the prior open family. Rigidity at fixed CY does not stabilize CY, brane positions or axions, and does not solve backreaction.')


PUBLISHED_LINES=((-1,0,0,1),(-1,-3,2,2),(0,1,-1,0),(1,1,-1,-1),(1,1,0,-2))


def ambient_multiplication(k):
    """Actual Koszul map when both ambient groups share a degree.

    H1(P1,O(k)) is represented by the Serre dual of monomials of
    degree-k-2. Multiplication by z^d therefore sends source index r
    to target index r-d. Positive factors use the ordinary r+d map.
    """
    src=tuple(a-2 for a in k)
    if -1 in k or -1 in src:return s.zeros(0)
    target=list(it.product(*[range(abs(a+1)) for a in k]))
    source=list(it.product(*[range(abs(a+1)) for a in src]))
    if sum(a<=-2 for a in k)!=sum(a<=-2 for a in src):return s.zeros(0)
    z,F,_,_=Q.reference_polynomial();coeff=dict(s.Poly(F,*z).terms())
    return s.Matrix([[coeff.get(tuple(r[i]-t[i] if k[i]<=-2 else t[i]-r[i] for i in range(4)),0)
                       for r in source] for t in target])


def exact_line_cohomology(k):
    a=M.ambient_cohomology(k);b=M.ambient_cohomology(tuple(x-2 for x in k));r=[0]*5
    for q in range(5):
        if a[q] and b[q]:r[q]=ambient_multiplication(k).rank()
    return [int(a[q]-r[q]+b[q+1]-r[q+1]) for q in range(4)]


def charge(*terms):
    out=s.zeros(5,1)
    for i,n in terms:out[i-1]+=n
    return out


@lru_cache(None)
def geometric_higgs_certificate():
    ks=PUBLISHED_LINES;assert list(map(sum,zip(*ks)))==[0]*4
    assert s.Matrix(ks).rank()==3 and all(sum(k)==0 for k in ks)
    hs=[exact_line_cohomology(k) for k in ks]
    assert hs==[[0,0,0,0],[0,8,0,0],[0,0,0,0],[0,0,0,0],[0,4,0,0]]
    wedges={str((a+1,b+1)):exact_line_cohomology(tuple(x+y for x,y in zip(ks[a],ks[b])))
            for a,b in it.combinations(range(5),2)}
    assert np.sum(list(wedges.values()),axis=0).tolist()==[0,15,3,0]
    koszul=ambient_multiplication(tuple(x+y for x,y in zip(ks[0],ks[1])))
    assert koszul.shape==(24,24) and koszul.det()!=0
    c2=[]
    for i in range(4):
        c2.append(-sum(k[j]*k[l] for k in ks for j,l in it.combinations([j for j in range(4) if j!=i],2))*2)
    assert c2==[24,8,20,12]
    # A separating charge covector certifies exclusion at every nonnegative
    # insertion order, not merely below a finite monomial-degree cutoff.
    separator=s.Matrix([-2,1,-2,2,1]);assert sum(separator)==0
    singlets={(a,b):charge((a,1),(b,-1)) for a,b in ((2,1),(5,1),(2,3),(5,3))}
    assert all((separator.T*q)[0]==3 for q in singlets.values())
    tens=[charge((a,1)) for a in (2,5)]
    matters=[charge((2,1),(4,1)),charge((4,1),(5,1))]
    hu=charge((2,-1),(5,-1));hd=-hu
    dim4=[(separator.T*(a+b+c))[0] for a,b,c in it.product(tens,matters,matters)]
    dim5=[(separator.T*(a+b+c+d))[0] for a,b,c,d in it.product(tens,tens,tens,matters)]
    down=[(separator.T*(a+b+hd))[0] for a,b in it.product(tens,matters)]
    assert set(dim4)=={7} and set(dim5)=={6} and set(down)=={6}
    assert hu+hd==s.zeros(5,1) # Direct mu is gauge allowed: do not over-read.
    return dict(status='PASS',published_line_degrees=[list(k) for k in ks],rank=3,
        cover_h_V=hs,cover_h_wedge2=wedges,total_cover_h_wedge2=[0,15,3,0],c2_pairings=c2,
        actual_L1L2_Koszul_map=koszul.tolist(),actual_L1L2_Koszul_determinant=str(koszul.det()),
        index_V=int(sum(line_euler(k) for k in ks)),slope_zero_point=[1,1,1,1],
        prior_downstairs_spectrum='Published1311.1941 eq5.8:3families,1Higgs doublet pair, no colored Higgs triplets,15 bundle singlets for an appropriate equivariance/Wilson line.',
        verified_here='Exact cover line cohomologies, wedge spectrum, index, c2 and slope point; no new full Wilson-line action is reconstructed.',
        allowed_singlet_VEVs=[list(x) for x in singlets],forbidden_Higgs_mixing_VEV=[2,4],
        charge_separator=list(map(int,separator)),singlet_separator_weights=[3]*4,
        dangerous_dim4_weights=sorted(set(map(int,dim4))),dangerous_dim5_weights=sorted(set(map(int,dim5))),
        down_Yukawa_weights=sorted(set(map(int,down))),all_orders_holomorphic_cone_exclusion=True,
        direct_mu_charge_zero=True,
        up_matrix='[[0,0,l1],[0,0,l2],[l1,l2,0]]',generic_up_rank=2,
        scope='A replay and explicit all-order selection-cone certificate for a published alternative SU5 bundle, not a new standard model or W33-selected vacuum. It avoids the prior cubic Higgs inventory but perturbative down Yukawas vanish; direct mu is gauge allowed, although the selected cohomology has massless Higgs at the Abelian locus. Nonperturbative mu/proton and stable deformation checks remain required.',
        literature='https://arxiv.org/abs/1311.1941')


@lru_cache(None)
def flavor_circuit_certificate():
    edges=[];values=[]
    for a,b in it.product(range(4),repeat=2):
        c=N.CHARS.index(tuple(x*y for x,y in zip(N.CHARS[a],N.CHARS[b])))
        chars=(N.CHARS[a],N.CHARS[b],N.CHARS[c])
        edges.append((a,b,c));values.append(s.Rational(N.cup(*[N.character_vector(ac,ch) for ac,ch in zip(N.cohomology_actions(),chars)]),4))
    incidence=s.zeros(12,16)
    for j,e in enumerate(edges):
        for f,a in enumerate(e):incidence[4*f+a,j]=1
    circuits=[]
    for v in incidence.nullspace():
        v=v*s.ilcm(*[x.q for x in v]);v=v/s.igcd(*v)
        assert incidence*v==s.zeros(12,1) and sum(v)==0
        value=s.prod(y**int(a) for y,a in zip(values,v))
        assert value in (-1,1)
        circuits.append(dict(exponents=list(map(int,v)),exact_value=str(value)))
    assert incidence.rank()==10 and len(circuits)==6
    # Rephase/rescale all12 fields by arbitrary nonzero Gaussian rationals.
    scales=[s.Rational(i+2,i+1)*(1+s.I*(i%3)) for i in range(12)]
    transformed=[values[j]/s.prod(scales[4*f+a] for f,a in enumerate(e)) for j,e in enumerate(edges)]
    for row in circuits:
        assert s.simplify(s.prod(y**a for y,a in zip(transformed,row['exponents']))-s.sympify(row['exact_value']))==0
    return dict(status='PASS',characters=[list(c) for c in N.CHARS],edges=[list(e) for e in edges],
        holomorphic_values=list(map(str,values)),incidence=incidence.tolist(),incidence_rank=10,
        independent_rational_circuits=6,circuits=circuits,
        physical_normalization_rule='Y_e=e^(K4/2) lambda_e / product_(v in e)sqrt(Z_v). For every integer incidence-kernel vector, product Y_e^v_e=product lambda_e^v_e exactly, if the12 kinetic sectors are one-dimensional and diagonal.',
        phase_reading='Some circuits equal-1: they obstruct making every nonzero coefficient simultaneously positive by field phases. All coefficients are nevertheless real, so this is not CP violation.',
        physical_scope='These are relations in the cover-character cubic or a quotient realization retaining the required character/gauge sectors. A single fixed triple of quotient lines has only one coupling, so it has no nontrivial circuit; no mass or CKM prediction follows. General off-diagonal mixing would invalidate diagonal normalization cancellation.',
        prior='11742/11749 own the16 character-compatible cups and their nonvanishing. The addition is an explicit integer-kernel map and six checked normalization/rephasing-invariant relations, not new cup values.')


def invariant_curve_lattice(a,b):return (a,b,2*a-b,3*b)
INSTANTON_GENERATORS=((4,0,8,0),(2,2,2,6),(4,8,0,24))
GENUS_ZERO_NECESSARY_GENERATORS=((4,0,8,0),(4,4,4,12),(4,8,0,24))


@lru_cache(None)
def instanton_lattice_certificate():
    K=s.Matrix(N.K);generators=INSTANTON_GENERATORS
    assert all(K*s.Matrix(q)==s.zeros(3,1) for q in generators)
    assert s.Matrix(generators[0])+s.Matrix(generators[2])==4*s.Matrix(generators[1])
    checked=0
    for a,b in it.product(range(0,41),repeat=2):
        q=invariant_curve_lattice(a,b)
        if min(q)<0 or any(v%2 for v in q) or len({v%4 for v in q})!=1:continue
        # Exact decomposition: use qB until the remaining lattice point is
        # on one extremal ray. The inequalities split at b=a.
        if b<=a:coeff=((a-b)//4,b//2,0)
        else:coeff=(0,a-b//2,(b-a)//4)
        assert all(c>=0 for c in coeff)
        assert tuple(sum(c*g[i] for c,g in zip(coeff,generators)) for i in range(4))==q
        checked+=1
    rational_generators=GENUS_ZERO_NECESSARY_GENERATORS
    assert s.Matrix(rational_generators[0])+s.Matrix(rational_generators[2])==2*s.Matrix(rational_generators[1])
    for m,n in it.product(range(41),repeat=2):
        if n>2*m:continue
        q=invariant_curve_lattice(4*m,4*n)
        cs=(m-n,n,0) if n<=m else (0,2*m-n,n-m)
        assert tuple(sum(c*g[i] for c,g in zip(cs,rational_generators)) for i in range(4))==q
    return dict(status='PASS',kernel_parameterization='q=(a,b,2a-b,3b)',
        integral_quotient_curve_lattice='q_i even and all q_i congruent mod4, using11755 pullback in J-pairings',
        generators=[list(q) for q in generators],relation='qA+qC=4qB',bounded_decomposition_checks=checked,
        proof='Write a=2m,b=2n with m=n mod2 and0<=n<=2m. If b<=a subtract (b/2)qB, leaving ((a-b)/4)qA; otherwise subtract (a-b/2)qB, leaving ((b-a)/4)qC. Thus the three generators span the entire nonnegative integral gauge-neutral semigroup.',
        neutral_anomaly_curve='The actual connected genus2 quotient curve from11751 pulls back to qB=(2,2,2,6), so one Hilbert generator has a named effective representative. Its genus2 representative is not a rational worldsheet instanton; individual elliptic components carry nonzero K degrees, computed in11763.',
        genus_zero_transfer_divisor=4,
        primitive_qB_genus_zero_excluded=True,odd_multiples_qB_genus_zero_excluded=True,
        genus_zero_necessary_generators=[list(q) for q in rational_generators],
        genus_zero_necessary_relation='qA+qC=2qD, qD=2qB',
        genus_zero_proof='For pi:X->Y free of degree4, every map P1->Y lifts to X because P1 is simply connected. Transfer of its pushforward class is the sum of four deck translates. The diagonal action is trivial on H2(X,Z)=Z4 (11755), so transfer equals4 times an integral class; all J-pairings must be divisible by4. Componentwise the argument also applies to genus-zero stable maps. Thus no genus-zero map represents qB or an odd multiple, independent of which curve representative is chosen. Conversely divisibility is only necessary. For q=(4m,4n,8m-4n,12n),0<=n<=2m, use coefficients(m-n,n,0) if n<=m, otherwise(0,2m-n,n-m).',
        genus_zero_literature='The lifting argument is standard covering-space topology. Applied here to11755 integral classes; quotient worldsheet instantons and possible cancellations are discussed in Buchbinder--Lukas--Ovrut--Ruehle1707.07214, section3.3. No new general covering theorem is claimed.',
        Pfaffian_boundary='Necessary charge/topological classes only. Existence of a rational holomorphic representative, its Pfaffian and any Beasley-Witten sum cancellation are uncomputed. Genus1/2 anomaly curves are not automatically superpotential-generating rational worldsheet instantons.',
        scope='The actual linear gauge-neutrality and integral descent conditions for the declared leading axion action; one-loop dilaton shifts and charged Pfaffians may modify allowed terms.')


@lru_cache(None)
def four_dimensional_certificate():
    # Explicit4D N=1 EFT with five chiral moduli and two gauged axion shifts.
    # W=sum(exp(-(U-U0))-1)^2 is engineered, not dynamically selected.
    t=s.symbols('t0:4',positive=True);sv=s.symbols('s',positive=True)
    volume=s.Rational(1,2)*sum(s.prod(t[i] for i in ids) for ids in it.combinations(range(4),3))
    ka=-s.log(2*sv)-s.log(volume)
    xs=(sv,*t);point=[s.Integer(10),*[s.sympify(x) for x in N.flavor_certificate()['positive_Kahler_point']]]
    sub=dict(zip(xs,point));metric=s.hessian(ka,xs)/4
    g=np.array(metric.subs(sub)).astype(float);assert np.linalg.eigvalsh(g).min()>0
    # Charges act on T only; K3=-K1-K2. D_a=K_a dot grad_t logV/2.
    charge_matrix=s.Matrix([[0,*k] for k in N.K[:2]])
    ds=[-sum(k[i]*s.diff(ka,t[i]) for i in range(4))/2 for k in N.K[:2]]
    assert all(s.simplify(d.subs(sub))==0 for d in ds)
    dd=s.Matrix([[s.diff(d,x) for x in xs] for d in ds])
    dd0=np.array(dd.subs(sub)).astype(float)
    U=s.Matrix([[1,0,0,0,0],[0,*GENUS_ZERO_NECESSARY_GENERATORS[0]],[0,*GENUS_ZERO_NECESSARY_GENERATORS[1]]])
    assert U*charge_matrix.T==s.zeros(3,2) and U.rank()==3
    # At U0: W=DW=0 and Hess W=2 U^T U exactly.
    wh=2*U.T*U;assert wh.rank()==3
    whn=np.array(wh).astype(float);ek=float(s.exp(ka.subs(sub)))
    HF=2*ek*whn@np.linalg.inv(g)@whn
    HD=dd0.T@dd0
    vals,vecs=np.linalg.eigh(2*g);ginvhalf=(vecs/np.sqrt(vals))@vecs.T
    real=np.linalg.eigvalsh(ginvhalf@(HF+HD)@ginvhalf)
    imaginary=np.linalg.eigvalsh(ginvhalf@HF@ginvhalf)
    # Algebraic rank and positivity proofs survive numerical conditioning.
    assert s.Matrix.vstack(U,charge_matrix*metric.subs(sub)).rank()==5
    assert np.min(real)>0 and sum(v>1e-7 for v in imaginary)==3
    return dict(status='PASS',action='S4=integral sqrt(-g)[M_P^2 R/2-K_IbarJ D zI Dbar zJ-VF-VD-1/4 f_ab F_a F_b]',
        CY_quotient_volume=str(volume),Kahler_potential=str(ka),Kahler_metric_at_point=g.tolist(),
        point=list(map(str,point)),gauged_axion_shifts=charge_matrix.tolist(),
        invariant_modulus_map=U.tolist(),superpotential='W=sum_(a=1)^3 (exp(-(U_a-U_a0))-1)^2',
        coefficient_origin='Supplied tuned constants include exp(U_a0); expand each square into constant,exp(-U_a),exp(-2U_a). Uses qD=2qB because the primitive qB is excluded by genus-zero transfer divisibility (11764). Divisibility does not establish instanton existence. No instanton amplitudes or hidden-condensate coefficients are derived.',
        W_at_point=0,DW_at_point=[0]*5,D_terms_at_point=[0,0],VF_at_point=0,
        exact_superpotential_hessian=wh.tolist(),real_scalar_mass_squared=real.tolist(),
        axion_mass_squared_before_unitary_gauge=imaginary.tolist(),eaten_axions=2,physical_massive_real_scalars=8,
        exact_stability_proof='At W=DW=D=0 the scalar quadratic form is a sum of positive norms. Hess W has rank3 and kernel exactly the two axion-charge directions. The D Jacobian removes the two real partners because the positive Kahler metric is nondegenerate on the rank2 charge span. Two imaginary zero directions are gauge, leaving eight positive real scalar modes.',
        origin='Classical4D N=1 CY moduli EFT and racetracks are prior literature;1102.0011 stresses anomalous-U1 restrictions. The addition is a fully explicit conditional witness on the actual11742 slope locus with integral neutral exponent vectors.',
        scope='A mathematically stable supersymmetric Minkowski vacuum of a supplied4D EFT. Not a derived W33 spacetime, natural vacuum selection, verified string instanton potential, backreacted compactification or observed cosmological constant. The separate3D E8 flux construction is not identified with this4D CY reduction.')


@lru_cache(None)
def interval_source_certificate():
    connected=(1,1,1,3);orbit_rows=[((0,1),2),((0,3),1),((1,2),1),((2,3),2)]
    rows=[connected]
    for pair,m in orbit_rows:
        rows += [tuple(0 if i in pair else 2 for i in range(4))]*m
    assert len(rows)==7 and tuple(map(sum,zip(*rows)))==(7,7,7,9)
    visible=s.Matrix([-1,-1,-1,-3]);hidden=s.Matrix([-6]*4)
    assert visible+hidden+sum(map(s.Matrix,rows),s.zeros(4,1))==s.zeros(4,1)
    positions=[s.Rational(i,8) for i in range(1,8)]
    z=s.symbols('z',real=True);knots=[s.Integer(0),*positions,s.Integer(1)]
    slopes=[];values=[]
    for point in knots:
        values.append([s.Rational(10)+visible[j]*point+sum(q[j]*max(s.Integer(0),point-p) for q,p in zip(rows,positions)) for j in range(4)])
    for i in range(8):slopes.append(list(visible+sum([s.Matrix(r) for r in rows[:i]],s.zeros(4,1))))
    assert all(v>0 for row in values for v in row)
    assert slopes[-1]==[-v for v in hidden]
    charges=[list(s.Matrix(N.K)*s.Matrix(q)/2) for q in rows]
    assert charges[0]==[0,0,0] and all(any(c for c in row) for row in charges[1:])
    return dict(status='PASS',descended_divisors='O_X(2J_i)',connected_curve_degrees=list(connected),
        brane_curve_degrees=[list(q) for q in rows],visible_boundary_charge=list(visible),hidden_boundary_charge=list(hidden),
        total_source=[0]*4,brane_positions=list(map(str,positions)),piecewise_slopes=slopes,
        knot_profile_values=values,curve_K_degrees=charges,
        neutral_genus2_curve_pullback=list(INSTANTON_GENERATORS[1]),
        equation='b_j(z)=10+beta0_j*z+sum_n beta_nj max(0,z-z_n); b_j prime jumps by beta_nj, endpoint slopes beta0 and -betahidden.',
        physical_scope='An exact harmonic cohomology/source profile of the leading interval backreaction architecture, in the conventions of hep-th/9808101. These b_j are source coefficients, not independently solved physical Kahler radii. Small expansion parameter, full nonlinear BPS reconstruction, localized transverse Green functions and higher-order corrections remain required. No visible opposite-X charged fields are supplied.')


@lru_cache(None)
def h4_real_operator_certificate():
    """Exact operator consequence of the incoming Oct8 chiral Cayley pair.

    Ownership: the two classes, golden spectra and120 W33 embeddings are
    the parallel Oct8 track. This constructs their real spectral selectors.
    """
    from w33_clifford_antipodal_a5_selector_group import clifford_antipodal_permutations,compose,inverse
    path=ROOT/'data/w33_20261008_H4_A5_chiral_5cycle_normal_Cayley.json'
    cert=json.loads(path.read_text());group=clifford_antipodal_permutations()
    index={g:i for i,g in group.items()};mats=[]
    for key in ('A5_neighbor_identity_permutations','mirror_A5_5cycle_identity_permutations'):
        a=np.zeros((60,60),dtype=np.int64)
        for i,g in group.items():
            for k in cert[key]:a[i,index[compose(g,k)]]=1
        assert np.array_equal(a,a.T) and np.all(a.sum(axis=0)==12)
        mats.append(a)
    plus,minus=mats;D=plus-minus;S=plus+minus;D2=D@D
    assert np.array_equal(D2@D,80*D)
    assert np.array_equal(D2@D2,80*D2) and np.trace(D2)==80*18
    assert np.array_equal(S@D2,4*D2) and np.trace(D)==0
    h=tuple(cert['order4_normalizer_witness_S6_permutation'])
    perm=[index[compose(compose(h,group[i]),inverse(h))] for i in range(60)]
    assert np.array_equal(D[np.ix_(perm,perm)],-D)
    assert np.array_equal(S[np.ix_(perm,perm)],S)
    # Every C5 generator acts trivially on the conjugacy-class difference.
    r=tuple(cert['A5_neighbor_identity_permutations'][0])
    rp=[index[compose(compose(r,group[i]),inverse(r))] for i in range(60)]
    assert np.array_equal(D[np.ix_(rp,rp)],D)
    return dict(status='PASS',actual_antipodal_address_order=list(range(60)),
        A_plus=plus.tolist(),A_minus=minus.tolist(),outer_order4_permutation=perm,
        exact_minimal_polynomial='D(D^2-80 I)=0, D=A_plus-A_minus',
        rational_projector='P18=D^2/80',real_involution='Chi=D/(4 sqrt(5)) on im(P18)',
        real_spectral_projectors='P_plus=(P18+Chi)/2, P_minus=(P18-Chi)/2',
        real_projector_ranks=[9,9],rational_support_rank=18,outer_exchanges_projectors=True,
        fused_adjacency_on_support='(A_plus+A_minus) P18=4 P18',
        symmetry_consequence='Any real symmetric operator preserving these two rank9 sectors and commuting with the order4 exchange has isospectral restrictions on them. A kinetic form with the same symmetries gives equal generalized mass spectra. The symmetry must be broken, or the sectors mixed, to evade this paired-sector statement.',
        reality_comparison='Unlike11766 C=-iJ on an irreducible real rotation plane, D and these spectral projectors are real symmetric operators on60 real graph amplitudes. This does not project the original compact-real E8 adjoint to one complex81 or identify graph chirality with a Lorentzian Weyl spinor.',
        source_certificate=str(path.relative_to(ROOT)),source_certificate_sha256=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        prior='Oct8 H4_A5_chiral_Cayley_pair owns the actual classes and outer map; H4_A5_golden_spectral_fusion owns their spectra; W33_H4_chiral_4regular_embedding owns the120 edge embeddings. The identities follow from standard A5 central idempotents; the addition is an exact actual-address operator certificate and an explicit symmetry boundary.',
        physical_chiral_fermion_or_mass_prediction=False)


@lru_cache(None)
def normalization_controls_certificate():
    cert=flavor_circuit_certificate();single=s.ones(3,1)
    assert len(single.nullspace())==0
    # For rescaling the defining equation F->aF: Omega->Omega/a and
    # type2 reference nu3->a nu3, including its optimized exact correction.
    a=s.symbols('a',positive=True);z1,z2,z3,o=s.symbols('Z1 Z2 Z3 O',positive=True)
    proxy=1/s.sqrt(z1*z2*z3);invariant=proxy/s.sqrt(o)
    assert s.simplify(invariant.subs({z3:a*a*z3,o:o/(a*a)},simultaneous=True)-invariant)==0
    return dict(status='PASS',single_quotient_coupling_circuit_dimension=0,
        F_rescaling='F->aF sends Omega_norm->Omega_norm/a^2 and Z3->a^2 Z3, while the unit-Serre holomorphic cup is fixed.',
        normalization_invariant_geometry_proxy='lambda_hol/sqrt(Z1 Z2 Z3 Omega_norm)',
        raw_geometry_proxy_changes_as='1/a',cross_character_circuits=cert['independent_rational_circuits'],
        negative_controls=['Off-diagonal kinetic mixing invalidates scalar-Z circuit cancellation.',
            'Exact Galerkin stationarity in a finite trial space does not imply global harmonicity.',
            'Positive sampled metric eigenvalues do not prove global positivity or smoothness.',
            'A finite-basis normalization estimate with large MA/HYM residuals is not an observed mass.'],
        h4_real_operator=h4_real_operator_certificate(),
        scope='Exact convention and identifiability controls preventing a polynomial/basis normalization artifact from being interpreted as a mass hierarchy; a real graph selector is distinguished from the compact-real E8 obstruction.')


def payload():
    fs=[fivebrane_normal_certificate,geometric_higgs_certificate,flavor_circuit_certificate,
        four_dimensional_certificate,interval_source_certificate,instanton_lattice_certificate,normalization_controls_certificate]
    passes={str(11759+i):f() for i,f in enumerate(fs)}
    return dict(schema='w33.pass11759_11765.geometry_flavor_stabilization.v1',status='PASS',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        prior_source_sha256=hashlib.sha256(Path(Q.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        prior_sources={str(Path(mod.__file__).relative_to(ROOT)):hashlib.sha256(Path(mod.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for mod in (Q,N)},
        passes=passes,physical_boundary='No measured flavor, protected full-spectrum vacuum, nonlinear backreaction, W33-derived4D spacetime or completed TOE is claimed.')


if __name__=='__main__':
    result=payload()
    def encoder(x):
        if isinstance(x,(np.integer,s.Integer)):return int(x)
        if isinstance(x,s.Rational):return str(x)
        raise TypeError(type(x).__name__)
    OUT.write_text(json.dumps(result,indent=2,default=encoder)+'\n')
    for k,v in result['passes'].items():print(k,v['status'],flush=True)
    print(OUT)
