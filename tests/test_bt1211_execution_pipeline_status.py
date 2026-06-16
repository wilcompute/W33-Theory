from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1211_execution_runner_exists():
    text = (ROOT / 'tools' / 'execute_bt1208_bt1210_artifacts.py').read_text(encoding='utf-8')
    assert 'bt1208_raw_z2_s3_contingency_table_writer.py' in text
    assert 'bt1209_isomorphism_dependence_sampler.py' in text
    assert 'bt1210_bt748_half_fiber_table_generator.py' in text
    assert 'PART_BT1211_EXECUTION_SUMMARY.json' in text
