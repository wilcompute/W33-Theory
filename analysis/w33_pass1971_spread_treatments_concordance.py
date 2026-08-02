#!/usr/bin/env python3
"""Rebuild the Pass-1971 concordance certificate from current repository text."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass1971_spread_treatments_concordance.json'

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    note=(ROOT/'analysis/W33_SPREAD_OBSTRUCTION_NOTE.md').read_text()
    draft=(ROOT/'analysis/W33_SPREAD_OBSTRUCTION_REFEREE_DRAFT.tex').read_text()
    concord=(ROOT/'analysis/w33_pass1971_spread_treatments_concordance.md').read_text()
    checks={
      'independent_seed_retained':'independent set' in note and 'independent set' in draft,
      'maximality_withdrawn':'not maximal independent' in note and 'not maximal independent' in draft,
      'candidate_counterexample_recorded':'15 residual candidate' in concord,
      'completion_obstruction_retained':'20 of 60' in note and '20 of the 60' in draft,
      'orbit_search_distinction_recorded':'orbit-volume reduction and search-tree reduction' in concord,
      'charge_flux_withdrawals_retained':'electric charge' in note and 'homological' in draft,
      'two_treatments_reconciled':'claim-by-claim reconciliation' in concord,
      'draft_corrected':'support deficiency' in draft,
      'note_corrected':'support deficiency' in note,
    }
    d={
      'schema':'w33.pass1971.spread_treatments_concordance.v1',
      'status':'PASS_WITH_FALSE_MAXIMALITY_WITHDRAWN',
      'claims_compared':16,
      'corrections':{
        'false_claim':'the 45 spread frames form a maximal independent set',
        'counterexample':'15 residual candidate frames are individually nonadjacent to all 45 spread frames',
        'replacement':'the 45-frame seed has a residual support-deficiency obstruction: the 15 candidates touch only 20 of 60 residual edges'},
      'solver_reconciliation':{'orbit_before':25920,'orbit_after_40_cuts':807,'spread_only_branches':60909,'combined_8_branches':451460,'combined_40_branches':512714,'conclusion':'orbit-volume reduction and search-tree reduction are distinct observables'},
      'scope':{'one_over_q':'exact under the candidate-orbit property; the property is verified for q=3,5,7, while a linewise involution alone certifies only the orbit-generated subfamily','sigma':'proved for the associated Desarguesian symplectic spread; uniqueness exact only at q=3','chi':'open'},
      'checks':checks,
      'theorem':'The two spread-obstruction treatments agree after one explicit withdrawal: the spread 45-set is independent but not maximal. The exact obstruction is that its 15 residual candidates cover only 20 of 60 residual edges, so no 60-frame exact cover extends the seed.',
      'boundary':'The concordance does not decide chi(H), does not classify arbitrary symplectic spreads, and does not turn orbit reduction into a performance claim.'}
    assert all(checks.values())
    d['sha256_without_hash_field']=digest(d)
    OUT.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n')
    print(d['sha256_without_hash_field'])
if __name__=='__main__':main()
