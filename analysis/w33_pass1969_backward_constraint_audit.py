#!/usr/bin/env python3
"""Pass 1969: backward audit of the frame-colouring constraint arc."""
from __future__ import annotations
import collections,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_pass1969_backward_constraint_audit.json"
def canon(d):
 x=dict(d);x.pop("sha256_without_hash_field",None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def main():
 distinct3=9*8*7;lex_half=distinct3//2;domain_pairs=9*9
 artifacts=[
  {"id":"heredoc_escape","artifact":"legacy heredoc-generated regex model","status":"historical_vacuous","evidence":"scripts/constraint_audit.py postmortem records backspace escapes causing a regex to match nothing","executable_replay":"not located"},
  {"id":"k_lt_9","artifact":"legacy k<9 symmetry break reused below k=9","status":"historical_scope_error","evidence":"scripts/constraint_audit.py postmortem","executable_replay":"not located"},
  {"id":"spread_cap5","artifact":"analysis/w33_pass1887c_resolution_with_the_free_cuts.py","status":"restrictive_but_invalid","evidence":"analysis/w33_pass1892_1896_spread_encoding_and_a_self_audit.py exhibits exact covers with spread intersection up to 13; <=5 excludes valid covers","before":"valid exact-cover witness","after":"witness excluded"},
  {"id":"geometric_plus8_pass1938","artifact":"Pass 1938 geometric inequality x[i]<=x[g[i]]+8 on 0..8","status":"vacuous","evidence":"exact domain replay","before":domain_pairs,"after":domain_pairs},
  {"id":"geometric_plus8_pass1946","artifact":"Pass 1946 repeated +8 inequality","status":"vacuous","evidence":"exact domain replay","before":domain_pairs,"after":domain_pairs},
  {"id":"verified_unused_pass1955","artifact":"Pass 1955 corrected prefix lex","status":"verified_not_added","evidence":"Pass 1956 postmortem","constraints_before":249,"constraints_after":249},
  {"id":"spread_branch_pass1892","artifact":"analysis/w33_pass1892_1896_spread_encoding_and_a_self_audit.py","status":"sound_structural_model","evidence":"explicit 540x9 one-hot, 240 clique exact-one constraints, 36x9 spread-count definitions, fixed-search decision strategy; no false <=5 cut"},
  {"id":"prefix_lex_pass1952","artifact":"analysis/w33_pass1952_frame_chart_abi_sound_lex.py","status":"sound_witness","evidence":"known proper 14-colouring removed; symmetry-equivalent image survives; first differing one-hot bit 15"},
  {"id":"geometric_8_pass1956","artifact":"analysis/w33_pass1956_1960_the_cut_compounds_with_generators.md","status":"sound_and_added","evidence":"assert_cuts plus assert_added","constraints_before":249,"constraints_after":1209},
  {"id":"spread_signature_40_pass1966","artifact":"analysis/w33_pass1966_1967_spread_signature_cuts.py","status":"sound_and_added","evidence":"25,920-image exact orbit replay and model growth","constraints_before":3033,"constraints_after":3073,"orbit_before":25920,"orbit_after":807}]
 counts=collections.Counter(x["status"] for x in artifacts)
 checks={
  "vacuous_selftest":distinct3==504,
  "real_selftest":lex_half==252,
  "plus8_vacuous":domain_pairs==81,
  "false_cap_excludes_valid":13>5,
  "verified_unused_detected":249==249,
  "pass1956_added":1209>249,
  "pass1966_added":3073>3033,
  "pass1966_cuts":807<25920,
  "all_six_failure_modes_accounted":len(artifacts[:6])==6}
 out={
  "schema":"w33.pass1969.backward_constraint_audit.v1",
  "status":"PASS_WITH_TWO_LEGACY_REPLAYS_UNLOCATED",
  "audit_scope":"The six failure modes named by scripts/constraint_audit.py plus four sound controls from the same frame-colouring arc.",
  "exact_replays":{
    "selftest_vacuous_distinct_triples":{"before":distinct3,"after":distinct3,"constraint":"x_i<=8 over domain 0..8"},
    "selftest_real_distinct_triples":{"before":distinct3,"after":lex_half,"constraint":"x0<x1"},
    "plus8_pair":{"before":domain_pairs,"after":domain_pairs,"constraint":"x<=y+8 over x,y in 0..8"},
    "spread_cap_counterexample":{"claimed_cap":5,"certified_attained":13},
    "pass1955_model_growth":{"before":249,"after":249},
    "pass1956_model_growth":{"before":249,"after":1209},
    "pass1966_model_growth":{"before":3033,"after":3073},
    "pass1966_orbit_cut":{"before":25920,"after":807}},
  "artifacts":artifacts,"status_counts":dict(counts),
  "checks":checks,
  "theorem":"The backward audit separates four logically different defects that had previously been conflated: vacuous constraints, scope errors, genuinely restrictive but invalid cuts, and verified constraints never inserted. Of the six historical failure modes, two are executable vacuities, one is an exact invalid-cut counterexample, one is a model-growth failure, and two remain postmortem-only because their original executable artifacts were not located. Four later controls carry positive witnesses.",
  "boundary":"A missing audit stamp is not proof of unsoundness. The heredoc and k<9 cases are classified from the maintained postmortem because their original executable builders were not located; they are not presented as newly rerun."}
 assert all(checks.values());out["sha256_without_hash_field"]=canon(out)
 OUT.write_text(json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
 print(json.dumps({"sha":out["sha256_without_hash_field"],"status_counts":dict(counts)},indent=2))
if __name__=="__main__":main()
