import json
from pathlib import Path

bundle = Path(__file__).resolve().parents[1] / 'bundles' / 'v23_toe_finish' / 'v23'

def test_lemma1_exists_and_ok():
    p = bundle / 'lemma1_check.json'
    assert p.exists(), 'lemma1_check.json missing'
    j = json.load(open(p))
    assert j.get('tri_ok') == True


def test_lemma2_order():
    p = bundle / 'lemma2_check.json'
    assert p.exists(), 'lemma2_check.json missing'
    j = json.load(open(p))
    assert j.get('parsed', {}).get('order_matches_51840') is True
