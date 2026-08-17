"""Pass6077-6088 compatibility file — corrected by Pass6137-6144.

The historical anchor-25 rows were analogy-generated and canned family counts
were declared as orbit coverage. No source CE2 rows or verified action were
provided. The six rows below are hypotheses only.
"""
from fractions import Fraction

analogy_rows=[
 {"triple":((25,0),(1,0),(19,1)),"W":Fraction(-1,54),"target":"E_(19,0)"},
 {"triple":((25,0),(1,1),(26,0)),"U":Fraction(-1,108),"V":Fraction(1,108),"u_src":"g1(18,2)","v_src":"E_(1,2)"},
 {"triple":((25,0),(4,0),(16,1)),"W":Fraction(1,54),"target":"E_(16,0)"},
 {"triple":((25,0),(2,0),(20,1)),"W":Fraction(-1,12),"target":"E_(20,0)"},
 {"triple":((25,0),(5,1),(14,0)),"W":Fraction(1,18),"target":"E_(14,0)"},
 {"triple":((25,0),(3,0),(17,1)),"W":Fraction(-1,6),"target":"E_(17,0)"},
]
status={
 'anchor':'(25,*)','status':'OPEN__UNVERIFIED_ANALOGY_SEEDS_ONLY__NOT_CLOSED',
 'hypothesis_rows':len(analogy_rows),'source_certificate':None,
 'orbit_action_constructed':False,'historical_family_counts':'WITHDRAWN_UNEVIDENCED'}
print(status)
for r in analogy_rows: print(' hypothesis:',r)
