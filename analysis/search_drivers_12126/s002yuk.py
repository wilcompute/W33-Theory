import sys, json
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import yuk as Y
m = 'N004_F1_03_S002'
fac, u1, fields = Y.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
byid = {f['i']: f for f in fields}
yk = json.load(open('yuk_5_exact.json'))[m]['quark']
lab = lambda f: tuple(int((f['lat'][2 * t] + f['lat'][2 * t + 1]) % 3) for t in range(3))
out = []
for q in yk:
    if q['Qy'] != '1/6':
        continue
    c, h = byid[q['c']], byid[q['H']]
    kind = 'up' if q['cy'][0] == '-2/3' else 'down'
    # U.T.Tbar: H weights equal minus (c weights + Q weight) for some pairing, and H is the T1 partner of the T2 field
    out.append(dict(kind=kind, c=q['c'], H=q['H'], c_fp=lab(c), H_fp=lab(h), c_sec=(c['n'], c['mm']), H_sec=(h['n'], h['mm']), Hm=h['m']))
for o in out:
    print(o)
up = {o['H'] for o in out if o['kind'] == 'up'}
dn = {o['H'] for o in out if o['kind'] == 'down'}
# are any up and down Higgs fields complex conjugates (negated weight sets)?
def wset(i):
    return frozenset(byid[i]['W'])
conj = [(a, b) for a in up for b in dn if wset(b) == frozenset(tuple(-x for x in w) for w in byid[a]['W'])]
print('up Higgs', sorted(up), 'down Higgs', sorted(dn), 'shared', up & dn, 'conjugate pairs', conj)
print('up fixed points', sorted({o['H_fp'] for o in out if o['kind'] == 'up'}), 'down', sorted({o['H_fp'] for o in out if o['kind'] == 'down'}))
json.dump(dict(couplings=out, up_higgs=sorted(up), down_higgs=sorted(dn), conjugate_pairs=conj), open('s002yuk.json', 'w'), indent=1, default=str)
