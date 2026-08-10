import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1212_materialized_tables():
    t1208 = json.loads((ROOT / 'data' / 'PART_BT1208_RAW_Z2_S3_CONTINGENCY_TABLE_results.json').read_text(encoding="utf-8"))
    assert t1208['raw_vs_s3_sign'] == {'0,0': 211, '0,1': 203, '1,0': 155, '1,1': 151}
    assert t1208['canonical_vs_s3_sign'] == {'0,0': 220, '0,1': 194, '1,0': 146, '1,1': 160}
    t1209 = json.loads((ROOT / 'data' / 'PART_BT1209_ISOMORPHISM_DEPENDENCE_SAMPLE_results.json').read_text(encoding="utf-8"))
    assert t1209['samples_collected'] == 16
    assert t1209['distinct_table_signatures'] == 4
    assert t1209['sample_invariant'] is False


def test_bt1212_schema_materialized():
    schema = json.loads((ROOT / 'data' / 'PART_BT1210_BT748_HALF_FIBER_TABLE_SCHEMA.json').read_text(encoding="utf-8"))
    assert schema['expected_rows'] == 51840
    assert schema['row_schema'] == ['root_triple_id', 'chirality', 'half_fiber_index', 'presentation_pair_key']
