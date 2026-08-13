#!/usr/bin/env python3
"""Pass4996 firewall, hardened after the Pass5000 workflow false-positive audit.

Scan authoritative live manuscript surfaces, not every historical/audit mirror.
Ambiguous Witting/Ihara patterns are ignored only when their local sentence is
explicitly corrective/negative. Exact stale assertions remain fail-closed.
"""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4996_STALE_CLAIM_FIREWALL.json'
MAN=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
RULES={
 'srg33_fake':re.compile(r'srg\(\s*33\s*,\s*8\s*,\s*2\s*,\s*2\s*\)',re.I),
 'ihara_bad_discriminants':re.compile(r'(?:43|107).{0,80}ihara|ihara.{0,80}(?:43|107)',re.I|re.S),
 'point_line_correlation_claim':re.compile(r'point/line duality is a\s+\*\*correlation, not a collineation\*\*',re.I),
 'witting_cp2':re.compile(r'witting.{0,100}(?:CP\s*\^?\s*2|CP2)|(?:CP\s*\^?\s*2|CP2).{0,100}witting',re.I|re.S),
 'witting_q43_identity':re.compile(r'witting.{0,120}(?:is|=|identif\w*).{0,80}(?:Q\s*\(\s*4\s*,\s*3\s*\)|Q43|steiner)',re.I|re.S),
 'outer_eigenspace_swap':re.compile(r'(?:outer|graph automorphism).{0,160}interchang\w*.{0,160}(?:24|15).{0,80}eigenspace',re.I|re.S),
 'reader_global_distance8':re.compile(r'(?:85[- ]sensor|line\+tritangent).{0,100}(?:distance|erasure).{0,30}\b8\b',re.I|re.S),
 'tritangent_support8_minimum':re.compile(r'(?:pure[- ]tritangent|tritangent).{0,120}(?:minimum|minimal).{0,80}(?:support[- ]?eight|support[- ]?8|2K4)|(?:support[- ]?eight|support[- ]?8|2K4).{0,120}(?:pure[- ]tritangent|tritangent).{0,80}(?:minimum|minimal)',re.I|re.S),
}
AMBIG={'ihara_bad_discriminants','witting_cp2','witting_q43_identity'}
NEG=re.compile(r'\b(?:not|nonisomorphic|withdrawn|superseded|incorrect|wrong|retracted|legacy|correction|corrected|false|former|old)\b',re.I)

def live_paths():
 out={'w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex','analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'}
 text=MAN.read_text(encoding='utf-8',errors='ignore')
 for m in re.finditer(r'\\input\{([^}]+)\}',text):
  p=m.group(1)
  if not Path(p).suffix:p+='.tex'
  if (ROOT/p).exists():out.add(p)
 out.update({'docs/pass4992-4999-oct-cocircuit-chain.html','docs/pass5000-5007-kernel-cocircuit-torsor.html'})
 return sorted(p for p in out if (ROOT/p).exists())

def affirmative_hits(text,rx,ambiguous):
 hits=[]
 for m in rx.finditer(text):
  if ambiguous:
   a=max(text.rfind('\n',0,m.start()),text.rfind('.',0,m.start()))+1
   b=min([x for x in (text.find('\n',m.end()),text.find('.',m.end())) if x>=0] or [len(text)])
   if NEG.search(text[a:b]):continue
  hits.append(m.group(0)[:180])
 return hits

def main():
 violations=[];scanned=live_paths()
 for rel in scanned:
  text=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
  for name,rx in RULES.items():
   if affirmative_hits(text,rx,name in AMBIG):violations.append({'rule':name,'path':rel})
 auth={
  'analysis/PASS4970_ihara_zeta_rational_corrected.tex':[
   re.compile(r'sqrt\{10\}|sqrt10'),re.compile(r'sqrt\{7\}|sqrt7')],
  'analysis/PASS4972_critical_group_40vertex_corrected.tex':[re.compile(r'Z/10'),re.compile(r'Z/40'),re.compile(r'Z/160')],
  'data/PART_W33_PASS4986_TWIN_DARK15_LEVI_OBSTRUCTION.json':[re.compile(r'incidence_preserving_side_swap_exists'),re.compile(r'false')],
  'data/PART_W33_PASS5002_CORRECTED_85_READER_ERASURE_DISTANCE.json':[re.compile(r'exact_global_erasure_distance'),re.compile(r'6')],
  'data/PART_W33_PASS5011_FIRST_MIXED_SUPPORT13_AND_TRIT_K33.json':[re.compile(r'pure_tritangent_minimum'),re.compile(r'"support"\s*:\s*6'),re.compile(r'120')],
 }
 checks={}
 for rel,rxs in auth.items():
  text=(ROOT/rel).read_text(encoding='utf-8',errors='ignore');checks[rel]=[bool(r.search(text)) for r in rxs]
  if not all(checks[rel]):violations.append({'rule':'authoritative_replacement_missing','path':rel,'checks':checks[rel]})
 out={'pass':4996,'status':'PASS' if not violations else 'FAIL','scope':'authoritative current-manifest manuscripts plus current theorem pages','scanned':scanned,'rules':sorted(RULES),'violations':violations,'authoritative_replacements':checks,'theorem':'Known retracted geometry/readout statements are fail-closed on authoritative live theory surfaces. Ambiguous historical wording is not scanned as affirmative merely because it appears in correction prose.','boundary':'Historical/audit mirrors are preserved as history and are outside the authoritative live-surface scan.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0 if not violations else 1
if __name__=='__main__':raise SystemExit(main())
