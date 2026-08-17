"""Pass5957-5968 compatibility file — corrected by Pass6017-6024.

The original producer claimed full CE2 anchor-22 orbit closure but did not
construct the W33 automorphism action or evaluate the CE2 tensor on that orbit.
It generated synthetic weights from a hard-coded rule on labels 1..39.

This corrected file retains only the three imported witness rows and reports the
honest status: anchor 22 remains OPEN beyond those witnesses.
"""
from fractions import Fraction

promoted_rows = [
    {"triple": ((22,0),(1,0),(16,1)), "W": Fraction(-1,54), "target":"E_(16,0)"},
    {"triple": ((22,0),(1,1),(23,0)), "U": Fraction(-1,108), "V":Fraction(1,108),
     "u_src":"g1(15,2)", "v_src":"E_(1,2)"},
    {"triple": ((22,0),(4,0),(13,1)), "W": Fraction(1,54), "target":"E_(13,0)"},
]

# These checks certify only exact denominators of the imported witnesses.
for row in promoted_rows:
    if 'W' in row:
        assert (54*row['W']).denominator == 1
    else:
        assert (108*row['U']).denominator == 1
        assert (108*row['V']).denominator == 1

ledger = {
    'anchor':'(0,0,2) / basis (22,*)',
    'status':'OPEN_BEYOND_THREE_IMPORTED_WITNESSES',
    'verified_witness_rows':len(promoted_rows),
    'full_orbit_enumerated':False,
    'automorphism_action_constructed':False,
    'next_required_step':'construct actual W33/CE2 data and enumerate the anchor orbit under the verified automorphism action',
}

print('=== CE2 Anchor-22 Corrected Status ===')
for k,v in ledger.items(): print(f'{k}: {v}')
for row in promoted_rows: print(' witness:', row)
