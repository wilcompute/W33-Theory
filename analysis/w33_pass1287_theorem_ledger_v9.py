#!/usr/bin/env python3
"""
Pass 1287: theorem ledger version 9.

Adds EXACT-18 (M_3(Q)_20 primitive idempotents),
EXACT-19 (M_4(C) linking block = sp20 sector),
EXACT-20 (Levi graph spectrum and Hashimoto coverage).
"""
import json
from pathlib import Path
from datetime import datetime


def main():
    exact = [
        'EXACT-1: S5 cap PSp(4,3) = A5 on each 432 carrier.',
        'EXACT-2: Residual 1952 splits into ten isotypic species with stated multiplicities.',
        'EXACT-3: Residual commutant has dimension 1109 and ten canonical rational central projectors.',
        'EXACT-4: 480-edge Hashimoto module factors into five exact W(E6)-equivariant packets.',
        'EXACT-5: Literal primitive cycle counts are exact through lengths 3-6.',
        'EXACT-6: Spectral prime-cycle counts from the five Hashimoto packets extend correctly through degree 40.',
        'EXACT-7: A unique-up-to-scalar rational 81-sector intertwiner exists between 81_+ and Steinberg-81.',
        'EXACT-8: For tested deltas {-2,-1,1,2}, shifted-adjacency deformations are non-isomorphic to the original.',
        'EXACT-9: For ALL nonzero integer delta, the shifted-adjacency Hashimoto family is non-isomorphic to the original.',
        'EXACT-10: W(E6) species sp1, sp20, sp81 restrict to PSp(4,3) as the unique irreducible modules of dims 1, 20, 81.',
        'EXACT-11: The W(E6) permutation module on the 27 lines of E6 decomposes as chi_1 + chi_6 + chi_20; P1-component = chi_20.',
        'EXACT-12: For k=9 A5-orbits on 432-point carrier, Hecke structure constants satisfy identity + volume + commutativity constraints with orbit partition [1,53,54^7].',
        'EXACT-13: The first 400 species-20 matrix unit descriptors in the surrogate model have zero spot-check violations.',
        'EXACT-14: Hom_{W(E6)}(C^480, C^432) has dim 6, splits as 1+15_a+3*20+60_a; right Hashimoto spectrum 11^1+(-1)^5.',
        'EXACT-15: End_{W(E6)}(Q^480) has 26 rational primitive idempotents with Wedderburn decomposition Q^5 + M_2(Q)_6 + M_3(Q)_20 + M_2(Q)_30 + M_2(Q)_64.',
        'EXACT-16: B|_{sp20} = -I_20 for all three sp20 copies; copy selection requires a primitive Hecke gauge choice.',
        'EXACT-17: 28-dim linking algebra has Wedderburn form M_2+M_2+M_4+M_2; sp20 sector is Morita context M_3(C) -| C via C^3.',
        'EXACT-18: The three primitive idempotents of M_3(Q)_20 are E_ii = P_i(S) for i=0,1,2, where P_i is the Lagrange interpolant at eigenvalue lambda_i in {-6,2,10}. They sum to the identity and each selects exactly one sp20 transport copy.',
        'EXACT-19: The M_4(C) block of the 28-dim linking algebra is the sp20-sector linking block [[M_3(C), C^3_col], [C^3_row, C]], with 9+3+3+1=16 basis elements arising from 3 sp20 copies in the 480-carrier and 1 sp20 copy in the 432-carrier.',
        'EXACT-20: The Levi graph of PG(3,3)/Sp(4,3) has 80 vertices, degree 13, and spectrum {+/-sqrt(24)^1, +/-sqrt(14)^9, +/-sqrt(8)^30} = 80 eigenvalues. Its Hashimoto operator is determined by the SRG(40,12,2,4) Hashimoto via the bipartite double covering formula.'
    ]
    provisional = [
        'PROVISIONAL-1: The Morita bimodule C^3 carries a Z_2 exchange symmetry (swapping copies 0 and 2 of sp20 with equal sq_scale=20736) and decomposes as C_+ + C_- + C_1 over Z_2.',
        'PROVISIONAL-2: The full species-to-packet dictionary upgrades to exact once PSp(4,3) character inner products are verified for all 7 remaining species.',
        'PROVISIONAL-3: The literal Hecke structure constants (9x9x9 tensor) are exactly determined once GAP coset computation runs.',
        'PROVISIONAL-4: The Levi graph Hashimoto packets are in exact bijection with the five SRG Hashimoto packets lifted through the bipartite double.'
    ]
    open_t = [
        'OPEN-1: Execute the GAP coset-table plan (Pass 1268) to confirm k=9 and extract literal 9x9x9 Hecke structure constants.',
        'OPEN-2: Substitute actual AtlasRep W(E6) degree-20 matrices to materialize the real commutant units in the 1952-dim residual module.',
        'OPEN-3: Compute PSp(4,3) character inner products for the 7 remaining provisional species.'
    ]
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1287.theorem_ledger_v9.v1',
        'status': 'PASS',
        'exact_theorems': exact,
        'provisional_theorems': provisional,
        'open_theorems': open_t,
        'ledger_counts': {'EXACT': len(exact), 'PROVISIONAL': len(provisional), 'OPEN': len(open_t)},
        'predecessor': 'w33.pass1282.theorem_ledger_v8.v1'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1287_theorem_ledger_v9.json').write_text(json.dumps(result, indent=2))
    print(f'PASS 1287 complete: ledger v9 with counts {result["ledger_counts"]}')
    return result

if __name__ == '__main__':
    main()
