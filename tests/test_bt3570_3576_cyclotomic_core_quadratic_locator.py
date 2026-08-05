import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis import bt3570_3576_cyclotomic_core_quadratic_locator as packet

def test_exact_certificate_matches_frozen():
    generated=packet.certificate()
    frozen=json.loads((ROOT/'data/PART_BT3570_BT3576_CYCLOTOMIC_CORE_QUADRATIC_LOCATOR_results.json').read_text())
    assert generated==frozen
    assert generated['semantic_sha256']=='38ea92c1767dda0b786232710f37ead7ec35628511c36dfb7b3d2c79f35a9ad0'

def test_maximal_cyclic_and_stable_extension_ladder():
    r=packet.certificate()['representation']
    assert r['rank_ladder']==[20,18,14]
    assert r['hom_ladder']==[80,40,10]
    assert r['D10']['cyclotomic_core_dimension']==16
    assert r['D10']['stable_dimension']==22
    assert r['A5']['stable_dimension']==26
    assert not r['borel']['contains_order_five']

def test_quadratic_locator_is_exact_and_gate_minimal():
    loc=packet.certificate()['locator']
    assert [packet.locator(x) for x in range(16)]==packet.LABELS
    assert loc['quadratic_span_rank']==5
    assert loc['and_lower_bound']==loc['and_construction']==5
    assert loc['xor_construction']==8
    assert loc['compound_patterns']==137
    assert loc['compound_minimum_distance']==3
