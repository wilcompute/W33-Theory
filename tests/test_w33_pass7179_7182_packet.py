import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRODUCERS=[
    'analysis/w33_pass7179_d4_scheme_krein.py',
    'analysis/w33_pass7180_q9_local_edit_radius.py',
    'analysis/w33_pass7181_e6_minuscule_fiber_voltage.py',
    'analysis/w33_pass7182_d4_glue_spread_code.py',
]

def test_pass7179_7182_exact_packet():
    for p in PRODUCERS:
        subprocess.run([sys.executable,str(ROOT/p)],check=True,cwd=ROOT)
    d=json.loads((ROOT/'data/PART_W33_PASS7179_D4_SCHEME_KREIN.json').read_text())
    assert d['status']=='PASS' and d['full_scheme_automorphism_order']==103680 and d['q_polynomial_orderings']==[]
    assert d['share_relation_maximal_9_cliques']==80
    q=json.loads((ROOT/'data/PART_W33_PASS7180_Q9_LOCAL_EDIT_RADIUS.json').read_text())
    assert q['status']=='PASS'
    assert q['exact_maximum_total_after_exact_core_deletions_0_to_5']=={'0':47,'1':46,'2':47,'3':46,'4':46,'5':46}
    assert q['target48_excluded_for_all_core_deletion_radii_0_through_8'] is True
    e=json.loads((ROOT/'data/PART_W33_PASS7181_E6_MINUSCULE_FIBER_VOLTAGE.json').read_text())
    assert e['status']=='PASS' and e['Schlaefli']['v']==27 and e['Schlaefli']['k']==16
    assert e['K9_triangle_voltage_holonomy']=={'0':12,'1':36,'2':36}
    g=json.loads((ROOT/'data/PART_W33_PASS7182_D4_GLUE_SPREAD_CODE.json').read_text())
    assert g['status']=='PASS' and g['all_E8_D4']['D4_subsystems']==3150
    assert g['spread_incidence_code']=='[45,21,5]_2' and g['spread_code_dual']=='[45,24,6]_2'
