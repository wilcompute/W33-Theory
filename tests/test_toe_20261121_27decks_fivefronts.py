"""Offline mathematical/ideal-quantum regression for the seven-front continuation.

No web fetches in tests. The static site-map link ledger is verified against
the frozen fetched certificate. Regenerate the latter with the producer.
"""
import itertools, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_hermitian45_pauli_sic_bridge as old
import toe_20261121_27decks_fivefronts as f

class TestWitting27Decks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rays,cls.wf4=old.witting_rays()
        cls.iso=sorted({old.norm4(v) for v in itertools.product(range(4),repeat=4)
                 if any(v) and old.herm4(v,v)==0})
        cls.supports=[frozenset(i for i,x in enumerate(cls.wf4)
                      if old.herm4(z,x)==0) for z in cls.iso]
        cls.mapping={int(k):int(v) for k,v in old.analyze()[
              "ray_index_to_F3_projective_point_index"].items()}
        ids={z:i for i,z in enumerate(cls.iso)}
        cls.lines=sorted({tuple(sorted({ids[old.norm4(f.plus4(u,v,a,b))]
                     for a,b in itertools.product(range(4),repeat=2) if a or b}))
                     for u,v in itertools.combinations(cls.iso,2)
                     if old.herm4(u,v)==0})
        cls.geometry,cls.graph,cls.schedules=f.first_front(
            cls.rays,cls.wf4,cls.iso,cls.lines,cls.supports)
        cls.group=f.group_front(cls.wf4,cls.iso,cls.supports,cls.graph,
                         cls.schedules,cls.mapping)
        cls.optics=f.optical_front(cls.rays,cls.wf4,cls.iso,
                                  cls.supports,cls.schedules)
        cls.channel=f.channel_front(cls.rays,cls.mapping)
        cls.selector=f.selector_front(cls.rays,cls.supports,cls.iso,cls.graph)
        cls.memory=f.memory_front()

    def test_27_five_chart_partitions(self):
        d=self.geometry
        self.assertEqual(d["H34_lines"],27)
        self.assertEqual(len(d["unique_27_five_chart_schedules"]),27)
        self.assertTrue(d["all_27_five_chart_schedules_partition_40_Witting_rays"])
        self.assertEqual(d["Schlaefli_skew_lines_SRG"],[27,16,10,8])

    def test_full_25920_equivariance(self):
        d=self.group
        self.assertEqual(d["projective_GF4_Hermitian_group_order"],25920)
        self.assertEqual(d["PSp4_F3_full_group_order"],25920)
        self.assertTrue(d["entire_25920_element_40point_actions_identical"])
        self.assertEqual(d["entire_45chart_group_order"],25920)
        self.assertEqual(d["entire_27deck_group_order"],25920)

    def test_45_explicit_naimark_unitaries_and_27_POVMs(self):
        d=self.optics
        self.assertEqual(d["genuine_Naimark_8x8_extensions"],45)
        self.assertLess(d["max_nai_unity_error"],1e-11)
        self.assertTrue(d["all_27_schedules_equal_the_Witting_40outcome_POVM"])
        self.assertLess(d["max_27_schedule_matched_operator_residual"],1e-11)
        self.assertEqual(d["entanglement_separable_threshold_trusted"],0.2)

    def test_genuine_CPTP_but_EB_bridge(self):
        d=self.channel
        self.assertTrue(d["physical_entanglement_breaking_CPTP_bridge_built"])
        self.assertLess(d["Choi_positive_semidefinite_error"],1e-12)
        self.assertLess(d["Choi_trace_preserving_error"],1e-12)
        self.assertTrue(d["injective_on_full_15dim_traceless_ququart_sector"])
        self.assertLess(d["max_15dim_HS_isotropy_Gram_error"],1e-11)

    def test_irreducible_weyl_leakage_no_go(self):
        d=self.channel
        self.assertAlmostEqual(d["rank_four_nonidentity_average_leakage"],9/16)
        self.assertAlmostEqual(d["rank_four_all_81_average_leakage"],5/9)
        self.assertEqual(len(d["independent_numeric_certificates"]),3)

    def test_chart_source_selector(self):
        d=self.selector
        self.assertEqual(d["single_Witting_source_compatible_charts"],9)
        self.assertEqual(d["orthogonal_source_pairs_3common_charts"],240)
        self.assertEqual(d["nonorthogonal_source_pairs_1common_chart"],540)
        self.assertLess(d["max_chart_entropy_residual"],1e-11)

    def test_causal_break_multitime_memory(self):
        d=self.memory
        self.assertEqual(d["qutrit_projective_2design_probe_states"],12)
        self.assertAlmostEqual(d["ideal_quantum_memory_average_fidelity"],1)
        self.assertAlmostEqual(d["classical_Zdephased_memory_average_fidelity"],0.5)
        self.assertAlmostEqual(d["reset_no_memory_average_fidelity"],1/3)

    def test_lorentzian_positive_Laplacian_boundary(self):
        self.assertEqual(self.geometry["chart_laplacian_spectrum"],{0:1,9:20,15:24})

    def test_frozen_mirror_source_ledger(self):
        payload=json.loads((ROOT/"data/toe_20261121_fivefront_27decks.json").read_text())
        d=payload["f7_restored_finitegeometry_site_index"]
        self.assertEqual(d["status"],"PASS")
        self.assertEqual(d["working_mirror"],"https://m759.github.io/map.html")
        self.assertGreaterEqual(d["total_distinct_link_targets"],150)
        self.assertTrue(any("m759.github.io" in u for u in d["internal_links"]))

if __name__=="__main__":
    unittest.main()
