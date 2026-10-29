"""Regression: frozen Spence catalog counts and explicit integral E8 cover."""
from pathlib import Path
import json
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
class SpectralTwinTest(unittest.TestCase):
    def test_frozen_catalog(self):
        o=json.loads((ROOT/'data/w33_20261029_srg28_css_population.json').read_text())
        self.assertEqual(len(o['records']),28)
        self.assertEqual(o['source_sha256'],'b899979459e6304bfff848d112d0ac8d738c837e5e21dc6e9d310a386aee8be6')
        self.assertEqual(sum(x['rank2']==16 for x in o['records']),17)
        self.assertEqual(sum(x['css_distance_exact']==6 for x in o['records']),17)
        self.assertEqual([x['index'] for x in o['records'] if x['number_K4']==40],[26,27])
        for a in o['records']:
            self.assertEqual(a['logical_qubits'],40-2*a['rank2'])
            self.assertEqual(a['css_distance_exact'],6 if a['rank2']==16 else 4)
    def test_integral_cover_and_reference_interference(self):
        from w33_20261029_e8_cover_photonic_sign import main
        main()
        o=json.loads((ROOT/'data/w33_20261029_e8_cover_photonic_sign.json').read_text())
        self.assertEqual(o['finite_order'],25920)
        self.assertEqual(o['integral_cover_order'],51840)
        self.assertEqual(o['rank4_involutions_order4_lifts'],270)
        self.assertEqual(o['rank2_involutions_order2_lifts'],45)
        self.assertEqual(o['unitary_mesh_gates'],28)
        self.assertLess(o['ideal_plus_port_probability'],1e-20)
        self.assertAlmostEqual(o['ideal_minus_port_probability'],1,places=11)
if __name__=='__main__':unittest.main()
