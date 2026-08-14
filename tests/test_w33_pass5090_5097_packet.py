import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_pass5090_5097_certificate():
    x=json.loads((R/'data/PART_W33_PASS5090_5097_RESULTS.json').read_text())
    assert x['status']=='PASS_WITH_OPEN_ALL_Q_DISTANCE_AND_Q4_HEAVY_SHELL'
    assert (x['5090']['sat'],x['5090']['unsat'])==(8,8)
    assert x['5091']['q3_conductor_index']==4
    assert x['5092']['one_swap_den780']==8
    assert sum(x['5093']['anchors']['q4'])==256
    assert x['5094']['q3_pair_generated_orders'][-1]==81
    assert 'x^2-2' in x['5095']['q2']['charpoly']
    assert x['5096']['exotic_requirement']=='t>=1'
    assert x['5097']['chamber_extremal'].startswith('muhat_edge=')
