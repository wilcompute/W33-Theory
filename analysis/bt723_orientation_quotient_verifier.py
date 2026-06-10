#!/usr/bin/env python3
"""BT723: executable check of the BT720 orientation quotient."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RANKS = json.loads((ROOT/'data/PART_BT713_SELECTOR_SHEET_RANK_FILTER_results.json').read_text())['sheet_ranks']
TYPE_A = ['1110','1101','1011','0111']
CHANNELS = {'011':'r0','101':'r1','110':'r2'}

hits = {}
for mask in TYPE_A:
    for fano, r in CHANNELS.items():
        key = f'{mask}_{r}'
        rank = RANKS[key]
        assert rank == 81, (key, rank)
        hits[f'{mask}_{fano}'] = rank

result = {
    'theorem': 'BT723 Orientation Quotient Verifier',
    'type_a_masks': TYPE_A,
    'fano_channels': list(CHANNELS),
    'admissible_sheet_count': len(hits),
    'all_admissible_ranks': sorted(set(hits.values())),
    'levi_e4_rank': 81,
    'verified_sheets': hits,
    'conclusion': 'Every Type-A mask times intrinsic Fano channel has rank 81, so the admissible orientation quotient lands in Levi E4.'
}
print(json.dumps(result, indent=2, sort_keys=True))
