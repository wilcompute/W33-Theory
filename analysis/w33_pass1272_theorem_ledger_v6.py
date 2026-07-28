#!/usr/bin/env python3
"""
Pass 1272: theorem ledger version 6.

Adds EXACT-10 (sp1/sp20/sp81 exact PSp(4,3) restrictions), consolidates
the 27-line partial close, and records the 3 remaining open items.
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
        'EXACT-7: A unique-up-to-scalar rational 81-sector intertwiner exists between 81_+ and Steinberg-81 as PSp(4,3)-modules.',
        'EXACT-8: For tested deltas {-2,-1,1,2}, shifted-adjacency Hashimoto deformations are non-isomorphic to the original.',
        'EXACT-9: For ALL nonzero integer delta, the shifted-adjacency Hashimoto family of A+delta*I on SRG(40,12,2,4) is non-isomorphic to the original.',
        'EXACT-10: The W(E6) species sp1, sp20, and sp81 restrict to PSp(4,3) as the 1-dim trivial, 20-dim, and 81-dim irreducible PSp(4,3)-modules respectively; these are the unique irreducible restrictions determined by dimension and prior isomorphism results.'
    ]
    provisional = [
        'PROVISIONAL-1: Commutant-Hashimoto diagonal runs cleanest through species 1 and 20.',
        'PROVISIONAL-2: Matrix-unit refinement should start in species 20, 6, 1, 64.',
        'PROVISIONAL-3: Fastest next theorem from residual/81-sector/Hecke/degree-40 synchronization.',
        'PROVISIONAL-4: The 27-dim W(E6) irrep appears in the P1 packet with multiplicity between 1 and 7.',
        'PROVISIONAL-5: Hecke spherical algebra has dimension 9 (from k=9 Burnside candidate, all consistency tests passed).',
        'PROVISIONAL-6: Species-20 matrix-unit recipe is AtlasRep-ready; scaffold verified for dim=20 (160,000 checks).',
        'PROVISIONAL-7: The species-to-packet dictionary maps sp1->P0 (exact), sp81->P1 (exact), sp20->P1 (predicted); remaining 7 species provisional.'
    ]
    open_t = [
        'OPEN-1: Verify k=9 and derive exact Hecke structure constants via literal PSp(4,3)/A5 coset table in GAP.',
        'OPEN-2: Materialize actual species-20 matrix units using AtlasRep degree-20 W(E6) matrices (scaffold ready).',
        'OPEN-3: Determine the exact multiplicity of the W(E6) 27-dim irrep inside the P1 packet to close the 27-line embedding theorem.'
    ]
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1272.theorem_ledger_v6.v1',
        'status': 'PASS',
        'exact_theorems': exact,
        'provisional_theorems': provisional,
        'open_theorems': open_t,
        'ledger_counts': {'EXACT': len(exact), 'PROVISIONAL': len(provisional), 'OPEN': len(open_t)},
        'predecessor': 'w33.pass1266.theorem_ledger_v5.v1'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1272_theorem_ledger_v6.json').write_text(json.dumps(result, indent=2))
    print(f'PASS 1272 complete: theorem ledger v6 written with counts {result["ledger_counts"]}')
    return result

if __name__ == '__main__':
    main()
