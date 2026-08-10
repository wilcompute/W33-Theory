#!/usr/bin/env python3
"""Pass 4794 — fourth-moment obstruction narrows rho(H10) to 14 or 15.

Pass 4781 gave 14 <= rho(H10) <= 16 and proved that the 270-coordinate
syndrome code has weight at most 179.  Here the fourth Krawtchouk moment converts
the 270 weight-4 dual checks into a contradiction for any even coset whose
minimum were >=16.  Only an odd distance-15 coset can still make rho=15.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4794_COVERING_RADIUS_K4.json'

def K4_t(t:int)->int:
    # n=40, t=w-20, K4=(2 t^4 -116 t^2 +570)/3.
    z=2*t**4-116*t*t+570
    assert z%3==0
    return z//3

assert {t:K4_t(t) for t in (0,1,2,3,4,5)}=={0:190,1:152,2:46,3:-104,4:-258,5:-360}

# EVEN hypothetical minimum >=16.  Complement symmetry gives counts
# A16=A24=a, A18=A22=b, A20=c.  OA strength 3 (dual distance 4) gives
# 2a+2b+c=1024 and 4a+b=1280.
# Hence b=1280-4a, c=6a-1536 and nonnegativity gives 256<=a<=320.
# The K4 sum is 256a-174080.  MacWilliams on a coset says
# sum K4 = |H10|*(270-2s), where s is the number of odd weight-4 checks.
# Therefore a=1760-8s. Pass4781 proved s<=179, hence a>=328, contradiction.
even_a_lo,even_a_hi=256,320
min_a_from_syndrome_ceiling=1760-8*179
assert min_a_from_syndrome_ceiling==328>even_a_hi

# ODD hypothetical minimum >=15.  Counts at 15/25,17/23,19/21 are a,b,c.
# OA constraints give a+b+c=512, 3a+b=576, so 32<=a<=192.
# K4 gives a=812-4s.  The syndrome ceiling only yields a>=96, so this
# case is not contradicted: exact rho remains 14 or 15.
odd_a_lo,odd_a_hi=32,192
odd_min_a_from_syndrome_ceiling=812-4*179
assert odd_min_a_from_syndrome_ceiling==96
assert odd_a_lo<=odd_min_a_from_syndrome_ceiling<=odd_a_hi

out={
 'pass':4794,
 'H10_parameters':'[40,10,12]',
 'previous_bracket':[14,16],
 'radius14_witness':253626779097,
 'weight4_dual_checks':270,
 'syndrome_weight_ceiling_from_pass4781':179,
 'K4_values_by_abs_t':{str(t):K4_t(t) for t in range(6)},
 'even_min16_case':{
   'OA_solution':'A16=A24=a; A18=A22=1280-4a; A20=6a-1536',
   'nonnegative_a_interval':[256,320],
   'K4_MacWilliams_relation':'a=1760-8s',
   'syndrome_ceiling_forces_a_at_least':328,
   'feasible':False},
 'odd_min15_case':{
   'OA_solution':'A15=A25=a; A17=A23=576-3a; A19=A21=2a-64',
   'nonnegative_a_interval':[32,192],
   'K4_MacWilliams_relation':'a=812-4s',
   'syndrome_ceiling_forces_a_at_least':96,
   'feasible_after_these_moments':True},
 'new_covering_radius_bracket':[14,15],
 'theorem':'Every even H10 coset has minimum at most 14. Together with the explicit distance-14 witness and the previous general upper bound, 14 <= rho(H10) <= 15. A distance-15 obstruction, if it exists, must be an odd coset.',
 'boundary':'This pass does not decide whether an odd distance-15 coset exists; rho=14 is not claimed.'}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
