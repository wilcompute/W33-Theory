"""Pass6041-6056 compatibility file — corrected by Pass6137-6144.

Five historical seed rows are retained. No actual W(3,3) automorphism orbit or
complete CE2 row set was constructed, so anchor 23 is NOT closed.
"""
from fractions import Fraction

anchor23_seed_rows=[
 {"triple":((23,0),(1,0),(17,1)),"W":Fraction(-1,54),"target":"E_(17,0)"},
 {"triple":((23,0),(1,1),(24,0)),"U":Fraction(-1,108),"V":Fraction(1,108),"u_src":"g1(16,2)","v_src":"E_(1,2)"},
 {"triple":((23,0),(4,0),(14,1)),"W":Fraction(1,54),"target":"E_(14,0)"},
 {"triple":((23,0),(2,0),(18,1)),"W":Fraction(-1,12),"target":"E_(18,0)"},
 {"triple":((23,0),(5,1),(12,0)),"W":Fraction(1,18),"target":"E_(12,0)"},
]
status={
 'anchor':'(0,0,3) / basis (23,*)',
 'status':'OPEN_BEYOND_FIVE_SEED_ROWS__NOT_CLOSED',
 'seed_rows':len(anchor23_seed_rows),
 'orbit_action_constructed':False,
 'orbit_rows_enumerated':False,
 'historical_family_counts':'WITHDRAWN_UNEVIDENCED',
}
print('=== CE2 Anchor-23 Corrected Status ===')
for k,v in status.items(): print(f'{k}: {v}')
for row in anchor23_seed_rows: print(' seed:',row)
