import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def cert(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
def test_pass4552_4559_frontier_invariants():
    c=cert('PART_W33_PASS4552_QMINUS5_RANK_THIRD_ANCHOR.json')
    assert [(x['q'],x['rank_N'],x['rank_NtN']) for x in c['three_exact_anchors']]==[(3,91,70),(5,651,546),(7,2451,2150)]
    assert c['candidate_all_odd_q']['status'].startswith('OPEN')
    c=cert('PART_W33_PASS4553_CANONICAL_H10_WEIGHT_QUADRATIC.json')
    assert c['dimensions']==[0,1,9,10] and c['middle_quotient']['type']=='O+(8,2)'
    assert (c['middle_quotient']['singular_including_zero'],c['middle_quotient']['anisotropic'])==(136,120)
    c=cert('PART_W33_PASS4554_LOCAL_BASIS_EXCHANGE_ENSEMBLE.json')
    assert c['bases']==108 and c['Borel_action']['orbit_sizes']==[81,27]
    assert c['basis_exchange_graph']['distance_distribution']==[1,15,48,44]
    c=cert('PART_W33_PASS4555_C8_SELECTOR_BOOTSTRAP.json')
    assert c['selector_size']==1620 and c['reconstructed_ranks']=={'dim_V9':9,'rank_Astar':10,'rank_H':39}
    c=cert('PART_W33_PASS4556_H10_O6MINUS_NO_LINEAR_TRANSPORT.json')
    assert set(c['hom_spaces'].values())=={0}
    c=cert('PART_W33_PASS4557_SHELL_CROSS_INCIDENCE.json')
    assert c['per_edge_cross_distance_profile']=={'12':2,'20':36,'28':2}
    c=cert('PART_W33_PASS4558_APARTMENT_SINGULAR_FIBERS.json')
    assert (c['apartments'],c['protected_images'],c['uniform_fiber_size'])==(1620,135,12)
    assert c['fiber_graph']['graph']=='K_{4,4,4}'
    c=cert('PART_W33_PASS4559_EDGE_ANISOTROPIC_DOUBLE_COVER.json')
    assert (c['edge_images'],c['quotient_classes'])==(240,120)
    assert c['anisotropic_polar_graph_srg']==[120,63,30,36]
