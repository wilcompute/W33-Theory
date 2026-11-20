"""Focused exact regressions for five-track TOE continuation (Nov 20, 2026)."""
import math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from toe_20261120_repetition_dial_codes import build,run as code_run
from toe_20261120_four_physics_controls import (
    matter,causal,holonomy,memory,run as physics_run
)

class CSSRepetitionDialTests(unittest.TestCase):
    def test_invalid_lengths(self):
        with self.assertRaises(AssertionError):build(1)
        with self.assertRaises(AssertionError):build(0)
    def test_exact_dial(self):
        d=code_run(write=False)
        self.assertEqual(len(d["samples"]),6)
        self.assertEqual([e["physical_qutrits"] for e in d["samples"]],
                         [399,638,877,1116,1833,2550])
        self.assertEqual([e["distance"] for e in d["samples"]],[2,3,4,5,8,8])
        self.assertTrue(all(e["logical_qutrits"]==81 for e in d["samples"]))
        self.assertTrue(all(e["HX_HZT_zero_mod3"] for e in d["samples"]))
    def test_L8_balanced(self):
        c=build(8)
        self.assertEqual((c["physical_qutrits"],c["logical_qutrits"],c["distance"]),(1833,81,8))
        self.assertEqual((c["rank_HX_by_full_row_rank"],c["rank_HZ_by_full_row_rank"]),(632,1120))
        self.assertEqual((c["maximum_X_check_weight"],c["maximum_Z_check_weight"]),(6,4))
        self.assertEqual((c["maximum_X_qudit_check_degree"],c["maximum_Z_qudit_check_degree"]),(2,4))

class PhysicsControlsTests(unittest.TestCase):
    def test_spin10_27_anomalies(self):
        r=matter()
        self.assertEqual((r["gravity_U1psi_anomaly"],r["U1psi_cubic_anomaly"],r["Spin10_squared_U1psi_anomaly_index_normalization"]),(0,0,0))
        self.assertEqual(r["triple_charge_sums"]["16_16_10"],0)
        self.assertEqual(r["triple_charge_sums"]["10_10_1"],0)
        self.assertNotEqual(r["triple_charge_sums"]["16_16_1"],0)
    def test_family_count_anomaly_no_go(self):
        self.assertEqual(matter()["family_multiplicity_not_fixed_by_anomalies"],[1,2,3,4,5,6])
    def test_order_and_volume_decouple(self):
        c=causal()
        vols=[r["coordinate_rectangle_volume"] for r in c["metrics"]]
        self.assertAlmostEqual(vols[0],4.)
        self.assertLess(vols[0],vols[1])
        self.assertLess(vols[1],vols[2])
        self.assertEqual([r["R_scalar_at_origin"] for r in c["metrics"]],[0.,-.6,-1.])
        self.assertEqual(len(set(r["same_Hasse_links"] for r in c["metrics"])),1)
    def test_su3_center_only_reference_sees_holonomy(self):
        h=holonomy()
        self.assertEqual(h["adjoint_tr_center"],8.)
        self.assertAlmostEqual(h["interferometric_controlled_center_p_plus"],.25)
        self.assertEqual(h["interferometric_identity_p_plus"],1.)
        self.assertEqual(h["ideal_bernoulli_Hoeffding_shots_99pct"],19)
    def test_memory_postselection_guard(self):
        m=memory()
        self.assertAlmostEqual(m["minimum_eta_for_negative_worst_case_upper"],.9897351649185687,places=11)
        self.assertLess(m["eta_0_995_worst_case_Wupper"],0)
        self.assertLess(m["eta_0_99_worst_case_Wupper"],0)
        self.assertGreater(m["eta_0_985_worst_case_Wupper"],0)
        self.assertEqual(m["accepted_samples_per_setting_99pct"],155975)
        self.assertEqual(m["seven_setting_accepted_total_99pct"],1091825)
    def test_full_reproducibility(self):
        r=physics_run(write=False)
        self.assertEqual(len(r["tracks"]),4)
        self.assertEqual(r["tracks"]["E6_matter_selection"],matter())

if __name__=="__main__":unittest.main()
