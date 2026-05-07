#!/usr/bin/env python3
"""PART CCCXCIII -- E8 Operation Bridge CI Workflow Audit.

Audits the GitHub Actions workflow that runs the E8 operation-bridge pipeline.

Workflow:
    .github/workflows/e8-operation-bridge-pipeline.yml

The workflow supports manual dispatch in dry-run/run mode, always performs a
preflight dry run, and uploads JSON/Markdown artifacts for review.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORKFLOW=ROOT/'.github'/'workflows'/'e8-operation-bridge-pipeline.yml'
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def read_workflow(): return WORKFLOW.read_text(encoding='utf-8') if WORKFLOW.exists() else ''
def build_results():
    text=read_workflow(); checks=[]
    checks.append(ok('workflow exists',WORKFLOW.exists(),str(WORKFLOW)))
    checks.append(ok('workflow has manual dispatch','workflow_dispatch:' in text,None))
    checks.append(ok('workflow has dry-run mode','dry-run' in text,None))
    checks.append(ok('workflow has run mode','run_mode' in text and '- run' in text,None))
    checks.append(ok('workflow calls runner dry-run','python tools/run_e8_operation_bridge_pipeline.py --dry-run' in text,None))
    checks.append(ok('workflow calls runner actual run','python tools/run_e8_operation_bridge_pipeline.py | tee' in text,None))
    checks.append(ok('workflow uploads artifacts','actions/upload-artifact@v4' in text,None))
    checks.append(ok('workflow installs sympy','python -m pip install sympy' in text,None))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXCIII","title":"E8 Operation Bridge CI Workflow Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"workflow":".github/workflows/e8-operation-bridge-pipeline.yml","manual_modes":["dry-run","run"],"architecture_upgrade":"Adds a GitHub Actions workflow so the E8 operation bridge pipeline can be run and reviewed reproducibly from CI, with preflight JSON and generated artifacts uploaded.","honesty_boundary":"This audits the workflow definition. It does not claim the remote workflow has already been executed successfully.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXCIII_e8_operation_bridge_ci_workflow_audit_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"workflow":r['workflow'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
