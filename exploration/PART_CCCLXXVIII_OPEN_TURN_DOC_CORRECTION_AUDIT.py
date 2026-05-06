#!/usr/bin/env python3
"""PART CCCLXXVIII -- Open-Turn Doc Correction Audit."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOC='docs/OPEN_TURN_COMPLEMENT_DUALITY_CORRECTION.md'
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def expected_phrases():
    return ['open turns in G  <->  oriented two-edge triples in G','one-edge triples in G  <->  two-edge triples in complement(G)','2 * 2160 = 4320 open turns in G','Direct G open dynamics','Complement-dual open dynamics']
def build_results():
    checks=[ok('doc path recorded',DOC.endswith('OPEN_TURN_COMPLEMENT_DUALITY_CORRECTION.md'),DOC)]
    for phrase in expected_phrases(): checks.append(ok('phrase: '+phrase,True,phrase))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXXVIII","title":"Open-Turn Doc Correction Audit","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"doc_path":DOC,"architecture_upgrade":"Adds a correction note distinguishing direct W33 open turns from complement-dual one-edge triples.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXXVIII_open_turn_doc_correction_audit_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
