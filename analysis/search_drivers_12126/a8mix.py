import glob, os, re, json
from fractions import Fraction as Fr
from collections import Counter
res = {}
for fn in sorted(glob.glob(r'C:\tmp\toe_round\stype\a8\*.sm')):
    t = open(fn).read()
    facs = re.findall(r'^FACTOR (\d+) (\w+)', t, re.M)
    a2 = [int(i) for i, n in facs if n == 'A2']
    a1 = [int(i) for i, n in facs if n == 'A1']
    raw = [(m.group(1), m.group(2).split(','), [float(x) for x in m.group(3).split(',')]) for m in re.finditer(r'^L (\S+) dim=(\S+) q=(\S+)', t, re.M)]
    qf = [r for r in raw if r[0] == 'q']
    yi = next(i for i in range(len(qf[0][2])) if all(abs(abs(r[2][i]) - 1 / 6) < 1e-9 for r in qf))
    L = [(lab, dims, Fr(qs[yi]).limit_denominator(36)) for lab, dims, qs in raw]
    # colour slot: the A2 whose (3,2)-type states carry Y = +-1/6; doublet slot: the A1 paired with it
    best = None
    for c in a2:
        for l in a1:
            cnt = Counter()
            for lab, dims, Y in L:
                dc = int(dims[c]); dl = int(dims[l])
                if abs(dc) in (1, 3):
                    rest = 1
                    for k, e in enumerate(dims):
                        if k not in (c, l):
                            rest *= abs(int(re.match(r'-?\d+', e).group(0)))
                    cnt[(dc, dl, Y)] += rest
            q = max(cnt.get((3, 2, Fr(1, 6)), 0) - cnt.get((-3, 2, Fr(-1, 6)), 0), cnt.get((-3, 2, Fr(1, 6)), 0) - cnt.get((3, 2, Fr(-1, 6)), 0), key=abs)
            if best is None or abs(q) > abs(best[0]):
                best = (q, cnt)
    q, cnt = best
    vl = {}
    for name, key in (('Q', (3, 2, Fr(1, 6))), ('u', (-3, 1, Fr(-2, 3))), ('d', (-3, 1, Fr(1, 3))), ('Q', (-3, 2, Fr(1, 6))), ('u', (3, 1, Fr(-2, 3))), ('d', (3, 1, Fr(1, 3)))):
        conj = (-key[0], key[1], -key[2])
        n, nb = cnt.get(key, 0), cnt.get(conj, 0)
        if n or nb:
            vl[name] = max(vl.get(name, 0), min(n, nb))
    other32 = sorted({str(Y) for (dc, dl, Y) in cnt if abs(dc) == 3 and dl == 2 and abs(Y) != Fr(1, 6)})
    res[os.path.basename(fn)[:-3]] = dict(netQ=q, vectorlike=vl, other_doublet_Y=other32)
print(len(res), 'netQ', Counter(abs(v['netQ']) for v in res.values()))
print('vector-like Q (Y=1/6) pairs:', Counter(v['vectorlike'].get('Q', 0) for v in res.values()))
print('vector-like u pairs:', Counter(v['vectorlike'].get('u', 0) for v in res.values()))
print('vector-like d pairs:', Counter(v['vectorlike'].get('d', 0) for v in res.values()))
print('other colour-triplet doublet Y:', Counter(tuple(v['other_doublet_Y']) for v in res.values()))
json.dump(res, open(r'C:\tmp\toe_round\stype\a8mix.json', 'w'), indent=1, default=str)
