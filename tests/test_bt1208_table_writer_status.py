from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1208_writer_exists():
    path = ROOT / 'analysis' / 'bt1208_raw_z2_s3_contingency_table_writer.py'
    text = path.read_text(encoding='utf-8')
    assert 'raw_vs_s3_sign' in text
    assert 'canonical_vs_s3_sign' in text
    assert 'PART_BT1208_RAW_Z2_S3_CONTINGENCY_TABLE_results.json' in text
