import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_pass5098_5101_certificate():
    d=json.loads((ROOT/'data'/'PART_W33_PASS5098_5101_ROOT_COSET_SUPPLEMENT.json').read_text())
    assert d['5098']['q2']=={'points':16,'charts':32,'chart_size':2,'hypergraph_isomorphic':True}
    assert d['5098']['q3']=={'points':81,'charts':108,'chart_size':3,'hypergraph_isomorphic':True}
    assert d['5099']['derivative_graph_automorphism_order']==324
    assert d['5099']['structure']=='U_81 semidirect V4'
    assert d['5099']['identity_stabilizer_element_orders']=={'1':1,'2':3}
    assert d['5100']['C2']=={'N':4,'count':'4q^3'}
    assert d['5101']['commutators']['[X0,X1]']=='X2'
    assert d['5101']['commutators']['[X0,X2]']=='2 X3'
