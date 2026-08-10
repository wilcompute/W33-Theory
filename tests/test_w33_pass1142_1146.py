from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"w33_pass1142_1146_exact_release.json"

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))

def test_hecke_wedderburn_certificate():
    d=load(); h=d["hecke"]
    assert d["status"]=="PASS"
    assert h["rank"]==26
    assert sum(h["subdegrees"])==432
    assert h["commutative"] is False
    assert sum(x["degree"]*x["multiplicity"] for x in h["decomposition"])==432
    assert sum(x["multiplicity"]**2 for x in h["decomposition"])==26
    assert h["inter_orbit_hom_rank_matrix"]==[[26,26,26],[26,26,26],[26,26,26]]
    assert h["full_three_copy_commutant_dimension"]==234

def test_first_steinberg_bridge():
    d=load(); b=d["explicit_bridge"]
    assert d["bridge_search"]["first_viable"]==[325,"Lambda2_26",1]
    assert b["class_size"]==36
    assert b["scaled_projector_rank"]==81
    assert b["scaled_projector_identity"]=="Q^2=11200 Q"
    assert b["intertwiner_shape"]==[325,432]
    assert b["intertwiner_rank_mod_1000003"]==81
    assert all(b["generator_equivariance"])
    assert b["hom_81_to_Lambda2Aug26_dimension"]==1
    assert b["hom_kernel_3x81_to_Lambda2Aug26_dimension"]==3

def test_a2_color_torsor():
    d=load(); t=d["a2_color_torsor"]
    assert t["order"]==3
    assert t["commutes_with_WE6"]
    assert sorted(t["orbit432_cycle"])==[11,12,13]
    assert set(t["color_cycle"])=={"0","1","2"}
    assert sorted(t["color_cycle"].values())==[0,1,2]

def test_parallel_claim_boundary():
    d=load(); audit=d["parallel_audit"]
    assert "imported" in audit["pr162"].lower()
    assert "rejected" in audit["pr160"].lower()
    assert "9 rays" in audit["pr160"]
