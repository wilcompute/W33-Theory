"""Independent chart, incidence, resolvent, algebra and measurement checks."""
import collections
import fractions
import itertools
import json
import pathlib
import sys

import numpy as np
import sympy as s
from scipy.sparse import csr_matrix
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))


def load(stem,date='20261103'):return json.loads((ROOT/f'data/w33_{date}_{stem}.json').read_text())
def parse(rows):return s.Matrix([[s.sympify(x) for x in row] for row in rows])


def test_F_flat_chart_by_independent_rational_gradient_evaluation():
    d=load('vacuum_effective_quantum_audit');z=s.symbols('z:27')
    native=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    rng=np.random.default_rng(30117)
    for _ in range(12):
        v=[s.Integer(int(x)) for x in rng.integers(-2,3,27)];v[d['pivot_coordinate']]=s.Rational(3,2)
        sub=dict(zip(z,v))
        for i,formula in d['rational_F_flat_chart']:v[i]=s.sympify(formula).subs(sub)
        gradient=[0]*27
        for row in native['coefficient_rows']:
            a,b,c=row['triple'];co=row['coefficient']
            gradient[a]+=co*v[b]*v[c];gradient[b]+=co*v[a]*v[c];gradient[c]+=co*v[a]*v[b]
        assert gradient==[0]*27


def test_light_charged_null_modes_and_Sp_flavor_convention():
    from w33_20261102_clifford_native_cubic_repair import cubic_terms,DUADS
    d=load('vacuum_effective_quantum_audit');z=s.symbols('z:27');v=[0]*27
    v[DUADS.index((0,2))]=v[DUADS.index((1,3))]=v[19]=v[26]=1
    W=sum(c*s.prod(z[i] for i in t) for t,c in cubic_terms().items())
    H=s.hessian(W,z).subs(dict(zip(z,v))).extract(d['charged_model_coordinates'],d['charged_model_coordinates'])
    K=s.Matrix.hstack(*(s.Matrix([s.sympify(x) for x in k]) for k in d['charged_null_basis']))
    assert H*K==s.zeros(16,8) and K.T*K==2*s.eye(8)
    assert K.rank()==8 and d['light_USp4_fundamentals']==2*d['Sp_SQCD_Nf']==2


def test_ADS_branch_has_no_finite_stationary_mesonic_point():
    t,q=s.symbols('t q',positive=True);W=1/(s.sqrt(t)*q)
    assert s.simplify(s.diff(W,t)/W)==-1/(2*t)
    assert s.simplify(s.diff(W,q)/W)==-1/q
    R=s.symbols('R',positive=True)
    assert s.simplify(W.subs({t:R,q:s.sqrt(R)}))==1/R


def test_native_extra_spinor_word_and_actual_six_form_matrix():
    d=load('wd5_native_klein_intertwiner');old=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    bridge=load('toroidal_knight_clifford_bridge','20261102')
    gens=[np.array(parse(x),dtype=complex) for x in old['unitary_generators']]+[np.array(parse(bridge['unitary_numerator']),dtype=complex)/np.sqrt(2)]
    U=np.eye(4,dtype=complex)
    for j in d['extra_native_spinor_word']:U=gens[j]@U
    assert np.max(abs(U-np.array(parse(d['extra_native_spinor_matrix']),dtype=complex)))<1e-13
    forms=[np.array(parse(x),dtype=complex) for x in load('spin6_rotation_group_audit','20261102')['exterior_square_basis']]
    A=np.array([[np.trace(a.conj().T@U@b@U.T).real/4 for b in forms] for a in forms])
    p,bits=d['selected_generator_signed_six_states'][-1];expected=np.zeros((6,6))
    for j,i in enumerate(p):expected[i,j]=(-1)**((bits>>j)&1)
    assert np.max(abs(A-expected))<1e-13


def test_q5_Klein_bijection_and_all_ambient_incidence_maps():
    d=load('wd5_native_klein_intertwiner');Q=d['line_to_quadric_coordinate'];L=d['q5_isotropic_lines']
    assert len({tuple(q) for q in Q})==156 and all(sum(x*x for x in q)%5==0 for q in Q)
    assert all(sum(x!=0 for x in Q[i])==2 for i in d['selected_hyperoval_lines'])
    for pointmap,linemap in zip(d['q5_point_generator_permutations'],d['q5_line_generator_permutations']):
        assert all({pointmap[v] for v in line}==set(L[linemap[j]]) for j,line in enumerate(L))


def test_Clebsch_action_order_by_independent_permutation_group_engine():
    d=load('wd5_native_klein_intertwiner')
    group=PermutationGroup(*[Permutation(p) for p in d['Clebsch_generator_permutations']])
    assert group.order()==1920
    B=d['Clebsch_even_weight_vertices'];A=np.array([[(a^b).bit_count()==4 for b in B] for a in B],dtype=int)
    assert np.array_equal(A@A,3*np.eye(16,dtype=int)-2*A+2*np.ones((16,16),dtype=int))


def test_compressed_cubic_by_random_integer_evaluations():
    d=load('induced_cubic_compression');rng=np.random.default_rng(31360)
    def cubic(v):return sum(r['coefficient']*v[r['triple'][0]]*v[r['triple'][1]]*v[r['triple'][2]] for r in d['compressed_cubic'])
    for _ in range(5):
        v=[int(x) for x in rng.integers(-2,3,313)];before=cubic(v)
        for p,bits in zip(d['signed_generator_permutations'],d['signed_generator_bits']):
            moved=[0]*313
            for i,j in enumerate(p):moved[j]=(-1)**bits[i]*v[i]
            assert cubic(moved)==before


def test_compressed_reference_subspace_really_is_old27():
    d=load('induced_cubic_compression');native=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    restricted={tuple(r['triple']):r['coefficient'] for r in d['compressed_cubic'] if max(r['triple'])<27}
    assert restricted=={tuple(r['triple']):r['coefficient'] for r in native['coefficient_rows']}
    for j in range(6):
        assert d['signed_generator_permutations'][j][:27]==native['signed_generators'][j]['permutation']
        assert d['signed_generator_bits'][j][:27]==native['signed_generators'][j]['sign_bits']


def test_all_ground_palettes_and_independent_small_Gram_spectrum():
    d=load('all_quartet_tunneling');P=np.array(d['ground_palettes']);C=np.array(load('chiral_surface_development','20261102')['completion_table'])
    from w33_20261102_chiral_surface_development import torus
    slot=d['parity_slot_at_vertex']
    assert len({tuple(p) for p in P})==9720
    assert all(np.all(C[P[:,slot[a]],P[:,slot[b]]]==P[:,slot[c]]) for a,b,c in torus(4,4))
    M=csr_matrix((np.ones(38880),(np.repeat(np.arange(9720),4),(P+120*np.arange(4)).ravel())),shape=(9720,480))
    eig=np.linalg.eigvalsh((M.T@M).toarray())
    expected=np.array([0]*3+[54]*24+[72]*45+[81]*320+[90]*72+[108]*15+[324])
    assert np.max(abs(eig-expected))<2e-10


def test_tunneling_coefficient_by_independent_resolvent_iteration():
    d=load('all_quartet_tunneling');slot=d['parity_slot_at_vertex'];changed=[v for v in range(16) if slot[v]!=0]
    from w33_20261102_chiral_surface_development import torus
    bit={v:1<<j for j,v in enumerate(changed)};local=[sum(bit.get(v,0) for v in f) for f in torus(4,4)]
    E=np.array([sum(bool(mask&t) and (mask&t)!=t for t in local) for mask in range(4096)])
    Q=list(range(1,4095));index={x:i for i,x in enumerate(Q)};rows=[];cols=[]
    for mask in Q:
        for j in range(12):
            other=mask^(1<<j)
            if other in index:rows.append(index[mask]);cols.append(index[other])
    A=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(4094,4094));left=np.zeros(4094);right=left.copy()
    for j in range(12):left[index[1<<j]]=1;right[index[4095^(1<<j)]]=1
    c=float(s.Rational(d['exact_leading_offdiagonal_coefficient']));errors=[]
    for h in [.02,.01]:
        x=right/E[1:-1]
        for _ in range(40):x=(right+h*(A@x))/E[1:-1]
        ratio=h*h*(left@x)/h**12;errors.append(abs(ratio/c-1))
    assert errors[1]<.003 and errors[1]<errors[0]/3


def test_full_K120_driver_single_flip_cost_and_norm():
    d=load('all_quartet_tunneling');C=np.array(load('chiral_surface_development','20261102')['completion_table'])
    from w33_20261102_chiral_surface_development import torus
    v=[d['ground_palettes'][0][k] for k in d['parity_slot_at_vertex']]
    for label in range(120):
        if label==v[0]:continue
        w=v.copy();w[0]=label
        assert sum(C[w[a],w[b]]!=w[c] for a,b,c in torus(4,4))==6
    assert s.Rational(d['second_order_diagonal'])==-s.Rational(16*119,6)
    assert d['driver_operator_norm']==16*119


def test_all_four_A4_invariant_cocycle_signatures():
    d=load('deck_cocycle_symmetry_selection')
    signatures=[]
    for row in d['invariant_classes']:
        negative=set(row['diagonal_negative_fluxes']);signatures.append(negative)
        assert all({p[g] for g in negative}==negative for p in d['oriented_tetrahedron_A4_actions'])
    assert {frozenset(x) for x in signatures}=={frozenset(),frozenset([1,2,4,7]),frozenset([3,5,6]),frozenset(range(1,8))}
    assert any({p[7] for p in d['oriented_tetrahedron_A4_actions']}!={7} for _ in [0])


def test_twisted_flux_spins_by_regular_projective_matrices():
    from w33_20261103_deck_cocycle_symmetry_selection import exponent
    d=load('deck_cocycle_symmetry_selection')
    for row in d['invariant_classes']:
        if not row['typeIII']:continue
        code=row['code']
        for g in range(1,8):
            def alpha(x,y):return (-1)**(exponent(code,g,x,y)^exponent(code,x,y,g)^exponent(code,x,g,y))
            regular=[]
            for x in range(8):
                M=np.zeros((8,8),dtype=complex)
                for y in range(8):M[x^y,y]=alpha(x,y)
                regular.append(M)
            assert np.max(abs(regular[g]@regular[g]-(-1)**exponent(code,g,g,g)*np.eye(8)))<1e-14
            commutators=np.array([np.concatenate([(M@N-N@M).ravel() for N in regular]) for M in regular]).T
            assert 8-np.linalg.matrix_rank(commutators)==2


def test_alternating_phase_is_coboundary_by_binary_determinant():
    def beta(a,b):return sum(((a>>i)&1)*((a>>j)&1)*((b>>k)&1) for i,j,k in [(0,1,2),(0,2,1),(1,2,0)])%2
    for a,b,c in itertools.product(range(8),repeat=3):
        M=np.array([[(x>>j)&1 for j in range(3)] for x in [a,b,c]])
        det=int(round(np.linalg.det(M)))%2
        assert det==beta(b,c)^beta(a,b^c)^beta(a^b,c)^beta(a,b)


def test_actual_native_center_word_has_the_exported_nontrivial_action():
    d=load('gauge_global_form_audit');repair=load('clifford_native_cubic_repair','20261102');R=[]
    for sparse in repair['native_generator_sparse_matrices']:
        M=np.zeros((27,27),dtype=complex)
        for i,j,z in sparse:M[i,j]=complex(s.sympify(z))
        R.append(M)
    P=np.eye(27,dtype=complex)
    for j in repair['old_word_for_pseudoscalar']:P=R[j]@P
    center=R[-1]@R[-1]@P
    expected=np.diag([complex(s.sympify(x)) for x in d['native_center_matrices'][1]['native_diagonal']])
    assert np.max(abs(center-expected))<1e-13 and np.max(abs(center-np.eye(27)))>1


def test_anomaly_and_Dynkin_index_polynomials():
    d=load('gauge_global_form_audit');a,b,c=s.symbols('a b c');w=[s.sympify(x) for x in d['Cartan_weights']]
    assert s.expand(sum(x**3 for x in w))==0
    assert s.expand(sum(x*x for x in w)-6*(a*a+b*b+c*c+(a+b+c)**2))==0


def test_Yang_Chern_sign_from_actual_gamma_volume():
    old=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text());g=[np.array(parse(x),dtype=complex) for x in old['gamma_axes']]
    product=np.linalg.multi_dot(g);d=load('clifford_yang_monopole_controls')
    assert np.max(abs(product+d['second_Chern_number']*np.eye(4)))<1e-13


def test_nonAbelian_control_loops_by_full_space_Kato_transport():
    old=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text());g=np.array([np.array(parse(x),dtype=complex) for x in old['gamma_axes']]);base=np.linalg.eigh(g[4])[1][:,:2]
    def loop(plane):
        P=base@base.conj().T;U=np.eye(4,dtype=complex)
        vertices=[(0,0),(.25,0),(.25,.25),(0,.25),(0,0)]
        for a,b in zip(vertices,vertices[1:]):
            for t in np.linspace(0,1,33)[1:]:
                x,y=(1-t)*np.array(a)+t*np.array(b);n=np.zeros(5);n[plane[0]]=x;n[plane[1]]=y;n[4]=np.sqrt(1-x*x-y*y)
                Q=(np.eye(4)-np.einsum('a,aij->ij',n,g))/2
                M=Q@P+(np.eye(4)-Q)@(np.eye(4)-P);L,_,R=np.linalg.svd(M);U=L@R@U;P=Q
        return base.conj().T@U@base
    A=loop((0,1));B=loop((0,2));d=load('clifford_yang_monopole_controls')
    assert abs(np.trace(A).real-d['noncommuting_Wilson_loop_convergence'][1]['loop_A_trace'])<1e-10
    assert np.linalg.norm(A@B-B@A)>1e-4


def test_added_Clifford_does_not_preserve_the_five_gamma_family():
    d=load('clifford_yang_monopole_controls');assert sorted(d['added_gate_gamma_span_residual_squared'])==[0,4,4,4,4]
    assert len(d['noncommuting_Wilson_loop_convergence'])==3


def test_holonomy_adjoint_group_order_with_independent_permutation_engine():
    d=load('native_projector_holonomic_qutrit');perms=[]
    for idx in d['selected_holonomy_indices']:
        a=d['holonomies'][idx]['action']
        perms.append(Permutation([3*a[j]+(phase+a[9+j])%3 for j in range(9) for phase in range(3)]))
    assert PermutationGroup(*perms).order()==216


def test_holonomic_central_words_and_postselection_cost():
    d=load('native_projector_holonomic_qutrit')
    def matrix(row):return (np.sqrt(3)*np.array(row['real_sqrt3_numerator']).reshape(3,3)+3j*np.array(row['imaginary_times3_numerator']).reshape(3,3))/12
    gens=[matrix(d['holonomies'][i]) for i in d['selected_holonomy_indices']]
    def word(seq):
        M=np.eye(3,dtype=complex)
        for j in seq:M=gens[j]@M
        return M
    X=word(d['logical_X_word']);Z=word(d['logical_Z_word']);omega=np.exp(2j*np.pi/3)
    assert np.max(abs(X@Z@X.conj().T@Z.conj().T-omega**2*np.eye(3)))<1e-12
    from w33_20261031_tick_loop_rigidity import PI
    for row in d['holonomies']:
        b,c=row['pair'];K=PI[0]@PI[b]@PI[c]@PI[0]
        assert np.max(abs(K.conj().T@K-PI[0]/27))<1e-14
    assert sum(r['multiplicity'] for r in d['holonomies'])==2187


def test_maximal_chiral_faces_have_only_scalar_logical_holonomy():
    from w33_20261031_tick_loop_rigidity import PI
    C=np.array(load('chiral_surface_development','20261102')['completion_table'])
    for a in range(120):
        b=np.flatnonzero(C[a]>=0);c=C[a,b]
        H=3*np.sqrt(3)*(PI[a]@PI[b]@PI[c]@PI[a])
        assert np.max(abs(H-1j*PI[a]))<3e-14
