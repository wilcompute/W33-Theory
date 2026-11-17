"""Independent tests: E6 genuine adjoint Casimir, competing SU5 vacua, J3O, 27x27 memory."""
import importlib.util,unittest
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def load(name,file):
    sp=importlib.util.spec_from_file_location(name,ROOT/file)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
e6=load("casE6","toe_20261116_E6_Casimir_UV_adjoint.py")
su5=load("su5else","toe_20261116_SU5_adjoint_three_family_spectral.py")
jordan=load("j3oct","toe_20261116_STU_Jordan_24missing.py")
sw=load("swapQ","toe_20261116_qutrit_SWAP_causal_break_memory.py")

class E6GenuineInvariant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=e6.verify()
    def test_6d_all_F_zero(self):
        self.assertEqual(self.r["gradient_rank"],2)
        self.assertEqual(self.r["gradient_nullspace_dim"],4)
    def test_exact_three_Casimir_selection(self):
        self.assertEqual(self.r["selected_Casimir_coefficients"],["-849","18/5","1","0","0","0"])
    def test_full_SU5_Cartan_Hessian_rank(self):
        self.assertEqual(self.r["selected_SU5_Cartan_Hessian_rank"],4)
        self.assertNotEqual(self.r["selected_SU5_Cartan_Hessian_det"],"0")
    def test_generalized_exact_mass(self):
        x=self.r["SU5_Cartan_generalized_mass_certificate"]
        self.assertEqual(x["canonical_trace_metric_generalized_F_Hessian_eigenvalues"],{"-180":1,"480":2,"7224":1})
    def test_overclaims_guarded(self):
        self.assertIn("Non-Cartan",self.r["scope"])

class SymmetrySelectionNotUnique(unittest.TestCase):
    def test_competing_vacua(self):
        z=su5.competing_SU5_F_flat_vacua()
        self.assertEqual(len(z["two_eigenvalue_branches"]),4)
        groups={v["centralizer"] for v in z["two_eigenvalue_branches"]}
        self.assertIn("S(U(4) x U(1))",groups)
        self.assertIn("S(U(3) x U(2))",groups)
    def test_all_F_zero_but_same_energy(self):
        x=su5.competing_SU5_F_flat_vacua()
        self.assertTrue(all(v["globally_SUSY_zero_F_energy"] for v in x["two_eigenvalue_branches"]))
    def test_SU5_effective_not_E6_cubic(self):
        self.assertIn("no degree-3",su5.su5_adjoint_spectral()["IMPORTANT_UV_CAVEAT"])

class STUOctonionic(unittest.TestCase):
    def test_exact_cubic_diagonal(self):
        x=jordan.diagonal_and_real_check()
        self.assertEqual(x["diagonal_restriction"],"abc")
        self.assertEqual(x["real_dim_total"],27)
    def test_24_missing(self):
        z=jordan.verify()
        self.assertEqual(z["topological_vector_obstruction"]["missing_variables_for_full_J3O_harmonic_C3_sector"],24)

class CausalMemory(unittest.TestCase):
    def test_coherent_vs_classical_Bell(self):
        x=sw.verify()
        self.assertAlmostEqual(x["coherent_memory"]["Bell_fidelity"],1)
        self.assertAlmostEqual(x["dephased_classical_memory"]["Bell_fidelity"],1/3)
        self.assertAlmostEqual(x["without_return_SWAP"]["Bell_fidelity"],1/9)
    def test_matched_MUB_witness(self):
        x=sw.verify()
        self.assertAlmostEqual(x["coherent_memory"]["four_MUB_witness_sum"],4)
        self.assertAlmostEqual(x["dephased_classical_memory"]["four_MUB_witness_sum"],2)
        self.assertAlmostEqual(x["without_return_SWAP"]["four_MUB_witness_sum"],4/3)
    def test_memory_reset_is_causal_break(self):
        x=sw.initial_density()
        y=sw.swap_SE(x)
        z0=sw.trace_E(sw.swap_SE(sw.reset_S(y,0)))
        z2=sw.trace_E(sw.swap_SE(sw.reset_S(y,2)))
        import numpy as np
        self.assertLess(float(np.max(np.abs(z0-z2))),1e-12)
    def test_photonic_hardware_not_claimed(self):
        self.assertTrue(sw.verify()["hardware_unperformed"])

if __name__=="__main__":unittest.main()
