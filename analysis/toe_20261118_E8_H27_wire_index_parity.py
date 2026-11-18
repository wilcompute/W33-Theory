"""Full E8 root census and restricted H27 linked-wire family-index gate.

Standard E8 lattice, matched to the existing native16 charge dictionary.
Not a completed Albert-to-E8 bracket map, G2 metric or physical spectrum.
"""
import json
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import sympy as s
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
omega=(-1+s.sqrt(-3))/2
K=s.QQ.algebraic_field(s.sqrt(-3))

def canon(M):
    f=lambda z:K.to_sympy(K.from_sympy(s.expand(z)))
    return M.applyfunc(f) if isinstance(M,s.MatrixBase) else f(M)

def e8_roots_twice():
    roots=[]
    for i,j in combinations(range(8),2):
        for a,b in product((-2,2),repeat=2):
            r=[0]*8;r[i]=a;r[j]=b;roots.append(tuple(r))
    roots += [v for v in product((-1,1),repeat=8) if sum(x<0 for x in v)%2==0]
    assert len(roots)==len(set(roots))==240
    assert all(sum(x*x for x in r)==8 for r in roots)
    # Root-system closure under all 240 reflections, integer arithmetic.
    R=set(roots)
    for a in roots:
        for b in roots:
            dot=sum(x*y for x,y in zip(a,b))
            assert dot%4==0
            reflected=tuple(x-dot*y//4 for x,y in zip(a,b))
            assert reflected in R
    return roots

def root_census():
    roots=e8_roots_twice()
    census=Counter(-sum(r[5:]) for r in roots)
    assert dict(census)=={-4:3,-3:16,-2:30,-1:48,0:46,1:48,2:30,3:16,4:3}
    d5=sum(all(x==0 for x in r[5:]) for r in roots)
    d3=sum(all(x==0 for x in r[:5]) for r in roots)
    mixed=sum(all(x%2==0 for x in r) and any(r[:5]) and any(r[5:]) for r in roots)
    half=sum(all(abs(x)==1 for x in r) for r in roots)
    assert (d5,d3,mixed,half)==(40,12,60,128)
    # Pair all spinor weights to the actual clock-Albert/Fock charge certificate.
    old=json.loads((ROOT/'data/toe_20261118_biCayley_Peirce16_SM.json').read_text())
    native={tuple(row['bits']):row['Q6Y'] for row in old['independent_even_Fock_control']}
    observed={};phase_by_Y={}
    for r in roots:
        if all(abs(x)==1 for x in r) and tuple(r[5:])==(1,1,1):
            bits=tuple(int(x<0) for x in r[:5])
            Y=sum(a*b for a,b in zip([2,2,2,-3,-3],r[:5]))//2
            chi=-sum(r[:5])
            assert chi==2*sum(bits)-5
            assert native[bits]==Y
            observed[bits]=Y
            phase=sum(a*b for a,b in zip([-2,-2,-2,-4,-4],r[:5]))//2%7
            phase_by_Y.setdefault(str(Y),set()).add(phase)
    assert observed==native and len(observed)==16
    linked=json.loads((ROOT/'data/toe_20261118_linked_wire_H27_Novikov.json').read_text())
    assert {k:next(iter(v)) for k,v in phase_by_Y.items()}==linked['compact_gauge_extension']['native16_W7_phase_by_Q6Y']
    assert all(len(v)==1 for v in phase_by_Y.values())
    invariant_D5=[r for r in roots if all(x==0 for x in r[5:])
                  and sum(a*b for a,b in zip([-2,-2,-2,-4,-4],r[:5]))//2%7==0]
    assert len(invariant_D5)==8
    # The SU3 flavor algebra has roots e_i-e_j in the last3 coordinates.
    # Roots commuting with its Cartan have all last coordinates equal;
    # these are orthogonal to the SU3 roots, hence are precisely E6 roots.
    e6=[r for r in roots if r[5]==r[6]==r[7]]
    assert len(e6)==72
    assert Counter(-sum(r[5:]) for r in e6)=={0:40,-3:16,3:16}
    assert sum(census.values())+8==248
    return dict(E8_roots=240,reflection_pairs_checked=240**2,
        D5_D3_root_blocks=dict(D5=d5,D3=d3,mixed_10x6=mixed,half_16x4_plus_dual=half),
        adjoint_branch='248=(45,1)+(1,15)+(16,4)+(16bar,4bar)+(10,6)',
        T_generator='T=-2*(e6+e7+e8), first5 coordinates form D5',
        T_root_census={str(k):census[k] for k in sorted(census)},
        grade_zero_dimension=54,E6_commuting_SU3_roots=72,
        E6_T_grades='45_0+1_0+16_-3+16bar_3',
        complete_positive_T_blocks={'16_1':48,'10_2':30,'16bar_3':16,'1_4':3},
        native_spinor_charge_dictionary_matches=16,
        native_W7_phase_dictionary_matches=True,D5_W7_invariant_roots=8,
        scope='Standard integral E8 root coordinates, anchored to native16 Fock Y/chi charges; no full native Albert/E8 Lie-bracket identification.')

def su4_holonomy():
    I=s.eye(3)
    X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    Y=s.diag(1,omega**2,omega)
    assert canon(X*Y*X.inv()*Y.inv())==omega*I
    A=s.diag(X,1); C=s.diag(X*Y,1)
    assert canon(A.det())==canon(C.det())==1
    # All 27 H27 elements give the same one-dimensional traceless commutant.
    # First determine End(4) via the two generators, then impose trace zero.
    units=[]
    for i in range(4):
        for j in range(4):
            E=s.zeros(4);E[i,j]=1;units.append(E)
    constraints=s.Matrix.hstack(*[s.Matrix(list(A*E-E*A)+list(C*E-E*C)+[s.trace(E)]) for E in units])
    from sympy.polys.matrices import DomainMatrix
    ns=DomainMatrix.from_Matrix(canon(constraints)).convert_to(K).nullspace().to_Matrix()
    assert ns.rows==1
    H=s.zeros(4)
    for a,E in zip(ns.row(0),units):H+=a*E
    H=canon(H/H[0,0])
    assert H==s.diag(1,1,1,-3)
    # SU4 commutant, not an externally appended arbitrary U1.
    T=s.diag(1,1,1,-3)
    assert A*T==T*A and C*T==T*C and s.trace(T)==0
    # Compact order5 scalar twist lies in SU4 and is nonresonant on
    # every nonzero E8 T grade. Use exponent arithmetic, no rounded roots.
    assert all((3*q)%5!=0 for q in (1,2,3,4))
    def mul(g,h,n):
        a,b,c,k=g;aa,bb,cc,kk=h
        return ((a+aa)%3,(b+bb)%3,(c+cc-b*aa)%3,(k+kk)%n)
    def closure(gens,n):
        seen={(0,0,0,0)};queue=list(seen)
        for g in queue:
            for h in gens:
                v=mul(g,h,n)
                if v not in seen:seen.add(v);queue.append(v)
        return len(seen)
    assert closure([(1,0,0,0),(1,1,0,1)],5)==135
    assert closure([(1,0,0,0),(1,1,0,1)],35)==945
    assert all((21*q+15*k)%35!=0 for q in (1,2,3,4) for k in range(7))
    return dict(SU4_traceless_H27_commutant_dimension=1,
        commutant_generator=[1,1,1,-3],compact_twist_order=5,
        full_SU4_flat_image='H27 x C5',image_order=135,
        with_Spin10_W7_image='H27 x C5 x C7',with_Spin10_W7_order=945,
        candidate_gauge_algebra='su3+su2+u1Y+u1chi+u1T, dimension14',
        combined_period_nonresonance='zeta35^(21q+15k) !=1 for all q=1..4,k=0..6',
        link_relation='[a,c^3]=1, a=diag(X,1), c=diag(v XY,v^-3), v^5=1',
        nonzero_grade_central_fiber='v^(3q) I on each T=q irreducible; never1 for q=+/-1,+/-2,+/-3,+/-4',
        charge_decomposition='4=3_1+1_-3; 6=3bar_2+3_-2; 15=8_0+1_0+3_4+3bar_-4')

def wire_complexes():
    # Eight nontrivial characters in End(3) minus identity = adjSU3.
    # a=X,c=XY; their conjugation characters span all nontrivial F3^2.
    neutral=[]
    for p,q in product(range(3),repeat=2):
        if (p,q)==(0,0):continue
        a=canon(s.Matrix([[omega**p]]))[0]
        c=canon(s.Matrix([[omega**((p+q)%3)]]))[0]
        d0=canon(s.Matrix([a-1,c-1]))
        d1=canon(s.Matrix([[1-c**3,(a-1)*(1+c+c*c)]]))
        assert canon(d1*d0)==s.zeros(1)
        r0=d0.rank();r1=d1.rank()
        b=[1-r0,2-r0-r1,1-r1,0]
        neutral.append(dict(p=p,q=q,base_betti=b))
    assert sum(r['base_betti'][0] for r in neutral)==0
    assert sum(r['base_betti'][1] for r in neutral)==6
    assert sum(r['base_betti'][2] for r in neutral)==6
    trivial_betti=[1,2,1,0]
    # Neutral point sources are filled, while nontrivial wire holonomies
    # remain. The 14 invariant gauge directions each see a trivial line.
    neutral_total=[14*trivial_betti[i]+sum(r['base_betti'][i] for r in neutral)
                   for i in range(4)]
    assert neutral_total==[14,34,20,0]
    parity=[dict(rank1_relative_index=nu,triplet_spinor_index=3*nu,
                 singlet_spinor_index=-nu,total_net_spinor_index=2*nu)
            for nu in range(-6,7)]
    assert all(r['total_net_spinor_index']%2==0 for r in parity)
    return dict(charged_base_betti=[0,0,0,0],
        charged_relative_sphere_betti='(0,rank(V),0,0) for positive T; opposite boundaries give CPT dual for negative T',
        one_relative_sphere_left_chiral_multiplets={'16_1':3,'16bar_3':1,'10_2':3,'singlet_4':3},
        net_complete_Spin10_families=2,
        general_restricted_index='I16=3*nu-nu=2*nu, nu integer; cannot equal3 under a common commuting T Higgs and complementary relative domains',
        parity_controls=parity,adjSU3_character_controls=neutral,
        neutral_SU3_flat_bundle_betti=[0,6,6,0],
        full_grade_zero_bundle_betti_with_W7=neutral_total,
        grade_zero_domain='Point caps filled in T-neutral sector, both wire tori retained with absolute cohomology; no additional boundary holonomy fixing. Other UV domains can change this.',
        neutral_scope='Six complex infinitesimal SL3 flat-connection deformations H1 on the cut linked base; no claim all integrate unobstructedly or acquire a physical massless chiral interpretation.',
        no_H0_flavor_gauge_generators=True)

def anomaly_controls():
    # T(16)=2,T(10)=1, T(SO10 singlet)=0; count each CPT pair once.
    blocks=[(3,16,1,2),(1,16,3,2),(3,10,2,1),(3,1,4,0)]
    grav=sum(n*d*q for n,d,q,t in blocks)
    cubic=sum(n*d*q**3 for n,d,q,t in blocks)
    mixed=sum(n*q*t for n,d,q,t in blocks)
    assert (grav,cubic,mixed)==(168,912,18)
    return dict(gravitational_T=grav,cubic_T=cubic,SO10_squared_T=mixed,
        all_left_chiral_T_charges_positive=True,
        zero_FI_D_flatness='D_T=sum_i q_i |phi_i|^2 with q_i>0; charged scalars alone cannot have nonzero zero-FI D-flat VEVs',
        holomorphic_selection='All counted charged chiral q>0: no holomorphic gauge-invariant monomial containing them exists without additional oppositely charged fields, transforming spurions or axionic/nonperturbative completion.',
        anomaly_scope='Open local effective spectrum needs boundary inflow/additional states; E8 adjoint branching alone does not cancel these localized4D anomalies.')

def callias_escape():
    # An explicit DIFFERENT operator class: smooth bounded non-Abelian
    # Hermitian mass in su4, coupled to a 3D spinor Dirac operator.
    x,y,z=s.symbols('x y z',real=True);r2=x*x+y*y+z*z
    P=s.Matrix([x**3-3*x*y*y,3*x*x*y-y**3,3*z*r2+z**3])
    assert s.expand((P.T*P)[0]-r2*(r2+3*z*z)**2)==0
    # A_i=(i/2)*(P cross partial_i P).sigma/(1+|P|^2),
    # embedded in the upper SU2 of SU4, is globally smooth. It gives
    # D_i Phi=3*(partial_i P).sigma/(1+|P|^2)^(3/2) EXACTLY.
    p2=(P.T*P)[0]
    for v in (x,y,z):
        Pi=P.diff(v)
        identity=(1+p2)*Pi-P*(P.dot(Pi))-P.cross(Pi).cross(P)-Pi
        assert all(s.expand(t)==0 for t in identity)
    # The finite-energy ansatz is NOT stationary for the specified
    # zero-potential energy: test scalar Euler-Lagrange residual D_i D_i Phi.
    J=[P.diff(v) for v in (x,y,z)]
    lap=sum((P.diff(v,2) for v in (x,y,z)),s.zeros(3,1))
    numerator=3*(1+p2)*lap-12*sum((Pi*P.dot(Pi) for Pi in J),s.zeros(3,1))
    numerator+=3*P*sum(Pi.dot(Pi) for Pi in J)
    residual=s.simplify(numerator.subs({x:1,y:0,z:0})/s.sqrt(2)**5)
    assert residual==s.Matrix([-27/(4*s.sqrt(2)),0,0])
    u=s.symbols('u',real=True)
    F=(3*u+u**3)/(1+3*u*u)
    assert s.factor(s.diff(F,u))==3*(u-1)**2*(u+1)**2/(3*u*u+1)**2
    degree=s.Rational(3,2)*(F.subs(u,1)-F.subs(u,-1))
    assert degree==3
    # g=P/sqrt(1+|P|^2), Phi=diag(3g.sigma-I2,I2).
    # Phi is globally smooth bounded Hermitian and traceless.
    # Outside r>=1, |P|>=r^3 and hence Phi^2>=I4. For r>=200,
    # ||sum sigma_i tensor d_i Phi|| <= (36+18sqrt3)/r <1/2.
    coercivity=1-(36+18*s.sqrt(3))/200
    assert coercivity>s.Rational(1,2)
    gauged_coercivity=1-(36+18*s.sqrt(3))/3**7
    assert gauged_coercivity>s.Rational(1,2)
    def berry(d,nt,np_):
        points=[np.array([0.,0.,1.]),np.array([0.,0.,-1.])]
        for i in range(1,nt):
            theta=np.pi*i/nt
            for j in range(np_):
                phi=2*np.pi*j/np_
                points.append(np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)]))
        def idx(i,j):return 2+(i-1)*np_+j%np_
        triangles=[]
        for j in range(np_):triangles.append((0,idx(1,j),idx(1,j+1)))
        for i in range(1,nt-1):
            for j in range(np_):
                a,b,c,e=idx(i,j),idx(i+1,j),idx(i+1,j+1),idx(i,j+1)
                triangles += [(a,b,c),(a,c,e)]
        for j in range(np_):triangles.append((idx(nt-1,j),1,idx(nt-1,j+1)))
        states=[]
        for p in points:
            a,b,c=p
            if d==3:
                h=1+3*c*c
                w=complex(a,b)**3/h
                n=np.array([w.real,w.imag,(3*c+c**3)/h])
            else:n=p
            assert abs(n@n-1)<1e-12
            H=np.array([[n[2],n[0]-1j*n[1]],[n[0]+1j*n[1],-n[2]]])
            _,V=np.linalg.eigh(H);states.append(V[:,0])
        phase=0.
        for a,b,c in triangles:
            loop=np.vdot(states[a],states[b])*np.vdot(states[b],states[c])*np.vdot(states[c],states[a])
            assert abs(loop)>1e-4
            phase+=np.angle(loop)
        chern=phase/(2*np.pi)
        assert abs(abs(chern)-d)<1e-9
        return dict(degree=d,mesh=[nt,np_],triangles=len(triangles),negative_line_oriented_Bargmann_chern=float(chern))
    meshes=[berry(d,nt,4*nt) for d in (1,3) for nt in (16,32)]
    # Cleaner E8 embedding: SU3 flavor commutes with E6. Replace the
    # constant spectator block by Phi3=diag(3g.sigma-I2/2,1).
    # Trace0, same winding eigenline/connection, and exterior gap>=1.
    su3_asym=[s.Rational(5,2),-s.Rational(7,2),s.Integer(1)]
    assert sum(su3_asym)==0 and min(abs(v) for v in su3_asym)==1
    # Whole27 chirality has a DIFFERENT charge inventory from T-positive
    # localization: 16_1+10_-2+1_4, uniform on all27 components.
    whole27=[(16,1,2),(10,-2,1),(1,4,0)]
    assert sum(d*q for d,q,t in whole27)==0
    assert sum(d*q**3 for d,q,t in whole27)==0
    assert sum(q*t for d,q,t in whole27)==0
    assert 1+1-2==0 and 4-2-2==0
    # Do not confuse a 3D Callias index with physical4D chirality.
    # C=i sigma2 is a matrix; C times complex conjugation is antiunitary.
    # C sigma_i* C^-1=-sigma_i. For the conjugate gauge representation,
    # Abar=A*, Phibar=-Phi*, Lbar=-C L* C^-1: SAME Callias index.
    eps=s.Matrix([[0,1],[-1,0]])
    paulis=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
    assert all(eps*s.conjugate(M)*eps.inv()==-M for M in paulis)
    return dict(operator='L=(sigma_i partial_i) tensor I4+I2 tensor Phi(x), on L2(R3,C2 tensor C4)',
        mass='Phi=diag(3*g.sigma-I2,I2); P=(Re(x+iy)^3,Im(x+iy)^3,z*(3r^2+z^2)); g=P/sqrt(1+|P|^2)',
        exact_polynomial_identity='|P|^2=r^2*(r^2+3z^2)^2',
        mass_in_su4_Hermitian_convention=True,asymptotic_eigenvalues=[2,-4,1,1],
        mass_norm_bound=4,mass_squared_lower_bound_outside_r1=1,
        Dirac_mass_commutator_bound='(36+18sqrt3)/r for r>=1',
        exterior_coercivity_outside_r200=str(coercivity),
        exact_asymptotic_map_degree=int(degree),negative_eigenbundle_rank=1,
        smooth_finite_energy_gauge_ansatz=dict(
            connection='A_i=diag((i/2)*(P cross partial_i P).sigma/(1+|P|^2),0_2)',
            exact_covariant_mass_derivative='D_i Phi=diag(3*(partial_i P).sigma/(1+|P|^2)^(3/2),0_2)',
            exterior_covariant_commutator_bound='(36+18sqrt3)/r^7 for r>=1',
            exterior_gauged_coercivity_outside_r3=str(gauged_coercivity),
            asymptotics_origin='A=O(r^5), F=O(r^4), D_A Phi=O(r^2)',
            asymptotics_infinity='A=O(r^-1), F=O(r^-2), D_A Phi=O(r^-7)',
            finite_energy='Integral[-sum_i<j Tr(F_ij^2)+sum_i Tr((D_i Phi)^2)] d3x is finite; no scalar potential added',
            gauge_index_modulus=3,
            scalar_Euler_Lagrange_residual_at_1_0_0=[str(v) for v in residual],
            qualification='Explicit finite-energy variational configuration; nonzero scalar Euler-Lagrange residual proves it is not a stationary solution of the stated zero-potential energy. Not an E8/G2 vacuum. A_t=tA preserves the Fredholm index.'),
        chern_mesh_controls=meshes,Callias_index_modulus=3,
        E6_preserving_SU3_alternative=dict(
            mass='Phi3=diag(3*g.sigma-I2/2,1), Hermitian su3',
            connection='same upperSU2 A_i, third row/column0',
            asymptotic_eigenvalues=[str(v) for v in su3_asym],
            operator_complex_components=6,Callias_index_modulus=3,
            E8_sector='(27,3); E6 commutes with this Higgs and connection',
            E6_27_component_index_modulus=81,
            auxiliary_27_sector_index_multiplicity=3,
            physical_net_chiral_E6_families_unproved=True,
            conjugate_sector_gate='For Abar=A*, Phibar=-Phi*, C=i sigma2 on spatial spinors gives Lbar=-C L* C^-1 (star denotes complex conjugation, not adjoint). The conjugate27bar block has the SAME3D Callias index. Actual4D chirality/Majorana/CPT projection must be derived.',
            charge_inventory_per_27={'16_1':1,'10_-2':1,'singlet_4':1},
            per27_abelian_checks=dict(gravitational_Psi=0,cubic_Psi=0,Spin10_squared_Psi=0),
            charge_allowed_known_cubic_channels=['16_1*16_1*10_-2','1_4*10_-2*10_-2'],
            remaining_Dflat_obstacle='The SM singlets Nc:(chi,Psi)=(-5,1) and S:(0,4) both have Psi>0: three27s alone still cannot give a nonzero zero-FI SM-preserving D-flat condensate.',
            scope='A different auxiliary family-sector Dirac operator, not an index of the full E8 adjoint. Neutral sectors remain ungapped. Three4D chiral27s are NOT established: conjugate block has sameCalliasindex and actual7D Clifford/Majorana/4D chirality assignment is missing. The oldT-negative-localizer antifamily argument no longer applies, but cannot be replaced by an assumed chiral projection.'),
        index_scope='Callias theorem gives net index magnitude3 for this explicit auxiliary gapped8-component Dirac operator, not a proof exactly3 modes with no additional pairs. Tensoring a spectator Spin10 spinor gives index modulus48.',
        exclusions='This is a scalar mass endomorphism, not the PW Higgs1-form or the earlier physical massless monopole vacuum. It does not commute with fixed H27 holonomies, select degree3, or settle all E8 sectors. The supplied nonzeroA gives finite energy but explicitly fails the stated zero-potential scalar equation; it is not a Yang-Mills-Higgs/BPS or G2 solution.',
        theorem_reference='Gesztesy-Waurick arXiv:1506.05144, bounded C2 Hermitian mass with exterior gap and derivatives O(1/r),O(1/r^2).')

def run():
    return dict(status='PASS',parents=['36eb8d951','c0ca57dab','27665720c'],
        roots=root_census(),holonomy=su4_holonomy(),wire=wire_complexes(),anomalies=anomaly_controls(),
        Callias_nonAbelian_escape=callias_escape(),
        central_connection='E6xSU3 and Spin10xSU4 branchings describe the same E8 inventory here: three16_1 from (27,3), but unavoidable16bar_3 from the E6 adjoint.',
        limitation='Restricted common-Cartan PW/flat-H27 linked-wire model with standard mixed relative domains. Not a no-go for general E8 compactifications, noncommuting Higgs fields, different source/domain assignments, flux/APS index contributions or extra matter.',
        standard_branching_source='Donagi-He-Ovrut-Reinbacher hep-th/0405014 section7; E6 subgroup comparison also EPJC2016 doi:10.1140/epjc/s10052-016-4432-y.',
        physical_scope='No complete G2 geometry, physical spinor boundary action, quantified anomaly inflow, chiral vacuum, dynamical family-number selection or physical TOE.')

if __name__=='__main__':
    result=run()
    (ROOT/'data/toe_20261118_E8_H27_wire_index_parity.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('PASS E8 root/charge closure, SU4 H27 commutant, finite135, restricted net2 parity gate, neutral H1=6 and anomaly168/912/18')
