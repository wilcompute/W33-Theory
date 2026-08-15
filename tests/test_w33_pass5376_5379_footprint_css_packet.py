from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def load(name:str):
    return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

class FootprintCssPacket(unittest.TestCase):
    def test_pass5376_allodd_rank_kernel(self):
        x=load('PART_W33_PASS5376_ALLODD_FOOTPRINT_RANK_MODULE_CLOSURE.json')
        self.assertEqual(x['status'],'THEOREM_ALLODD_BINARY_FOOTPRINT_RANK_CLOSED')
        for qs,r in x['sample_dimensions'].items():
            q=int(qs)
            self.assertEqual(r['binary_footprint_rank'],q*(q*q+1)//2)
            self.assertEqual(r['binary_kernel_dimension'],1+q*(q+1)**2//2)
            self.assertEqual(r['components_through_point']%2,1)
        self.assertIn('q=11 dual weight-20',x['boundary'])

    def test_pass5377_rank_complement_and_generation(self):
        x=load('PART_W33_PASS5377_ALLODD_RANK_COMPLEMENT_GENERATION_CLOSURE.json')
        self.assertEqual(x['status'],'THEOREM_ALLODD_RANK_COMPLEMENT_KERNEL_AND_K0_GENERATION_CLOSED')
        for qs,r in x['sample_rows'].items():
            q=int(qs)
            self.assertEqual(r['rank_Q'],r['null_F2'])
            self.assertEqual(r['null_Q'],r['rank_F2'])
            self.assertEqual(r['D_q_dimension'],r['K0_dimension'])
            self.assertEqual(r['rank_F2'],q*(q*q+1)//2)

    def test_pass5378_complete_minimum_shell(self):
        x=load('PART_W33_PASS5378_FOOTPRINT_CODE_MINIMUM_ORBIT.json')
        self.assertEqual(x['status'],'THEOREM_ALLODD_COMPLETE_MINIMUM_SHELL_SPANS_FOOTPRINT_CODE')
        for qs,r in x['sample_parameters'].items():
            q=int(qs)
            self.assertEqual(r['minimum_distance'],2*(q+1))
            self.assertEqual(r['complete_minimum_shell_size'],q*q*(q*q+1)//2)
            self.assertTrue(r['minimum_shell_spans_code'])

    def test_pass5379_css_formula(self):
        x=load('PART_W33_PASS5379_ALLODD_BINARY_CSS_POINT_CODE.json')
        self.assertEqual(x['status'],'THEOREM_ALLODD_BINARY_CSS_POINT_CODE_FAMILY')
        for qs,r in x['samples'].items():
            q=int(qs)
            self.assertEqual(r['n'],(q+1)*(q*q+1))
            self.assertEqual(r['k'],q*q+1)
            self.assertEqual(r['d'],q+1)
            self.assertEqual(r['n']-2*r['stabilizer_rank_each'],r['k'])
        self.assertIn('distinct from',x['separation'])

    def test_pass5406_logical_weil_clock(self):
        x=load('PART_W33_PASS5406_CSS_LOGICAL_WEIL_CLOCK.json')
        self.assertEqual(x['status'],'THEOREM_ALLODD_CSS_LOGICAL_WEIL_QMOD8_CLOCK')
        for qs,r in x['samples'].items():
            q=int(qs);w=(q*q-1)//2
            self.assertEqual(r['logical_dimension'],q*q+1)
            self.assertEqual(r['algebraic_closure_composition_dimensions'],[1,1,w,w])
            self.assertEqual(r['Weil_field_of_definition'],'F2' if q%8 in (1,7) else 'F4')
        self.assertIn('No direct-sum splitting',x['boundary'])

    def test_manifest_and_wrappers(self):
        manifest=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text(encoding='utf-8')
        needle='\\input{analysis/PASS5376_5379_allodd_footprint_rank_css_insert}'
        self.assertEqual(manifest.count(needle),1)
        for wrapper in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
            text=(ROOT/wrapper).read_text(encoding='utf-8')
            self.assertIn('W33_CURRENT_FRONTIER_MANIFEST',text)

    def test_old_open_boundary_is_superseded_not_erased(self):
        old=(ROOT/'analysis/PASS5332_5338_k0_wedderburn_characteristic_insert.tex').read_text(encoding='utf-8')
        new=(ROOT/'analysis/PASS5376_5379_allodd_footprint_rank_css_insert.tex').read_text(encoding='utf-8')
        self.assertIn('remains open',old)
        self.assertIn('formerly open all-odd footprint-rank theorem',new)
        self.assertIn('q=11',new)
        self.assertIn('Hoffman',new)
        self.assertIn('logical-channel decomposition',new)

    def test_site_materializer_contract(self):
        src=(ROOT/'analysis/PASS5376_5379_allodd_footprint_rank_css_index_insert.html').read_text(encoding='utf-8')
        tool=(ROOT/'tools/materialize_pass5376_5379_footprint_css.py').read_text(encoding='utf-8')
        token='id="pass-5376-5379-allodd-footprint-css"'
        self.assertEqual(src.count(token),1)
        self.assertIn('root and docs index mirrors diverged',tool)
        self.assertIn("TARGETS=(ROOT/'docs/index.html',ROOT/'index.html')",tool)

if __name__=='__main__':
    unittest.main()
