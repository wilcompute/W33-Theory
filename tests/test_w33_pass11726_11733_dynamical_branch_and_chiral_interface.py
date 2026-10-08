"""Independent boundary, tensor, topology and nonlinear controls."""
import hashlib
import itertools as it
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11726_11733_dynamical_branch_and_chiral_interface as M


def frozen():return json.loads(M.OUT.read_text())


def test_frozen_source_binding_and_eight_scoped_results():
    p=frozen()
    assert p['source_sha256']==hashlib.sha256(Path(M.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert set(p['passes'])=={str(x) for x in range(11726,11734)}
    assert all(x['status']=='PASS' and x['scope'] for x in p['passes'].values())
    assert 'No derived Lorentzian' in p['physical_boundary']


def test_density_stabilizer_for_each_of_nine_coordinate_rays():
    _,ws,_=M.roots()
    for i in range(9):
        charges=[s.Rational(w[i],3) for w in ws]
        assert charges.count(0)+8==64
        assert sum(q!=0 for q in charges)==184
        assert sum(q in (-1,1) for q in charges)==16


def test_density_projective_descent_and_genuine_trivector_transport():
    psi=np.eye(9,dtype=complex)[:,0]
    rho=np.outer(psi,psi.conj())-np.eye(9)/9
    assert np.allclose(np.outer(M.B.V.W*psi,(M.B.V.W*psi).conj())-np.eye(9)/9,rho)
    p=M.orbit_certificate()
    assert p['leaves_sl9_slice'] and p['compact_transport_norm_residual']<1e-12
    assert p['SU9_ray_fiber_real_dimension']+p['E8_SU9_base_real_dimension']==184


def test_orbit_integrality_requires_three_and_quantizes_to147250():
    _,ws,_=M.roots()
    for level in (1,2,3):
        integral=all(s.Rational(level*int(w[0]),3).q==1 for w in ws)
        assert integral==(level==3)
    q=M.orbit_certificate()['KKS_quantization']
    assert q['holomorphic_orbit_quantization_dimension']==147250
    # Independent Casimir/index agreement with Slansky's Table53 entry.
    assert s.Rational(144*147250,248)==1425*60
    # The CP8 fiber's O(3) quantization is Sym3(9), already the11651 carrier.
    assert s.binomial(11,3)==165
    for D in M.B.OPS:
        p1=np.trace(D);p2=np.trace(D@D);p3=np.trace(D@D@D)
        assert abs((p1**3+3*p1*p2+2*p3)/6-3)<1e-12
    assert s.Rational(165+80*3,81)==5 and s.Rational(165-3,81)==2


def test_inverse_casimir_excludes_every_other_partition_exactly():
    for p in M.partitions(5):
        c=[s.Rational(d*d-1,4) for d in p for _ in range(d)]
        # A scalar inverse exists iff all diagonal entries agree and are nonzero.
        has_inverse=len(set(c))==1 and c[0]!=0
        assert has_inverse==(p==(5,))
    J=M.su2_generators((5,))
    assert np.allclose(sum(a@a for a in J),6*np.eye(5))
    assert np.allclose(J[0]@J[1]-J[1]@J[0],1j*J[2])


def test_auxiliary_runaway_requires_the_stated_compact_domain():
    J=M.su2_generators((5,));values=[]
    for eps in [.1,.03,.01]:
        phi=[eps*j for j in J];t=1/(6*eps*eps)
        assert t>2 and np.linalg.norm(t*sum(x@x for x in phi)-np.eye(5))<1e-12
        val=0
        for a,b in it.permutations(range(3),2):
            c=3-a-b;sign=1 if (a,b,c) in [(0,1,2),(1,2,0),(2,0,1)] else -1
            val+=np.linalg.norm(phi[a]@phi[b]-phi[b]@phi[a]-1j*sign*phi[c])**2
        assert abs(val-60*eps*eps*(eps-1)**2)<1e-12
        values.append(val)
    assert values[2]<values[1]<values[0]


def test_clock_open_wedge_and_phase_boundary_not_only_one_fit():
    for a,b in [(1,1),(s.Rational(7,3),3),(2,1),(100,1)]:
        assert b>0 and a>2*b/3
        rows=M.clock_classes();energies=[-a*s.Rational(r['Im_trace_squared'])-b*s.Rational(r['Re_trace']) for r in rows]
        winners=[r['multiplicities'] for r,e in zip(rows,energies) if e==min(energies)]
        assert winners==[[2,0,3],[2,3,0]]
    # At the exact boundary the identity ties; below it the identity wins.
    rows=M.clock_classes()
    for a,expected in [(s.Rational(2,3),3),(s.Rational(1,2),1)]:
        es=[-a*s.Rational(r['Im_trace_squared'])-s.Rational(r['Re_trace']) for r in rows]
        assert es.count(min(es))==expected


def test_actual_E8_Casimir_clock_contractions():
    p=M.branch_certificate()
    assert p['Casimir_projector_ranks']=={'P0':24,'P2':33}
    assert p['clock_contraction_max_error']<1e-11


def test_spin_bundle_zero_mode_count_and_index_are_distinct():
    ns=[(1,1,1),(1,1,-2),(-2,-2,1)]
    assert sum(int(np.prod(n)) for n in ns)==3
    assert [M.line_spin_cohomology(n) for n in ns]==[(0,1),(1,2),(2,4)]
    assert M.line_spin_cohomology((0,2,-3))==(0,0)
    p=M.chiral_certificate()
    assert p['actual_zero_modes']=={'positive':5,'negative':2}
    lift=s.Matrix(p['smoothing_pair_lift_matrix'])
    assert lift.T*lift==s.diag(0,1,0,0,1)
    assert lift*lift.T==s.eye(2)


def test_same_bundle_higgs_topology_obstruction_survives_rotations():
    p=M.topology_certificate()
    assert p['integral_c3_W']==-6 and p['rotating_triplet_c3']==0
    # Reality pairs all nonzero spin2 Chern roots, independently of coordinates.
    u,v=s.symbols('u v');roots=[u,v,0,-v,-u]
    assert s.expand(sum(s.prod(t) for t in it.combinations(roots,3)))==0


def test_hidden_five_really_restricts_to_dual_family_three():
    units,_,_=M.B.hidden_su5()
    h=np.array([2.,-1.,-1.,0.,0.])
    embedded=M.B.add(*[M.B.scale(h[i],units[i,i]) for i in range(5)])
    expected=np.zeros(9);expected[M.B.R4[:3]]=-h[:3]
    assert np.allclose(embedded[0],np.diag(expected),atol=1e-13)
    assert np.linalg.norm(embedded[1])+np.linalg.norm(embedded[2])<1e-13


def test_nonzero_yukawa_projection_is_exact_idempotent():
    p=M.yukawa_projector_certificate();Om=s.Matrix(p['cross_Casimir_matrix'])
    P=s.Matrix(p['projector_matrix'])
    assert Om*Om+10*Om-24*s.eye(7)==s.zeros(7)
    assert P.T==P and P*P==P and P.trace()==1
    e=s.eye(7)[:,p['seed_index']]
    assert (P*e).dot(P*e)==s.Rational(1,7)
    assert p['tensor_bracket_constants_checked']==168 and p['tensor_bracket_residual']==0


def test_projected_channel_has_family_symmetric_highest_weight():
    p=M.yukawa_projector_certificate();P=s.Matrix(p['projector_matrix'])
    vector=P[:,p['seed_index']]
    for raising in [('A',3,4),('A',4,5)]:
        out={}
        for coeff,pair in zip(vector,p['symmetric_root_pair_basis']):
            a,b=map(tuple,pair)
            for u,v in [(a,b),(b,a)]:
                c,k=M.root_bracket(raising,u)
                if k:
                    key=tuple(sorted((c,v)))
                    out[key]=out.get(key,0)+coeff*k
        assert all(x==0 for x in out.values())
    w=p['selected_weight_times3']
    assert (s.Rational(w[3]-w[4],3),s.Rational(w[4]-w[5],3))==(2,0)


def test_all36_actual_exceptional_section_pairs_and_matter_counterexample():
    p=M.exceptional_section_certificate()
    assert len(p['all36_symmetric_pair_checks'])==36
    assert all(x['P3875_zero'] for x in p['all36_symmetric_pair_checks'])
    assert p['section_dimension']==8 and p['singlet_and_adjoint_constraints_zero']
    assert p['maximal_linear_section'] and p['Cartan_extension_constraint_rank']==8
    assert p['extension_rejections']=={'singlet':1,'adjoint':57,'3875':174}
    assert len(p['all240_root_extension_audit'])==232
    assert M.yukawa_projector_certificate()['seed_projected_norm_squared']=='1/7'


def test_complex_section_survives_nontrivial_SU9_basis_change():
    rng=np.random.default_rng(11729);h=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));h=(h+h.conj().T)/2
    U=expm(.1j*h);generators=[]
    for i in range(1,9):
        a=np.zeros((9,9),complex);a[0,i]=1;generators.append(U@a@U.conj().T)
    for a,b in it.combinations_with_replacement(generators,2):
        assert np.linalg.norm(a@b-b@a)<1e-13
        assert abs(np.trace(a@b))<1e-13
    # This is a complex covariance check; U is not assumed split-real.
    assert np.linalg.norm(U.imag)>.01


def test_graph_conformal_constraint_permutation_and_source_response():
    L=M.w33_laplacian();source=1+np.arange(40)/40
    phi,res,gap=M.conformal_solution(source,L=L)
    assert np.min(phi)>0 and res<1e-10 and gap>20
    changed,_,_=M.conformal_solution(source+.01,L=L)
    # The inverse of the positive M-matrix has nonnegative entries.
    assert np.min(changed-phi)>0
    p=np.arange(39,-1,-1);q,_,_=M.conformal_solution(source[p],L=L[np.ix_(p,p)])
    assert np.linalg.norm(q-phi[p],np.inf)<1e-10


def test_constant_graph_constraint_matches_exact_continuum_algebraic_root():
    phi,_,_=M.conformal_solution(np.full(40,3.))
    assert np.max(abs(phi-1))<1e-12
    # Energy gradient checked away from the solution, not just the solver.
    L=M.w33_laplacian();a=np.ones(40);q=np.linspace(.8,1.1,40);v=np.sin(np.arange(40))
    energy=lambda p:4*p@L@p+.5*np.sum(p*p)+np.sum(a/(6*p**6))+np.sum(p**6)/3
    h=1e-6;numeric=(energy(q+h*v)-energy(q-h*v))/(2*h)
    exact=(8*L@q+q-a*q**-7+2*q**5)@v
    assert abs(numeric-exact)<1e-6


def test_constant_energy_shift_is_visible_across_volume_sectors():
    p=M.vacuum_shift_certificate();z=complex(p['volume_coherent_cross_phase']['real'],p['volume_coherent_cross_phase']['imag'])
    assert abs(z-np.exp(1j*.73*.4))<1e-12 and abs(z-1)>.1
    assert p['translated_Lambda_operator_residual']<1e-12
    assert 'changes Lambda-state' in p['fixed_data_boundary']


def test_full_SU5_branch_Hessian_lifts_eleven_shapes_only():
    basis=[]
    for i,j in it.combinations(range(5),2):
        a=np.zeros((5,5),complex);a[i,j]=a[j,i]=1/np.sqrt(2);basis.append(a)
        a=np.zeros((5,5),complex);a[i,j]=1j/np.sqrt(2);a[j,i]=-1j/np.sqrt(2);basis.append(a)
    Q=np.linalg.qr(np.array([np.eye(5)[i]-np.eye(5)[4] for i in range(4)]).T)[0]
    basis += [np.diag(Q[:,i]) for i in range(4)]
    Y=np.diag([-2,-2,-2,3,3]);ys=np.array([np.trace(Y@a).real for a in basis])
    H=np.zeros((24,24))
    for i,a in enumerate(basis):
        for j,b in enumerate(basis):
            d4=4*np.trace((Y@Y@a+Y@a@Y+a@Y@Y)@b).real
            dp22=8*ys[i]*ys[j]+120*np.trace(a@b).real
            H[i,j]=960*(d4-7*dp22/30)+8*ys[i]*ys[j]
    vals=np.linalg.eigvalsh(H)
    assert np.allclose(vals,[*([0]*12),240,*([19200]*8),*([76800]*3)],atol=1e-8)
