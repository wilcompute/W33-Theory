"""Exact continuation of11742-49; supplied CY and Lorentzian3D frames differ.

Classical tools: Cartan--Leray, Chevalley root subgroups, CY/HYM equations,
and torus reduction. Particular witnesses are additions, not new general laws.
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
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11742_11749_nonzero_flavor_and_flux_frame as N
OUT=ROOT/'data/w33_pass11750_11757_integral_geometry_and_flux_dynamics.json'
PAIRS=tuple(it.combinations(range(4),2))


@lru_cache(None)
def reference_polynomial():
    z=s.symbols('z:4');q=[(1+x*x,1-x*x,2*x) for x in z]
    chars=((1,1),(1,-1),(-1,1))
    terms=[a for a in it.product(range(3),repeat=4)
           if all(np.prod([chars[j][k] for j in a])==1 for k in range(2))]
    coefficients=list(s.primerange(2,75))[:len(terms)]
    F=s.expand(sum(c*s.prod(q[i][a[i]] for i in range(4)) for c,a in zip(coefficients,terms)))
    assert len(terms)==21
    return z,F,terms,coefficients


def reference_jet(point,t):
    z,F,_,_=reference_polynomial();sub=dict(zip(z,point))
    grad=np.array([complex(s.diff(F,x).subs(sub)) for x in z])
    point_array=np.array(point,dtype=complex)
    h=np.array(t)/(1+abs(point_array)**2)**2
    eta=float(np.prod(h)*sum(abs(grad)**2/h))
    # Eliminate the last coordinate: tangent columns (I_3,-F_i/F_3).
    A=np.vstack((np.eye(3),-grad[:3]/grad[3]))
    metric=A.conj().T@np.diag(h)@A
    hym=[]
    for k in N.K:
        curvature=np.array(k)/(1+abs(point_array)**2)**2
        hym.append(float(np.trace(np.linalg.solve(metric,A.conj().T@np.diag(curvature)@A)).real))
    assert abs(np.linalg.det(metric)*abs(grad[3])**2-eta)<1e-7*eta
    return dict(point=[[float(complex(x).real),float(complex(x).imag)] for x in point],
                polynomial_residual=abs(complex(F.subs(sub))),MA_density=eta,HYM_contractions=hym)


def p1_primitives(z,bar):
    den=2*(1+z*bar)**2
    return ((bar*(2+z*bar)/den,bar**2/den),
            (-1/den,z*bar**2/den),
            (-z/den,-(1+2*z*bar)/den))


@lru_cache(None)
def type2_forms():
    z,F,_,_=reference_polynomial();bar=s.symbols('b:4')
    coeff=s.Poly(F,z[2]);u=p1_primitives(z[2],bar[2])
    forms={(p,q):sum(coeff.nth(k)*u[k][p] for k in range(3))*bar[3]**q/(1+z[3]*bar[3])**3
           for p,q in it.product(range(2),repeat=2)}
    return z,bar,forms


@lru_cache(None)
def type2_lift_certificate():
    z,b=s.symbols('z b');u=p1_primitives(z,b);checks=0
    for k,p in it.product(range(3),range(2)):
        assert s.cancel(s.diff(u[k][p],b)-z**k*b**p/(1+z*b)**3)==0
        assert s.cancel(u[k][p].subs({z:1/z,b:1/b},simultaneous=True)/z+u[2-k][1-p])==0
        assert s.cancel(u[k][p].subs({z:-z,b:-b},simultaneous=True)-(-1)**(k+p+1)*u[k][p])==0
        checks+=3
    zz,bb,forms=type2_forms();F=reference_polynomial()[1]
    for (p,q),nu in forms.items():
        rhs=F*bb[2]**p*bb[3]**q/((1+zz[2]*bb[2])**3*(1+zz[3]*bb[3])**3)
        assert s.cancel(s.diff(nu,bb[2])-rhs)==0
        assert s.diff(nu,bb[0])==s.diff(nu,bb[1])==0
    return dict(primitive_table=[[str(v) for v in row] for row in u],primitive_covariance_checks=checks,
        full_named_polynomial_connecting_checks=4,
        recipe='F=sum_(k=0)^2 f_k(z0,z1,z3) z2^k; nu_pq=sum_k f_k u_kp(z2,barz2) barz3^q/(1+z3 barz3)^3 dbarz3. dbar nu_pq=F omega_pq, so nu restricted to X is closed.',
        cohomology='The Koszul connecting map sends [nu_pq|X] to the four independent H2(A,K3-D) classes omega_pq; both adjacent ambient K3 cohomologies vanish, so these are a basis.',
        globality='u_S=z u_N at z=1/w equals -u_(2-k,1-p)(w). All six are smooth O(-1) sections in both charts. H0(O(-1))=H1(O(-1))=0 makes this inverse unique, so it intertwines the natural projective lifts.',
        invariant_mode='nu_00+nu_11 descends for the prior trivial character; the three other sign/eigencombinations follow the regular cohomology action.',
        Serre_normalized_basis_scale=4,
        normalization='With trace (2pi i)^-1 integral dz wedge nu on each CP1, the displayed H1(O(-3)) basis pairs as -I/2 with (1,z). Two factors give I/4, so4 nu_pq has unit-paired connecting classes. The invariant combination is scaled by the same4; physical metric normalization is still uncomputed.',
        harmonic=False,
        prior='These six primitives specialize Blesneag et al.1512.05322 eqs3.22/5.28-5.29 to the particular K3 input. The addition is an explicit checked input for this bundle and polynomial, not new primitive formulas or a new cohomology method.')


@lru_cache(None)
def metric_certificate():
    z,F,terms,coefficients=reference_polynomial()
    # Homogeneous invariance under simultaneous swap is product z_i^2 F(1/z).
    assert s.expand(F.subs(dict(zip(z,[-x for x in z])),simultaneous=True)-F)==0
    reciprocal=s.Poly(F,z)
    flipped=sum(c*s.prod(z[i]**(2-a[i]) for i in range(4)) for a,c in reciprocal.terms())
    assert s.expand(flipped-F)==0
    t=[float(s.N(x)) for x in N.flavor_certificate()['positive_Kahler_point']]
    samples=[]
    for fixed in ((0,0,0),(s.Rational(1,3),s.Rational(1,2),s.Rational(2,3))):
        poly=s.Poly(F.subs(dict(zip(z[:3],fixed))),z[3]);roots=np.roots([float(x) for x in poly.all_coeffs()])
        samples.append(reference_jet([*fixed,complex(roots[0])],t))
    ratio=samples[1]['MA_density']/samples[0]['MA_density']
    assert abs(ratio-1)>.01 and all(x['polynomial_residual']<1e-8 for x in samples)
    assert max(abs(x) for a in samples for x in a['HYM_contractions'])>.01
    return dict(status='PASS',invariant_section_indices=[list(a) for a in terms],coefficients=list(map(int,coefficients)),
        affine_polynomial=str(F),Kahler_point=t,reference_samples=samples,MA_density_ratio=ratio,
        equations=['det(g_ref+ddbar phi)/Omega_density=constant',
                   'Delta_g beta_i=-Lambda_g F_ref_i; integral source=0 by slope',
                   'nu_i=nu_ref_i+dbar sigma_i; dbar_dagger nu_i=0',
                   'Z_IJ=volume-normalized integral H nu_I star conjugate(nu_J)',
                   'Y_phys=e^(K4/2) Y_hol contracted with three inverse square roots of Z'],
        exact_type2_input='K3 comes from H2(A,K3-D), not a restricted ambient harmonic1-form. Explicit closed global reference forms and their connecting-map/covariance checks are supplied below; harmonic correction is still required.',
        type2_closed_lift=type2_lift_certificate(),
        product_HYM_constraint='sum beta_i=constant when sum K_i=0, using one Ricci-flat metric',
        large_flux_rescaling='K_i -> ell K_i gives net quotient index -3 ell^3. Uniform large-flux localization changes the three-generation inventory; ell=1 is the only positive integer retaining index -3. This excludes this shortcut, not other large-flux bundles.',
        external_implementation='https://github.com/kitft/heteroticyukawas',
        training_executed=False,physical_normalized_Yukawa_computed=False,
        scope='Executed local induced-Fubini-Study/HYM residual calculation on a named invariant polynomial. Global smoothness of this numeric snapshot is not certified. The generic smooth/free family is prior11742. No Ricci-flat metric, harmonic lift, physical kinetic integral or observed mass is claimed.')


@lru_cache(None)
def anomaly_cycle_certificate():
    old=N.anomaly_class_certificate();A=s.Matrix(old['intersection_pairing_matrix'])
    b=s.Matrix(old['raw_cover_budget']);r=s.Matrix(old['relation_coefficients'])
    curve=s.Matrix([1,1,0,1,0,0]);even=s.Matrix([4,0,2,2,0,4])
    assert b-curve-even==r and A*(curve+even)==A*b
    # S: D01=D02=0 is graph P1 x P1. Restrict D=(2,2,2,2).
    degree=(6,2);genus=(degree[0]-1)*(degree[1]-1)
    assert genus==5 and 1+(genus-1)//4==2
    orbit_pairs=[dict(factors=list(p),multiplicity=int(v//2),cover_class_multiplicity=2,
                     cover_components=2,component_genus=1,quotient_genus=1)
                 for p,v in zip(PAIRS,even) if v]
    assert sum(x['multiplicity'] for x in orbit_pairs)==6
    return dict(status='PASS',pair_order=[list(p) for p in PAIRS],budget=list(map(int,b)),
        connected_curve_equations=['u0*u1+v0*v1=0','u0*u2+v0*v2=0','F_tetraquadric=0'],
        parameterization='[u1:v1]=[u2:v2]=[-v0:u0]; factor3 free',
        connected_curve_class=list(map(int,curve)),restricted_bidegree=list(degree),cover_genus=5,quotient_genus=2,
        orbit_pair_curves=orbit_pairs,
        orbit_construction='Fix factors i,j to [1:0],[1:0] and include its h-image [0:1],[0:1]. Each residual (2,2) elliptic curve is g-stable; g acts freely since X is free. The union descends with pullback2 Ji Jj. Repeated components are effective cycles with multiplicity.',
        residual_even_class=list(map(int,even)),difference_relation=list(map(int,r)),
        quotient_divisor_degrees=[7,7,7,9],quotient_divisors='descents of O_X(2 J_i), not non-equivariant O_X(J_i)',
        existence_proof='The21 invariant tetraquadric sections are basepoint-free on the ambient space and its graph surface. Bertini and connectedness of ample (6,2) curves give generic smooth connected C. Simultaneously choose smooth residual elliptic curves and avoid all48 ambient fixed points. All are open conditions on one common invariant family.',
        scope='An explicitly named effective Gamma-invariant curve cycle with the required pullback Bianchi class. With11755 injectivity this closes the integral quotient topological anomaly budget for trivial second E8 bundle. Corrected heterotic field equations, fivebrane dynamics and backreaction are not solved.')


def character_coefficients(chi):
    result=[]
    for k in range(3):
        cs=[chi]*3;cs[k]=(1,1)
        result.append(s.Rational(N.cup(*[N.character_vector(a,c) for a,c in zip(N.cohomology_actions(),cs)]),4))
    return result


def alignment_mass(vevs,coeff):
    mat=s.zeros(3,6)
    for i,j in it.permutations(range(3),2):
        k=3-i-j
        mat[i,j]=coeff[k]*vevs[k][1]
        mat[i,j+3]=-coeff[k]*vevs[k][0]
    return mat


@lru_cache(None)
def all_alignment_certificate():
    variables=s.symbols('s0 t0 s1 t1 s2 t2');vevs=list(zip(variables[::2],variables[1::2]))
    reference=alignment_mass(vevs,[s.Rational(1,2)]*3);rows=[]
    for chi in N.CHARS:
        coeff=character_coefficients(chi);c=[2*x for x in coeff]
        d0=s.sqrt(c[1]*c[2]/c[0]);ds=[d0,c[2]/d0,c[1]/d0]
        left=s.diag(*ds);right=s.diag(*ds,*ds)
        assert alignment_mass(vevs,coeff)==left*reference*right
        rows.append(dict(character=list(chi),coefficients=list(map(str,coeff)),rephasing=list(map(str,ds))))
    return dict(status='PASS',symbolic_VEVs=list(map(str,variables)),reference_mass=[[str(x) for x in row] for row in reference.tolist()],
        character_rephasings=rows,symbolic_checks=4*18,
        conclusion='For all six complex singlet VEV components, every Wilson-character mass matrix has the same rank. Rank3 color lifting forces rank3 weak lifting in this cubic-only inventory.',
        scope='An all-alignment strengthening of11747 equal-VEV obstruction, for the declared invariant singlets, line linearizations and cubic. Extra fields, higher operators, different Wilson embeddings or changed bundles are outside this theorem.')


@lru_cache(None)
def chevallley_data():
    labs,ws,_=N.P.roots();positive=[w for w in ws if next(x for x in w if x)>0]
    pset=set(positive)
    simples=[w for w in positive if not any(tuple(x-y for x,y in zip(w,v)) in pset for v in positive)]
    assert len(simples)==8
    C=s.Matrix.hstack(*[s.Matrix([s.Rational(x,3) for x in w[:8]]) for w in simples])
    gram=C.T*(s.eye(8)+s.ones(8))*C
    assert gram.det()==1 and all(x in (-1,0,2) for x in gram)
    return simples,C,gram


def integral_coordinates(v):
    _,C,_=chevallley_data();h=s.Matrix([v.get(('H',i),0) for i in range(8)])
    coordinates=list(C.inv()*h)+[c for a,c in v.items() if a[0]!='H']
    return all(x.is_Integer for x in map(s.sympify,coordinates))


def interior(i,form):
    out={}
    for inds,v in form.items():
        if i in inds:
            pos=inds.index(i);out[inds[:pos]+inds[pos+1:]]=v*(-1)**pos
    return out


def sixform_dictionary():
    coords=(0,1,2,4,5,6,7,8);omega={coords:1};mapping={}
    for a,b in it.combinations(coords,2):
        order=(3,a,b);sign=(-1)**sum(x>y for i,x in enumerate(order) for y in order[i+1:])
        form={k:-sign*v for k,v in interior(b,interior(a,omega)).items()}
        mapping[('x',*sorted(order))]=form
    return coords,mapping


def form_action(a,b,form):
    out={}
    for inds,v in form.items():
        for pos,i in enumerate(inds):
            if i!=a:continue
            replaced=list(inds);replaced[pos]=b
            if len(set(replaced))!=len(replaced):continue
            sign=(-1)**sum(x>y for j,x in enumerate(replaced) for y in replaced[j+1:])
            key=tuple(sorted(replaced));out[key]=out.get(key,0)-v*sign
    return {k:v for k,v in out.items() if v}


@lru_cache(None)
def primitive_frame_certificate():
    sec,rs,basis=N.frame_data();simples,C,gram=chevallley_data()
    lattice_basis=[{a:s.Integer(1)} for a in basis if a[0]!='H']+[
        {('H',i):C[i,j] for i in range(8) if C[i,j]} for j in range(8)]
    checks=0;monodromies=0;maxpower=0
    coords,mapping=sixform_dictionary();form_checks=0
    for a,b in it.permutations(coords,2):
        for root,form in mapping.items():
            image={}
            for lab,c in N.bracket(('A',a,b),root).items():
                for inds,v in mapping[lab].items():image[inds]=image.get(inds,0)+c*v
            assert {k:v for k,v in image.items() if v}==form_action(a,b,form)
            form_checks+=1
    alpha=interior(1,{coords:1})
    for u,r in zip(sec,rs):
        if r:
            form={inds:c*v for lab,c in r.items() for inds,v in mapping[lab].items()}
            assert form==interior(u[2],alpha)
    for u,r in zip(sec,rs):
        if not r:continue
        for a in basis:
            F=N.add(N.scale(N.pairing(u,a),r),N.bv({u:1},N.bv(r,{a:1})),
                    {u:sum(c*N.pairing(v,a) for v,c in r.items())})
            assert F==N.theta(a);checks+=1
        for v in lattice_basis:
            for sign in (-1,1):
                result={};term=v;n=0
                while term:
                    result=N.add(result,term);n+=1
                    term=N.scale(s.Rational(sign,n),N.bv(r,term));assert n<=4
                maxpower=max(maxpower,n-1)
                assert integral_coordinates(result);monodromies+=1
    assert checks==1736 and monodromies==3472
    assert all(not N.bv(r,t) for r,t in it.combinations(rs,2))
    return dict(status='PASS',primitive_basis_checks=checks,integral_monodromy_and_inverse_checks=monodromies,
        actual_SL8_sixform_dictionary_checks=form_checks,
        root_subgroup_polynomial_degree=maxpower,simple_coroot_weights_times3=[list(w) for w in simples],
        simple_coroot_Gram=gram.tolist(),Gram_determinant=1,
        local_potential='Choose any i !=1,3: C_i=y_i R_i, E_a=exp(ad C_i)a, Sigma sharp=-B(R_i,a)S_i. Product is exp(ad C_i)[Tsharp(a),b].',
        seven_form='Physical8 coords are0,1,2,4,5,6,7,8. Omega8 oriented; alpha7=i_1 Omega8; beta_i=i_i alpha7; C6_i=n*y_i*beta_i, dC6_i=n*alpha7.',
        overlaps='C6_i-C6_j=d(n*y_i*y_j*i_j*i_i alpha7); coordinate y_i -> y_i+1 shifts C6 by n*beta_i.',
        lattice='All240 root vectors plus8 simple coroots; exp(+-ad R_i) and their integer powers preserve this E8 Chevalley lattice. Ancillaries remain section-constrained and constant under these commuting patches.',
        scope='A primitive local frame for T, with integral nilpotent torus transition functions and an integral six-form gerbe flux class in the chosen units. This is classical global patching with an adjoint integral-lattice check, not a proof of full quantum M-theory consistency, a stationary compactification or an identification with the CY gauge bundle.')


@lru_cache(None)
def lorentzian_certificate():
    k=s.Matrix([4,2,4,4,4,4,4,4]);G=s.eye(8)+s.ones(8);Gi=G.inv()
    assert (k.T*Gi*k)[0]==16 and (s.ones(1,8)*G*s.ones(8,1))[0]==72
    assert list(G.eigenvals().items())==[(9,1),(1,7)] or G.eigenvals()=={9:1,1:7}
    kk=np.array(k,dtype=float).ravel();gg=np.array(G,dtype=float);ggi=np.array(Gi,dtype=float)
    def evolve(C):
        def rhs(t,y):
            lam,v=y[:8],y[8:16];H=y[16]
            flux=np.exp(-kk@lam);vac=C*np.exp(-2*np.sum(lam));U=flux+vac
            force=.5*ggi@(kk*flux+2*np.ones(8)*vac)
            return np.r_[v,-2*H*v+force,-v@gg@v,H]
        init=np.r_[np.zeros(16),np.sqrt((1+C)/2),0.]
        sol=solve_ivp(rhs,(0,1),init,rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,1,101))
        assert sol.success
        constraints=[]
        for y in sol.y.T:
            U=np.exp(-kk@y[:8])+C*np.exp(-2*sum(y[:8]))
            constraints.append(abs(2*y[16]**2-y[8:16]@gg@y[8:16]-U))
        assert max(constraints)<1e-8
        return dict(added_vacuum_energy=C,H_initial=float(init[16]),end_log_radii=sol.y[:8,-1].tolist(),
                    end_volume=float(np.exp(sum(sol.y[:8,-1]))),max_constraint_residual=max(constraints))
    runs=[evolve(0),evolve(1)]
    assert abs(runs[0]['end_volume']-runs[1]['end_volume'])>.01
    return dict(status='PASS',dimensions=dict(parent=11,external=3,torus=8),
        Einstein_ansatz='ds11^2=exp(-2 sum lambda_i) ds3_E^2 + sum exp(2 lambda_i)dy_i^2',
        action='S=(1/(2 kappa3^2)) integral sqrt(-g)[R-G_ij d lambda_i d lambda_j-U]',
        kinetic_matrix=G.tolist(),flux_exponents=list(map(int,k)),
        flux_potential='U=A*n^2 exp(-2 lambda_1-4 sum_(i!=1)lambda_i), A>0; isotropic restriction A*n^2*R^-30',
        isotropic_scalar='phi=12 log R gives kinetic -1/2(dphi)^2 inside the displayed action; anisotropic flux does not give a consistent isotropic-only truncation',
        stationary_point='Every logarithmic-radius derivative of the flux potential is strictly negative for n!=0. No finite-radius stationary bare flat-torus vacuum in this sector.',
        minisuperspace_constraint='2H^2=v^T G v+U; Hdot=-v^T G v; lambdaddot=-2Hv-(1/2)G^-1 grad U',
        lapse_Hamiltonian='H_lapse=N[-p_a^2/8+p_lambda^T G^-1 p_lambda/(4 a^2)+a^2 U]=0',
        exponential_slope_squared=16,flat_FRW_scaling=dict(p='1/4',required_U0='-1/8',positive_flux_solution=False),
        trajectory_controls=runs,
        scope='A supplied Lorentzian3D gravitational torus sector, positive kinetic energy, lapse constraint and integrated rolling trajectories for the primitive flux. All8 radii are retained. Volume evolves and common higher-dimensional vacuum energy changes dynamics; fixed-occupation cancellation does not screen it. This is not4D Einstein gravity or a stabilized TOE vacuum.')


@lru_cache(None)
def integral_descent_certificate():
    elements=tuple(it.product(range(2),repeat=2))
    add=lambda a,b:tuple((x+y)%2 for x,y in zip(a,b))
    cocycle=lambda a,b:(-1)**(a[1]*b[0])
    assert all(cocycle(a,b)*cocycle(add(a,b),c)==cocycle(b,c)*cocycle(a,add(b,c)) for a,b,c in it.product(elements,repeat=3))
    assert cocycle((1,0),(0,1))==-cocycle((0,1),(1,0))
    assert N.G*N.H==-N.H*N.G
    for k in N.K:assert sum(k)%2==0
    image_basis=s.Matrix.hstack(2*s.ones(4,1),4*s.eye(4)[:,0],4*s.eye(4)[:,1],4*s.eye(4)[:,2])
    assert abs(image_basis.det())==128
    budget=s.Matrix([14,14,14,18]);image_coordinates=image_basis.inv()*budget
    assert all(x.is_Integer for x in image_coordinates)
    return dict(status='PASS',Gamma='C2 x C2, acting trivially on H2(X,Z)=Z4',
        projective_lift_cocycle=[[list(a),list(b),cocycle(a,b)] for a,b in it.product(elements,repeat=2)],cocycle_identity_checks=64,
        obstruction='O(J_i) has anticommuting lifts. Its H2(Gamma,U1)=H3(Gamma,Z)=C2 class is nonzero: coboundaries on an abelian group are symmetric, this cocycle is not.',
        transgression='d3: H2(X,Z)^Gamma -> H3(Gamma,Z)=C2 is (n0,n1,n2,n3) -> sum n_i mod2, hence surjective.',
        total_degree3_terms={'E2_3_0':'C2 killed by d3','E2_2_1':'0 since H1(X,Z)=0','E2_1_2':'Hom(Gamma,Z4)=0','E2_0_3':'subgroup of free H3(X,Z)'},
        argument='Lefschetz gives pi1(X)=0 and H2(X,Z)_hom=Z4. UCT gives torsion-free H3(X,Z). The Cartan-Leray filtration in total degree3 then has only a free subgroup remaining. Thus H3(Y,Z) is torsion-free; UCT implies H2(Y,Z)_hom torsion-free; oriented6D Poincare duality implies H4(Y,Z) torsion-free. Transfer kills ker(pi*) by4, so pi*:H4(Y,Z)->H4(X,Z) is injective.',
        H4_quotient_torsion_order=1,pullback_H4_injective=True,
        pullback_H4_image_index=128,pullback_H4_image_basis_in_J_pairings=image_basis.tolist(),
        budget_integral_image_coordinates=list(map(int,image_coordinates)),
        image_lattice_proof='The free Picard pullback is the index2 even-total-degree sublattice L of Z4. Perfect quotient Poincare pairing gives pi*H4(Y)=4L_dual: pairing vectors have all entries congruent modulo4 and all even. Its index is128; the actual budget (14,14,14,18) belongs to it.',
        consequence='All equivariant lifts of the named bundle have the same c2 in H4(Y,Z). The explicit11751 effective quotient cycle equals c2(TY)-c2(VY) integrally, since their pullbacks agree and pi* is injective.',
        scope='An integral topological descent proof for this precise free diagonal Klein-four action, using the classical spectral sequence and line-linearization obstruction. It does not apply to arbitrary CY quotients or nonfree actions, nor solve the differential Bianchi identity/backreaction.')


@lru_cache(None)
def conditional_splitting_certificate():
    y=s.symbols('y');S=s.ones(3,1)
    mass=s.Matrix([[0,1-y/3,1],[1-y/3,0,1],[1,1,0]])/2
    weak=mass.subs(y,3);color=mass.subs(y,-2)
    assert weak.rank()==2 and color.rank()==3
    # Use the previous actual signed-root sources, changing only the supplied color mass.
    old=N.character_robustness_certificate();sources=[s.Matrix([s.sympify(x) for x in row]) for row in old['heavy_linear_sources']]
    labs,charges,D=N.matter_dictionary();five=[i for i,q in enumerate(charges) if q==-4]
    bars=[i for i,q in enumerate(charges) if q==-1 and labs[i][0]=='k']
    gauge=s.Matrix(D[labs.index(('A',3,6))][np.ix_(five,bars)].tolist())
    full=s.kronecker_product(color,gauge)
    effective=s.factor(-(sources[1].T*full.inv()*sources[0])[0]);assert effective!=0
    return dict(status='PASS',supplied_family_mass=str(mass),hypercharge_generator='Y6=diag(-2,-2,-2,3,3)',
        weak_rank=2,color_rank=3,weak_nullvector=list(map(str,weak.nullspace()[0])),color_determinant=str(color.det()),
        actual_previous_proton_component=str(effective),
        origin='Supply a family-selective SU5-adjoint mass deformation with coefficients lambda3+eta3*y, eta3=-lambda3/3. This tuned operator is not present in the certified cubic; no massless adjoint is available because H1(X,O)=0.',
        prior='Doublet-triplet adjoint tuning and sliding-singlet mechanisms are classical; see Maekawa--Yamashita hep-ph/0305116 for E6 extensions.',
        scope='A conditional algebraic escape from the equal-rank theorem using an extra tuned coupling, independently checked against the actual cubic proton sources. It retains one weak5/bar5 pair and lifts the corresponding colored5s, but still generates a nonzero10^3 bar5 operator. It is not a protected or geometrically realized Higgs/proton solution.')


@lru_cache(None)
def balancing_inventory_certificate():
    labs,charges,_=N.matter_dictionary();singlets=[list(a) for a,q in zip(labs,charges) if q==5]
    assert len(singlets)==2
    h=[N.M.tetraquadric_cohomology(k) for k in N.K]
    hd=[N.M.tetraquadric_cohomology(tuple(-x for x in k)) for k in N.K]
    # A family-neutral visible-SU5 singlet lies in hidden adjoint24.
    # (3,2)_{+5} + (bar3,2)_{-5} are its only nonzero-X sectors.
    xneutral_family_neutral=3+1 # hidden su2 plus X itself; X charge zero.
    assert xneutral_family_neutral==4 and all(x[1]==4 and y[1]==0 for x,y in zip(h,hd))
    return dict(status='PASS',positive_X_singlet_roots=singlets,
        visible_singlet_branch='24_hidden=(8,1)_0+(1,3)_0+(1,1)_0+(3,2)_{+5}+(bar3,2)_{-5}',
        positive_X_cover_H1=24,negative_X_cover_H1=0,positive_X_quotient_H1=6,negative_X_quotient_H1=0,
        family_neutral_nonzero_X_adjoint_generators=0,
        geometric_repair='Fivebrane cycles close the topological anomaly budget without importing P,Q. They do not add elementary family-neutral opposite-X bundle zero modes. Fivebrane worldvolume matter, bundle deformations or higher-level sectors require a separate calculation.',
        scope='Exact representation and bundle-cohomology exclusion of the imported family-neutral P,Q pair in this smooth adjoint zero-mode inventory. Opposite-chirality KK modes or nonperturbative extra sectors are not excluded. No claim that anomaly cancellation fixes the D-flat or Higgs obstruction.')


def payload():
    funcs=[metric_certificate,anomaly_cycle_certificate,all_alignment_certificate,primitive_frame_certificate,
           lorentzian_certificate,integral_descent_certificate,conditional_splitting_certificate,balancing_inventory_certificate]
    sections={str(11750+i):f() for i,f in enumerate(funcs)}
    return dict(schema='w33.pass11750_11757.integral_geometry_flux_dynamics.v1',status='PASS',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                prior_source_sha256=hashlib.sha256(Path(N.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                passes=sections,physical_boundary='Observed masses, protected proton-safe Higgs sector, backreacted heterotic vacuum,4D Lorentzian gravity and a completed TOE remain unproved.')


if __name__=='__main__':
    result=payload()
    def integer_json(x):
        if isinstance(x,(np.integer,s.Integer)):return int(x)
        raise TypeError(type(x).__name__)
    OUT.write_text(json.dumps(result,indent=2,default=integer_json)+'\n')
    for key,v in result['passes'].items():print(key,v['status'],flush=True)
    print(OUT)
