import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_release_lock():
 p=load('w33_pass563_567_triality_quadratic_order_walsh_bayesian_release.json');assert p['status']=='PASS';assert p['owner_check_total']==53;assert all(p['release_checks'].values())
def test_triality_normalizer():
 p=load('w33_pass563_triality_a8_witting_normalizer.json');assert p['gl42_a8']['normalizer_order']==60;assert p['gl42_a8']['conjugacy_class_size']==336;assert p['witting_alignment']['intersection_order']==4
def test_quadratic_irreducible():
 p=load('w33_pass564_z9_full_quadratic_irreducibles.json');assert p['module']['augmentation_irreducible'];assert p['layers'][-1]['sections']==6561;assert p['layers'][-1]['distinct_charpolys']==2605
def test_native_order_scaffold():
 p=load('w33_pass565_cyclotomic_order_formal.json');assert p['checks']['native_adjoinroot_construction'];assert p['algebraic_order']['discriminant']==125
def test_twisted_walsh():
 p=load('w33_pass566_q5_twisted_walsh_krawtchouk.json');assert p['catalog_custody']['records']==98;assert p['group']['dual_frequency_orbits']==292;assert p['catalog_custody']['radial_exact_count']==0
def test_joint_decoder():
 p=load('w33_pass567_joint_bayesian_decoder.json');assert all(x['mean_shot_reduction']>0 for x in p['results'].values());assert all(x['joint_errors']<=20 for x in p['results'].values())
