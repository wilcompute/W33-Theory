import pathlib,sys,unittest,itertools
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261102_two_sided_phase_convention as P

class PhaseConvention(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result=P.build()
    def test_all_pairs_and_wrong_convention_count(self):
        self.assertEqual(self.result['ordered_label_pairs'],6561)
        self.assertEqual(self.result['shift_first_pairs_disagreeing_with_displayed_clock_first_phase'],4320)
        self.assertLess(self.result['maximum_clock_first_matrix_residual'],1e-12)
    def test_exact_commuting_pair_census(self):
        self.assertEqual(self.result['exact_phase_histogram'],{0:2241,1:2160,2:2160})
    def test_two_sided_operator_action_on_every_matrix_unit(self):
        U=P.old.qutrit_pauli(1,2);V=P.old.qutrit_pauli(2,1)
        for i,j in itertools.product(range(3),repeat=2):
            M=np.zeros((3,3));M[i,j]=1
            vector=np.kron(U,V.conj())@M.ravel()
            self.assertTrue(np.allclose(vector,(U@M@V.conj().T).ravel()))
    def test_explicit_shift_clock_witness(self):
        w=P.old.omega;X=P.old.qutrit_pauli(0,1);Z=P.old.qutrit_pauli(1,0)
        self.assertTrue(np.allclose(X@Z,w*w*Z@X))
        self.assertFalse(np.allclose(X@Z,w*Z@X))
    def test_paper_uses_the_same_clock_first_definition_as_source(self):
        text=(ROOT/'papers/forty_points/sec03_selfentangle.tex').read_text()
        self.assertIn('P_u=Z^{u_1}X^{u_2}',text)
        self.assertIn('clock-first',text);self.assertIn('Section~2',text)
if __name__=='__main__':unittest.main()
