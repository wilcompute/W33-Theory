import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def test_exact_semantic_certificate():
 module=load(ROOT/'analysis'/'w33_pass3837_3854_ovoid_wedderburn_code_leech_triality.py','pass3837')
 observed=module.build();frozen=json.loads((ROOT/'data'/'PART_3837_3854_OVOID_WEDDERBURN_CODE_LEECH_TRIALITY_results.json').read_text())
 assert observed==frozen
 assert observed['semantic_sha256']=='ede91cc799f9093209c589fb0b73c88fca4159bedcc8e1e7cd6680c5f0c778fd'
 assert all(observed['checks'].values())

def test_independent_graph_certificate():
 module=load(ROOT/'analysis'/'w33_pass3837_3854_graph_aut_certificate.py','pass3837graph')
 observed=module.build();frozen=json.loads((ROOT/'data'/'PART_3837_3854_GRAPH_AUT_CERTIFICATE.json').read_text())
 assert observed==frozen
 assert observed['gq45_full_automorphism_order']==observed['row40_full_automorphism_order']==51840
 assert observed['row_column_isomorphic'] is False

def test_claim_boundaries_and_pending_monster_slot():
 frozen=json.loads((ROOT/'data'/'PART_3837_3854_OVOID_WEDDERBURN_CODE_LEECH_TRIALITY_results.json').read_text())
 candidate=json.loads((ROOT/'data'/'PART_3837_3854_MONSTER_DESCENT_candidate.json').read_text())
 assert candidate['status']=='PENDING' and not candidate['mmgroup_strings']
 assert 'serialized Monster/mmgroup words or Monster class fusion' in frozen['evidence_boundary']['not_proved_here']
 assert frozen['universal_axial_presentation']['boundary'].startswith('The full unmarked')
