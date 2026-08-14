import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_pass5074_5081_certificate():
    x=json.loads((R/'data/PART_W33_PASS5074_5081_RESULTS.json').read_text())
    assert x['status']=='PASS_WITH_OPEN_ALL_Q_DISTANCE_AND_Q4_HEAVY_CHART_SHELL'
    assert x['5074']['chamber_equality']['active_charts']=='4q^3'
    assert x['5075']['satisfiable_seeds']==x['5075']['unsatisfiable_seeds']==8
    assert x['5076']['q3_order_index_conductor']==4
    assert x['5077']['one_swap_floor_bases']==8
    assert x['5078']['tanner_six_cycles']=='T(q)(q-2)'
    assert sum(x['5079']['q4_role_counts'])==256
    assert x['5080']['q3_pair_generated_subgroup_orders'][-1]==81
    assert x['5081']['q4']['vertices']==256
