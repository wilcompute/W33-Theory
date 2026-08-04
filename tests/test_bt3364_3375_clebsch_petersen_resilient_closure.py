import importlib.util
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'analysis'/'bt3364_3375_clebsch_petersen_resilient_closure.py'
spec=importlib.util.spec_from_file_location('bt3364_3375',P)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def test_exact_packet():
    out=m.verify()
    assert out['checks']['passed']==out['checks']['total']
    assert out['clebsch']['srg']==[16,5,0,2]
    assert out['clebsch']['second_subconstituent']=='Petersen=KG(5,2)'
    assert out['systematic_code']['parity_bits']==7
    assert out['systematic_code']['distance']==5
    assert out['replication']['three_vertex_catastrophic']==480
