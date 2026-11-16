import importlib.util
from fractions import Fraction as Q
from pathlib import Path
from math import log2
import unittest
P=Path(__file__).resolve().parents[1]/"analysis"/"toe_20261116_qutrit_causal_break_discriminator.py"
spec=importlib.util.spec_from_file_location("causal",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ProcessCausalBreak(unittest.TestCase):
    def test_verify(self): self.assertTrue(m.verify()["status"].startswith("PASS"))
    def test_marginals(self):
        for t in [Q(0),Q(1,3),Q(1)]:
            P=m.joint(t)
            self.assertTrue(all(sum(P[j])==Q(1,3) for j in range(3)))
            self.assertTrue(all(sum(P[j][k] for j in range(3))==Q(1,3) for k in range(3)))
    def test_same_probability(self):
        self.assertEqual(m.witness(Q(0))["probability_matching_outcomes"],"1/3")
        self.assertEqual(m.witness(Q(1))["probability_matching_outcomes"],"1")
        self.assertAlmostEqual(m.witness(Q(1))["mutual_information_bits"],log2(3))
    def test_quantum_memory_restores_Bell_correlations(self):
        r=m.quantum_memory_bell_return()
        self.assertEqual(r["coherent_Bell_return_fidelity"],"1")
        self.assertEqual(r["classical_memory_Bell_return_fidelity"],"1/3")
        self.assertEqual(r["coherent_partial_transpose_negative_eigenvalues"],3)
        self.assertTrue(r["computational_joint_probabilities_identical"])
    def test_exact_tail(self):
        self.assertEqual(m.pvalue_null(9,9),Q(1,3)**9)
        self.assertLess(float(m.pvalue_null(24,16)),.001)
if __name__=="__main__":unittest.main()
