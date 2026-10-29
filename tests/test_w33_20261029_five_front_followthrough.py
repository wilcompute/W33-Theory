"""Independent 2026-10-29 continuation regressions, excluding timed q7 SAT."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))

class TestOptimizedCSS(unittest.TestCase):
 def test_optimal_132_and_max_four(self):
  from w33_20261029_minimum_132_check_basis import verify
  r=verify()
  self.assertEqual(r['status'],'PASS')
  self.assertEqual(r['minimum_total_check_weight'],132)
  self.assertEqual(r['max_incidence'],4)
  self.assertEqual(r['weight8_span_rank'],15)
  self.assertEqual(r['uncorrectable_hook_examples'],16)

class TestH27ContinuumAndChirality(unittest.TestCase):
 def test_growth_and_conjugate_sectors(self):
  from w33_20261029_heisenberg_intrinsic_growth_chirality import verify
  r=verify()
  self.assertEqual(r['status'],'PASS')
  self.assertEqual(r['H27_diameter'],4)
  self.assertEqual(r['established_homogeneous_growth_dimension'],4)
  self.assertEqual(r['infinite_integer_Heisenberg_ball_volumes_r0_to15'][-1],21569)
  self.assertLess(r['central_H27']['conjugate_sector_eigenvalue_max_gap'],1.e-12)

class TestUnknownPhotonOverlap(unittest.TestCase):
 def test_minimax_threshold(self):
  from w33_20261029_optical_overlap_agnostic_minimax import verify
  r=verify()
  self.assertEqual(r['status'],'PASS')
  self.assertEqual((r['unknown_overlap_minimax_optimum']['N'],
                    r['unknown_overlap_minimax_optimum']['threshold']),(20333,16))
  self.assertEqual((r['known_s0_optimum']['N'],
                    r['known_s0_optimum']['threshold']),(19427,15))
  self.assertEqual(r['unknown_overlap_and_unknown_eta_in_085_to1_beta0']['N'],54144)
  self.assertTrue(r['unknown_overlap_minimax_optimum']['globally_minimal_among_scanned_N'])

class TestQ7RankOnly(unittest.TestCase):
 def test_rank176_and_pair_orbits(self):
  from w33_20261029_q7_rank176_xor_sat import geometry, independent_rows
  A=geometry();B=independent_rows(A)
  self.assertEqual(len(B),176)
  self.assertEqual(len(A),400)
  self.assertEqual(A[0].bit_count(),56)
  self.assertTrue(any(A[0]>>i&1 for i in range(1,400)))
  self.assertTrue(any(not (A[0]>>i&1) for i in range(1,400)))
if __name__=='__main__':unittest.main()
