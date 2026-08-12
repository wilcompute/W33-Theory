#!/usr/bin/env python3
"""Pass4996 — fail closed on known retracted W33/Q43/Witting claims.

Historical, erratum, and explicit audit/outcomes files that must quote a bad
claim are allowlisted. Everything else is scanned. This is intentionally narrow:
only claims with an already-established corrected replacement are blocked here.
"""
from __future__ import annotations
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4996_STALE_CLAIM_FIREWALL.json'
EXT={'.md','.tex','.html','.py','.json','.g','.txt'}
SKIP_PREFIX=('archive/','.git/','build/','dist/')
SELF='tools/w33_stale_claim_firewall.py'
OUT_REL=OUT.relative_to(ROOT).as_posix()

RULES={
 'srg33_fake': re.compile(r'srg\(\s*33\s*,\s*8\s*,\s*2\s*,\s*2\s*\)',re.I),
 'ihara_bad_discriminants': re.compile(r'(?:sqrt\s*\{?\s*(?:43|107)\s*\}?|√(?:43|107)).{0,100}ihara|ihara.{0,100}(?:sqrt\s*\{?\s*(?:43|107)\s*\}?|√(?:43|107))',re.I|re.S),
 'point_line_correlation_claim': re.compile(r'point/line duality is a\s+\*\*correlation, not a collineation\*\*',re.I),
 'witting_cp2': re.compile(r'witting.{0,120}(?:CP\s*\^?\s*2|CP2)|(?:CP\s*\^?\s*2|CP2).{0,120}witting',re.I|re.S),
 'witting_q43_identity': re.compile(r'witting.{0,120}(?:is|=|identif\w*).{0,80}(?:Q\s*\(\s*4\s*,\s*3\s*\)|Q43|steiner)',re.I|re.S),
 'outer_eigenspace_swap': re.compile(r'(?:outer|graph automorphism).{0,160}interchang\w*.{0,160}(?:24|15).{0,80}eigenspace',re.I|re.S),
}

ALLOW={
 'srg33_fake':{
  'PASS4801_gap_verification.g','PASS4801_4812_SRG_CONSTELLATION_BREAKTHROUGH.md',
  'analysis/PASS4971_fano_deletion_retraction.md','analysis/ERRATUM_passes4968_prior_srg33_retraction.md',
  'data/w33_pass_namespace_registry_v2.d/4950.json'},
 'ihara_bad_discriminants':{
  'analysis/ERRATUM_passes4968_prior_srg33_retraction.md','analysis/PASS4984_4991_EXECUTED_OUTCOMES.md',
  'analysis/w33_pass4985_collision_packet_audit.py','data/PART_W33_PASS4985_COLLISION_PACKET_AUDIT.json'},
 'point_line_correlation_claim':{'analysis/w33_pass1877_1881_the_involution_the_third_class_and_a_parity_correction.md'},
 'witting_cp2':{'analysis/PASS4992_4999_EXECUTED_OUTCOMES.md'},
 'witting_q43_identity':{'analysis/PASS4992_4999_EXECUTED_OUTCOMES.md'},
 'outer_eigenspace_swap':set(),
}

def live_files():
 for p in ROOT.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in EXT:continue
  rel=p.relative_to(ROOT).as_posix()
  if rel in (SELF,OUT_REL) or rel.startswith(SKIP_PREFIX):continue
  yield rel,p

def main()->int:
 allowed_hits={k:[] for k in RULES};violations=[]
 for rel,p in live_files():
  try:text=p.read_text(encoding='utf-8',errors='ignore')
  except OSError:continue
  for name,rx in RULES.items():
   if not rx.search(text):continue
   if rel in ALLOW[name]:allowed_hits[name].append(rel)
   else:violations.append({'rule':name,'path':rel})
 auth={
  'analysis/PASS4970_ihara_zeta_rational_corrected.tex':['sqrt{10}','sqrt{7}'],
  'analysis/PASS4972_critical_group_40vertex_corrected.tex':['Z/10','Z/40','Z/160'],
  'data/PART_W33_PASS4986_TWIN_DARK15_LEVI_OBSTRUCTION.json':['incidence_preserving_side_swap_exists','false'],
 }
 authoritative={}
 for rel,tokens in auth.items():
  text=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
  authoritative[rel]={tok:(tok in text) for tok in tokens}
  if not all(authoritative[rel].values()):violations.append({'rule':'authoritative_replacement_missing','path':rel,'tokens':authoritative[rel]})
 out={'pass':4996,'status':'PASS' if not violations else 'FAIL','rules':sorted(RULES),
      'allowlisted_historical_hits':{k:sorted(v) for k,v in allowed_hits.items()},
      'violations':violations,'authoritative_replacements':authoritative,
      'theorem':'Known retracted W33/Q43/Witting claims are now fail-closed on live text surfaces; only explicit historical, erratum, or audit/outcomes paths may quote them. The firewall also asserts the corrected Ihara, critical-group, and no-point-line-correlation replacements remain present.',
      'boundary':'This is a targeted stale-claim firewall, not a proof that every sentence in the repository is current.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2,sort_keys=True))
 return 0 if not violations else 1
if __name__=='__main__':raise SystemExit(main())
