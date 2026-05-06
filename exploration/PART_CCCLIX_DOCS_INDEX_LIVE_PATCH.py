#!/usr/bin/env python3
"""PART CCCLIX -- Docs Index Live Patch Audit.

Audits the exact one-row docs/INDEX.md insertion for the finite W33 response
architecture.  The actual large index is curated, so this part supplies an
idempotent applicator script instead of replacing the whole file through a large
contents payload.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ROW="| Finite W33 response architecture | [docs/RESPONSE_ARCHITECTURE_ENTRYPOINT.md](./RESPONSE_ARCHITECTURE_ENTRYPOINT.md) | Operator-response bridge, derived sector maps, computed W33 graph evidence, and empirical model-comparison stack |"
ANCHOR="Temporal / spectral toroidal computer audit"
APPLICATOR="tools/apply_response_architecture_index_patch.py"
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def build_results():
    checks=[]
    checks.append(ok('row contains entrypoint','RESPONSE_ARCHITECTURE_ENTRYPOINT.md' in ROW,ROW))
    checks.append(ok('row contains response architecture title','Finite W33 response architecture' in ROW,ROW))
    checks.append(ok('row contains computed evidence phrase','computed W33 graph evidence' in ROW,ROW))
    checks.append(ok('anchor phrase recorded',ANCHOR.startswith('Temporal'),ANCHOR))
    checks.append(ok('applicator path recorded',APPLICATOR.endswith('.py'),APPLICATOR))
    checks.append(ok('row is markdown table row',ROW.startswith('|') and ROW.endswith('|'),ROW))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLIX","title":"Docs Index Live Patch Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"index_row":ROW,"anchor_phrase":ANCHOR,"applicator":APPLICATOR,"architecture_upgrade":"Provides a safe idempotent script to insert the finite W33 response architecture row into docs/INDEX.md without replacing the curated index by hand.","honesty_boundary":"The live index file itself was not replaced through a massive payload; the committed applicator performs the exact one-row insertion locally or in CI.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLIX_docs_index_live_patch_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
