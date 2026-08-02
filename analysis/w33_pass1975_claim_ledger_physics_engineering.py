#!/usr/bin/env python3
"""Verify Pass-1975 ledger and bounded physics/engineering separation."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass1975_claim_ledger_physics_engineering.json'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 ledger=(ROOT/'analysis/W33_CLAIM_STATUS_LEDGER.md').read_text()
 eng=(ROOT/'analysis/w33_pass1975_physics_computer_engineering_implications.md').read_text()
 checks={'claim_ledger_created':'consolidated claim-status ledger' in ledger,'maximality_retraction_in_ledger':'spread 45-set is maximal independent' in ledger and 'retracted: false' in ledger,'solver_inference_retraction_in_ledger':'orbit-volume reduction predicts search-tree reduction' in ledger,'charge_flux_retractions_in_ledger':'electric charge' in ledger and 'Dirac/homological' in ledger,'exact_facts_separated':'Exact structural inputs' in eng,'engineering_proposals_labelled':'Computer-engineering proposals' in eng,'physics_hypotheses_labelled':'Physics hypotheses worth testing, not claiming' in eng,'linear_confinement_not_absolute_nature_claim':'not an absolute law of nature' in eng,'hardware_does_not_claim_chi':'do not establish `chi(H)=9`' in eng,'five_nonsequential_architectures_recorded':eng.count('### ')>=5}
 d={'schema':'w33.pass1975.claim_ledger_physics_engineering.v1','status':'PASS_WITH_PHYSICS_HYPOTHESES_SEPARATED','ledger':{'rows':32,'retracted_or_refuted':12,'narrowed_or_provisional':7,'standing_exact_or_scoped':13,'path':'analysis/W33_CLAIM_STATUS_LEDGER.md'},'exact_inputs':{'hodge_dimensions':[39,81,120],'signed_blocks':[15,24,81,30,90],'phase_sector_dimension':90,'phase_group':'C6','phase_normalizer':'D12','equivariant_linear_exports_from_90':0,'frames':540,'edge_cliques':240,'spread_signatures':36,'point_transvections':40},'engineering_proposals':['FPGA or ASIC spread-signature symmetry canonicaliser outside the solver','cube-and-conquer with geometric deduplication and stored group tags','240-bit exact-cover accelerator with wide mask intersection and popcount','three-plane exact/harmonic/coexact control architecture','isolated six-phase calibration domain with explicit symmetry-breaking interfaces'],'physics':{'supported':['orientation-signed coexact sector is necessary for the non-rational phase','the phase is linearly confined to the 90 under PSp-equivariant maps','chirality reverses the phase','the 81 cannot carry a real complex structure by parity'],'hypotheses':['nonlinear invariant mediation from two phase-sector states','minimal-subgroup controlled symmetry breaking','D12 six-state phase-reversal protocol','Hodge-projected fault diagnostics'],'withdrawn':['electric charge','homological or Dirac flux','QCD colour','generation number','neutrino assignment']},'checks':checks,'theorem':'The surviving physics content is a representation-theoretic isolation theorem: the unique Eisenstein C6 phase is supported on the coexact 90, reversed by chirality, and has no PSp-equivariant linear export to the other blocks. The engineering consequence is architectural separation—canonicalisation, exact-cover search, and phase control should be distinct modules—not a particle or charge identification.','boundary':'All hardware items are proposals. Broken symmetry or nonlinear interfaces can couple sectors that the ideal equivariant linear model separates.'}
 assert all(checks.values()),checks
 d['sha256_without_hash_field']=digest(d)
 OUT.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(d['sha256_without_hash_field'])
if __name__=='__main__':main()
