import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_pass5066_5073_certificate():
    x=json.loads((ROOT/'data/PART_W33_PASS5066_5073_RESULTS.json').read_text())
    assert x['5066']['W3q']['theta_generates_full_dual']
    assert x['5067']['status']=='UNKNOWN'
    assert x['5068']['subdivision_2_height_dimensions']==[81,29,29,23,1,1,0]
    assert x['5069']['outer_split']==[2,3]
    assert x['5070']['smith_floor_raw_basis']['inverse_denominator']==780
    assert x['5072']['orders']['N_PGSp_H']==64
    assert x['5073']['tanner_6_cycles']==1170000

def test_pass5071_exact_matrix_bridge():
    from sympy import Matrix,Rational
    A=Matrix([[1,4],[1,0]]);B=Matrix([[4,2],[2,5]])
    S=Matrix([[1,Rational(1,2)],[0,Rational(1,2)]])
    assert A*S==S*(B-4*Matrix.eye(2))
