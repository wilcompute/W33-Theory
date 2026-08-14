import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]

def test_pass5074_5081_packet():
    J=json.loads((R/'data/PART_W33_PASS5074_5081_RESULTS.json').read_text())
    assert J['status']=='EXECUTED_WITH_OPEN_ALL_Q_DISTANCE_AND_Q4_FULL_SHELL'
    assert J['5074']['chamber_star']['active_charts']=='4q^3'
    assert J['5076']['two_generator_min']==J['5076']['three_generator_min']==384
    assert J['5077']['exact_two_star_minimum']==1000 and J['5077']['best_nonzero_weight_found']==625
    assert J['5078']['q3']['syndrome_bits']==3 and J['5078']['q3']['rom_entries']==8
    assert J['5079']['anchors']=={'q2':0,'q3':4320,'q4':108800,'q5':1170000}
    assert J['5080']['q2']['minimum_words']==J['5080']['q2']['chamber_stars']==45
    assert J['5081']['dual_minimum_distance']==3 and J['5081']['q2_dual_coefficients']['A3']==120
