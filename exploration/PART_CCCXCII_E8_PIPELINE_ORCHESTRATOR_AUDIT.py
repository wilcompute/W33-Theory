#!/usr/bin/env python3
"""PART CCCXCII -- E8 Pipeline Orchestrator Audit.

Audits the single-command operation-bridge pipeline runner:

    tools/run_e8_operation_bridge_pipeline.py

The runner performs dry-run/preflight and ordered execution for the E8 artifact
bridge.  This audit imports the runner, checks the five-step DAG, and records the
current readiness state without executing the heavy pipeline.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/'tools'/'run_e8_operation_bridge_pipeline.py'
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def load_runner():
    spec=importlib.util.spec_from_file_location('run_e8_operation_bridge_pipeline',RUNNER)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod
def build_results():
    mod=load_runner(); pf=mod.preflight(); checks=[]
    checks.append(ok('runner exists',RUNNER.exists(),str(RUNNER)))
    checks.append(ok('pipeline has five steps',len(mod.STEPS)==5,[s.name for s in mod.STEPS]))
    checks.append(ok('first step builds root metadata',mod.STEPS[0].name=='build_root_metadata',mod.STEPS[0].name))
    checks.append(ok('second step exports structure constants',mod.STEPS[1].name=='export_structure_constants',mod.STEPS[1].name))
    checks.append(ok('preflight has first_blocked or ready flag','first_blocked' in pf and 'ready_to_run_all' in pf,pf))
    checks.append(ok('preflight step records match pipeline length',len(pf['steps'])==len(mod.STEPS),len(pf['steps'])))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXCII","title":"E8 Pipeline Orchestrator Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"runner":"tools/run_e8_operation_bridge_pipeline.py","dry_run_command":"python tools/run_e8_operation_bridge_pipeline.py --dry-run","run_command":"python tools/run_e8_operation_bridge_pipeline.py","preflight":pf,"architecture_upgrade":"Adds a single-command runner that preflights and executes the E8 artifact bridge pipeline in dependency order, stopping at the first missing dependency or failed script.","honesty_boundary":"The audit imports and preflights the runner only. It does not execute heavy subprocess steps.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXCII_e8_pipeline_orchestrator_audit_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"runner":r['runner'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
