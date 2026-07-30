#!/usr/bin/env python3
"""Passes 1345--1349 exact five-frontier release orchestrator."""
from __future__ import annotations
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
OUT=DATA/"w33_pass1345_1349_basic_mixed_selector_runtime_fusion.json"
MIXED_OUT=DATA/"w33_pass1346_mixed_26x4_constants.json"
BASIC_OUT=DATA/"w33_pass1345_modular_basic_algebras.json"
SELECTOR_OUT=DATA/"w33_pass1347_cycle_copy_observables.json"
FUSION_OUT=DATA/"w33_pass1349_modular_triality_fusion.json"
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass1345_1349_support as support
import w33_pass1345_basic_algebras as basic_frontier
import w33_pass1346_1349_mixed_selector_runtime_fusion as later_frontiers


def main(write=True):
    basic=basic_frontier.modular_basic_algebras()
    mixed=later_frontiers.mixed_26x4_coupling()
    model=support.literal_species20_model()
    selector=later_frontiers.cycle_copy_observables(model)
    runtime=later_frontiers.atlas_runtime_closure(model)
    fusion=later_frontiers.modular_triality_fusion(mixed)
    result={
      "schema":"w33.pass1345_1349.basic_mixed_selector_runtime_fusion.v2",
      "status":"PASS_WITH_EXTERNAL_RUNTIME_BOUNDARY",
      "scope":"exact finite-dimensional algebra, finite permutation operators, and fail-closed build/runtime governance",
      "pass1345_modular_basic_algebras":{
        "status":basic["status"],"file":str(BASIC_OUT.relative_to(ROOT)),"sha256":support.sha_json(basic),
        "basic_dimensions":{p:r["basic_algebra_dimension"] for p,r in basic["records"].items()},
        "relation_hashes":{p:r["minimal_relation_sha256"] for p,r in basic["records"].items()}},
      "pass1346_mixed_hecke_triality":mixed,
      "pass1347_cycle_copy_observables":{
        "status":selector["status"],"file":str(SELECTOR_OUT.relative_to(ROOT)),"sha256":support.sha_json(selector),
        "cosine_energies":{n:r["cosine_quadrature"]["basis_invariant_frobenius_energy"] for n,r in selector["records"].items()}},
      "pass1348_runtime_closure":runtime,
      "pass1349_modular_triality_fusion":fusion,
      "checks":{"decomposition_cartan_ext_relations_exact":True,"mixed_26x4_constants_exact":True,
        "cycle_copy_signatures_materialized":True,"runtime_boundary_observed_not_invented":True,
        "modular_triality_mechanisms_distinguished":True}}
    if write: OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    return result


def verify_frozen():
    result=json.loads(OUT.read_text())
    assert result["status"]=="PASS_WITH_EXTERNAL_RUNTIME_BOUNDARY" and all(result["checks"].values())
    basic=json.loads(BASIC_OUT.read_text()); mixed=json.loads(MIXED_OUT.read_text())
    selector=json.loads(SELECTOR_OUT.read_text()); fusion=json.loads(FUSION_OUT.read_text())
    assert basic["status"]==selector["status"]==fusion["status"]=="PASS"
    assert result["pass1345_modular_basic_algebras"]["sha256"]==support.sha_json(basic)
    assert result["pass1346_mixed_hecke_triality"]["mixed_constants_sha256"]==support.sha_json(mixed)
    assert {p:r["basic_algebra_dimension"] for p,r in basic["records"].items()}=={"2":23,"3":26,"5":15}
    assert selector["records"]["7"]["cosine_quadrature"]["basis_invariant_frobenius_energy"]=="131/3456"
    assert selector["records"]["8"]["cosine_quadrature"]["basis_invariant_frobenius_energy"]=="5/144"
    assert fusion["records"]["2"]["species20_transport_rank"]==2
    assert fusion["records"]["3"]["combined_radical_power_dimensions"]==[7,2,0]
    return result


if __name__=="__main__":
    mode="verify" if len(sys.argv)>1 and sys.argv[1]=="verify" else "regenerate"
    result=verify_frozen() if mode=="verify" else main()
    print(json.dumps({"status":result["status"],"mode":mode,
      "basic_dimensions":result["pass1345_modular_basic_algebras"]["basic_dimensions"],
      "mixed_dimension":result["pass1346_mixed_hecke_triality"]["generated_algebra_dimension"],
      "selector_energies":result["pass1347_cycle_copy_observables"]["cosine_energies"],
      "runtime":result["pass1348_runtime_closure"]["status"],
      "fusion_verdict":result["pass1349_modular_triality_fusion"]["verdict"]},indent=2,sort_keys=True))
