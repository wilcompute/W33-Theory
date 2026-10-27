"""12274: the 3 consistent Z2xZ2 relabellings with B != 0 but an unchanged spectrum.  For each, the twisted sectors (Witten label e,
twist (a,b), fixed point) on which B != 0, compared with the sectors that carry massless fields in the engine dump.  Fixed-point labels
are reduced to the rotated directions of the twist (fixed-torus coordinates do not label fixed points)."""
import json, sys, collections, re
import numpy as np
sys.path.insert(0, '.')
from torsion_B import table, diff_relabel
R = '../search_drivers_12271/'
ROT = {(1, 0): [2, 3, 4, 5], (0, 1): [0, 1, 4, 5], (1, 1): [0, 1, 2, 3]}
TW = [(0, 0), (1, 0), (0, 1), (1, 1)]


def hit_sectors(r0, S, lam):
    blocks, _ = table(r0, 'Z2xZ2', S, lam)
    I = np.eye(6, dtype=np.int64)
    hit = set()
    for hb in blocks:
        if hb['ti'] == 0:
            continue
        tw = TW[hb['ti']]
        for gb in blocks:
            A = gb['labs'] @ (I - hb['M']).T; Bf = hb['labs'] @ (I - gb['M']).T
            keyA = collections.defaultdict(list)
            for k, row in enumerate(map(tuple, A)):
                keyA[row].append(k)
            for j, row in enumerate(map(tuple, Bf)):
                gi = keyA.get(row)
                if not gi:
                    continue
                num = (gb['sig'][np.array(gi)] * hb['VL'][j] - hb['sig'][j] * gb['VL'][np.array(gi)]) % 48
                if (num != 0).any():
                    fp = tuple(int(hb['labs'][j][d]) % 2 if d in ROT[tw] else 0 for d in range(6))
                    hit.add((hb['e'], tw, fp))
    return hit


def populated(nsoq):
    sect = collections.Counter()
    for l in open(nsoq):
        m = re.match(r'FIELD \d+ m=\S+ k=(\S+) mm=(\S+) n=(\S+) lat=(\S+)', l)
        if m:
            tw = (int(m.group(1)), int(m.group(3)))
            lat = [int(F.split('/')[0]) // int(F.split('/')[1]) for F in m.group(4).split(',')]
            fp = tuple(lat[d] % 2 if tw != (0, 0) and d in ROT[tw] else 0 for d in range(6))
            sect[(int(m.group(2)), tw, fp)] += 1
    return sect


if __name__ == '__main__':
    d = json.load(open('correlate.json'))
    out = {}
    for r in d['rows']:
        if not r['lab'].startswith('ctrl') or not r['nonzeroB']:
            continue
        i = int(r['lab'][4:7])
        r0, S, lam = diff_relabel(R + f'even/{i:03d}_s0.txt', R + f'relabel/{r["lab"]}.txt')
        hit = hit_sectors(r0, S, lam)
        pop = populated(R + f'even/{i:03d}_s0.nsoq')
        massless_hit = sum(pop[h] for h in hit)
        out[r['lab']] = dict(spectrum=r['spectrum'], torsion_sectors=len(hit), populated_torsion_sectors=sum(1 for h in hit if pop[h]),
                             massless_fields_in_torsion_sectors=massless_hit)
    tab = collections.Counter((v['spectrum'], v['massless_fields_in_torsion_sectors'] > 0) for v in out.values())
    print(tab)
    for k, v in out.items():
        if v['spectrum'] == 'identical':
            print(k, v)
    json.dump(dict(table={str(k): v for k, v in tab.items()}, rows=out), open('exceptions.json', 'w'), indent=1)
