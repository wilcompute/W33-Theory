from pathlib import Path
import importlib.util
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def test_complete_hull_replay():
    import w33_affine_holonomy_hull as m
    out=m.main(False)
    assert out==json.loads(m.OUT.read_text())
    assert sum(out['hull']['weight_enumerator'].values())==3**9
    assert out['hull']['parameters']=='[45,9,12]_3'
    assert out['CSS']['parameters']=='[[45,27,2]]_3'
    assert out['punctured_dual']['parameters']=='[21,9,5]_3'
