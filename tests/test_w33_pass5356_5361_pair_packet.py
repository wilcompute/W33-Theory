from __future__ import annotations
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

def load(name:str):
    return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

class PairPacket(unittest.TestCase):
    def test_pass5356_sym2_dimensions_and_firewall(self):
        x=load('PART_W33_PASS5356_ALLODD_PSL2_PAIR_FIBER_STEINBERG.json')
        self.assertIn('CHARACTERISTIC_ZERO',x['status'])
        for q in (3,5,7,9,11,13,17,19,25):
            r=x['arithmetic_checks'][str(q)]
            self.assertEqual(r['pair_fiber_size'],q*(q+1)//2)
            self.assertEqual(r['Sym2_Steinberg_dimension'],q*(q+1)//2)
            self.assertEqual(r['PSL2_order']//r['pair_stabilizer_order'],r['pair_fiber_size'])
        self.assertIn('not an assertion',x['boundary'])

    def test_pass5357_rank_formula(self):
        x=load('PART_W33_PASS5357_ALLODD_PSL2_PAIR_ORBITAL_RANK.json')
        for qs,r in x['prime_anchor_orbit_checks'].items():
            q=int(qs); expected=(3*q+9)//4 if q%4==1 else (3*q+7)//4
            self.assertEqual(r['orbital_rank'],expected)
            self.assertEqual(sum(r['subdegrees']),r['fiber_size'])

    def test_pass5358_nonsplitting(self):
        x=load('PART_W33_PASS5358_CHAR2_PROJECTIVE_LINE_NONSPLITTING_FIREWALL.json')
        self.assertIn('DOES_NOT_SPLIT',x['status'])
        for r in x['checks'].values():
            self.assertEqual(r['augmentation_of_all_one_mod2'],0)
            self.assertFalse(r['trivial_projection_possible'])
        self.assertIn('not a proof or disproof',x['boundary'])

    def test_pass5359_matches_pass5360(self):
        finite=load('PART_W33_PASS5359_PRIME_PAIR_HECKE_WEDDERBURN_CENSUS.json')['anchors']
        allq=load('PART_W33_PASS5360_ALLODD_PAIR_HECKE_WEDDERBURN.json')
        for qs,r in finite.items():
            q=int(qs); d=(q+3)//8
            expected_rank=(3*q+9)//4 if q%4==1 else (3*q+7)//4
            self.assertEqual(r['orbital_rank'],expected_rank)
            self.assertEqual(r['M2_block_count'],d)
            self.assertEqual(r['center_dimension'],expected_rank-3*d)
            self.assertEqual(r['commutator_dimension'],3*d)
        self.assertIn('does not prove the all-odd footprint-rank',allq['boundary'])

    def test_pass5361_klein_clock(self):
        x=load('PART_W33_PASS5361_QMOD8_PAIR_WEIL_KLEIN_CLOCK.json')
        sig=set()
        for r in x['table'].values():
            self.assertEqual(r['chi_minus2']*r['chi_2'],r['chi_minus1'])
            sig.add((r['chi_minus2'],r['chi_2']))
        self.assertEqual(len(sig),4)
        self.assertIn('No isomorphism is claimed',x['boundary'])

    def test_shared_manifest_reaches_insert_once(self):
        text=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text(encoding='utf-8')
        needle='\\input{analysis/PASS5356_5361_psl2_pair_steinberg_qmod8_insert}'
        self.assertEqual(text.count(needle),1)
        for wrapper in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
            w=(ROOT/wrapper).read_text(encoding='utf-8')
            self.assertIn('W33_CURRENT_FRONTIER_MANIFEST',w)

    def test_index_materializer_contract(self):
        src=(ROOT/'analysis/PASS5356_5361_psl2_pair_steinberg_qmod8_index_insert.html').read_text(encoding='utf-8')
        tool=(ROOT/'tools/materialize_pass5356_5361_psl2_pair.py').read_text(encoding='utf-8')
        token='id="pass-5356-5361-psl2-pair-steinberg"'
        self.assertEqual(src.count(token),1)
        self.assertIn('root and docs index mirrors diverged',tool)
        self.assertIn("TARGETS=(ROOT/'docs/index.html',ROOT/'index.html')",tool)

if __name__=='__main__':
    unittest.main()
