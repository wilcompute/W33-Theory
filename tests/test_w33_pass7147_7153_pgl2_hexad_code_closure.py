import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data'/'PART_W33_PASS7147_7153_PGL2_HEXAD_CODE_CLOSURE.json'

def test_exact_closure_replay():
    subprocess.run([sys.executable,str(ROOT/'analysis'/'w33_pass7147_7153_pgl2_hexad_code_closure.py')],check=True,cwd=ROOT)
    d=json.loads(CERT.read_text())
    assert d['status']=='PASS'
    assert d['pass_7147_pgl2_involution_schreier']['full_quotient_spectrum_status'].startswith('THEOREM')
    assert d['pass_7148_m2_relative_compatibility']['pair_pairs_checked']==64620
    h=d['pass_7149_d12_hexad_classification']
    assert h['ambient_stabilizer_order']==12 and h['abstract_membership_pattern_aut_order']==72
    assert h['unique_hexad_per_witness_in_orbit'] is True
    c=d['pass_7150_code_anatomy']
    assert c['dual_minimum_distance']==2 and c['dual_weight2_words']==3048
    assert c['outer_order']==72
    assert d['pass_7152_bonkers_symmetry_gap']['index']==6
    assert d['pass_7153_bonkers_puncture_symmetry_restoration']['puncture_point_50']['outer_order']==36
    assert d['pass_7153_bonkers_puncture_symmetry_restoration']['puncture_both_50_80']['outer_order']==72
