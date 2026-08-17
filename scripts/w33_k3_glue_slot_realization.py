"""Pass5989-6002 K3 glue-slot formal avatar — corrected by Pass6017-6024.

The original file failed its own arithmetic assertion: gcd(780,7944,62600,53979)
is 1, not 217. It also inserted the nonzero tail-to-head map as I_81 by hand,
so it constructed a formal square-zero matrix avatar rather than a K3 geometric
realization.

This corrected file verifies only those statements.
"""
import math
import numpy as np
from fractions import Fraction

n=81
split_glue=np.zeros((n,n),dtype=int)
glue_slot=np.eye(n,dtype=int)  # deliberately inserted formal tail->head isomorphism
J2_full=np.zeros((2*n,2*n),dtype=int)
J2_full[:n,n:]=glue_slot

assert np.linalg.matrix_rank(split_glue)==0
assert np.linalg.matrix_rank(glue_slot)==81
assert np.linalg.matrix_rank(J2_full)==81
assert np.array_equal(J2_full@J2_full,np.zeros_like(J2_full))

advertised_generator=[780,7944,62600,53979]
g=0
for x in advertised_generator:
    g=math.gcd(g,x)
assert g==1

# Retained arithmetic identity; not a gcd/primitive-generator theorem.
C=Fraction(217,12)*780
assert C==14105

result={
 'status':'FORMAL_AVATAR_ONLY',
 'split_glue_rank':0,
 'inserted_glue_rank':81,
 'square_zero':True,
 'advertised_generator':advertised_generator,
 'actual_gcd':g,
 'superseded_claimed_gcd':217,
 'retained_arithmetic_C':str(C),
 'genuine_K3_glue_witness':'OPEN',
}

print('=== K3 Glue-Slot Corrected Status ===')
for k,v in result.items(): print(f'{k}: {v}')
