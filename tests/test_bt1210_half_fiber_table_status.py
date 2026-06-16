from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1210_half_fiber_generator_schema():
    text = (ROOT / 'analysis' / 'bt1210_bt748_half_fiber_table_generator.py').read_text(encoding='utf-8')
    assert 'root_triple_id' in text
    assert 'chirality' in text
    assert 'half_fiber_index' in text
    assert 'presentation_pair_key' in text
    assert '51840' in text
