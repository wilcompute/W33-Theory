import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/"data/PART_BT3871_BT3886_EIGHT_FRONT_CLOSURE_results.json"
SEEDS=ROOT/"data/PART_BT3871_BT3886_TOP115_CYCLIC_SEEDS.json"
def load(): return json.loads(RESULT.read_text(encoding="utf-8"))
def test_status_boundaries():
 d=load(); assert d["status"]=="PASS_5_FRONTS_PLUS_3_BONKERS_WITH_TWO_CORRECTIONS"; assert d["semantic_sha256"]=="d1ac79b9df49e25d84c2e08f5c440ac9a0e5bd90b60e89deebe6699f309143b5"; assert d["live_boundaries"]=={"cap_maximum":[63,None],"chromatic_number":[10,11],"covering_radius":[389,435],"cubic_transversal":[106,177]}
def test_cap():
 d=load(); f=d["fronts"]["cubic_transversal_tightening"]; c=d["bonkers"]["free_cap_orbit_code"]; assert f["new_interval"]==[106,177]; assert f["radius_two_local_optimality"]["locally_optimal"]; assert f["transversal_hit_profile"]=={"1":876,"2":2217,"3":1947}; assert (c["length"],c["size"],c["constant_weight"],c["minimum_hamming_distance"])==(240,25920,63,62)
def test_tomotope():
 f=load()["fronts"]["tomotope_outer_extension_correction"]; assert f["corrected_exceptional_group"]=="2^4:D12"; assert f["exceptional_group_center_order"]==1; assert f["split"] and f["outer"]
def test_modular():
 f=load()["fronts"]["modular_top115_complete_descent"]; assert f["composition_multiset"]=={"1":3,"5":3,"10":3,"14":3,"25":1}; assert sum(f["successive_factor_dimensions"])==115; assert f["all_factors_absolutely_irreducible"]; s=json.loads(SEEDS.read_text(encoding="utf-8")); assert sorted(map(int,s))==f["composition_series_dimensions"][1:-1]; assert all(len(v)==115 for v in s.values())
def test_gewirtz_and_frame():
 d=load(); g=d["fronts"]["gewirtz_asymmetric_residual_scheme"]; b=d["bonkers"]["gewirtz_residual_Petersen_blowup"]; f=d["bonkers"]["cap_fibre_orbit_frame"]; assert g["W33_verdict"]=="not SRG(40,12,2,4)"; assert b["quotient_parameters"]==[10,3,0,1]; assert sum(f["count_vector"])==63; assert f["count_vector_orbit_size"]==25920
