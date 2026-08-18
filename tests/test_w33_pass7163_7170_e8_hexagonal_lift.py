import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data'/'PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json'


def test_pass7163_7170_exact_replay():
    subprocess.run([sys.executable,str(ROOT/'analysis'/'w33_pass7163_7170_e8_hexagonal_lift.py')],check=True,cwd=ROOT)
    d=json.loads(CERT.read_text())
    assert d['status']=='PASS'
    q=d['pass_7163_q9_rank_boundary']
    order=['(1, 1, 2)','(1, 1, 3)','(1, 1, 4)','(1, 1, 5)','(1, 2, 3)','(1, 2, 4)','(1, 3, 4)','(1, 3, 5)']
    assert [q['anchor_cases'][k]['rank1_independence_number_exact'] for k in order]==[21,25,22,25,23,24,21,26]
    assert q['known_47_residual_rank_split']=={'rank1':5,'rank2':42}
    e=d['pass_7164_e8_hexagonal_root_graph_lift']
    assert (e['roots'],e['fibers'],e['base_zero_edge_pairs'],e['base_nonadjacent_pairs'])==(240,40,240,540)
    assert e['cross_graph']=='C12 for all 540 pairs'
    c=d['pass_7165_e8_fiber_code_and_d4']
    assert c['e8_fiber_constant_code']=='[240,16,48]_2'
    assert (c['d4_halves'],c['orthogonal_d4_pairs'],c['gq42_partition_lines'])==(90,45,27)
    assert c['d4_equals_center_quads_objectwise'] is True
    assert d['pass_7168_z12_holonomy']['z12_holonomy_histogram']=={'1':1440,'3':180,'9':180,'11':1440}
