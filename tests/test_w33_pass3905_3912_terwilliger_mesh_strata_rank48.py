from __future__ import annotations
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'analysis/w33_pass3905_3912_terwilliger_mesh_strata_rank48.py'
FROZEN=ROOT/'data/PART_3905_3912_TERWILLIGER_MESH_STRATA_RANK48_results.json'
def load():
 spec=importlib.util.spec_from_file_location('p3905',SOURCE);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def test_frozen_certificate():
 mod=load();actual=json.loads(json.dumps(mod.build_certificate(ROOT),sort_keys=True));expected=json.loads(FROZEN.read_text());assert actual==expected
def test_frontier_values():
 c=json.loads(FROZEN.read_text());assert c['symmetry_adapted_mesh']['nontrivial_adjacent_rotations']==398;assert c['terwilliger_wedderburn_arithmetic_sieve']['candidate_count']==14;assert c['maximal_code_strata']['enumerator_types_observed']==[0,1,2,3,4,5];assert c['rank48_character_overlap']['cross_hom_dimension']==7;assert c['monster_gate']['status']=='PENDING'
