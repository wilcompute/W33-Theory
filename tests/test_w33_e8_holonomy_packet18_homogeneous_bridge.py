import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run():
    subprocess.run([sys.executable,str(ROOT/'analysis/w33_e8_holonomy_packet18_homogeneous_bridge.py')],cwd=ROOT,check=True)
    return json.loads((ROOT/'data/w33_e8_holonomy_packet18_homogeneous_bridge.json').read_text())

def test_packet18_is_homogeneous_space_not_group():
    d=run()
    assert d['status']=='PASS_TORSOR_BRIDGE__GROUP_IDENTIFICATION_KILLED'
    n=d['negative_result']
    assert n['abelian_order18_subgroup_exists'] is False
    assert n['centralizer_of_T_order']==9
    p=d['positive_bridge']
    assert p['coset_count']==18
    assert p['coset_size']==4
    assert p['C4_normal'] is False
    assert p['translation_orbits']==[9,9]

def test_e8_18_sector_fingerprint():
    d=run()
    m=d['E8_joint_sector_dimensions']
    assert len(m)==18
    assert sum(m.values())==248
    assert sorted(set(d['E8_holonomy_trace_fingerprint'].values()))==[-8,-4,-2,1,4,5,14,248]
