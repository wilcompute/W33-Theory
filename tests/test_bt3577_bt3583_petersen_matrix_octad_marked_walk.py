from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'analysis/bt3577_3583_petersen_matrix_octad_marked_walk.py'
CANARY=ROOT/'analysis/bt3580_star_proof_canary.py'
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);assert spec.loader;spec.loader.exec_module(mod);return mod

def test_borel_petersen_spine_duality():
 m=load(SRC,'p3583a');x=m.borel_petersen_spine();assert x['P19']['residual_variables']==30870;assert x['P57']['residual_variables']==30870;assert x['fixed_graph'].startswith('Petersen')

def test_constructive_perkel_matrix_model():
 m=load(SRC,'p3583b');x=m.perkel_matrix_model();assert x['matrix_model_digest']=='366405ad8400779a79eb6b92437b6d354ad3019eb16e9b5a81b99c5adc77eb33';assert x['minimal_right_ideal_Q_dimension']==6;assert x['nonzero_matrix_entries']==171

def test_octad_phase_separation_and_moore_shell():
 m=load(SRC,'p3583c');x=m.octad_phases();s=x['sunflower_phase'];q=x['mixed_phase'];assert s['S8_stabilizer']==1 and q['S8_stabilizer']==4;assert s['common_core_size']==1 and q['common_core_size']==0;assert s['compiled_graph']['triangles']==0;assert s['compiled_graph']['four_cycles']==3024;assert s['compiled_graph']['diameter']==3;assert q['compiled_graph']['triangles']==76 and q['compiled_graph']['four_cycles']==375

def test_marked_resolvent_discriminator():
 m=load(SRC,'p3583d');x=m.marked_resolvent_discriminator();assert x['W33_line']['induced_edges']==6;assert 'at most four' in x['Gewirtz_boundary'];assert x['shared_restricted_resolvent']['b']=='1/((z - 2)*(z + 4))'

def test_real_proof_canary():
 m=load(CANARY,'p3580');x=m.run();assert x['compatibility_vertices']==52;assert x['maximum_clique']==11;assert x['proof_sha256']=='a07611183bd01fad1b60134aebba7dc3a8ec0ce7bc29fd7c46ea8c4146010b50';assert x['record_sha256']=='2a984b9a2f51646691657a8dfe5d01b9e33496f75500ba9b79abdd5a68385390'

def test_frozen_semantic_result():
 m=load(SRC,'p3583e');got=json.loads(json.dumps(m.build_result()));frozen=json.loads((ROOT/'data/PART_BT3577_BT3583_PETERSEN_MATRIX_OCTAD_MARKED_WALK_results.json').read_text());assert got==frozen;assert got['semantic_sha256']=='2a4a06836164c6eb92d971aa18ecd1369990c7bf501ae1aaf342e7b5e5bc23a4'
