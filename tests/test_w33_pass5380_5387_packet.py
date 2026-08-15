import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class Pass5380_5387Packet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((ROOT/'data/PART_W33_PASS5380_5387_RESULTS.json').read_text())

    def test_q5_filtered_code_tower(self):
        self.assertEqual(self.r['5380']['codes'],['C_A=[73125,625,625]_2','K0=[73125,560,1000]_2','C_F=[325,65,25]_2'])
        self.assertEqual(self.r['5380']['minimum_shells'],{'C_A':936,'K0':2340,'C_F':156})

    def test_radius9_boundary(self):
        self.assertEqual(self.r['5381']['eventual_radius'],9)
        self.assertEqual(self.r['5381']['monotone_true_only_radius'],7)

    def test_connectedL_projectors(self):
        self.assertEqual(self.r['5382']['minimal_polynomial'],'x^3(x+1)^4')
        self.assertEqual(self.r['5382']['projectors'],['P1=A_L^4','P0=I+A_L^4'])
        self.assertEqual(self.r['5382']['ranks'],[6034,3716])

    def test_hoffman_stays_fail_closed(self):
        self.assertEqual(self.r['5383']['status'],'EXACT_HOFFMAN_XORSAT_REPLAY_COMMITTED_SOLVER_PENDING')
        self.assertEqual(self.r['5383']['known_distance_set'],[28,32,36,40])

    def test_allodd_sequence(self):
        self.assertEqual(self.r['5384']['exact_sequence'],'0 -> D_q=K0 -> C_A -> C_F -> 0')

    def test_three_bonkers(self):
        self.assertEqual(self.r['5385']['reconstructed_graph'],'SRG(156,30,4,6)=W(3,5)')
        self.assertEqual(self.r['5386']['tower'],['q^4','q^3','q^2','q','1'])
        self.assertEqual(self.r['5387']['difference_set'],'(16,6,2)')

    def test_manifest_and_public_page(self):
        m=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text()
        self.assertIn('PASS5380_5387_distance_radius9_projector_gallery_insert',m)
        self.assertTrue((ROOT/'docs/pass5380-5387-distance-radius9-projectors.html').exists())

if __name__=='__main__':unittest.main()
