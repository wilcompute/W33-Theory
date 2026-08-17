"""Pass6065-6076 compatibility file — corrected by Pass6137-6144.

The historical anchor-24 rows were introduced 'by symmetry' from earlier anchors
and then canned family counts were labelled a full orbit. No source certificate,
CE2 tensor evaluation, or group action was supplied. Treat these as hypotheses,
not verified rows or a closed orbit.
"""
from fractions import Fraction

analogy_rows=[
 {"triple":((24,0),(1,0),(18,1)),"W":Fraction(-1,54),"target":"E_(18,0)"},
 {"triple":((24,0),(1,1),(25,0)),"U":Fraction(-1,108),"V":Fraction(1,108),"u_src":"g1(17,2)","v_src":"E_(1,2)"},
 {"triple":((24,0),(4,0),(15,1)),"W":Fraction(1,54),"target":"E_(15,0)"},
 {"triple":((24,0),(2,0),(19,1)),"W":Fraction(-1,12),"target":"E_(19,0)"},
 {"triple":((24,0),(5,1),(13,0)),"W":Fraction(1,18),"target":"E_(13,0)"},
 {"triple":((24,0),(3,0),(16,1)),"W":Fraction(-1,6),"target":"E_(16,0)"},
]
status={
 'anchor':'(24,*)',
 'status':'OPEN__UNVERIFIED_ANALOGY_SEEDS_ONLY__NOT_CLOSED',
 'hypothesis_rows':len(analogy_rows),
 'source_certificate':None,
 'orbit_action_constructed':False,
 'historical_family_counts':'WITHDRAWN_UNEVIDENCED',
}
print(status)
for r in analogy_rows: print(' hypothesis:',r)
