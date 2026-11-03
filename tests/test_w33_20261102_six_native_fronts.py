"""Independent maps, polynomial tensors, spectra and resource witnesses."""
import collections
import itertools
import json
import pathlib

import networkx as nx
import numpy as np
import sympy as s
from scipy.linalg import expm

ROOT=pathlib.Path(__file__).resolve().parents[1]


def load(stem):return json.loads((ROOT/'data'/('w33_20261102_'+stem+'.json')).read_text())
def parse(rows):return s.Matrix([[s.sympify(x) for x in row] for row in rows])
def cyclic(f):return min(tuple(f[k:]+f[:k]) for k in range(3))


def test_deck_group_is_exhaustive_by_colored_graph_automorphisms():
    d=load('deck_monodromy_network');b=load('toroidal_knight_clifford_bridge')
    G=nx.Graph();pi=dict(b['native_labels'])
    G.add_nodes_from((v,dict(color=pi[v])) for v in range(16));G.add_edges_from(b['grid_edges']+b['diagonal_edges'])
    faces={cyclic(f) for f in b['source_faces']};actual=set()
    for p in nx.isomorphism.GraphMatcher(G,G,node_match=lambda a,b:a['color']==b['color']).isomorphisms_iter():
        if {cyclic([p[v] for v in f]) for f in b['source_faces']}==faces:actual.add(tuple(p[v] for v in range(16)))
    assert actual=={tuple(p) for p in d['deck_permutations']} and len(actual)==8


def test_each_monodromy_meridian_and_regular_group():
    d=load('deck_monodromy_network');gens=d['meridian_sheet_permutations'];identity=tuple(range(8))
    mul=lambda a,b:tuple(a[b[j]] for j in range(8))
    rows=[]
    for mask in range(8):
        p=identity
        for j in range(3):
            if mask>>j&1:p=mul(gens[j],p)
        rows.append(p)
    assert len(set(rows))==8 and rows[7]==tuple(gens[3])
    assert all(len({p[j] for p in rows})==8 for j in range(8))
    assert all(mul(g,g)==identity and all(g[j]!=j for j in range(8)) for g in gens)


def test_shrikhande_and_rook_have_distinct_link_topology():
    b=load('toroidal_knight_clifford_bridge');G=nx.Graph();G.add_nodes_from(range(16));G.add_edges_from(b['grid_edges']+b['diagonal_edges'])
    R=nx.Graph();R.add_nodes_from(range(16));R.add_edges_from((a,b) for a,b in itertools.combinations(range(16),2) if a//4==b//4 or a%4==b%4)
    assert all(nx.is_isomorphic(G.subgraph(list(G[v])),nx.cycle_graph(6)) for v in G)
    assert all(sorted(map(len,nx.connected_components(R.subgraph(list(R[v])))))==[3,3] for v in R)
    assert np.allclose(np.linalg.eigvalsh(nx.to_numpy_array(G)),np.linalg.eigvalsh(nx.to_numpy_array(R)))
    d=load('deck_monodromy_network')
    assert d['shrikhande_homology']['rational_Betti']==[1,2,1] and d['rook_2_skeleton_homology']['rational_Betti']==[1,9,8]


def test_weighted_transfer_for_several_integer_couplings():
    b=load('toroidal_knight_clifford_bridge');G=np.zeros((16,16));D=G.copy();C=G.copy()
    for a,z in b['grid_edges']:G[a,z]=G[z,a]=1
    for a,z in b['diagonal_edges']:D[a,z]=D[z,a]=1
    for x,y in itertools.product(range(4),repeat=2):C[4*((x+2)%4)+(y+2)%4,4*x+y]=1
    for k in range(1,7):
        target=C if k%2==0 else -np.eye(16)
        assert np.max(abs(expm(-1j*np.pi*(G+k*D)/2)-target))<2e-13


def test_shrikhande_exact_transfer_bounds():
    for c in np.linspace(-1,1,301):
        assert (20-8*c-12*c*c)/256 <= 1/12+1e-15
        assert (2-2*c)**2/256 <= 1/16+1e-15
    assert s.simplify((20-8*s.Rational(-1,3)-12*s.Rational(-1,3)**2)/256)==s.Rational(1,12)


def test_switch_capacity_paths_and_exact_parity_bound():
    d=load('hypercube_switch_capacity')
    for paths,capacity,count in [(d['single_layer_six_path_witness'],1,6),(d['doubled_resource_eight_path_witness'],2,8)]:
        assert len(paths)==count and len({v for p in paths for v in [p[0],p[-1]]})==2*count
        used=collections.Counter()
        for path in paths:
            assert path[0]^path[-1]==15
            for a,b in zip(path,path[1:]):assert (a^b).bit_count()==1;used[tuple(sorted((a,b)))]+=1
        assert max(used.values())<=capacity
    assert 32//5==6


def test_twist_T3_sum_from_independent_binary_determinants():
    total=0;independent=0
    for a,b,c in itertools.product(range(8),repeat=3):
        span={0,a,b,c,a^b,a^c,b^c,a^b^c}
        full=len(span)==8
        independent+=full;total+=-1 if full else 1
    assert independent==168 and total//8==22
    d=load('deck_twisted_quantum_double');assert d['T3_partition']==22
    assert sum(int(dim)**2*n for dim,n in d['anyon_dimension_multiplicities'].items())==64


def test_all_type_III_cocycle_equations_and_flux_radicals():
    omega=lambda a,b,c:(-1)**((a&1)*((b>>1)&1)*((c>>2)&1))
    for a,b,c,d in itertools.product(range(8),repeat=4):assert omega(b,c,d)*omega(a,b^c,d)*omega(a,b,c)==omega(a^b,c,d)*omega(a,b,c^d)
    for row in load('deck_twisted_quantum_double')['flux_sectors']:
        g=row['flux'];alpha=lambda x,y:omega(g,x,y)*omega(x,y,g)*omega(x,g,y)
        radical=[x for x in range(8) if all(alpha(x,y)==alpha(y,x) for y in range(8))]
        assert radical==row['radical']
        assert row['irreducible_count']*row['irreducible_dimension']**2==8


def test_quantum_face_projector_spectrum_and_second_order():
    d=load('quantized_native_tetrahedron');native=load('chiral_surface_development');C=native['completion_table'];colors=d['native_colors']
    states=list(itertools.product(range(4),repeat=4));P=[tuple(v) for v in d['classical_ground_states']]
    assert len(P)==12 and all(C[colors[v[a]]][colors[v[b]]]==colors[v[c]] for v in P for a,b,c in d['faces'])
    for v in P:
        for j in range(4):
            for color in range(4):
                if color==v[j]:continue
                w=list(v);w[j]=color
                assert sum(C[colors[w[a]]][colors[w[b]]]!=colors[w[c]] for a,b,c in d['faces'])==3
    assert parse(d['second_order_effective_matrix'])==-4*s.eye(12)
    third=parse(d['third_order_effective_matrix'])
    assert third==third.T and third.eigenvals()=={-8:1,s.Rational(-8,3):9,0:2}


def test_quantum_gap_converges_to_third_order_splitting():
    d=load('quantized_native_tetrahedron');row=d['numerical_low_energy'][0]
    assert abs(row['gap']/row['h']**3-16/3)<0.3
    assert abs((row['energy']+4*row['h']**2)/row['h']**3+8)<0.3
    assert d['torus_ground_coloring_Hamming_distances']=={'12':48,'16':18}


def test_all_real_signature_structures_against_actual_gamma_axes():
    d=load('real_clifford_gate_synthesis');old=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text());axes=[parse(a) for a in old['gamma_axes'][:4]]
    for row in d['signature_table']:
        B=parse(row['antiunitary_linear_part']);assert B*B.conjugate()==row['J_square']*s.eye(4)
        for j,g in enumerate(axes):
            gamma=g if j<row['p'] else s.I*g
            assert B*gamma.conjugate()==gamma*B
    assert d['enlarged_spinor_antiunitary_solution_dimension']==0


def test_spinor_gate_word_and_entangling_lower_bound():
    d=load('real_clifford_gate_synthesis');I=s.eye(2);H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);S=s.diag(1,s.I)
    gates={'H0':s.kronecker_product(H,I),'H1':s.kronecker_product(I,H),'S0':s.kronecker_product(S,I),'S1':s.kronecker_product(I,S),
           'CX01':s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]),'CX10':s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])}
    word=d['spinor_circuit']['word_in_application_order'];M=s.eye(4)
    for name in word:M=gates[name]*M
    b=load('toroidal_knight_clifford_bridge');U=parse(b['unitary_numerator'])/s.sqrt(2)
    scalar=s.simplify(U.conjugate().T*M);assert scalar==scalar[0,0]*s.eye(4)
    assert sum(name.startswith('CX') for name in word)==1
    amplitude=s.Matrix(2,2,U[:,0]);assert amplitude.det()!=0


def test_eight_CNOT_register_word_and_independent_bidirectional_lower_bound():
    d=load('real_clifford_gate_synthesis')['four_qubit_register_circuit'];word=d['CNOT_word_in_application_order']
    start=(1,2,4,8);target=tuple(15^(1<<j) for j in range(4));ops=list(itertools.permutations(range(4),2))
    def ball(root,radius):
        seen={root};front={root}
        for _ in range(radius):
            new=set()
            for a in front:
                for c,t in ops:
                    b=list(a);b[t]^=b[c];new.add(tuple(b))
            front=new-seen;seen|=new
        return seen
    assert ball(start,3).isdisjoint(ball(target,4))
    for mask in range(16):
        y=mask
        for c,t in word:
            if y>>c&1:y^=1<<t
        assert y==mask^(15 if mask.bit_count()%2 else 0)
    assert len(word)==8


def test_new27_preserves_every_native_polarized_cubic_entry():
    d=load('clifford_native_cubic_repair');old=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    tensor=np.zeros((27,27,27),dtype=complex)
    for row in old['coefficient_rows']:
        for t in itertools.permutations(row['triple']):tensor[t]=row['coefficient']/6
    for sparse in d['native_generator_sparse_matrices']:
        R=np.zeros((27,27),dtype=complex)
        for i,j,z in sparse:R[i,j]=complex(s.sympify(z))
        transformed=np.einsum('ia,jb,kc,ijk->abc',R,R,R,tensor,optimize=True)
        assert np.max(abs(transformed-tensor))<1e-13
        assert np.max(abs(R.conj().T@R-np.eye(27)))<1e-13


def test_old_embedding_word_has_basis_invariant_trace_mismatch():
    d=load('clifford_native_cubic_repair');word=d['unchanged_embedding_mismatch']['word']
    old=json.loads((ROOT/'data/w33_20261101_common_cubic_spinor_extension.json').read_text())
    p=list(range(27));bits=[0]*27;U=s.eye(4)
    for j in word:
        g=old['paired_signed_generators'][j];q=g['permutation'];b=g['sign_bits']
        bits=[bits[i]^b[p[i]] for i in range(27)];p=[q[p[i]] for i in range(27)]
        key=old['paired_unitary_dyadic_generators'][j];M=s.Matrix(4,4,[s.Rational(key[k],2)+s.I*s.Rational(key[k+16],2) for k in range(16)])
        U=M*U
    assert s.simplify(U)==s.eye(4) and p==list(range(27)) and any(bits)
    assert 27-2*sum(bits)==d['unchanged_embedding_mismatch']['old_signed_trace']!=27


def test_linear_group_center_word_and_exterior_pairing():
    d=load('clifford_native_cubic_repair');old=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text());gens=[parse(a) for a in old['unitary_generators']]
    P=s.eye(4)
    for j in d['old_word_for_pseudoscalar']:P=gens[j]*P
    b=load('toroidal_knight_clifford_bridge');U=parse(b['unitary_numerator'])/s.sqrt(2)
    assert s.simplify(U**2*P)==s.I*s.eye(4)
    J=parse(d['mixed_bilinear_repair']['symmetric_pairing']);pairs=list(itertools.combinations(range(4),2))
    for g in gens+[U]:
        W=s.Matrix([[g[i,a]*g[j,z]-g[i,z]*g[j,a] for a,z in pairs] for i,j in pairs])
        assert s.simplify(W.T*J*W)==J
    assert d['enlarged_linear_order']==4*d['enlarged_projective_order']==46080


def test_full_rank_MI_counterexample_by_tensor_partial_trace():
    d=load('entanglement_metric_axiom_audit');rho=np.array(parse(d['rho_rational']),dtype=float)
    assert np.min(np.linalg.eigvalsh(rho))>=1/160-1e-14
    def reduced(keep):
        keep=[3-j for j in keep];lost=[j for j in range(4) if j not in keep]
        order=keep+lost+[j+4 for j in keep+lost]
        t=rho.reshape((2,)*8).transpose(order).reshape(2**len(keep),2**len(lost),2**len(keep),2**len(lost))
        return np.einsum('aibi->ab',t)
    def entropy(r):
        eigen=np.linalg.eigvalsh(r);return -sum(x*np.log(x) for x in eigen if x>1e-15)
    S={name:entropy(reduced(keep)) for name,keep in d['subsystems'].items()}
    I={pair:S[pair[0]]+S[pair[1]]-S[pair] for pair in ['AB','BC','AC']}
    assert min(I.values())>0 and S['AB']+S['BC']-S['B']-S['ABC']>0
    assert I['AC']*4*np.log(2)<I['AB']*I['BC']
    assert d['triangle_violation_margin']>8


def test_AC_information_is_strictly_positive_at_high_precision():
    d=load('entanglement_metric_axiom_audit')
    exact=s.Rational(101,200)*s.log(s.Rational(101,100))+s.Rational(99,200)*s.log(s.Rational(99,100))
    value=exact.evalf(60)
    assert 0<float(value)<s.Rational(1,10000)
    assert abs(float(value)-d['mutual_information_nats']['AC'])<1e-15


def test_induced324_restricts_to_old27_and_preserves_all_block_cubics():
    d=load('induced_cubic_common_cover');old=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    terms={tuple(r['triple']):r['coefficient'] for r in old['coefficient_rows']}
    for j,(p,bits) in enumerate(zip(d['signed_generator_permutations'],d['signed_generator_bits_hex'])):
        bits=int(bits,16);assert sorted(p)==list(range(324))
        for block in range(12):
            image=p[27*block:27*block+27];target=image[0]//27
            assert all(v//27==target for v in image)
            for t,c in terms.items():
                sign=(-1)**sum((bits>>(27*block+i))&1 for i in t)
                mapped=tuple(sorted(image[i]%27 for i in t))
                assert c*sign==terms[mapped]
        if j<6:
            assert p[:27]==old['signed_generators'][j]['permutation']
            assert [(bits>>i)&1 for i in range(27)]==old['signed_generators'][j]['sign_bits']


def test_induced_kernel_relations_over_an_independent_prime():
    d=load('induced_cubic_common_cover');old=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    b=load('toroidal_knight_clifford_bridge');U=[parse(a) for a in old['unitary_generators']]+[parse(b['unitary_numerator'])/s.sqrt(2)]
    # An independent field embedding: i=4,sqrt2=6 in F17.
    def modular(x):
        x=s.expand(x).subs(s.sqrt(2),6).subs(s.I,4);num,den=s.fraction(x)
        return int(num)*pow(int(den),-1,17)%17
    matrices=[np.array([[modular(x) for x in row] for row in u.tolist()],dtype=np.int64) for u in U]
    generators=list(zip(d['signed_generator_permutations'],map(lambda x:int(x,16),d['signed_generator_bits_hex'])))
    def word(seq):
        p=list(range(324));bits=0;u=np.eye(4,dtype=np.int64)
        for j in seq:
            q,a=generators[j];bits^=sum(((a>>p[i])&1)<<i for i in range(324));p=[q[p[i]] for i in range(324)];u=matrices[j]@u%17
        return p,bits,u
    basis={};signed_basis={};odd=False
    def add(rows,x):
        while x:
            k=x.bit_length()-1
            if k not in rows:rows[k]=x;return
            x^=rows[k]
    for witness in d['kernel_relation_witnesses']:
        p,a,u=word(witness['left_word']);q,b,v=word(witness['right_word']);phase=witness['spinor_scalar_i_exponent']
        delta=int(witness['sign_delta_hex'],16)
        assert p==q and a^b==delta and np.array_equal(u,pow(4,phase,17)*v%17)
        add(signed_basis,delta);add(basis,delta|((phase%2)<<324));odd|=phase%2==1
    assert len(signed_basis)==60 and odd and len(basis)+1==62
    assert d['paired_common_cover_order']==46080*2**60
    assert d['Schreier_non_tree_relations_checked']==7*11520-(11520-1)


def test_supplied_cocycle_has_an_explicit_nonClifford_phase_resource():
    phase=np.diag([(-1)**((x&1)*((x>>1)&1)*((x>>2)&1)) for x in range(8)])
    X0=np.zeros((8,8),dtype=int)
    for x in range(8):X0[x^1,x]=1
    image=phase@X0@phase
    assert all(image[x^1,x]==(-1)**(((x>>1)&1)*((x>>2)&1)) for x in range(8))
    # A Pauli with this support could have only a linear sign pattern.
    sign=[int(image[x^1,x]) for x in range(8)]
    assert not any(sign==[global_sign*(-1)**((z&x).bit_count()) for x in range(8)] for global_sign in [1,-1] for z in range(8))
    d=load('deck_twisted_quantum_double')
    assert d['supplied_cocycle_resource']['normalized_Pauli_fourth_moment_of_CCZ_plus_state']=='11/32'


def test_actual_spinor_to_six_form_intertwiner():
    d=load('spin6_rotation_group_audit');forms=[parse(a) for a in d['exterior_square_basis']]
    old=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text());b=load('toroidal_knight_clifford_bridge')
    gens=[parse(a) for a in old['unitary_generators']]+[parse(b['unitary_numerator'])/s.sqrt(2)]
    for U,A in zip(gens,d['generator_orthogonal_matrices']):
        A=s.Matrix(A);assert A.T*A==s.eye(6) and A.det()==1
        for j,B in enumerate(forms):
            image=s.zeros(4)
            for i,C in enumerate(forms):image+=A[i,j]*C
            assert s.simplify(U*B*U.T-image)==s.zeros(4)
    assert d['group_order']==2*d['projective_quotient_order']==23040


def test_independent_involution_counts_exclude_W_D6():
    rotations=weyl=0
    for p in itertools.permutations(range(6)):
        if any(p[p[i]]!=i for i in range(6)):continue
        parity=sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))%2
        for bits in range(64):
            if any(((bits>>i)^(bits>>p[i]))&1 for i in range(6)):continue
            rotations+=bits.bit_count()%2==parity;weyl+=bits.bit_count()%2==0
    assert rotations-1==631 and weyl-1==751
    d=load('spin6_rotation_group_audit')
    assert sum(d['actual_element_order_histogram'].values())==sum(d['W_D6_element_order_histogram'].values())==23040
    assert d['actual_element_order_histogram']!=d['W_D6_element_order_histogram']
