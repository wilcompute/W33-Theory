"""control: at cap = 0 the MILP must agree, triple by triple, with 12354's independent coupling_ok (HNF translation test) on every
(Q-like, T-like, Higgs, Higgs orientation) triple of SM_2913_v6."""
import sys, os, json, itertools
sys.path.insert(0, '.')
from mono import FS, min_degree, smsing, I3, I2
os.chdir('../search_drivers_12354')
src = open('yukawa.py').read().split('import networkx')[0]
exec(src)
os.chdir('../search_drivers_12357')
byid = {f['id']: f for f in FS}
agree = dis = pos = 0
for name, ka, kb in (('up', ('Q', sp.Rational(-1, 6)), ('T', sp.Rational(-2, 3))), ('down', ('Q', sp.Rational(-1, 6)), ('T', sp.Rational(1, 3))),
                     ('lepton', ('L', sp.Rational(1, 2)), ('S', -1))):
    for a in groups.get(ka, []):
        for b in groups.get(kb, []):
            for h in [x for x in H if x['m'] == 15]:
                for sh in (1, -1):
                    ref = False
                    if all(x + y + sh * z == 0 for x, y, z in zip(a['q'], b['q'], h['q'])) and a['y'] + b['y'] + sh * h['y'] == 0:
                        nsum = a['n'] + b['n'] + sh * h['n']; wsum = a['w'] + b['w'] + sh * h['w']
                        if not (nsum % 6 or wsum % 2):
                            lat = [a['lat'][i] + b['lat'][i] + sh * h['lat'][i] for i in range(6)]
                            sectors = sorted({k % 6 for k in (a['n'], b['n'], h['n']) if k % 6} | {(6 - k) % 6 for k in (a['n'], b['n'], h['n']) if k % 6})
                            ref = in_translation_lattice(lat, sectors)
                    r = min_degree([(byid[a['id']] if 'id' in a else a, 1), (b, 1), (h, sh)], cap=0) if False else None
                    A_, B_, H_ = [next(f for f in FS if f['m'] == g['m'] and f['n'] == g['n'] and f['lat'] == g['lat'] and f['P'] == g['P']) for g in (a, b, h)]
                    got = min_degree([(A_, 1), (B_, 1), (H_, sh)], cap=0) is not None
                    pos += ref; agree += (ref == got); dis += (ref != got)
print(dict(agree=agree, disagree=dis, positives=pos))
json.dump(dict(agree=agree, disagree=dis, positives=pos), open('control.json', 'w'))
