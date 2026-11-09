"""Five W33 extensions: exact PPT blind spot, SDP, optical routing, gauge and DES gate."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_q8_five_extensions as m

class TestFiveExtensions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=m.main()

    def test_pyramids_orthogonal_ppt_witness(self):
        x=self.d["PPT_benchmarks"]
        self.assertLess(x["pyramid_UPB_orthogonality_error"],1e-12)
        a=x["two_UPB_benchmarks"]
        self.assertGreater(a["Pyramids"]["correlation_trace_norm"],a["Tiles"]["correlation_trace_norm"])
        self.assertGreater(a["Pyramids"]["witness_excess"],.044)
        self.assertLess(abs(a["Pyramids"]["PPT_min_eigenvalue"]),1e-12)

    def test_horodecki_exact_blind_spot(self):
        x=self.d["PPT_benchmarks"]
        self.assertTrue(x["Horodecki_all_a_exact_proof"]["trace_norm_witness_blind_spot"])
        for row in x["Horodecki_PPT_family_scan"]:
            self.assertAlmostEqual(row["trace_norm"],2/3,places=12)

    def test_sdp_improves_lp_conservatively(self):
        a=self.d["robust_SDP"]
        for name in ("Tiles","Pyramids"):
            self.assertEqual(a[name]["solver_status"],"optimal")
            self.assertGreater(a[name]["gain_over_fixed_dual"],0)
            self.assertGreater(a[name]["solver_approx_full_min_nuclear_norm"],2/3+1e-3)
            self.assertLess(a[name]["solver_approx_full_min_nuclear_norm"],a[name]["true_trace_norm"])
        self.assertGreater(a["Tiles"]["gain_over_fixed_dual"],.005)

    def test_all_clifford_cosets_cannot_see_local_purity(self):
        x=self.d["information_kernel"]
        self.assertTrue(x["all_24_Choi_MUB_bases_unable_to_distinguish_these_two_states"])
        self.assertLess(x["max_outcome_probability_difference"],1e-12)
        self.assertAlmostEqual(x["global_purities"][0],1/9)
        self.assertAlmostEqual(x["global_purities"][1],1/3)

    def test_optical_routing_geometry(self):
        x=self.d["optical_routing"]
        self.assertEqual(x["minimal_adjacent_swaps_in_one_linear_rail_order"],13)
        self.assertEqual(x["parallel_layer_depth"],6)
        self.assertEqual(sum(map(len,x["constructed_parallel_layers"])),13)
        self.assertEqual(max(x["per_logical_mode_swap_exposures"]),6)
        self.assertEqual(x["if_all_13_SWAPS_require_2mode_components_total_upper_budget"],31)

    def test_finite_gauge_no_spacetime(self):
        x=self.d["gauge_continuum"]
        self.assertEqual(x["native_gauge"]["free_U1_cycle_fluxes"],81)
        self.assertLess(x["native_gauge"]["relative_gauge_action_error"],1e-11)
        self.assertAlmostEqual(x["continuum"]["3"]["64"],3.0059057194,places=6)
        self.assertAlmostEqual(x["continuum"]["4"]["64"],4.0078742926,places=6)

    def test_des_data_acquisition_failure_not_a_fake_fit(self):
        x=self.d["DES_Y6_gate"]
        self.assertEqual(x["unblinded_candidate_direct_HTTP_2026_11_09"],404)
        self.assertFalse(x["S9_scored"])
        self.assertIn("FAILED_404",x["direct_download_status"])
        self.assertEqual(len(x["required_named_inputs"]),7)

    def test_frozen_result(self):
        p=ROOT/"data/w33_20261109_q8_five_extensions.json"
        if p.exists():
            saved=json.loads(p.read_text(encoding="utf8"))
            self.assertEqual(saved["status"],self.d["status"])
            self.assertEqual(saved["PPT_benchmarks"]["Horodecki_all_a_exact_proof"]["exact_nuclear_norm"],"2/3 for every 0<a<1")

if __name__=="__main__":
    unittest.main()
