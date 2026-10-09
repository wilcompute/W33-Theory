"""No PSp(4,3)-equivariant rank-three lattice quotient of W33 Levi H1.

Reuses already-existing BT1688 character census and applies Schur/irreducibility
to the intrinsic universal Abelian cover produced Oct9. No new claim to the
irreducibility theorem itself. A symmetry-breaking quotient is NOT excluded.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def certificate():
    p=json.loads((ROOT/'data/PART_BT1688_EXACT_H1_CHARACTER_IRREDUCIBILITY_results.json').read_text())
    G=p['group']['projective_order']
    dim=p['levi_complex']['h1_dimension']
    dist={int(x):int(y) for x,y in p['character_distribution'].items()}
    assert sum(dist.values())==G==25920
    squared=sum(k*k*v for k,v in dist.items())
    assert squared==G
    assert dim==81 and dist[81]==1
    cover=json.loads((ROOT/'data/w33_20261009_universal_abelian_cover.json').read_text())
    assert cover['deck_rank']==81
    # If pi: Z^81 -> Z^3 is equivariant and surjective, pi_C gives a
    # nonzero complex linear quotient of the irreducible C^81. Impossible.
    return dict(status='PASS',automorphism_subgroup='PSp(4,3)',
       group_order=G,deck_rank=dim,character_norm_square=f'{squared}/{G}=1',
       prior_exact_character='BT1688: independently enumerated all 25920 group elements',
       result='No nontrivial PSp(4,3)-equivariant Z-linear homomorphism H1 -> lattice of rank 1 through 80, regardless of induced quotient action. In particular no equivariant rank-three deck quotient.',
       proof='Tensor a presumed nonzero equivariant Z-homomorphism with C; image is nonzero quotient of an irreducible 81-dimensional complex module, hence dimension 81. Cannot map onto rank three.',
       boundary='Applies to connected W33 Levi cycle lattice with full PSp symmetry. Spontaneous/explicit subgroup breaking or nonlinear emergent geometries remain possible. Rank-three quotient under a proper subgroup not excluded.')
if __name__=='__main__':
    c=certificate()
    (ROOT/'data/w33_20261009_no_equivariant_three_space.json').write_text(json.dumps(c,indent=2)+'\n')
    print(c)
