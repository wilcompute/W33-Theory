#!/usr/bin/env python3
"""PART CCCXCI -- E8 Artifact Regeneration Pipeline.

The operation-preserving H1 -> E8 bridge is blocked only by concrete artifact
availability.  The repo already contains the builder/exporter/analyzer scripts.
This part records the exact regeneration order and source dependencies.

Pipeline:
  1. tools/build_e8_root_metadata_table.py
     -> artifacts/e8_root_metadata_table.json
  2. tools/export_e8_structure_constants_from_w33_discrete.py
     -> artifacts/e8_structure_constants_w33_discrete.json
  3. tools/verify_e8_z3grading_from_structure_constants.py
     -> grading verification
  4. tools/analyze_e8_g1g2_to_g0_couplings.py
     -> g1*g2 -> g0 semantics
  5. tools/analyze_e8_g1g1_couplings_cubic_firewall.py
     -> g1*g1 -> g2 cubic/firewall semantics

This script is a DAG/preflight checker, not a subprocess runner.  It tells us
exactly what can be run and what source dependency is missing.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STEPS=[
    {
        "step":1,
        "name":"build_root_metadata",
        "script":"tools/build_e8_root_metadata_table.py",
        "requires":[
            "tools/verify_e8_root_system_from_trinification.py",
            "artifacts/verify_e8_dynkin_from_trinification.json",
            "artifacts/sage_verify_e8_trinification_closeout.json",
            "artifacts/e8_coxeter6_orbits.json",
            "artifacts/e8_root_to_edge.json"
        ],
        "produces":["artifacts/e8_root_metadata_table.json","artifacts/e8_root_metadata_table.md"]
    },
    {
        "step":2,
        "name":"export_structure_constants",
        "script":"tools/export_e8_structure_constants_from_w33_discrete.py",
        "requires":["artifacts/e8_root_metadata_table.json"],
        "produces":["artifacts/e8_structure_constants_w33_discrete.json","artifacts/e8_structure_constants_w33_discrete.md"]
    },
    {
        "step":3,
        "name":"verify_z3_grading",
        "script":"tools/verify_e8_z3grading_from_structure_constants.py",
        "requires":["artifacts/e8_structure_constants_w33_discrete.json","artifacts/e8_root_metadata_table.json"],
        "produces":["artifacts/verify_e8_z3grading_from_structure_constants.json","artifacts/verify_e8_z3grading_from_structure_constants.md"]
    },
    {
        "step":4,
        "name":"analyze_g1g2_to_g0",
        "script":"tools/analyze_e8_g1g2_to_g0_couplings.py",
        "requires":["artifacts/e8_structure_constants_w33_discrete.json","artifacts/e8_root_metadata_table.json"],
        "produces":["artifacts/e8_g1g2_to_g0_couplings.json","artifacts/e8_g1g2_to_g0_couplings.md"]
    },
    {
        "step":5,
        "name":"analyze_g1g1_cubic_firewall",
        "script":"tools/analyze_e8_g1g1_couplings_cubic_firewall.py",
        "requires":["artifacts/e8_structure_constants_w33_discrete.json","artifacts/e8_root_metadata_table.json","artifacts/canonical_su3_gauge_and_cubic.json","artifacts/firewall_bad_triads_mapping.json"],
        "produces":["artifacts/e8_g1g1_couplings_cubic_firewall.json","artifacts/e8_g1g1_couplings_cubic_firewall.md"]
    }
]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def exists(path): return (ROOT/path).exists()
def preflight():
    out=[]
    available=set()
    for st in STEPS:
        script_exists=exists(st['script'])
        req_status={p:(exists(p) or p in available) for p in st['requires']}
        ready=script_exists and all(req_status.values())
        out.append({"step":st['step'],"name":st['name'],"script":st['script'],"script_exists":script_exists,"ready":ready,"requires":req_status,"produces":st['produces']})
        if ready:
            available.update(st['produces'])
    return out
def next_action(pf):
    for st in pf:
        if not st['ready']:
            missing=[p for p,v in st['requires'].items() if not v]
            if not st['script_exists']:
                missing.append(st['script'])
            return {"blocked_at_step":st['step'],"blocked_name":st['name'],"missing":missing,"command_when_ready":f"python {st['script']}"}
    return {"blocked_at_step":None,"state":"ALL_STEPS_PREFLIGHT_READY","commands":[f"python {st['script']}" for st in STEPS]}
def build_results():
    pf=preflight(); na=next_action(pf); checks=[]
    checks.append(ok('five pipeline steps recorded',len(STEPS)==5,[s['name'] for s in STEPS]))
    checks.append(ok('root metadata builder exists',exists('tools/build_e8_root_metadata_table.py'),None))
    checks.append(ok('structure constants exporter exists',exists('tools/export_e8_structure_constants_from_w33_discrete.py'),None))
    checks.append(ok('z3 verifier exists',exists('tools/verify_e8_z3grading_from_structure_constants.py'),None))
    checks.append(ok('z3 manifest declares actual verifier JSON',STEPS[2]['produces'][0]=='artifacts/verify_e8_z3grading_from_structure_constants.json',STEPS[2]['produces']))
    checks.append(ok('preflight returns five records',len(pf)==5,pf))
    checks.append(ok('next action is defined','blocked_at_step' in na or na.get('state')=='ALL_STEPS_PREFLIGHT_READY',na))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXCI","title":"E8 Artifact Regeneration Pipeline","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"pipeline":STEPS,"preflight":pf,"next_action":na,"architecture_upgrade":"Records the exact regeneration DAG from root metadata to structure constants to Z3/bracket analyzers, turning the artifact blocker into an executable pipeline plan.","theorem":"The E8 operation bridge has a finite regeneration order: root metadata must be built first, structure constants second, grading verification third, and coupling analyzers after that. No bracket-level claim is allowed until the preflight reaches the relevant ready state.","honesty_boundary":"This is a preflight/pipeline manifest, not a run log. It does not execute subprocesses or fabricate missing artifacts.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXCI_e8_artifact_regeneration_pipeline_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"next_action":r['next_action'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
