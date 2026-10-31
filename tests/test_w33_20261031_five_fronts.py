"""Scientific controls for the five-front continuation, including frozen witnesses."""
import importlib.util
import itertools,json,math,unittest
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'analysis'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


arc=module('w33_20261031_exterior_search')
bounds=module('w33_20261031_even_set_bounds')
rates=module('w33_20261031_tick_rate_entropy')
continuum=module('w33_20261031_continuum_chirality')


class FiveFrontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.group=json.loads((ROOT/'data/w33_20261031_petersen_stabilizer.json').read_text())

    def test_search_known_positive_and_negative_controls(self):
        self.assertEqual(arc.solve(7)['status'],'found')
        self.assertEqual(arc.solve(5,square=True)['status'],'found')
        self.assertEqual(arc.solve(13,square=True)['status'],'none_complete')
        self.assertEqual(arc.solve(19)['status'],'none_complete')

    def test_independent_cross_ratio_and_conic_predicates(self):
        for square in (True,False):
            a=arc.solve(19,square=square,backend='conic')
            b=arc.solve(19,square=square,backend='cross_ratio')
            self.assertEqual(a['compatibility_sha256'],b['compatibility_sha256'])
            self.assertEqual((a['status'],a['nodes']),(b['status'],b['nodes']))

    def test_reject_nonfields_in_prime_field_search(self):
        with self.assertRaises(ValueError):arc.solve(9)

    def test_full_projective_group_witness_and_symplectic_generators(self):
        J=np.block([[np.zeros((2,2),dtype=int),np.eye(2,dtype=int)],[-np.eye(2,dtype=int),np.zeros((2,2),dtype=int)]])
        for g in self.group['symplectic_matrix_generators']:
            G=np.array(g);self.assertTrue(np.array_equal(G.T@J@G%5,J%5))
        ident=tuple(range(20));seen={ident};queue=[ident]
        for p in queue:
            for g in self.group['projective_permutation_generators']:
                t=tuple(g[p[i]] for i in range(20))
                if t not in seen:seen.add(t);queue.append(t)
        self.assertEqual(len(seen),960)
        self.assertEqual(self.group['pair_image_order'],60)
        self.assertEqual(self.group['kernel_order'],16)

    def test_kernel_is_cut_code_not_just_group_of_same_order(self):
        labels=self.group['K5_edge_labels']
        cut={tuple(v[i]^v[j] for i,j in labels) for v in itertools.product(range(2),repeat=5)}
        self.assertEqual(cut,{tuple(v) for v in self.group['kernel_flip_vectors']})
        self.assertEqual(self.group['group_element_order_counts']['6'],240)
        self.assertEqual(self.group['lifted_kernel_order_counts'],{'1':1,'2':11,'4':20})

    def test_search_113_completion_is_required_for_moore_claim(self):
        a=json.loads((ROOT/'data/w33_20261031_exterior_search_square.json').read_text())[-1]
        b=json.loads((ROOT/'data/w33_20261031_exterior_search_square_cross_ratio.json').read_text())[-1]
        self.assertEqual((a['q'],a['status']),(113,'none_complete'))
        # The second backend independently constructs the entire exact
        # compatibility graph. Its timed-out traversal is not an exclusion.
        self.assertEqual(b['q'],113)
        self.assertEqual(a['compatibility_sha256'],b['compatibility_sha256'])

    def test_actual_lift_has_an_explicit_two_qubit_pauli_dictionary(self):
        d=self.group['two_qubit_kernel_intertwiner'];S=np.array(d['intertwiner_mod5'])
        self.assertNotEqual(round(np.linalg.det(S))%5,0)
        for a,t in zip(d['actual_symplectic_generators'],d['reduced_Pauli_generators']):
            self.assertTrue(np.array_equal(np.array(a)@S%5,S@np.array(t)%5))
        self.assertEqual(d['kernel_order'],32)

    def test_general_bound_keeps_heavy_coverage_branch(self):
        self.assertEqual([bounds.local_bound(q)['general_even_set_lower_bound'] for q in (3,5,7)],[10,16,24])
        r=bounds.local_bound(17)
        self.assertEqual(r['general_even_set_lower_bound'],72)
        self.assertGreater(r['coverage_0_2_lower_bound'],r['general_even_set_lower_bound'])

    def test_context_entropy_beats_event_in_specified_model(self):
        rho=np.diag([1]+[0]*8)
        support=np.flatnonzero(np.real(np.einsum('aij,ji->a',rates.PI,rho))>1-1e-10)
        self.assertEqual(len(support),4)
        p=np.zeros(120);p[0]=1;c=np.zeros(120);c[support]=.25
        self.assertAlmostEqual(rates.objective(p,.01)/.01,-math.log(3),places=10)
        self.assertAlmostEqual(rates.objective(c,.01)/.01,-math.log(4),places=10)
        self.assertLess(rates.objective(c,.01),rates.objective(p,.01))

    def test_uniform_hessian_is_exact_not_fitted_transition(self):
        uniform=np.ones(120)/120;v=np.zeros(120);v[0]=1/np.sqrt(2);v[1]=-1/np.sqrt(2)
        for T in (.04,.08):
            eps=1e-6
            actual=(rates.objective(uniform+eps*v,T)-2*rates.objective(uniform,T)+rates.objective(uniform-eps*v,T))/(eps*eps)
            self.assertAlmostEqual(actual,120*T-1/(3*T),delta=.001)

    def test_first_order_global_transition_bound_above_spinodal(self):
        lower=2/(3*math.log(270));spinodal=1/math.sqrt(360)
        self.assertGreater(lower,spinodal)
        T=.1
        uniform=2/3-T*math.log(1080)
        context_trial=-T*math.log(4)
        self.assertLess(context_trial,uniform)
        self.assertGreater(120*T-1/(3*T),0)

    def test_rate_count_ratio_can_select_event_or_context(self):
        p=np.zeros(120);p[0]=1;c=np.zeros(120);c[[0,3,6,9]]=.25
        self.assertLess(rates.objective(p,.01,.5),rates.objective(c,.01,.5))
        self.assertLess(rates.objective(c,.01,1),rates.objective(p,.01,1))
        self.assertAlmostEqual(math.log(3)/math.log(4),.7924812503605781)

    def test_continuum_control_converges_and_respects_actual_group(self):
        k=np.array([.2,-.3,.4,.1,-.2]);target=k@k
        self.assertLess(abs(continuum.d5_symbol(k,.05)-target),abs(continuum.d5_symbol(k,.1)-target))
        value=continuum.d5_symbol(k,.1)
        for g in self.group['signed_five_dimensional_generators']:
            self.assertAlmostEqual(continuum.d5_symbol(np.array(g)@k,.1),value,places=12)

    def test_actual_stabilizer_preserves_named_unsigned_e6_support(self):
        r=continuum.internal_e6_support(self.group['signed_five_dimensional_generators'])
        self.assertEqual(r['sector_orbit_sizes'],[1,10,16])
        self.assertEqual(len(r['cubic_support']),45)
        self.assertEqual(r['cubic_support_sector_sizes'],[5,40])

    def test_functional_regulator_does_not_manufacture_chiral_index(self):
        M=np.diag([0,.4,1.2]).astype(complex)
        r=continuum.overlap_control(M,lambda x:x*x-2*x-.3)
        self.assertEqual(r['index'],0)
        self.assertLess(r['GW_defect'],1e-10)


if __name__=='__main__':unittest.main()
