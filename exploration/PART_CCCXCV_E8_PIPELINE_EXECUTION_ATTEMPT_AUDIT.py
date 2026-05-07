#!/usr/bin/env python3
"""PART CCCXCV -- E8 Pipeline Execution Attempt Audit.

Records the attempted execution path for the E8 operation bridge pipeline.

What has been done:
1. The workflow was updated so push-triggered runs execute the full bridge
   pipeline, not dry-run only.
2. A run-request artifact was pushed under artifacts/ci/ to match the workflow
   path trigger.
3. The connector returned no workflow runs/statuses for the workflow-update or
   run-request commits, so remote execution status is not available through the
   current connector view.

This audit keeps the state honest: the pipeline is wired and a trigger request
was pushed, but remote GitHub Actions execution is not confirmed here.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORKFLOW='.github/workflows/e8-operation-bridge-pipeline.yml'
RUNNER='tools/run_e8_operation_bridge_pipeline.py'
REQUEST='artifacts/ci/e8_operation_bridge_run_request.json'
COMMITS={
    'workflow_update':'7c5b774e3d380eb05c0bc95871013d899acd8e39',
    'run_request':'cc1a9c0edcadb296fc8aa86baef941c814ef4797',
}
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def exists(path): return (ROOT/path).exists()
def build_results():
    checks=[]
    checks.append(ok('workflow exists',exists(WORKFLOW),WORKFLOW))
    checks.append(ok('runner exists',exists(RUNNER),RUNNER))
    checks.append(ok('run request marker exists',exists(REQUEST),REQUEST))
    checks.append(ok('workflow update commit recorded',len(COMMITS['workflow_update'])==40,COMMITS['workflow_update']))
    checks.append(ok('run request commit recorded',len(COMMITS['run_request'])==40,COMMITS['run_request']))
    checks.append(ok('remote status remains external to this audit',True,'connector returned no workflow runs/statuses'))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXCV","title":"E8 Pipeline Execution Attempt Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"workflow":WORKFLOW,"runner":RUNNER,"run_request_marker":REQUEST,"commits":COMMITS,"execution_status":"REQUESTED_BUT_REMOTE_RUN_NOT_VISIBLE_THROUGH_CONNECTOR","manual_verification_steps":["Open GitHub Actions", "Select E8 Operation Bridge Pipeline", "Check run for commit cc1a9c0edcadb296fc8aa86baef941c814ef4797", "Download e8-operation-bridge-artifacts if present"],"architecture_upgrade":"Records the attempted execution of the E8 operation bridge pipeline after wiring push-mode full runs and pushing a run-request marker.","honesty_boundary":"This is not a successful remote run log. The GitHub connector returned no workflow runs/statuses for the relevant commits, so the remote execution must be checked directly in GitHub Actions or rerun manually via workflow_dispatch.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXCV_e8_pipeline_execution_attempt_audit_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"execution_status":r['execution_status'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
