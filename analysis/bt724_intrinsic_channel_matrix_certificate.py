#!/usr/bin/env python3
"""BT724: intrinsic Fano-channel selector matrix certificate.

This certificate records the three channel sheets for the selected hinge mask 1110.
The full signed row construction is BT713; here we assert and package the channel
comparison in intrinsic Fano labels.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rank_data = json.loads((ROOT/'data/PART_BT713_SELECTOR_SHEET_RANK_FILTER_results.json').read_text())
ranks = rank_data['sheet_ranks']
channels = {'011/far':'r0','101/middle':'r1','110/active':'r2'}
mask = '1110'
certificate = {}
for label, r in channels.items():
    key = f'{mask}_{r}'
    rank = ranks[key]
    assert rank == 81
    certificate[label] = {'sheet': key, 'rank': rank, 'levi_e4_rank': 81}

assert rank_data['mask_bundle_ranks'][mask] == 81
result = {
    'theorem': 'BT724 Intrinsic Channel Matrix Certificate',
    'mask': mask,
    'intrinsic_channels': certificate,
    'bundle_rank': rank_data['mask_bundle_ranks'][mask],
    'all_three_channels_rank_81': True,
    'rowspace_statement': 'Each intrinsic channel selector is individually rank 81 and therefore spans the Levi E4/H1 cycle sector.',
    'boundary': 'This certificate compares ranks and the common E4 target using the BT713 matrix construction; it does not dump the 2160 sparse signed rows into the repository.'
}
print(json.dumps(result, indent=2, sort_keys=True))
