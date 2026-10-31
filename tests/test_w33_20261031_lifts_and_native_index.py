"""Independent operator, provenance and exact-certificate controls."""
import copy,itertools,json,sys,unittest
from pathlib import Path
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261031_signed_cubic_lift as cubic
import w33_20261031_arc_degree_obstruction as arcs
import w33_20261031_native_phase_space_overlap as native
import w33_20261031_local_tick_mediator as local

def read(name):return json.loads((ROOT/f'data/w33_20261031_{name}.json').read_text())
def matrix(rows):return s.Matrix([[s.sympify(x)for x in row]for row in rows])

class LiftAndIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit=read('unitary_stabilizer_lift');cls.cubic=read('signed_cubic_lift');cls.old=read('petersen_stabilizer');cls.index=read('native_phase_space_overlap')

    def test_unitaries_match_actual_finite_field_generators(self):
        S=s.Matrix(self.old['two_qubit_kernel_intertwiner']['intertwiner_mod5']);Si=S.inv_mod(5)
        def scalar(x):
            a,b=s.fraction(x);return int(a)*pow(int(b),-1,5)%5
        for row,G in zip(self.unit['unitary_generators'],self.old['symplectic_matrix_generators']):
            U=matrix(row);self.assertEqual(U.conjugate().T*U,s.eye(4));self.assertEqual(s.simplify(U.det()),1)
            reduced=s.Matrix(4,4,[scalar(s.re(x))+2*scalar(s.im(x))for x in U])%5
            self.assertEqual(reduced,(Si*s.Matrix(G)*S)%5)

    def test_spinor_lift_recovers_frozen_five_axis_action(self):
        axes=[matrix(row)for row in self.unit['gamma_axes']];L=s.Matrix(self.unit['five_dimensional_basis_intertwiner'])
        for A,B in itertools.combinations(axes,2):self.assertEqual(A*B,-B*A)
        for u,old in zip(self.unit['unitary_generators'],self.old['signed_five_dimensional_generators']):
            U=matrix(u);M=L*s.Matrix(old)*L.T
            for j,A in enumerate(axes):self.assertEqual(U*A*U.conjugate().T,sum((M[i,j]*B for i,B in enumerate(axes)),s.zeros(4)))

    def test_signed_cubic_transport_preserves_actual_repository_coefficients(self):
        native_terms=json.loads((ROOT/'artifacts/canonical_su3_gauge_and_cubic.json').read_text())['solution']['d_triples']
        signs={tuple(sorted(t['triple'])):int(t['sign'])for t in native_terms};mapping=self.cubic['weight_to_native']
        coeff={tuple(row['triple']):row['coefficient']for row in self.cubic['coefficient_rows']}
        for t,c in coeff.items():self.assertEqual(c,signs[tuple(sorted(mapping[i]for i in t))])
        for gen in self.cubic['signed_generators']:
            p,b=gen['permutation'],gen['sign_bits']
            for t,c in coeff.items():self.assertEqual(c*(-1)**sum(b[i]for i in t),coeff[tuple(sorted(p[i]for i in t))])
        self.assertEqual((self.cubic['signed_group_order'],self.cubic['diagonal_kernel_order']),(30720,32))

    def test_real_sign_obstruction_reconstructs_group_words(self):
        d=self.cubic;p=[g['permutation']for g in d['signed_generators']];co={tuple(r['triple']):r['coefficient']for r in d['coefficient_rows']}
        self.assertTrue(cubic.verify_section_witness(d['real_sign_section'],p,co))
        central=[int(i>=11)for i in range(27)]
        self.assertTrue(cubic.verify_section_witness(d['unitary_double_cover_sign_lift'],p,co,self.old['symplectic_matrix_generators'],central))
        bad=copy.deepcopy(d['real_sign_section']);bad['contradiction_rows'][0]['rhs']^=1
        with self.assertRaises(AssertionError):cubic.verify_section_witness(bad,p,co)

    def test_degree_witnesses_are_morphisms_at_infinity_too(self):
        d=read('arc_degree_obstruction');old=read('exterior_search')
        for row in d['interpolations']:
            q=row['q'];F=row['numerator_coefficients'];G=row['denominator_coefficients']
            for a,b in next(r['matching']for r in old if r['q']==q):
                for a,b in ((a,b),(b,a)):
                    f=F[-1]if a=='inf'else sum(v*pow(a,i,q)for i,v in enumerate(F))%q
                    g=G[-1]if a=='inf'else sum(v*pow(a,i,q)for i,v in enumerate(G))%q
                    self.assertTrue(f or g)
                    self.assertEqual(g,0)if b=='inf'else self.assertEqual((f-b*g)%q,0)
            self.assertGreaterEqual(row['minimum_morphism_degree']**2,q)

    def test_paley_blocks_retain_independent_concurrence_condition(self):
        for row in read('arc_degree_obstruction')['conference_controls']:
            C=np.array(row['reordered_Paley_conference']);q=row['q']
            np.testing.assert_array_equal(C@C.T,q*np.eye(q+1,dtype=int))
            for i,j in itertools.combinations(range((q+1)//2),2):
                B=C[2*i:2*i+2,2*j:2*j+2];np.testing.assert_array_equal(B@B.T,2*np.eye(2,dtype=int))

    def test_native_inertia_is_verified_with_integer_arithmetic(self):
        for row in self.index['exact_inertia_certificates']:
            result=native.verify_inertia(row['certificate'])
            self.assertEqual(result['index'],row['verified']['index']);self.assertGreater(result['gap_lower_decimal'],.1)
        bad=copy.deepcopy(self.index['exact_inertia_certificates'][0]['certificate']);bad['rational_congruence_numerators'][0]=[0]*72
        with self.assertRaises(AssertionError):native.verify_inertia(bad)

    def test_exact_certificate_is_bound_to_native_kernel(self):
        gs,c,ts=native.operators();gs=[np.array(g,dtype=complex)for g in gs];c=np.array(c,dtype=complex);ts=[np.array(t,dtype=complex)for t in ts]
        for row in self.index['exact_inertia_certificates']:
            H,Gamma=native.kernel(gs,c,ts,float(s.Rational(row['mass'])));M=np.block([[H.real,-H.imag],[H.imag,H.real]])
            cert=row['certificate'];reconstructed=(np.array(cert['A'])+np.sqrt(3)*np.array(cert['B']))/cert['denominator']
            np.testing.assert_allclose(M,reconstructed,atol=1e-14)
            self.assertEqual(native.overlap(H,Gamma)['index'],row['verified']['index'])

    def test_native_index_counts_net_chirality_not_just_zero_modes(self):
        a,b=self.index['mass_samples'];self.assertEqual((a['index'],a['zero_modes']),(-1,1));self.assertEqual((b['index'],b['zero_modes']),(1,3))
        self.assertAlmostEqual(sum(b['zero_mode_chiralities']),1)
        controls=self.index['controls'];self.assertEqual(controls['reverse_one_flux_plane']['index'],-1);self.assertEqual(controls['commuting_translations']['index'],0)
        self.assertLess(controls['small_link_perturbation']['kernel_norm_change'],.1);self.assertEqual(controls['small_link_perturbation']['index'],1)

    def test_local_mediator_has_the_claimed_exact_accidental_symmetry(self):
        E=local.energy_matrix();self.assertEqual(set(E.flat),{0,2,3});self.assertTrue(np.all(np.sum(E==3,axis=1)==2));self.assertTrue(np.all(np.sum(E==2,axis=1)==117))
        permutation=np.arange(120);permutation[[0,1]]=permutation[[1,0]]
        # Ticks0,1 are two outcomes of the same source direction.
        np.testing.assert_array_equal(E[np.ix_(permutation,permutation)],E)

    def test_local_heatbath_is_reversible_and_not_a_time_arrow(self):
        E=local.energy_matrix();neighbors=[0,3,7,11];beta=.4;p=local.heatbath(E,neighbors,beta);energy=E[:,neighbors].sum(axis=1)
        weights=np.exp(-beta*energy)
        np.testing.assert_allclose(weights[:,None]*p[None,:],weights[None,:]*p[:,None],atol=1e-15)
        self.assertAlmostEqual(p.sum(),1);self.assertGreater(p.min(),0)

    def test_local_transfer_spectrum_and_high_temperature_gate(self):
        E=local.energy_matrix();t=.31;x=np.exp(-t);a=x**3;b=x**2
        eigen=np.linalg.eigvalsh(np.exp(-t*E));expected=sorted([1+2*a+117*b]+[1+2*a-3*b]*39+[1-a]*80)
        np.testing.assert_allclose(eigen,expected,atol=1e-12)
        self.assertTrue(np.all(eigen>0));self.assertLess(4*np.tanh(1.5*.16),1)

if __name__=='__main__':unittest.main()
