from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1209_sampler_exists():
    text = (ROOT / 'analysis' / 'bt1209_isomorphism_dependence_sampler.py').read_text(encoding='utf-8')
    assert '--max-isomorphisms' in text
    assert 'sample_invariant' in text
    assert 'distinct_table_signatures' in text
