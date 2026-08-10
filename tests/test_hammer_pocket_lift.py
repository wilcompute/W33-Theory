import json
from pathlib import Path

def test_hammer_pocket_lift_results():
    repo = Path(__file__).resolve().parents[1]
    bundle = repo / 'TOE_hammer_pocket_lift_g2_v01_20260227_bundle' / 'TOE_hammer_pocket_lift_g2_v01_20260227'
    results_file = bundle / 'RESULTS.json'
    assert results_file.exists(), "Hammer results missing"
    res = json.loads(results_file.read_text(encoding="utf-8"))
    # basic counts
    assert res['g2_derivations_basis_14']
    assert len(res['g2_derivations_basis_14']) == 14
    assert len(res['g2_sl3_axis_fix_basis_8']) == 8
    assert len(res['g2_axis_movers_basis_6']) == 6
    # axis images should be 6 vectors with single nonzero entry
    imgs = res.get('axis_images') or res.get('axis_movers_images_of_axis_column')
    assert imgs is not None
    assert len(imgs) == 6
    for v in imgs:
        assert sum(1 for x in v if x != 0) == 1
    # orbit stats
    orb = res['completion_orbit_under_PSp43_on_36']
    assert orb['group_order'] == 25920
    assert orb['orbit_size'] == 4320
    assert orb['stabilizer_size'] == 6
    assert orb['completions_per_pocket'] == 8
