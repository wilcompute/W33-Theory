"""Controls for the third continuation: phases, fields, codes and modules."""
import pathlib,sys,json,copy,itertools,unittest,math
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261031_complex_cubic_obstruction as phase
import w33_20261031_exterior_arc_code as code
import w33_20261031_geometry_sensitive_mediator as dynamics
import w33_20261031_phase_space_refinement as refine
from w33_20261031_native_phase_space_overlap import operators,kernel

def read(stem):return json.loads((ROOT/f'data/w33_20261031_{stem}.json').read_text())

class CrossFieldRefinementTests(unittest.TestCase):
    def test_complex_phase_certificate_is_multiplicative_not_mod2_only(self):
        d=read('complex_cubic_obstruction');self.assertTrue(phase.verify(d));self.assertEqual(len(d['multiplicative_contradiction']),9)
        total=np.zeros(16,dtype=int);b=0
        for row in d['multiplicative_contradiction']:total+=row['integer_power']*np.array(row['exponents']);b+=row['integer_power']*row['rhs_sign_exponent']
        self.assertFalse(total.any());self.assertEqual(b%2,1)
        bad=copy.deepcopy(d);bad['multiplicative_contradiction'][0]['integer_power']+=1
        with self.assertRaises(AssertionError):phase.verify(bad)

    def test_perfect_stabilizer_hypotheses_are_frozen_explicitly(self):
        controls=read('complex_cubic_obstruction')['group_controls']
        self.assertEqual(controls['projective_perfect']['derived_order'],960)
        self.assertEqual(controls['spinor_point_stabilizer_perfect']['derived_order'],60)
        self.assertEqual(controls['covering_spinor_point_stabilizer_perfect']['derived_order'],120)

    def test_cross_field_generator_map_respects_all_group_products(self):
        d=read('cross_field_stabilizers');A=[np.array(M)for M in d['q5_matrix_generators']];B=[np.array(M)for M in d['q3_corrected_matrix_generators']]
        key=lambda M:tuple(map(int,M.flat));I=np.eye(4,dtype=int);seen={key(I):I};todo=[I]
        for P in todo:
            for g,h in zip(A,B):
                Q=g@P%5;R=h@seen[key(P)]%3;k=key(Q)
                if k not in seen:seen[k]=R;todo.append(Q)
                else:np.testing.assert_array_equal(R,seen[k])
        self.assertEqual(len(seen),1920);self.assertEqual(len({key(M)for M in seen.values()}),1920)
        np.testing.assert_array_equal(seen[key(-I%5)],-I%3)

    def test_q3_generators_preserve_the_actual_five_octet_frame(self):
        d=read('cross_field_stabilizers');P=np.array(d['q3_point_coordinates']);pid={tuple(p):i for i,p in enumerate(P)}
        frame={frozenset(o)for o in d['selected_q3_frame_octets']};J=np.array(d['q3_symplectic_form'])
        for raw in d['q3_corrected_matrix_generators']:
            M=np.array(raw);np.testing.assert_array_equal(M.T@J@M%3,J%3)
            mapped=P@M.T%3;lead=np.argmax(mapped!=0,axis=1);mapped=mapped*mapped[np.arange(40),lead,None]%3
            perm=[pid[tuple(p)]for p in mapped];self.assertEqual({frozenset(perm[i]for i in o)for o in frame},frame)

    def test_external_code_geometry_is_biregular_and_has_no_four_cycles(self):
        for q in (3,5,7,11):
            E,L,H=code.geometry(q);n=(q+1)//2
            self.assertTrue(np.all(H.sum(0)==n-1));self.assertTrue(np.all(H.sum(1)==n))
            G=H.astype(int).T@H.astype(int);np.fill_diagonal(G,0);self.assertLessEqual(G.max(),1)
        with self.assertRaises(ValueError):code.geometry(9)

    def test_small_external_codes_have_exact_distances(self):
        for q,want in ((3,2),(5,5),(7,4)):
            E,L,H=code.geometry(q);r,K=code.binary_kernel(H);words=[0]
            for k in K:words.extend(w^k for w in list(words))
            distance=min(w.bit_count()for w in words if w);self.assertEqual(distance,want)
            for w in words:
                if w.bit_count()==(q+1)//2:self.assertTrue(code.verify_arc(q,[p for i,p in enumerate(E)if w>>i&1]))

    def test_frozen_arc_code_witnesses_satisfy_independent_parities(self):
        for row in read('exterior_arc_code')['rows']:
            if 'bound_equality_points'not in row:continue
            q=row['q'];E,L,H=code.geometry(q);points=[tuple(p)for p in row['bound_equality_points']]
            word=np.array([int(p in points)for p in E]);self.assertFalse(np.any(H@word%2));self.assertTrue(code.verify_arc(q,points))

    def test_current_norm_resolves_the_actual_commutation_graph(self):
        C=dynamics.current_cost();self.assertEqual(set(np.round(C.flat,8)),{0.,round(4/3,8)})
        self.assertTrue(np.all(np.sum(C>1,axis=1)==81))
        self.assertEqual(np.linalg.matrix_rank(dynamics.ADJ),40)

    def test_sensitive_transfer_splits_the_24_and_15_modes(self):
        E=dynamics.energy_matrix()-.6*dynamics.current_cost();beta=.7
        expected=sorted(v for v,m in dynamics.spectrum(beta,1.,.6)for _ in range(m))
        np.testing.assert_allclose(np.linalg.eigvalsh(np.exp(-beta*E)),expected,atol=1e-12)
        self.assertNotAlmostEqual(dynamics.spectrum(beta,1.,.6)[1][0],dynamics.spectrum(beta,1.,.6)[2][0])

    def test_local_zero_temperature_threshold_has_constructive_competitors(self):
        E0=dynamics.energy_matrix();C=dynamics.current_cost();a,b=np.argwhere(C>1)[0]
        self.assertGreater((E0-1.4*C)[a,b],0)
        self.assertAlmostEqual((E0-1.5*C)[a,b],0)
        self.assertLess((E0-1.6*C)[a,b],0)

    def test_detailed_balance_survives_negative_current_bond_energy(self):
        E=dynamics.energy_matrix()-2*dynamics.current_cost();neighbors=[0,3,14,28];p=dynamics.heatbath(E,neighbors,.6);w=np.exp(-.6*E[:,neighbors].sum(1))
        np.testing.assert_allclose(w[:,None]*p[None,:],w[None,:]*p[:,None],atol=1e-12)

    def test_adjoint_cancels_central_flux_while_fundamental_does_not(self):
        T=refine.translations(3)
        self.assertGreater(np.linalg.norm(T[0]@T[1]-T[1]@T[0]),1)
        A=[np.kron(U.conj(),U)for U in T]
        for X,Y in itertools.combinations(A,2):self.assertLess(np.linalg.norm(X@Y-Y@X),1e-12)

    def test_adjoint_free_gap_bound_holds_for_continuous_momenta(self):
        for p in np.random.default_rng(333).uniform(-np.pi,np.pi,(500,4)):
            W,v,r=refine.flat_symbol(p);u=1-np.cos(p)
            self.assertAlmostEqual(r*r,1+2*sum(u[i]*u[j]for i,j in itertools.combinations(range(4),2)),places=12)
            self.assertGreaterEqual(r,1);self.assertLessEqual(r,7)

    def test_charged_ledger_requires_common_resolution(self):
        d=read('phase_space_refinement');coarse,fine=d['charged_index_resolution']
        self.assertEqual([r['N']for r in coarse['rows']],[15]*3);self.assertEqual([r['N']for r in fine['rows']],[23]*3)
        self.assertEqual(coarse['weighted_index_sum'],60);self.assertEqual(fine['weighted_index_sum'],0)
        self.assertEqual([r['numerical_index']for r in fine['rows']],[-1,-4,-16])
        self.assertTrue(all(r['numerical_gap']>.1 for r in fine['rows']))

if __name__=='__main__':unittest.main()
