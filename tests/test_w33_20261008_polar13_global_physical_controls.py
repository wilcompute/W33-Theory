"""2026-10-08 rigorous integration: W33 polar13, cycle centers, physical controls."""
from __future__ import annotations
import itertools,json,math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_polar13_symplectic_module as polar
import w33_20261008_global_cycle_center_census as center
import w33_20261008_physical_five_controls as physics

def test_full_point_stabilizer_216_projective_polar_representation():
 r=polar.analyze()
 assert r["plane_points"]==13 and r["projective_stabilizer_image_order"]==216
 assert r["H27_plane_orbit_sizes"]==[1,3,3,3,3]
 assert r["tested_symplectic_stabilizer_generators"]==5
 assert r["augmentation_rank"]==12

def test_polar13_augmentation_has_no_invariant_symplectic_structure():
 r=json.loads((ROOT/"data/w33_20261008_polar13_symplectic_module.json").read_text())
 assert r["invariant_alternating_form_dimension"]==1
 assert r["max_attained_rank"]==0
 assert r["nondegenerate_witness_coefficients"] is None
 assert r["alternating_rank_histogram"]=={"0":3}

def test_exhaustive_1620_cycle_pair_census_and_symmetry_counts():
 x=json.loads((ROOT/"data/w33_20261008_global_cycle_center_census.json").read_text())
 assert x["induced_C8_total"]==1620
 assert len(center.cycles())==1620
 assert x["all_distinct_cycle_pairs"]==1620*1619//2==1311390
 assert x["commuting_local_center_pairs"]==1048950
 assert x["noncommuting_local_center_pairs"]==262440
 assert sum(x["intersection_signature_census"].values())==1311390

def test_every_overlap_class_has_matrix_identity_and_binary_rank():
 r=json.loads((ROOT/"data/w33_20261008_global_cycle_center_census.json").read_text())
 for k,v in r["representative_witnesses"].items():
  A,B=[set(p) for p in v["cycles"]]
  pu=np.zeros(80,dtype=int);qu=np.zeros(80,dtype=int)
  ps=np.zeros(80,dtype=int);qs=np.zeros(80,dtype=int)
  for x in A:pu[x]=1;ps[x]=1 if x<40 else -1
  for x in B:qu[x]=1;qs[x]=1 if x<40 else -1
  X=np.outer(pu,ps);Y=np.outer(qu,qs)
  m=len([q for q in A&B if q<40])-len([q for q in A&B if q>=40])
  comm=X@Y-Y@X
  assert np.array_equal(comm,m*(np.outer(pu,qs)-np.outer(qu,ps)))
  assert np.linalg.matrix_rank(comm)==v["commutator_rank"]
  assert v["commutator_rank"]==(0 if m==0 else 2)

def test_finite_field_tetraquadric_singular_rational_points():
 r=physics.tetraquadric_affine_sieve()
 assert r["smoothness_proved"] is False
 assert {p:v["singular_Fp_points"] for p,v in r["sieve"].items()}=={"3":8,"5":12,"7":2}
 assert {p:v["all_projective_ambient_Fp_points"] for p,v in r["sieve"].items()}=={"3":256,"5":1296,"7":4096}
 assert all(v["hypersurface_Fp_points"]>v["singular_Fp_points"] for v in r["sieve"].values())

def test_groebner_pilot_reports_negative_correctly():
 r=json.loads((ROOT/"data/w33_20261008_tetraquadric_modular_smoothness.json").read_text())
 assert r["prime"]==5
 assert len(r["charts_checked"])==1
 assert r["charts_checked"][0]["smooth_geometric_mod_p"] is False
 assert r["globally_smooth_mod5_certificate"] is False

def test_photonic_loss_break_even_and_depth_phase_diagram():
 r=physics.optical_crossover()
 assert math.isclose(r["36_vs_72_stage_survival_threshold_eta"],.9901977594782718,rel_tol=1e-12)
 assert r["loss_per_stage_phase_diagram"]["0.99"]["optimal_tested_stages"]==36
 assert r["loss_per_stage_phase_diagram"]["0.9902"]["optimal_tested_stages"]==72
 assert r["loss_per_stage_phase_diagram"]["0.999"]["optimal_tested_stages"]==144
 assert r["loss_per_stage_phase_diagram"]["0.98"]["optimal_tested_stages"]==36

def test_proton_hexality_supplied_charge_filter_distinguishes_Z3():
 r=physics.proton_selection()["operator_charges"]
 for op in ("up_Yukawa","down_Yukawa","charged_lepton_Yukawa","neutrino_Yukawa","mu_term"):
  assert r[op]["P6"]==0
 for op in ("QLDc","UcDcDc","LLEc","QQQL","UcUcDcEc"):
  assert r[op]["P6"]!=0
 assert r["QLDc"]["X3"]==0
 assert r["LLEc"]["X3"]==0
 # Extra Z3 alone fails to veto two operators; the full P6 needs Z2.
 assert r["QLDc"]["P6"]!=0 and r["LLEc"]["P6"]!=0

def test_all_five_control_certificate_keys_and_scope():
 a=json.loads((ROOT/"data/w33_20261008_physical_five_controls.json").read_text())
 assert set(a)=={"tetraquadric","photonic","proton"}
 assert a["tetraquadric"]["smoothness_proved"] is False
 assert "not chip-calibrated" in a["photonic"]["note"]
