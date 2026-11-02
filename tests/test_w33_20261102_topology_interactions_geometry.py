import pathlib,sys,json,itertools,unittest,copy
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
import w33_20261102_chiral_surface_development as S
import w33_20261102_common_cover_interactions as I
import w33_20261102_graded_parent_geometry as G
from w33_20261101_frame_tomography_octahedron import PI,scaled_pair

def load(name):return json.loads((R/'data'/('w33_20261102_'+name+'.json')).read_text())

class NativeContinuation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=load('chiral_surface_development');cls.i=load('common_cover_interactions');cls.g=load('graded_parent_geometry')
        cls.C=np.array(cls.s['completion_table']);cls.cover=json.loads((R/'data/w33_20261101_common_cubic_spinor_extension.json').read_text())

    def test_unique_positive_completion_against_native_matrix_traces(self):
        triples=[(a,b,int(self.C[a,b]))for a,b in np.argwhere(self.C>=0)]
        self.assertEqual(len(triples),9720)
        for a,b,c in triples[::97]:
            values=[np.trace(PI[a]@PI[b]@P).imag for P in PI]
            self.assertAlmostEqual(values[c],1/np.sqrt(3))
            self.assertEqual(sum(abs(x-1/np.sqrt(3))<1e-10 for x in values),1)

    def test_edge_reversal_completes_four_distinct_tetrahedron_labels(self):
        quartets=set()
        for a,b in np.argwhere(self.C>=0):
            q={int(a),int(b),int(self.C[a,b]),int(self.C[b,a])}
            self.assertEqual(len(q),4);quartets.add(tuple(sorted(q)))
        self.assertEqual(len(quartets),810)

    def test_torus_map_saturates_every_actual_pair_and_face(self):
        faces=S.torus(4,4);row=S.develop(faces,self.C);labels=dict(row['labels']);E=scaled_pair();edges,_,_=S.manifold(faces)
        self.assertTrue(row['saturated'])
        self.assertTrue(all(E[labels[a],labels[b]]==-4 for a,b in edges))
        chi=sum(np.trace(PI[labels[a]]@PI[labels[b]]@PI[labels[c]]).imag for a,b,c in faces)
        energy=sum(E[labels[a],labels[b]]/6 for a,b in edges)-np.sqrt(3)*chi
        self.assertAlmostEqual(energy,-64)
        self.assertEqual((row['cover_degree'],row['total_ramification']),(8,16))

    def test_local_divisibility_does_not_remove_global_obstruction(self):
        faces=S.torus(3,4);_,degrees,chi=S.manifold(faces)
        self.assertEqual(set(degrees.values()),{6});self.assertEqual(chi,0)
        self.assertFalse(S.develop(faces,self.C)['saturated'])

    def test_seed_independence_for_success_and_failure(self):
        rows=np.argwhere(self.C>=0)
        for a,b in rows[::811]:
            seed=(int(a),int(b),int(self.C[a,b]))
            self.assertTrue(S.develop(S.torus(4,4),self.C,seed)['saturated'])
            self.assertFalse(S.develop(S.torus(3,4),self.C,seed)['saturated'])

    def test_all_even_tori_in_small_grid_and_riemann_hurwitz(self):
        for m,n in itertools.product((3,4,5,6),repeat=2):
            row=S.develop(S.torus(m,n),self.C)
            self.assertEqual(row['saturated'],m%2==0 and n%2==0)
            if row['saturated']:
                self.assertEqual(row['cover_degree'],m*n//2)
                self.assertEqual(row['total_ramification'],m*n)
                self.assertEqual(row['Euler_characteristic'],2*row['cover_degree']-row['total_ramification'])

    def test_manifold_orientation_errors_are_rejected(self):
        faces=S.torus(4,4);faces[0]=faces[0][::-1]
        with self.assertRaises(AssertionError):S.manifold(faces)

    def test_all_signed_kernel_words_reconstruct_and_forbid26_coordinates(self):
        gens=[(tuple(x['permutation']),tuple(x['sign_bits']))for x in self.cover['paired_signed_generators']]
        bits=[]
        for row in self.i['signed_kernel_word_witnesses']:
            x=(tuple(range(27)),(0,)*27)
            for j in row['word']:x=I.signed_mul(gens[j],x)
            self.assertEqual(x[0],tuple(range(27)));self.assertEqual(list(x[1]),row['sign_bits']);bits.append(x[1])
        self.assertEqual(len(set(bits)),32)
        self.assertEqual([j for j in range(27)if all(b[j]==0 for b in bits)],[0])

    def test_exact_bilinear_witness_is_symplectic_on_every_generator(self):
        block=self.i['exact_witnesses'][0]['blocks'][0]
        W=np.array(block['real'])+1j*np.array(block['imag'])
        self.assertEqual(block['coordinate'],0);self.assertTrue(np.array_equal(W.T,-W));self.assertEqual(np.linalg.matrix_rank(W),4)
        for key in self.cover['paired_unitary_dyadic_generators']:
            U=(np.array(key[:16]).reshape(4,4)+1j*np.array(key[16:]).reshape(4,4))/2
            self.assertTrue(np.array_equal(U.T@W@U,W))

    def test_identical_commuting_spinors_have_no_alternating_polynomial(self):
        W=np.array(self.i['exact_witnesses'][0]['blocks'][0]['real']);rng=np.random.default_rng(261102)
        psi=rng.normal(size=4)+1j*rng.normal(size=4)
        self.assertAlmostEqual(abs(psi@W@psi),0.)
        self.assertEqual((self.i['invariant_dimension'],self.i['symmetric_spinor_bilinear_dimension'],self.i['alternating_spinor_bilinear_dimension']),(1,0,1))

    def test_modular_upper_bound_has_independent_constraint_rank(self):
        p=1009;r=self.i['imaginary_unit_modulus'];self.assertEqual(r*r%p,p-1)
        rows=[]
        for key in self.cover['paired_unitary_dyadic_generators']:
            A=np.array(key[:16]).reshape(4,4);B=np.array(key[16:]).reshape(4,4)
            U=(A+r*B)*pow(2,-1,p)%p
            rows.append(np.kron(U.T,U.T)-np.eye(16,dtype=int))
        self.assertEqual(I.rank_mod(np.vstack(rows),p),15)

    def test_KO6_matrices_act_on_independent_random_spin_operator_vectors(self):
        _,_,_,Q=G.parent_data();H=np.eye(9)-Q;rng=np.random.default_rng(3246)
        M=rng.normal(size=(2,2,9,9))+1j*rng.normal(size=(2,2,9,9))
        D=lambda x:np.einsum('ab,bcij->acij',G.X,H@x-x@H)
        Gamma=lambda x:np.einsum('ab,bcij->acij',G.Z,x)
        J=lambda x:np.einsum('ab,cd,bdij->acij',G.Y,G.Y,x.conj().swapaxes(-1,-2))
        self.assertLess(np.linalg.norm(J(J(M))-M),1e-10)
        self.assertLess(np.linalg.norm(J(D(M))-D(J(M))),1e-10)
        self.assertLess(np.linalg.norm(J(Gamma(M))+Gamma(J(M))),1e-10)
        self.assertLess(np.linalg.norm(D(Gamma(M))+Gamma(D(M))),1e-10)

    def test_two_spin_completion_has_the_wrong_J_square(self):
        self.assertTrue(np.array_equal(G.Y@G.Y.conj(),-np.eye(2)))
        self.assertTrue(np.array_equal(np.kron(G.Y,G.Y)@np.kron(G.Y,G.Y).conj(),np.eye(4)))

    def test_restricted_minimum_and_zero_intersection_are_explicit(self):
        self.assertEqual(self.g['minimum_spin_multiplicity_in_tensor_ansatz'],4)
        self.assertEqual(self.g['dimension'],324);self.assertEqual(self.g['intersection_form'],[[0.]])
        self.assertEqual(self.g['spectrum'],{'-1':72,'0':180,'1':72})
        # A zero-cycle is identity on spin; its spin partial trace against Gamma vanishes.
        self.assertEqual(np.trace(np.kron(G.Z,np.eye(2))),0)

if __name__=='__main__':unittest.main()
