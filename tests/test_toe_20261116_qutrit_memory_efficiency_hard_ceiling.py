"""Trusted event-ready qutrit witness necessary conditions under memory loss."""
import math,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261116_qutrit_memory_loss_hard_ceiling as m
from toe_20261116_qutrit_eventready_timetag_sequential import plan
class MemoryHardCeilings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=m.verify()
    def test_one_memory_no_router_threshold(self):
        z=m.case(.8,1,path=1,f=.95)
        self.assertGreater(z["required_equal_router_efficiency"],.97)
        self.assertLess(z["required_equal_router_efficiency"],.98)
    def test_good_99pct_router(self):
        self.assertTrue(m.case(.8,1,path=1,f=.99)["asymptotically_violates_with_chosen_routers"])
    def test_one_memory_pathloss_impossible(self):
        self.assertFalse(m.case(.8,1,path=.95,f=1)["physically_possible_below_or_equal_100_percent_routers"])
    def test_two_memories_impossible(self):
        self.assertFalse(m.case(.8,2,path=1,f=1)["physically_possible_below_or_equal_100_percent_routers"])
    def test_95pct_reference(self):
        z=m.case(.95,1,path=.95,f=.95)
        self.assertAlmostEqual(z["required_equal_router_efficiency"],.919590802,places=5)
    def test_better_mem_improves(self):
        self.assertLess(m.case(.99,1,path=1)["required_equal_router_efficiency"],
                        m.case(.8,1,path=1)["required_equal_router_efficiency"])
    def test_two_mems_harder(self):
        self.assertGreater(m.case(.8,2,path=1)["required_equal_router_efficiency"],
                           m.case(.8,1,path=1)["required_equal_router_efficiency"])
    def test_no_mem_better(self):
        self.assertLess(m.case(.8,0,path=1)["required_equal_router_efficiency"],
                        m.case(.8,1,path=1)["required_equal_router_efficiency"])
    def test_efficiency_not_fidelity(self):
        self.assertIn("NOT",self.z["fidelity_vs_efficiency"])
    def test_detector_product_formula(self):
        z=m.case(1,0,path=1,f=1)
        self.assertAlmostEqual(z["maximum_gross_match_with_perfect_routers"],
                         .81*z["mean_ideal_match_conditioned_two_click"])
    def test_source_model_crosscheck(self):
        self.assertAlmostEqual(m.case(.95,1,.95,.95)["mean_ideal_match_conditioned_two_click"],
                               plan(fR=1,fS=1,etaMem=1,etaPath=1,dark=0)["ideal_matched_probability_given_pair"])
    def test_no_experimental_claim(self):
        self.assertTrue(self.z["not_observed_hardware"])
if __name__=="__main__":unittest.main()
