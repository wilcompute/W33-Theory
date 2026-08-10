import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pass595_johnson_triangle_curvature():
    payload = json.loads((ROOT / 'data' / 'w33_pass595_johnson_triangle_curvature.json').read_text(encoding="utf-8"))
    assert payload['status'] == 'PASS'
    assert payload['base']['triangles'] == 840
    assert payload['base']['triangle_types'] == {'top': 560, 'tetrahedral': 280}
    counts = {row['holonomy_label']: row['count'] for row in payload['holonomy_census']}
    assert counts == {
        'flat_identity': 112,
        'top_double_transposition': 112,
        'top_order_three': 336,
        'tetrahedral_fixed_point_free_involution': 280,
    }
    assert payload['wilson_curvature']['global_augmentation_wilson_sum'] == 56
    assert payload['wilson_curvature']['permutation_character_sum'] == 896
    assert all(payload['checks'].values())
