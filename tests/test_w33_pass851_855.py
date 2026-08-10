from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
 p=json.loads((ROOT/'data'/name).read_text(encoding="utf-8"));assert p['status']=='PASS';assert all(p['checks'].values());return p

def test_pass682_correction():
 p=load('w33_pass682_flatblock_h1_branch_separation.json');c=p['flatblock_specialization']['pass808_saturated_cyclotomic_correction'];assert c['two_branch_gluing_invariant_factors']==[2,2];assert c['3_primary_rank']==0

def test_pass851_atlas_factor_compatibility():
 p=load('w33_pass851_atlas_factor_compatibility.json');assert p['source_module']['composition_factors_bottom_to_top']==[14,6,40,6]

def test_pass852_heisenberg_coalescence_separation():
 p=load('w33_pass852_heisenberg_coalescence_separation.json');assert p['Heisenberg_restriction']['Loewy_layers']==[1,2,4,2,1]

def test_pass853_bockstein_scalar_isolation():
 p=load('w33_pass853_bockstein_scalar_isolation.json');assert p['cohomology']['Bockstein_rank']==0

def test_pass854_cost_aware_adaptive_audit():
 p=load('w33_pass854_cost_aware_adaptive_audit.json');assert p['replay']['fractional_worst_cost_improvement']>.20

def test_pass855_generic_cell_optimal_decision_trees():
 p=load('w33_pass855_generic_cell_optimal_decision_trees.json');assert p['arrangement']['feasible_full_dimensional_cells']==19;assert p['optimal_phase_trees']['worst_optimal_depth']==4;assert len(p['wall_only_phases'])==6
