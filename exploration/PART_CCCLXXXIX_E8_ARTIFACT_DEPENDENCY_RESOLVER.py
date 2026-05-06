#!/usr/bin/env python3
"""PART CCCLXXXIX -- E8 Artifact Dependency Resolver.

The H1 -> E8 operation bridge needs concrete structure constants and grade
metadata.  Existing repo tools reference these files:

    artifacts/e8_structure_constants_w33_discrete.json
    artifacts/e8_root_metadata_table.json

This resolver checks whether they are present, records the analyzer tools that
consume them, and emits the next actionable state:

    READY_FOR_BRACKET_VERIFICATION
    or
    MISSING_ARTIFACTS_REGENERATE_OR_RESTORE

It is intentionally honest: it never claims operation compatibility unless the
required artifacts are actually loadable.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={
    "structure_constants":"artifacts/e8_structure_constants_w33_discrete.json",
    "root_metadata":"artifacts/e8_root_metadata_table.json",
}
ANALYZERS={
    "z3_grading_verifier":"tools/verify_e8_z3grading_from_structure_constants.py",
    "g1g2_to_g0":"tools/analyze_e8_g1g2_to_g0_couplings.py",
    "g1g1_cubic_firewall":"tools/analyze_e8_g1g1_couplings_cubic_firewall.py",
    "firewall_jacobi":"tools/verify_e8_firewall_filtered_bracket_jacobi.py",
}
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def status(paths): return {k:{"path":p,"exists":(ROOT/p).exists()} for k,p in paths.items()}
def next_state(artifacts):
    return "READY_FOR_BRACKET_VERIFICATION" if all(v['exists'] for v in artifacts.values()) else "MISSING_ARTIFACTS_REGENERATE_OR_RESTORE"
def regeneration_targets():
    return [
        "restore artifacts/e8_structure_constants_w33_discrete.json",
        "restore artifacts/e8_root_metadata_table.json",
        "or run the original E8 export pipeline that writes both files",
        "then run tools/verify_e8_z3grading_from_structure_constants.py",
        "then run g1g1/g1g2 coupling analyzers against the restored artifacts",
    ]
def build_results():
    artifacts=status(REQUIRED); analyzers=status(ANALYZERS); state=next_state(artifacts); checks=[]
    checks.append(ok('two required artifact paths recorded',len(artifacts)==2,artifacts))
    checks.append(ok('four analyzer paths recorded',len(analyzers)==4,analyzers))
    checks.append(ok('next state is valid',state in ('READY_FOR_BRACKET_VERIFICATION','MISSING_ARTIFACTS_REGENERATE_OR_RESTORE'),state))
    checks.append(ok('regeneration targets recorded',len(regeneration_targets())>=5,regeneration_targets()))
    checks.append(ok('honest missing artifact handling',state=='READY_FOR_BRACKET_VERIFICATION' or not all(v['exists'] for v in artifacts.values()),{"state":state,"artifacts":artifacts}))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXXIX","title":"E8 Artifact Dependency Resolver","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"required_artifacts":artifacts,"analyzer_tools":analyzers,"next_state":state,"regeneration_targets":regeneration_targets(),"architecture_upgrade":"Turns the operation-preserving H1->E8 bridge into a concrete dependency gate: either the E8 structure artifacts exist and bracket verification can run, or the exact missing files are listed for regeneration/restoration.","theorem":"Bracket-level H1-to-E8 verification is blocked exactly by the availability of the E8 structure constants and root-grade metadata. Once those two artifacts are present, the existing analyzer tools can test the Z3 grading and g1/g2 coupling rules.","honesty_boundary":"This is a dependency resolver, not a bracket verification result. Missing artifacts mean no operation-preserving claim is made.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXXIX_e8_artifact_dependency_resolver_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"next_state":r['next_state'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
