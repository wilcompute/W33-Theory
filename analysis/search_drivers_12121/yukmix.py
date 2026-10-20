import sys, json, itertools
from collections import Counter, defaultdict
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import yuk as Y, hyper as H
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
    chiral = [f for f in left if abs(dc(f)) == 3 and dl(f) == 2 and len(f['R']) == 3]
    st = Counter()
    for A in chiral:
        for B in left:
            if B is A:
                pass
            seen = set()
            for wa in A['W']:
                for wb in B['W']:
                    for S in hset.get(tuple(-(x + z) for x, z in zip(wa, wb)), []):
                        if (B['i'], S['i']) in seen:
                            continue
                        seen.add((B['i'], S['i']))
                        kind = 'B(%s,%s)%s S(%s,%s)' % (dc(B), dl(B), 'chiralQ' if B in chiral else '', dc(S), dl(S))
                        st['gauge ' + kind] += 1
                        if Y.sg_ok([A, B, S]) and Y.hm_ok([A, B, S], [False] * 3):
                            st['ALLOWED ' + kind + ' secB=%d,%d secS=%d,%d' % (B['n'], B['mm'], S['n'], S['mm'])] += 1
    res[m] = dict(st)
    print(m, json.dumps(res[m], indent=0), flush=True)
json.dump(res, open(r'C:\tmp\toe_round\stype\yukmix_5' + ('_exact' if Y.EXACT else '') + '.json', 'w'), indent=1)
