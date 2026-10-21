"""12166: proton decay through colour-triplet scalars in the survivors whose single-scale threshold fit works (2, 15, 77): for every
colour-triplet scalar component, does it couple (trilinear, all rules, exact H-momentum) both to a diquark (QQ, u^c d^c) and to a
quark-lepton pair (QL, u^c e^c)? Corpus hypercharge (nsosm)."""
import sys
import os
import json
import itertools
from fractions import Fraction as Fr
from collections import defaultdict
sys.path.insert(0, r'C:\tmp\toe_round\stype')
os.environ['EXACT'] = '1'
import hyper as H
import yuk as Y
import a8down as A
import a8ff


def run(lab):
    base = r'C:\tmp\toe_round\stype\a8\%s' % lab
    fac, u1, fields = Y.parse(base + '.q')
    y = A.ydir(base + '.sm')
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    c, l = a8ff.slots(fac, left, y)
    dc = lambda f: H.dsgn(f['dim'][c])  # noqa: E731
    best = None
    for cq in (3, -3):
        for yq in (Fr(1, 6), Fr(-1, 6)):
            net = sum((1 if (dc(f) == cq and H.dot(y, w) == yq) else -1 if (dc(f) == -cq and H.dot(y, w) == -yq) else 0)
                      for f in left if f['dim'][l] == '2' for w in f['W']) // 6
            if best is None or net > best[0]:
                best = (net, cq, yq)
    _, cq, yq = best

    def comps(fs, want_dc, want_dl, want_Y):
        out = []
        for f in fs:
            if dc(f) != want_dc or f['dim'][l] != str(want_dl):
                continue
            g = defaultdict(list)
            for w in f['W']:
                g[H.dot(y, w)].append(w)
            for yy, ws in g.items():
                if yy == want_Y:
                    out.append((f, ws))
        return out
    S = {'Q': comps(left, cq, 2, yq), 'u': comps(left, -cq, 1, -4 * yq), 'd': comps(left, -cq, 1, 2 * yq),
         'L': comps(left, 1, 2, -3 * yq), 'e': comps(left, 1, 1, 6 * yq)}
    trip = []
    for s in scal:
        if abs(dc(s)) == 3 and s['dim'][l] == '1':
            g = defaultdict(list)
            for w in s['W']:
                g[H.dot(y, w)].append(w)
            for yy, ws in g.items():
                trip.append((s, ws, yy))

    def allowed(A1, B1, T):
        for wa in A1[1]:
            for wb in B1[1]:
                for wt in T[1]:
                    if all(x + z + t == 0 for x, z, t in zip(wa, wb, wt)):
                        fs = [A1[0], B1[0], T[0]]
                        if Y.sg_ok(fs) and Y.hm_ok(fs, [False] * 3):
                            return True
        return False
    res = []
    for T in trip:
        dq = any(allowed(a, b, T) for x, z in (('Q', 'Q'), ('u', 'd')) for a, b in itertools.combinations_with_replacement(S[x], 2) if x == z) \
            or any(allowed(a, b, T) for a in S['u'] for b in S['d'])
        lq = any(allowed(a, b, T) for a in S['Q'] for b in S['L']) or any(allowed(a, b, T) for a in S['u'] for b in S['e'])
        res.append(dict(field=T[0]['i'], Y=str(T[2]), diquark=dq, leptoquark=lq))
    return dict(n_triplet_components=len(res), diquark=sum(r['diquark'] for r in res), leptoquark=sum(r['leptoquark'] for r in res),
                both=sum(r['diquark'] and r['leptoquark'] for r in res), detail=res)


if __name__ == '__main__':
    labs = json.load(open(r'C:\tmp\toe_wt\data\w33_pass11106_survivor_shifts.json'))['models']
    out = {}
    for k in ('2', '15', '77'):
        out[k] = run(labs[k]['label'])
        print(k, labs[k]['label'], {kk: v for kk, v in out[k].items() if kk != 'detail'}, flush=True)
    json.dump(out, open(r'C:\tmp\toe_round\stype\protonT.json', 'w'), indent=1, default=str)
    print('DONE')
