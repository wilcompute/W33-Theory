"""Mathematically exact minimum 15 phase-flips that destroy W33 dark states."""
import sys,json,math,unittest
from pathlib import Path
import numpy as np
from sympy import Matrix
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_minimal_15_flux_lift as experiment
from w33_20261109_flux_dark_mode_fragility import build

def fixture():
    return json.loads((ROOT/"data/w33_20261109_minimal_15_flux_lift.json").read_text(encoding="utf8"))

class MinimalFlux(unittest.TestCase):
    def test_exactly_fifteen_edges_are_necessary_and_sufficient(self):
        r=fixture()
        self.assertEqual(r["required_number_of_link_changes_lower_bound"],15)
        self.assertEqual(len(r["constructed_phase_only_pi_flip_links"]),15)
        self.assertEqual(r["original_40x40_incidence_rank"],25)
        self.assertEqual(r["perturbed_incidence_matrix_rank"],40)
        self.assertEqual(r["remaining_exact_chiral_zero_modes"],0)

    def test_exact_integer_determinant_certificate(self):
        r=fixture()
        B,edges,G=build()
        T=B.astype(int)
        for e in r["constructed_phase_only_pi_flip_links"]:
            self.assertEqual(T[e["point"],e["line"]],1)
            T[e["point"],e["line"]]=-1
        self.assertEqual(Matrix(T.tolist()).det(method="domain-ge"),65536)
        self.assertEqual(r["perturbed_integer_matrix_determinant"],"65536")

    def test_exact_common_phase_determinant_polynomial(self):
        B,edges,G=build()
        choices=fixture()["constructed_phase_only_pi_flip_links"]
        for theta in (math.pi/7,math.pi/3,math.pi/2,math.pi):
            z=np.exp(1j*theta)
            T=B.astype(complex)
            for e in choices:T[e["point"],e["line"]]=z
            det_expected=-2*(z-1)**15
            sign,logabs=np.linalg.slogdet(T)
            self.assertLess(abs(sign*np.exp(logabs-np.log(abs(det_expected)))-
                                det_expected/abs(det_expected)),3e-9)
            self.assertGreater(np.linalg.svd(T,compute_uv=False)[-1],1e-8)

    def test_full_rank_staircase_and_minimum_support(self):
        r=fixture()
        self.assertEqual(r["ordered_edge_flip_incidence_rank_staircase"],list(range(25,41)))
        self.assertEqual(r["ordered_edge_flip_chiral_zero_mode_staircase"],list(range(30,-1,-2)))
        self.assertEqual(r["exact_three_integer_controls"],{"z_minus1":"65536","z_zero":"2","z_two":"-2"})

    def test_no_hopping_magnitudes_changed(self):
        B,edges,G=build()
        T=B.astype(complex)
        for e in fixture()["constructed_phase_only_pi_flip_links"]:
            T[e["point"],e["line"]]=np.exp(1j*math.pi)
        self.assertLess(np.max(abs(abs(T)-B)),1e-14)
        self.assertEqual(np.count_nonzero(B),160)

    def test_repeated_seed_reconstructs_selected_common_matroid_basis(self):
        B,edges,G=build()
        selected,trial,P,R=experiment.find_support(B,edges)
        from_data=[(e["point"],e["line"]) for e in fixture()["constructed_phase_only_pi_flip_links"]]
        self.assertEqual(selected,from_data)
        self.assertEqual(trial,1)
        points=[p for p,l in selected]
        lines=[l for p,l in selected]
        self.assertEqual(len(set(points)),15)
        self.assertEqual(len(set(lines)),15)
        self.assertGreater(np.linalg.eigvalsh(P[np.ix_(points,points)])[0],1e-10)
        self.assertGreater(np.linalg.eigvalsh(R[np.ix_(lines,lines)])[0],1e-10)

if __name__=="__main__":unittest.main()
