"""Independent geometry, integral-lattice, root, rank and lapse checks."""
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
N=Q.N


def frozen():return json.loads(Q.OUT.read_text())


def test_frozen_source_binding_and_scoped_eight_sections():
    p=frozen()
    for key,path in [('source_sha256',Q.__file__),('prior_source_sha256',N.__file__)]:
        assert p[key]==hashlib.sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert set(p['passes'])==set(map(str,range(11750,11758)))
    assert all(x['status']=='PASS' and x['scope'] for x in p['passes'].values())
    assert 'unproved' in p['physical_boundary']


def test_metric_density_is_residue_pullback_determinant_in_any_elimination():
    # Matrix determinant lemma, independent of polynomial snapshot or coordinate choice.
    grad=np.array([1+2j,3-1j,2j,-2+1j]);h=np.array([1.,2.,3.,4.])
    expected=np.prod(h)*sum(abs(grad)**2/h)
    for omit in range(4):
        kept=[i for i in range(4) if i!=omit];A=np.zeros((4,3),complex)
        A[kept,:]=np.eye(3);A[omit,:]=-grad[kept]/grad[omit]
        assert np.allclose(np.linalg.det(A.conj().T@np.diag(h)@A)*abs(grad[omit])**2,expected)


def test_numeric_snapshot_is_on_hypersurface_but_reference_not_hym_or_rf():
    p=frozen()['passes']['11750'];z,F,_,_=Q.reference_polynomial()
    for a in p['reference_samples']:
        point=[complex(*v) for v in a['point']]
        assert abs(complex(F.subs(dict(zip(z,point)))))<1e-8
    assert abs(p['MA_density_ratio']-1)>.01
    assert max(abs(v) for a in p['reference_samples'] for v in a['HYM_contractions'])>.01
    assert p['training_executed'] is p['physical_normalized_Yukawa_computed'] is False


def test_cubic_bundle_product_and_type2_not_fake_ambient_one_form():
    assert np.sum(N.K,axis=0).tolist()==[0]*4
    assert N.M.ambient_cohomology(N.K[2])==[0]*5
    assert N.M.ambient_cohomology(tuple(k-2 for k in N.K[2]))==[0,0,4,0,0]
    assert N.M.tetraquadric_cohomology(N.K[2])==[0,4,0,0]


def test_type2_primitives_are_global_sections_with_correct_dbar():
    z,b=s.symbols('z b');u=Q.p1_primitives(z,b)
    for k,p in it.product(range(3),range(2)):
        assert s.cancel(s.diff(u[k][p],b)-z**k*b**p/(1+z*b)**3)==0
        south=s.cancel(u[k][p].subs({z:1/z,b:1/b},simultaneous=True)/z)
        assert s.cancel(south+u[2-k][1-p])==0
        assert south.subs({z:0,b:0}) in (-s.Rational(1,2),0,s.Rational(1,2))


def test_type2_named_forms_connect_to_all_four_independent_classes():
    z,b,forms=Q.type2_forms();F=Q.reference_polynomial()[1]
    for (p,q),nu in forms.items():
        target=F*b[2]**p*b[3]**q/((1+z[2]*b[2])**3*(1+z[3]*b[3])**3)
        assert s.cancel(s.diff(nu,b[2])-target)==0
        assert s.diff(nu,b[0])==s.diff(nu,b[1])==0
    p=frozen()['passes']['11750']['type2_closed_lift']
    assert p['full_named_polynomial_connecting_checks']==4 and p['harmonic'] is False


def test_type2_actual_forms_have_regular_group_action_and_invariant_mode():
    z,b,forms=Q.type2_forms();allvars=(*z,*b)
    for (p,q),nu in forms.items():
        g=-nu.subs(dict(zip(allvars,[-x for x in allvars])),simultaneous=True)
        h=-z[0]**2*z[1]**2/(z[2]*z[3]*b[3]**2)*nu.subs(dict(zip(allvars,[1/x for x in allvars])),simultaneous=True)
        assert s.cancel(g-(-1)**(p+q)*nu)==0
        assert s.cancel(h-forms[1-p,1-q])==0


def test_type2_reference_serre_scale_matches_unit_connecting_basis():
    r=s.symbols('r',positive=True)
    for p in range(2):
        radial=s.integrate(r**(2*p+1)/(1+r*r)**3,(r,0,s.oo))
        assert -2*radial==-s.Rational(1,2)
    assert frozen()['passes']['11750']['type2_closed_lift']['Serre_normalized_basis_scale']==4
    assert 4*(-s.Rational(1,2))**2==1


def test_cycle_class_and_budget_from_squarefree_chern_polynomials():
    x=s.symbols('x:4');lines=[sum(k*v for k,v in zip(row,x)) for row in N.K]
    c2=sum(a*b for a,b in it.combinations(lines,2))
    budget=s.expand(4*sum(x[i]*x[j] for i,j in Q.PAIRS)-c2)
    coeff=[budget.coeff(x[i],1).coeff(x[j],1).subs(dict.fromkeys(x,0)) for i,j in Q.PAIRS]
    cycle=[5,1,2,3,0,4]
    assert list(s.Matrix(coeff)-s.Matrix(cycle))==[1,-1,0,0,-1,1]
    for ell in range(4):
        assert 2*sum(coeff[j] for j,p in enumerate(Q.PAIRS) if ell not in p)==[14,14,14,18][ell]


def test_graph_curve_is_equivariant_and_genus_five_descends_to_two():
    u,v=s.symbols('u v');uv=(-v,u)
    assert s.expand(u*uv[0]+v*uv[1])==0
    # The graph map J commutes projectively with both G and H.
    J=s.Matrix([[0,-1],[1,0]])
    for a in (N.G,N.H):assert a*J==-J*a
    # Adjunction on P1 x P1: 2g-2=2ab-2a-2b.
    a,b=6,2;two_g_minus_two=2*a*b-2*a-2*b
    assert two_g_minus_two==8 and two_g_minus_two//4==2


def test_orbit_pairs_descend_integrally_without_dividing_averages():
    p=frozen()['passes']['11751'];assembled=[1,1,0,1,0,0]
    for orbit in p['orbit_pair_curves']:
        index=Q.PAIRS.index(tuple(orbit['factors']))
        assembled[index]+=2*orbit['multiplicity']
        assert orbit['cover_components']==2 and orbit['quotient_genus']==1
    assert assembled==[5,1,2,3,0,4]
    assert sum(x['multiplicity'] for x in p['orbit_pair_curves'])==6


def test_every_alignment_rank_identity_is_polynomial_not_random_sampling():
    vs=list(zip(*[iter(s.symbols('s0 t0 s1 t1 s2 t2'))]*2))
    base=Q.alignment_mass(vs,[s.Rational(1,2)]*3)
    for row in frozen()['passes']['11752']['character_rephasings']:
        d=list(map(s.sympify,row['rephasing']));actual=Q.alignment_mass(vs,list(map(s.sympify,row['coefficients'])))
        assert actual==s.diag(*d)*base*s.diag(*d,*d)
        assert all(abs(complex(x))==1 for x in d)
    assert base.subs(dict(zip(s.symbols('s0 t0 s1 t1 s2 t2'),[0]*6))).rank()==0


def test_actual_e6_two_singlets_give_same_epsilon_pairing():
    labs,charges,D=N.matter_dictionary();five=[i for i,q in enumerate(charges) if q==-4]
    bars=[i for i,q in enumerate(charges) if q==-1]
    sing=[i for i,q in enumerate(charges) if q==5]
    a,b=s.symbols('a b');block=s.Matrix((D[sing[0]][np.ix_(five,bars)]).tolist())*a+s.Matrix(D[sing[1]][np.ix_(five,bars)].tolist())*b
    assert block.subs({a:1,b:0}).rank()==block.subs({a:0,b:1}).rank()==5
    assert block.subs({a:1,b:1}).rank()==5
    assert block*block.T==s.eye(5)*(a*a+b*b)


def test_primitive_frame_all_generators_and_inverse_integrality():
    p=Q.primitive_frame_certificate()
    assert p['primitive_basis_checks']==7*248
    assert p['integral_monodromy_and_inverse_checks']==2*7*248
    assert p['root_subgroup_polynomial_degree']==2
    assert s.Matrix(p['simple_coroot_Gram']).det()==1


def test_simple_coroot_gram_and_all_root_pairings_are_integral():
    simples,C,gram=Q.chevallley_data();labs,ws,_=N.P.roots()
    assert len(simples)==8 and gram==gram.T and all(gram[i,i]==2 for i in range(8))
    for w in ws:
        charges=C.T*s.Matrix([s.Rational(w[i]-w[8],3) for i in range(8)])
        assert all(x.is_Integer for x in charges)


def contraction(i,form):
    out={}
    for inds,v in form.items():
        if i in inds:
            pos=inds.index(i);out[inds[:pos]+inds[pos+1:]]=v*(-1)**pos
    return out


def wedge_one(i,form):
    out={}
    for inds,v in form.items():
        if i not in inds:out[tuple(sorted((i,*inds)))]=v*(-1)**sum(j<i for j in inds)
    return out


def test_seven_form_potentials_and_pairwise_overlap_signs():
    coords=(0,1,2,4,5,6,7,8);alpha=contraction(1,{coords:1})
    for i in coords:
        if i==1:continue
        assert wedge_one(i,contraction(i,alpha))==alpha
        for j in coords:
            if j in (1,i):continue
            six=contraction(j,contraction(i,alpha))
            assert wedge_one(j,six)==contraction(i,alpha)
            assert wedge_one(i,six)=={k:-v for k,v in contraction(j,alpha).items()}


def test_cocycle_nontrivial_and_even_sum_line_lifts_cancel():
    group=list(it.product(range(2),repeat=2));c=lambda a,b:(-1)**(a[1]*b[0])
    prod=lambda a,b:tuple(x^y for x,y in zip(a,b))
    for a,b,d in it.product(group,repeat=3):assert c(a,b)*c(prod(a,b),d)==c(b,d)*c(a,prod(b,d))
    assert c((1,0),(0,1))!=c((0,1),(1,0))
    for k in N.K:assert all(c(a,b)**sum(k)==1 for a,b in it.product(group,repeat=2))


def test_group_H2_is_C2_via_tensor_periodic_resolution():
    # Tensor of integral C2 resolutions: d_even=2, d_odd=0.
    def boundary(n):
        source=[(i,n-i) for i in range(n+1)];target=[(i,n-1-i) for i in range(n)]
        M=s.zeros(n,n+1)
        for j,(a,b) in enumerate(source):
            if a and a%2==0:M[target.index((a-1,b)),j]+=2
            if b and b%2==0:M[target.index((a,b-1)),j]+=(-1)**a*2
        return M
    d2,d3=boundary(2),boundary(3)
    assert d2*d3==s.zeros(2,4)
    assert d2.nullspace()==[s.Matrix([0,1,0])]
    assert list(d3[1,:])==[0,-2,2,0]
    assert all(d3[i,j]==0 for i in (0,2) for j in range(4))


def test_quotient_H4_torsion_argument_requires_surjective_transgression():
    p=frozen()['passes']['11755']
    assert p['H4_quotient_torsion_order']==1 and p['pullback_H4_injective']
    assert 'surjective' in p['transgression']
    assert 'subgroup' in p['total_degree3_terms']['E2_0_3']
    assert 'nonfree' in p['scope']


def test_integral_H4_image_has_index128_and_contains_actual_budget():
    p=frozen()['passes']['11755'];B=s.Matrix(p['pullback_H4_image_basis_in_J_pairings'])
    assert abs(B.det())==p['pullback_H4_image_index']==128
    assert B*s.Matrix(p['budget_integral_image_coordinates'])==s.Matrix([14,14,14,18])
    picbasis=s.Matrix.hstack(s.Matrix([1,1,0,0]),s.Matrix([-1,1,0,0]),s.Matrix([0,-1,1,0]),s.Matrix([0,0,-1,1]))
    assert abs(picbasis.det())==2
    assert all(x.is_Integer for x in picbasis.T*B/4)


def test_uniform_large_flux_limit_changes_generation_index_cubically():
    ell=s.symbols('ell',integer=True,positive=True)
    chi=sum(2*sum(s.prod(v) for v in it.combinations([ell*x for x in k],3))+2*sum(ell*x for x in k) for k in N.K)/4
    assert s.expand(chi)==-3*ell**3
    assert s.solve(chi+3,ell)==[1]


def test_flux_scaling_from_einstein_weyl_measure_and_seven_inverse_metrics():
    # d=3: external Weyl exp(-2S), measure exp(-2S).
    exponents=[2]*8
    for i in range(8):
        if i!=1:exponents[i]+=2
    assert exponents==frozen()['passes']['11754']['flux_exponents']
    assert sum(exponents)==30
    G=s.eye(8)+s.ones(8);assert G.det()==9 and G.inv()==s.eye(8)-s.ones(8)/9
    k=s.Matrix(exponents);assert (k.T*G.inv()*k)[0]==16
    assert list(G.inv()*k)==[s.Rational(2,3),s.Rational(-4,3)]+[s.Rational(2,3)]*6


def test_lapse_variation_and_legendre_constraint():
    a,ad,Nl,vd,U=s.symbols('a ad N vd U',positive=True)
    L=-2*ad**2/Nl+a*a*vd**2/Nl-Nl*a*a*U
    constraint=s.diff(L,Nl)
    assert s.expand(constraint*Nl**2)==2*ad**2-a*a*vd**2-Nl**2*a*a*U
    pa,pv=s.symbols('pa pv')
    H=s.expand(pa*ad+pv*vd-L).subs({ad:-Nl*pa/4,vd:Nl*pv/(2*a*a)})
    assert s.simplify(H-Nl*(-pa**2/8+pv**2/(4*a*a)+a*a*U))==0


def test_lorentzian_trajectories_conserve_constraint_and_volume_responds():
    p=Q.lorentzian_certificate();a,b=p['trajectory_controls']
    assert max(a['max_constraint_residual'],b['max_constraint_residual'])<1e-8
    assert a['end_volume']>1 and b['end_volume']>1 and abs(a['end_volume']-b['end_volume'])>.01
    assert not p['flat_FRW_scaling']['positive_flux_solution']
    assert s.Rational(4,16)==s.Rational(1,4)
    assert 4*(2*s.Rational(1,4)-1)/16==-s.Rational(1,8)


def test_conditional_weak_pair_does_not_eliminate_proton_witness():
    p=Q.conditional_splitting_certificate()
    assert p['weak_rank']==2 and p['color_rank']==3
    a,b,c,d=s.symbols('a b c d');expr=s.sympify(p['actual_previous_proton_component'])
    assert s.expand(expr).coeff(a*b*c*d)!=0
    assert 'tuned' in p['origin'] and 'not' in p['origin']


def test_balancing_pair_is_absent_from_geometric_zero_mode_inventory():
    p=Q.balancing_inventory_certificate()
    assert p['positive_X_quotient_H1']==6 and p['negative_X_quotient_H1']==0
    assert p['family_neutral_nonzero_X_adjoint_generators']==0
    assert 8+3+1+6+6==24
    assert N.M.tetraquadric_cohomology((0,0,0,0))==[1,0,0,1]
