#!/usr/bin/env python3
"""BT939 - quotient status for support-76 selector candidates.

Combines BT937 and BT938.  Since the full support-76 enumeration and full
order-48 chain action are not yet available, BT939 quotients only the current
best certificate under the transported C3 subgroup and records the exact
remaining blockers.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/bt939_support76_quotient_status.json'

BEST_PROFILE=[6,6,6,10,10,10,14,14]
C3_ACTIONS=3

def rotate_blocks(profile):
    # Treat profile as four displayed hyperbolic-pair support pairs.
    pairs=[tuple(profile[i:i+2]) for i in range(0,8,2)]
    return [pairs, [pairs[0],pairs[2],pairs[3],pairs[1]], [pairs[0],pairs[3],pairs[1],pairs[2]]]

def main():
    orbit=rotate_blocks(BEST_PROFILE)
    canonical=min(tuple(x for pair in o for x in pair) for o in orbit)
    result={
        'theorem':'BT939 quotient status for support-76 selector candidates',
        'status':'partial quotient: current certificate under transported C3 only; full many-or-one unresolved',
        'current_best_profile':BEST_PROFILE,
        'transported_group_used':'coordinate C3 subgroup from BT937',
        'group_size_used':C3_ACTIONS,
        'current_certificate_orbit_size_under_C3':len({tuple(x for pair in o for x in pair) for o in orbit}),
        'canonical_representative_under_C3':list(canonical),
        'unresolved_requirements':['enumerate all support-sum-76 hyperbolic decompositions','construct full order-48 signed monomial action on chain H','quotient the full candidate set by the full action'],
        'orbit_conclusion':'The single current certificate has a C3 orbit of size 3 under the transported coordinate action. This does not resolve one-orbit uniqueness because the full support-76 candidate set and full order-48 chain action are still missing.',
        'checks':{'T1_current_certificate_quotiented_by_C3':True,'T2_C3_orbit_size_recorded':True,'T3_full_support76_set_not_assumed':True,'T4_full_order48_action_not_assumed':True,'T5_many_or_one_remains_unresolved':True}
    }
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('BT939 wrote',OUT)
if __name__=='__main__': main()
