import sys, json, itertools
from collections import Counter
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import yuk as Y, hyper as H
from collections import defaultdict
res = {}
for m in sys.argv[1:]:
    fac, u1, fields = Y.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0]
    L = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)['L']
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    hset = defaultdict(list)
    for s in scal:
        for w in s['W']:
            hset[w].append(s)
    dc = lambda f: H.dsgn(f['dim'][col])
    dl = lambda f: int(f['dim'][L])
    # chiral Q: the (3,2) fields that come in a triple with 3 RM weights (three planes); vector-like: the rest
    q32 = [f for f in left if abs(dc(f)) == 3 and dl(f) == 2]
    chiral = [f for f in q32 if len(f['R']) == 3]
    stats = Counter()
    for A in chiral:
        for B in left:
            if not (abs(dc(B)) == 3 and dl(B) == 1):
                continue
            seen = set()
            for wa in A['W']:
                for wb in B['W']:
                    for S in hset.get(tuple(-(x + z) for x, z in zip(wa, wb)), []):
                        if S['i'] in seen or not (dc(S) == 1 and dl(S) == 2):
                            continue
                        seen.add(S['i'])
                        stats['gauge'] += 1
                        sg = Y.sg_ok([A, B, S])
                        hm = Y.hm_ok([A, B, S], [False] * 3)
                        stats['gauge+sg'] += sg
                        stats['gauge+hm'] += hm
                        stats['all'] += sg and hm
                        stats['secs ' + '/'.join(str((f['n'], f['mm'])) for f in (A, B, S))] += 1
    res[m] = dict(n_chiral_Q_fields=len(chiral), n_q32=len(q32), stats=dict(stats))
    print(m, res[m], flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\yukrob_5' + ('_exact' if Y.EXACT else '') + '.json', 'w'), indent=1)
