import json
from pathlib import Path


def test_identify_script_writes_summary(tmp_path):
    # Run the script and assert the extended summary exists and contains expected keys
    import runpy
    repo_root = Path.cwd()
    runpy.run_module('scripts.identify_45_12_3', run_name='__main__')
    out = Path('bundles/v23_toe_finish/v23/veld_summary_extended.json')
    assert out.exists(), 'Extended JSON was not written'
    data = json.loads(out.read_text(encoding='utf-8'))
    assert data['n_points'] == 45
    assert data['n_generators'] == 45
    assert 'automorphism' in data
    # the group we found earlier was size 103680; assert estimated size present
    assert data['automorphism'].get('estimated_group_size', 0) == 103680
    # basic linear algebra invariants
    assert data['gf2_rank_generators'] == 45
    assert data['gf2_rank_incidence'] == 44
    assert data['gf3_rank_incidence'] == 15
