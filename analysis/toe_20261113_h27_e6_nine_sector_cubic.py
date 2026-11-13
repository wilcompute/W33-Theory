#!/usr/bin/env python3
"""Exact E6 45-triple decomposition along maximal H27 nine-sectors.
Determine whether the central H27 permutation has an order-three ±1
monomial lift preserving every signed term of the cubic norm.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_h27_maximal_translation_bridge as H
OUT=ROOT/"data/toe_20261113_h27_e6_nine_sector_cubic.json"

def eliminate(A,n):
    """Return one exact GF2 solution, or None."""
    piv={}
    for indices,rhs in A:
        mask=0
        for i in indices:mask ^= 1<<i
        mask |= (int(rhs)&1)<<n
        while mask&((1<<n)-1):
            j=(mask&((1<<n)-1)).bit_length()-1
            if j in piv:mask ^= piv[j]
            else:
                piv[j]=mask
                break
        else:
            if mask>>n:return None
    x=[0]*n
    for j in sorted(piv):
        mask=piv[j]
        lhs=sum(x[i] for i in range(n) if i!=j and mask>>i&1)%2
        x[j]=lhs^((mask>>n)&1)
    assert all(sum(x[i] for i in indices)%2 == rhs%2 for indices,rhs in A)
    return x

def main():
    can=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text())
    table=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    signs={tuple(sorted(map(int,r["triple"]))):(1 if int(r["sign"])%3==1 else -1)
           for r in can["solution"]["d_triples"]}
    eh={int(i):tuple(map(int,v)) for i,v in table["maps"]["e6id_to_current_H27_address"].items()}
    he={h:i for i,h in eh.items()}
    fibres={b:sorted(i for i,h in eh.items() if h[1]==b) for b in range(3)}
    assert all(len(v)==9 for v in fibres.values())
    patterns=Counter(tuple(sorted(eh[i][1] for i in tr)) for tr in signs)
    assert patterns==Counter({(0,0,0):6,(1,1,1):6,(2,2,2):6,(0,1,2):27}),patterns
    # Compare b-fibres to blocks 0:9 9:18 18:27 as sets.
    canonical_blocks={tuple(range(9*j,9*j+9)) for j in range(3)}
    matches={tuple(x) for x in fibres.values()}==canonical_blocks
    # For the generator of the H27 centre, solve all 45 sign constraints
    # plus P^3=I on its nine 3-cycles.
    g=(0,0,1)
    perm={i:he[H.mul(eh[i],g)] for i in range(27)}
    assert len(set(perm.values()))==27
    transformed={tuple(sorted(perm[i] for i in tr)):sgn for tr,sgn in signs.items()}
    assert set(transformed)==set(signs)
    constraints=[(tr, int(transformed[tr]!=signs[tr])) for tr in signs]
    seen=set()
    cycles=[]
    for i in range(27):
        if i in seen:continue
        orbit=[];j=i
        while j not in seen:
            seen.add(j);orbit.append(j);j=perm[j]
        assert j==i and len(orbit)==3
        cycles.append(orbit)
        constraints.append((tuple(orbit),0))
    assert len(cycles)==9
    solution=eliminate(constraints,27)
    status="ORDER3_SIGNED_LIFT" if solution is not None else "NO_ORDER3_SIGNED_LIFT"
    if solution is not None:
        P=np.zeros((27,27),dtype=np.int64)
        for i,j in perm.items():P[j,i]=(-1)**solution[j]
        assert np.array_equal(P@P@P,np.eye(27,dtype=np.int64))
        assert np.array_equal(P.T@P,np.eye(27,dtype=np.int64))
        def N(x):return sum(sgn*int(x[t[0]])*int(x[t[1]])*int(x[t[2]]) for t,sgn in signs.items())
        rng=np.random.default_rng(1131327)
        for z in range(100):
            x=rng.integers(-3,4,size=27,dtype=np.int64)
            assert N(P@x)==N(x)
        # Exact monomial termwise check already follows from constraints.
        neg=sum(solution)
    else: neg=None
    result={
      "status":status,
      "canonical_E6_signed_cubic_triples":45,
      "nine_sector_ids_by_b":{str(b):ids for b,ids in fibres.items()},
      "nine_sectors_equal_standard_3_matrix_blocks_as_unordered_sets":matches,
      "b_fibre_patterns":{"000":6,"111":6,"222":6,"012":27},
      "decomposition":"18 intra-sector determinant-like monomials and 27 trilinear cross-sector monomials, exactly canonical det(A)+det(B)+det(C)-tr(ABC) support counts",
      "central_h27_generator":list(g),
      "signed_order_three_lift_exists":solution is not None,
      "central_permutation_cycle_lengths":[len(x) for x in cycles],
      "explicit_target_coordinate_negative_sign_indices":([i for i,a in enumerate(solution) if a] if solution is not None else []),
      "negative_coordinate_sign_count":neg,
      "integer_random_vector_norm_invariance_tests":100 if solution is not None else 0,
      "scope":"Concrete monomial lift of center only; the 24 noncentral right H27 shifts violate unsigned 45-triple incidence with current address map. This is not a no-go against nonmonomial E6 representations or mass derivations."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ("status","nine_sectors_equal_standard_3_matrix_blocks_as_unordered_sets","b_fibre_patterns","signed_order_three_lift_exists","negative_coordinate_sign_count")},indent=2))
    return result
if __name__=="__main__":main()
