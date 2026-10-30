# V20 — Sparsity-aware exact δL5 on candidate sextuples, full l6 table, and δL6 probe

Now that l5 is effectively complete on g1^5 (V19), we enumerate δL5 exactly on the induced candidate sextuples and build a full l6 patch. We then probe δL6 on random g1^7.

## Candidate sextuples
- l5 quintuples: 85429
- unique candidate sextuples generated (contain an l5 quint): 5635865
Sanity: tested 49,118 non-candidate sextuples (no l5 5-subtuple) and saw 0 δL5 violations.

## Exact δL5 on candidates
- time: 23.41s
- stats: {'nonzero': 777495, 'single': 777495, 'zero': 4858370}
- all nonzero δL5 were single-term: termcount={1: 777495}
- nonzero rate on candidates: 0.137955
- l6 table size: 777495 (JSONL)
- l6 output support size: 234

## δL6 sample (using full l6)
- sampled 7-tuples: 500000
- δL6 stats: {'zero': 499037, 'nonzero': 963, 'single': 963}
- nonzero rate: 0.00192600
- all nonzero δL6 were single-term: termcount={1: 963}

