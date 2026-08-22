import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

LIGHT=[
 'w33_pass7425_global_leaf_incidence_design.py',
 'w33_pass7426_d4_a2_rook_latin.py',
 'w33_pass7427_d4_pair_64_leaf_grid.py',
 'w33_pass7428_d4_latin_hoffman_composed_bridge.py',
 'w33_pass7429_global_double_six_leaf_orbit.py',
 'w33_pass7430_steiner24_d4_root_refutation.py',
 'w33_pass7432_leaf_spherical_300_design.py',
]

def test_pass7425_7432_light_replay():
    for name in LIGHT:
        subprocess.run([sys.executable,str(ROOT/'analysis'/name)],check=True,cwd=ROOT)
    agg=json.loads((ROOT/'data'/'PART_W33_PASS7425_7432_GLOBAL_LEAF_D4_GRID.json').read_text())
    assert agg['status']=='PASS_WITH_Q9_GLOBAL_TARGET48_OPEN'
    p25=json.loads((ROOT/'data'/'PART_W33_PASS7425_GLOBAL_LEAF_INCIDENCE_DESIGN.json').read_text())
    assert p25['real_rank_B']==301
    assert p25['pair_replication_by_relation']==[80,8,0,8,0]
    p26=json.loads((ROOT/'data'/'PART_W33_PASS7426_D4_A2_ROOK_LATIN.json').read_text())
    assert p26['A2_subsystems_in_D4']==16 and p26['labelled_order4_Latin_squares']==576
    p27=json.loads((ROOT/'data'/'PART_W33_PASS7427_D4_PAIR_64_LEAF_GRID.json').read_text())
    assert p27['same_partition_graph']=='L_2(8) = SRG(64,14,6,2)'
    p28=json.loads((ROOT/'data'/'PART_W33_PASS7428_D4_LATIN_HOFFMAN_COMPOSED_BRIDGE.json').read_text())
    assert [p28['V4_even_parastrophe_order'],p28['V4_autoparatopy_order'],p28['full_D4_A2_graph_aut_order']]==[288,576,1152]
    p29=json.loads((ROOT/'data'/'PART_W33_PASS7429_GLOBAL_DOUBLE_SIX_LEAF_ORBIT.json').read_text())
    assert p29['global_leaf_spread_charts']==80640 and p29['charts_per_A2_4_line']==72
    p30=json.loads((ROOT/'data'/'PART_W33_PASS7430_STEINER24_D4_ROOT_REFUTATION.json').read_text())
    assert p30['normal_2^3_orbits_on_slots']==[8,8,8]
    assert p30['normal_2^3_orbits_on_D4_roots']==[4,4,4,4,4,4]
    p32=json.loads((ROOT/'data'/'PART_W33_PASS7432_LEAF_SPHERICAL_300_DESIGN.json').read_text())
    assert p32['irreducible_dimension']==300 and p32['integral_norm_squared']==30240

def test_pass7431_q9_radius9_replay():
    subprocess.run([sys.executable,str(ROOT/'analysis'/'w33_pass7431_q9_radius9.py')],check=True,cwd=ROOT)
    d=json.loads((ROOT/'data'/'PART_W33_PASS7431_Q9_RADIUS9.json').read_text())
    assert d['exists'] is False
    assert d['exact_core_deletions']==9
    assert d['branch_nodes']==2535139
