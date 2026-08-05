import json
from pathlib import Path
from analysis.bt3649_3662_seven_front_closure import build_certificate


def test_seven_front_certificate_matches_frozen():
    generated=build_certificate()
    frozen=json.loads(Path('data/PART_BT3649_BT3662_SEVEN_FRONT_CLOSURE_results.json').read_text())
    assert generated==frozen
    assert generated['semantic_sha256']=='067047bbf3fe04301fcb26bf484a3d151bf6db4ab762fa6bf31f527889d09a89'
    assert generated['fronts']['degree_three_covering']['integral_transversal_lower_bound']==81
    assert generated['fronts']['modular_E81']['simple_projective_conclusion'] is True
    assert generated['fronts']['tomotope_cocycle_correction']['simple_double_cover_count']==3
    assert generated['fronts']['objectwise_gewirtz_bridge']['constant_row_sum']==560
