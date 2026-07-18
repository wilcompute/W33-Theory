#!/usr/bin/env python3
"""Pass 462 structural audit for the end-to-end q=3 cover-law L1 Lean module."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'formal'/'W33'/'Pass462CoverLawL1Q3.lean';OUT=ROOT/'data'/'w33_pass462_formal_cover_l1_audit.json'
def build_payload():
 s=SRC.read_text();required=['def symp','def Canonical','def zact','theorem abstract_l1_axis','theorem q3_L1_all_common_in_rim','theorem q3_L1_common_card_four','theorem q3_L1_bulk_common_card_zero','theorem q3_cover_law_L1']
 checks={
  'source_present':SRC.exists(),'imports_pass457':'import W33.Pass457PerpMonotonicity' in s,
  'defines_projective_q3_objects':all(x in s for x in ['abbrev V4','def points','def Opposite','def Rim','def Common']),
  'all_required_theorems_present':all(x in s for x in required),
  'uses_native_decide_three_times':s.count('native_decide')==3,
  'uses_pass457_axis_bridge':'shifted_pair_orthogonal_le_axis' in s,
  'no_sorry':'sorry' not in s.lower(),'no_custom_axiom':'axiom ' not in s.lower(),
 }
 return {'schema':'w33.pass462.formal_cover_l1_audit.v1','status':'PASS' if all(checks.values()) else 'FAIL','source_sha256':hashlib.sha256(s.encode()).hexdigest(),'required_declarations':required,'formal_result':'The span/perp implication is generic; the complete L1 rim inclusion and exact q+1=4 versus bulk=0 count are formalized objectwise for W(3,3) using canonical PG(3,3) representatives.','boundary':'This closes L1 end-to-end at q=3. The uniform symbolic cardinality proof for every odd prime power remains a separate formalization target.','checks':checks}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 462 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
 return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
