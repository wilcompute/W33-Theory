"""12460b: does |N y| >= 2q persist beyond k = q + 1 lines?  Exhaustive over all k-subsets of the 40 lines of W(3,3) for k = 5, 6
(658,008 and 3,838,380 subsets), bitmask arithmetic.  The proved range is 2 <= k <= q + 1 (k-line lemma + the no-triangle step)."""
import json, itertools, sys
import numpy as np
exec(open('kline_profile.py', encoding='utf-8').read().split('# kernel basis')[0])
masks = [sum(1 << p for p in L) for L in lines]
out = {}
for k in (5, 6):
    mn = 10 ** 9; cnt = 0
    for Y in itertools.combinations(range(m), k):
        x = 0
        for j in Y: x ^= masks[j]
        w = bin(x).count('1')
        if w < mn: mn = w; cnt = 0
        if w == mn: cnt += 1
    out[k] = dict(min_weight=mn, count_at_min=cnt)
    print(k, out[k], flush=True)
json.dump(out, open('kline_extend_q3.json', 'w'), indent=1)
