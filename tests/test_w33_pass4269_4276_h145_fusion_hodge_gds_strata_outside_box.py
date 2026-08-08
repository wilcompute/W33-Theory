import json, subprocess, sys
from pathlib import Path

def test_pass4269_4276_quick():
    root=Path(__file__).resolve().parents[1]
    p=subprocess.run([sys.executable,str(root/'analysis/w33_pass4269_4276_h145_fusion_hodge_gds_strata_outside_box.py')],cwd=root,text=True,capture_output=True,check=True)
    out=json.loads(p.stdout)
    assert out['H_order']==72
    assert out['GHZ_CNOTs']==33
    assert out['signed16_rows']==2
    assert out['GDS_bbox_mm']==[11.04,14.85]
    assert out['three_subset_orbits']==5
    assert out['four_subset_orbits']==16
    assert out['graphstate_uniformity']==5
