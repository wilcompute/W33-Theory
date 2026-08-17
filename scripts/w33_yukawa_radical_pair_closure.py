"""Pass5975-5988 radical-pair spectral audit — corrected by Pass6017-6024.

Exact retained result: the two displayed symmetric 2x2 blocks have the stated
trace/determinant data and positive discriminants, hence real spectra.

Withdrawn result: neither block has the equal-coordinate vector (1,1) as an
eigenvector, so this producer does not prove the proposed generation-flag
alignment. K3/Yukawa physical interpretation remains open.
"""
import math
from fractions import Fraction

blocks={
 'A':((367,-55),(-55,175)),
 'B':((323,275),(275,659)),
}

def invariants(M):
    tr=M[0][0]+M[1][1]
    det=M[0][0]*M[1][1]-M[0][1]*M[1][0]
    disc=tr*tr-4*det
    ev=((tr+math.sqrt(disc))/2,(tr-math.sqrt(disc))/2)
    row_sums=(sum(M[0]),sum(M[1]))
    equal_coordinate_is_eigen=(row_sums[0]==row_sums[1])
    return {'trace':tr,'det':det,'discriminant':disc,'eigenvalues':ev,
            'row_sums':row_sums,'equal_coordinate_is_eigen':equal_coordinate_is_eigen}

results={k:invariants(v) for k,v in blocks.items()}
assert results['A']['trace']==542 and results['A']['det']==61200 and results['A']['discriminant']==48964
assert results['B']['trace']==982 and results['B']['det']==137232 and results['B']['discriminant']==415396
assert results['A']['discriminant']>0 and results['B']['discriminant']>0
assert not results['A']['equal_coordinate_is_eigen']
assert not results['B']['equal_coordinate_is_eigen']

print('=== Yukawa Radical-Pair Corrected Spectral Report ===')
for label,r in results.items():
    print(label,r)
print('Retained: both displayed blocks have real spectra.')
print('Refuted: equal-coordinate/generation-flag eigenvector alignment.')
print('Open: any K3-side or physical Yukawa realization of these blocks.')
