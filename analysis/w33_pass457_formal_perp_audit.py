#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'formal'/'W33'/'Pass457PerpMonotonicity.lean';OUT=ROOT/'data'/'w33_pass457_formal_perp_audit.json'
REQ=['singleton_span_le_pair_span','pair_orthogonal_le_axis','shifted_pair_orthogonal_le_axis']
def build_payload():
    text=SOURCE.read_text();checks={
      'source_present':SOURCE.exists(),'imports_pass447':'import W33.Pass447SpanLemma' in text,
      'imports_bilinear_orthogonal':'Mathlib.LinearAlgebra.BilinearForm.Orthogonal' in text,
      'uses_mathlib_orthogonal_le':'B.orthogonal_le' in text,
      'all_theorems_present':all(f'theorem {x}' in text for x in REQ),
      'uses_pass447_span_pair_shift':'W33.Pass447.span_pair_shift' in text,
      'no_sorry':'sorry' not in text.lower(),'no_axiom':'axiom ' not in text.lower(),
    }
    return {'schema':'w33.pass457.formal_perp_audit.v1','status':'PASS' if all(checks.values()) else 'FAIL','source_sha256':hashlib.sha256(text.encode()).hexdigest(),'required_theorems':REQ,'formal_boundary':'The span-shift and orthogonal-antitonicity core of L1 is formalized. The finite-geometric identification of the elation center and the rim/bulk count remain outside this module.','checks':checks}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 457 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
