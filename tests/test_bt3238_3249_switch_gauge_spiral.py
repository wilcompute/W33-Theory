from __future__ import annotations
import importlib.util
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("bt",ROOT/"analysis/bt3238_3249_switch_gauge_spiral.py")
BT=importlib.util.module_from_spec(SPEC); assert SPEC.loader; SPEC.loader.exec_module(BT)

@lru_cache(maxsize=1)
def data():
    return BT.certificate()

def test_cover_family_psp_classification():
    d=data()["pass3238_3239_PSp_switch_family"]
    assert d["group_order"]==25920
    assert d["setwise_stabilizer_structure"]=="C4"
    assert d["fixed_covers"]==27 and d["paired_covers"]==216
    assert d["internal_PSp_orbit_classes"]==135
    assert d["cover_stabilizer_order_histogram"]=={"2":216,"4":27}
    assert d["fixed27_affine_code"]["Schlaefli_SRG_27_10_1_5_relation_unions"]==0

def test_nonabelian_port_gauge_and_css_shadow():
    d=data()["pass3240_3241_nonabelian_port_gauge"]
    assert d["cell_counts"]=={"V":45,"E":720,"F":240}
    assert d["fundamental_group"]=="free group F_436"
    assert d["free_nonabelian_generators"]==436
    assert d["sign_abelianization"].startswith("S3 -> C2")
    assert d["fixed_length_information_bits"]==1128

def test_real_spiral_and_fail_closed_sat_boundary():
    d=data()
    s=d["pass3242_3243_real_spiral_and_S3_shadow"]
    assert s["characteristic_polynomial"]=="t^4+3t^2+1"
    assert s["split_metric_signature"]==[2,2]
    assert s["mod2_dihedral_group_order"]==12
    assert s["mod2_even_rotation_reflection_group_order"]==6
    assert len(s["six_matching_compiler_table"])==6
    q=d["pass3244_sat_shards"]
    assert q["shards_executed"]==100
    assert q["SAT_models"]==q["UNSAT_proofs"]==0
    assert d["live_chromatic_boundary"]=="10 <= chi(H) <= 11"
