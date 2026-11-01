import pathlib,sys,json,unittest,itertools,math,copy
import numpy as np
from scipy.linalg import expm
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261101_frame_tomography_octahedron as F
import w33_20261101_parent_control_quantum_geometry as C
import w33_20261101_common_cubic_spinor_extension as G

def read(name):return json.loads((ROOT/'data'/name).read_text())

class NativeFiveFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f=read('w33_20261101_frame_tomography_octahedron.json')
        cls.c=read('w33_20261101_parent_control_quantum_geometry.json')
        cls.g=read('w33_20261101_common_cubic_spinor_extension.json')
        cls.tetra,cls.loop,cls.Q=F.inputs()

    def test_every_frame_is_a_positive_normalized_povm(self):
        for ids in self.f['tomography']['frame_outcome_indices']:
            effects=self.Q[ids]/30
            self.assertLess(np.linalg.norm(effects.sum(0)-np.eye(9)),1e-11)
            self.assertGreater(np.linalg.eigvalsh(effects).min(),-1e-12)

    def test_reconstruction_on_all_matrix_units(self):
        q=self.Q[self.f['tomography']['frame_outcome_indices'][0]]
        for i,j in itertools.product(range(9),repeat=2):
            A=np.zeros((9,9));A[i,j]=1
            p=np.einsum('aij,ji->a',q,A)/30
            reconstructed=(40/3)*np.einsum('a,aij->ij',p,q)-(13/3)*np.trace(A)*np.eye(9)
            self.assertLess(np.linalg.norm(A-reconstructed),1e-11)

    def test_common_channel_and_probability_noise_bound(self):
        q=self.Q[self.f['tomography']['frame_outcome_indices'][3]]
        rng=np.random.default_rng(2740);A=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));rho=A@A.conj().T;rho/=np.trace(rho)
        p=np.einsum('aij,ji->a',q,rho).real/30
        channel=np.einsum('a,aij->ij',p,q)/3
        self.assertLess(np.linalg.norm(channel-rho/40-13*np.eye(9)/120),1e-12)
        L=sum(P@rho@P for P in q)/30
        self.assertLess(np.linalg.norm(L-13*rho/40-3*np.eye(9)/40),1e-12)
        J=sum(np.outer(P.ravel(),P.ravel().conj()) for P in q)/270
        pt=J.reshape(9,9,9,9).transpose(0,3,2,1).reshape(81,81)
        self.assertAlmostEqual(np.linalg.eigvalsh(pt).min(),-1/36)
        noise=rng.normal(size=90);noise-=noise.mean()
        err=(40/3)*np.einsum('a,aij->ij',noise,q)
        self.assertLessEqual(np.linalg.norm(err),20*np.linalg.norm(noise)+1e-9)

    def test_overlap_incidence_and_native_cubic_dictionary(self):
        t=self.f['tomography'];M=np.zeros((810,27),dtype=int)
        for j,ids in enumerate(t['frame_outcome_indices']):M[ids,j]=1
        self.assertTrue(np.all(M.sum(1)==3));self.assertEqual(np.linalg.matrix_rank(M),21)
        native=read('../artifacts/canonical_su3_gauge_and_cubic.json')['solution']['d_triples']
        p=t['frame_to_native_cubic']
        self.assertEqual({tuple(sorted(p[i] for i in x)) for x in t['cubic_support_frame_triples']},
                         {tuple(sorted(x['triple'])) for x in native})
        self.assertEqual((t['unitary_frame_image_order'],t['unitary_antiunitary_frame_image_order']),(25920,51840))

    def test_oct_ground_witness_direct_matrix_energy(self):
        t=self.f['energies']['ground_witness'];a,b,c,d,e,f=t
        E=0.
        for u,v in [((a,b),(c,d)),((a,b),(e,f)),((c,d),(e,f))]:
            for i,j in itertools.product(u,v):
                P,Q=F.PI[i],F.PI[j];comm=P@Q-Q@P
                E+=3-np.trace(P@Q).real-2*np.linalg.norm(comm)**2
        chi=np.trace((F.PI[a]-F.PI[b])@(F.PI[c]-F.PI[d])@(F.PI[e]-F.PI[f])).imag
        E-=np.sqrt(3)*chi
        self.assertAlmostEqual(E,-12.5);self.assertAlmostEqual(chi,3*np.sqrt(3)/2)

    def test_oct_last_pair_separation_matches_exhaustion(self):
        E=F.scaled_pair()
        for case in self.f['energies']['pair_orbit_cases']:
            a,b=case['pair'];c,d=12,17
            V=(F.PI[a]-F.PI[b])@(F.PI[c]-F.PI[d])
            v=np.array([np.trace(V@P).imag*2*np.sqrt(3) for P in F.PI])
            L=E[a]+E[b]+E[c]+E[d]
            matrix=L[:,None]+L[None,:]-3*(v[:,None]-v[None,:])
            self.assertAlmostEqual(matrix.min(),min(L-3*v)+min(L+3*v))

    def test_exact_density_of_states_and_level_witnesses(self):
        rows=self.f['energies']['tetrahedron_density_of_states']
        self.assertEqual(sum(x['count'] for x in rows),120**4)
        self.assertEqual((rows[0]['six_energy'],rows[0]['count']),(-48,9720))
        self.assertEqual((rows[1]['six_energy']-rows[0]['six_energy'])/6,3)
        E=F.scaled_pair()
        for row in rows:
            a,b,c,d=row['witness']
            pair=sum(int(E[i,j]) for i,j in itertools.combinations((a,b,c,d),2))
            face=sum(F.exact_trace(t)[1] for t in [(a,b,c),(a,d,b),(a,c,d),(b,d,c)])
            self.assertEqual(pair-3*face,row['six_energy'])

    def test_control_words_act_on_actual_parents(self):
        gates=C.native_gates();_,_,labels,Q=C.parent_data()
        entries=self.c['control']['Clifford_words']
        self.assertEqual(len(entries),810)
        for row in entries[::73]:
            U=np.eye(9)
            for name in row['word']:U=gates[name]@U
            H=sum(F.PI[i] for i in row['ticks'])/2
            controlled=U@expm(-.371j*(np.eye(9)-Q))@U.conj().T
            self.assertLess(np.linalg.norm(controlled-expm(-.371j*H)),1e-11)

    def test_continuous_gate_clifford_boundary(self):
        S=np.array([[0,0,0],[0,.5,-.5],[0,-.5,.5]])
        for t in (-.37,0.,math.pi/2,math.pi,2*math.pi):
            U=expm(-1j*t*(np.eye(3)-S));Z=U@C.Z@U.conj().T
            monomial=np.all(np.sum(abs(Z)>1e-9,axis=0)==1)
            self.assertEqual(bool(monomial),abs(math.sin(t))<1e-9)

    def test_continuous_parent_controls_span_full_unitary_lie_algebra(self):
        ids=self.f['tomography']['frame_outcome_indices'][0]
        H=np.eye(9)[None]-self.Q[ids]
        gram=np.einsum('aij,bji->ab',H,H).real
        self.assertEqual(np.linalg.matrix_rank(gram,tol=1e-9),81)
        self.assertTrue(np.allclose(np.linalg.eigvalsh(gram),[0]*9+[2.25]*80+[360]))

    def test_thermal_magic_threshold_and_resource_limit(self):
        samples=self.c['control']['thermal_controls']
        for row in samples:
            self.assertAlmostEqual(row['ground_fidelity'],1/(1+2*math.exp(-row['beta'])))
            self.assertEqual(row['mana']>1e-10,row['beta']>math.log(2)+1e-10)

    def test_cluster_and_trace_bounds_recorded_with_hypotheses(self):
        for row in self.c['robustness']['samples']:
            self.assertLess(row['projector_error'],.25)
            self.assertGreaterEqual(row['observed_cluster_gap']+1e-12,row['certified_gap_lower'])
            self.assertLessEqual(row['cluster_projector_distance'],row['certified_projector_upper']+1e-12)
            self.assertLessEqual(row['loop_trace_error'],row['loop_error_upper']+1e-12)

    def test_pair_energy_perturbation_bound_on_new_perturbations(self):
        rng=np.random.default_rng(61101);P,Q=F.PI[0],F.PI[12]
        def energy(P,Q):return 3-np.trace(P@Q).real-2*np.linalg.norm(P@Q-Q@P)**2
        for angle in (.002,.02,.1):
            moved=[]
            for A in (P,Q):
                h=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9));h=(h+h.conj().T)/2
                U=expm(1j*angle*h/np.linalg.norm(h,2));moved.append(U@A@U.conj().T)
            eps=max(np.linalg.norm(moved[0]-P,2),np.linalg.norm(moved[1]-Q,2))
            self.assertLessEqual(abs(energy(*moved)-energy(P,Q)),(6+24*np.sqrt(2))*eps+1e-12)

    def test_minimal_extension_commutator_certificate_and_tamper(self):
        gens=[(tuple(x['permutation']),tuple(x['sign_bits'])) for x in self.g['paired_signed_generators']]
        mats=[np.array(x) for x in self.g['paired_GF5_generators']]
        rows=self.g['no_lift_integer_GF2_certificate']
        self.assertTrue(G.verify_witness(rows,gens,mats))
        bad=copy.deepcopy(rows);bad[0]['rhs']^=1
        with self.assertRaises(AssertionError):G.verify_witness(bad,gens,mats)
        self.assertEqual((self.g['minimum_common_extension_order'],self.g['fibre_center_order']),(61440,4))
        self.assertEqual(self.g['central_generator_sign_choices_allowed'],[])

    def test_spinor_anticommutation_cannot_be_scalar_rephased(self):
        def matrix(key):return (np.array(key[:16]).reshape(4,4)+1j*np.array(key[16:]).reshape(4,4))/2
        A,B=map(matrix,self.g['paired_unitary_dyadic_generators'][:2])
        self.assertLess(np.linalg.norm(A@B+B@A),1e-12)
        A=np.exp(.31j)*A;B=np.exp(-.77j)*B
        self.assertGreater(np.linalg.norm(A@B-B@A),1.)

    def test_markov_failure_is_an_exact_native_matrix_witness(self):
        R=F.PI[3];Q=np.eye(9)-sum(F.PI[i] for i in self.tetra['canonical_native_ticks'])/2;f4=R@Q
        self.assertAlmostEqual(np.trace(f4@R).real/9,1/9)
        self.assertAlmostEqual(np.trace(f4).real/27,1/27)
        self.assertEqual(self.c['markov']['fusion_path_ledger'][5]['minimum_ordinary_trace_dimension'],27)

    def test_fresh_register_markov_property_on_every_matrix_unit(self):
        W=np.kron(np.kron(C.Z,np.eye(3)),C.Z);P=(np.eye(27)+W+W@W)/3
        for i,j in itertools.product(range(9),repeat=2):
            x=np.zeros((9,9));x[i,j]=1
            self.assertAlmostEqual(abs(np.trace(np.kron(x,np.eye(3))@P)/27-np.trace(x)/27),0.)

    def test_real_first_order_geometry_in_operator_not_vector_coordinates(self):
        _,_,labels,Q=C.parent_data();H=np.eye(9)-Q;rng=np.random.default_rng(8145)
        a,b,M=[rng.normal(size=(9,9))+1j*rng.normal(size=(9,9)) for _ in range(3)]
        D=lambda x:H@x-x@H
        first=D(a@M@b)-a@D(M@b)-(D(a@M)-a@D(M))@b
        self.assertLess(np.linalg.norm(first),1e-10)
        self.assertLess(np.linalg.norm(D(M).conj().T+D(M.conj().T)),1e-10)

    def test_spectral_action_is_constant_on_distinct_parents(self):
        for t in self.tetra['oriented_tetrahedra'][::269]:
            H=sum(F.PI[i] for i in t)/2
            D=np.kron(np.eye(9),H)-np.kron(H.T,np.eye(9))
            self.assertAlmostEqual(np.exp(-.73*np.linalg.eigvalsh(D)**2).sum(),45+36*np.exp(-.73))

if __name__=='__main__':unittest.main()
