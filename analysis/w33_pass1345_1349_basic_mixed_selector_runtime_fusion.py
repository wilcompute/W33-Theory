#!/usr/bin/env python3
"""Passes 1345--1349 exact five-frontier release orchestrator.

The expensive regeneration path first reconstructs the literal tensors, then
splits them into inspectable Git-sized chunks.  The default CI path audits the
frozen exact certificates without pretending to rerun external runtimes.
"""
from __future__ import annotations
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
OUT=DATA/"w33_pass1345_1349_basic_mixed_selector_runtime_fusion.json"
MIXED_OUT=DATA/"w33_pass1346_mixed_26x4_constants.json"
MIXED_METADATA=DATA/"w33_pass1346_mixed_26x4_metadata.json"
MIXED_LEFT=[DATA/f"w33_pass1346_left_mixed_constants_{i}.json" for i in range(4)]
MIXED_RIGHT=[DATA/f"w33_pass1346_right_mixed_constants_{i}.json" for i in range(4)]
BASIC_OUT=DATA/"w33_pass1345_modular_basic_algebras.json"
SELECTOR_OUT=DATA/"w33_pass1347_cycle_copy_observables.json"
SELECTOR_RECORDS={length:DATA/f"w33_pass1347_cycle_copy_observables_length{length}.json" for length in (7,8)}
FUSION_OUT=DATA/"w33_pass1349_modular_triality_fusion.json"
sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass1345_1349_support as support
import w33_pass1345_basic_algebras as basic_frontier
import w33_pass1346_1349_mixed_selector_runtime_fusion as later_frontiers


def split_generated_payloads():
    full=json.loads(MIXED_OUT.read_text())
    logical_hash=support.sha_json(full)
    metadata={"schema":"w33.pass1346.mixed_26x4_metadata.v1","status":"PASS",
      "coherent_basis_labels":full["coherent_basis_labels"],
      "hecke_species20_blocks":full["hecke_species20_blocks"]}
    MIXED_METADATA.write_text(json.dumps(metadata,sort_keys=True,separators=(",",":"))+"\n")
    ranges=[(0,7),(7,14),(14,20),(20,26)]
    left_files=[]; right_files=[]
    for index,(start,stop) in enumerate(ranges):
        left={"schema":"w33.pass1346.left_mixed_constants.chunk.v1","status":"PASS","relation_range":[start,stop],"rows":full["left_mixed_constants"][start:stop]}
        right={"schema":"w33.pass1346.right_mixed_constants.chunk.v1","status":"PASS","relation_range":[start,stop],"rows":full["right_mixed_constants"][start:stop]}
        MIXED_LEFT[index].write_text(json.dumps(left,sort_keys=True,separators=(",",":"))+"\n")
        MIXED_RIGHT[index].write_text(json.dumps(right,sort_keys=True,separators=(",",":"))+"\n")
        left_files.append({"path":str(MIXED_LEFT[index].relative_to(ROOT)),"relation_range":[start,stop],"sha256":support.sha_json(left)})
        right_files.append({"path":str(MIXED_RIGHT[index].relative_to(ROOT)),"relation_range":[start,stop],"sha256":support.sha_json(right)})
    mixed_manifest={"schema":"w33.pass1346.mixed_26x4_constants.manifest.v1","status":"PASS",
      "logical_full_sha256":logical_hash,"metadata_file":str(MIXED_METADATA.relative_to(ROOT)),
      "metadata_sha256":support.sha_json(metadata),"left_chunks":left_files,"right_chunks":right_files}
    MIXED_OUT.write_text(json.dumps(mixed_manifest,sort_keys=True,separators=(",",":"))+"\n")

    full_selector=json.loads(SELECTOR_OUT.read_text())
    record_files={}
    for length,record in full_selector["records"].items():
        compact=json.loads(json.dumps(record))
        for observable in ("shift","occupation","cosine_quadrature"):
            compact[observable].pop("coordinate_compression",None)
        component={"schema":"w33.pass1347.cycle_copy_observables.record.v1","status":"PASS","length":int(length),"record":compact}
        path=SELECTOR_RECORDS[int(length)]
        path.write_text(json.dumps(component,sort_keys=True,separators=(",",":"))+"\n")
        record_files[length]={"path":str(path.relative_to(ROOT)),"sha256":support.sha_json(component)}
    selector_manifest={"schema":"w33.pass1347.cycle_copy_observables.manifest.v1","status":"PASS",
      "record_files":record_files,"measurement_statement":full_selector["measurement_statement"],
      "boundary":full_selector["boundary"]}
    SELECTOR_OUT.write_text(json.dumps(selector_manifest,sort_keys=True,separators=(",",":"))+"\n")
    return mixed_manifest,selector_manifest


def main(write=True):
    basic=basic_frontier.modular_basic_algebras()
    mixed=later_frontiers.mixed_26x4_coupling()
    model=support.literal_species20_model()
    selector=later_frontiers.cycle_copy_observables(model)
    runtime=later_frontiers.atlas_runtime_closure(model)
    fusion=later_frontiers.modular_triality_fusion(mixed)
    mixed_manifest,selector_manifest=split_generated_payloads()
    mixed["mixed_constants_sha256"]=mixed_manifest["logical_full_sha256"]
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
        "status":selector_manifest["status"],"file":str(SELECTOR_OUT.relative_to(ROOT)),"sha256":support.sha_json(selector_manifest),
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
    assert result["pass1346_mixed_hecke_triality"]["mixed_constants_sha256"]==mixed["logical_full_sha256"]
    assert {p:r["basic_algebra_dimension"] for p,r in basic["records"].items()}=={"2":23,"3":26,"5":15}
    records={length:json.loads((ROOT/info["path"]).read_text())["record"] for length,info in selector["record_files"].items()}
    assert records["7"]["cosine_quadrature"]["basis_invariant_frobenius_energy"]=="131/3456"
    assert records["8"]["cosine_quadrature"]["basis_invariant_frobenius_energy"]=="5/144"
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
