"""12261: existence counts restated on the Ploger-consistent sets (all of (7a)-(7f)).  SU(5) x U(1) scans of 12161-12182 (flipscan2 JSONs)
and the twisted-10 models of 12217/12223: models, three-generation models, scalar 10s."""
import json, os
from collections import Counter
exec(open('ploger.py').read().split('sets = {')[0])
out = {}
for name, path in (('12163_third_torus', '../search_drivers_12162/flipscan2_21_third.json'),
                   ('12182_third_torus', '../search_drivers_12180/flipscan2_31_third.json')):
    js = [r for r in json.load(open(path)) if 'net10' in r]
    c = Counter()
    for r in js:
        f = r'C:\tmp\toe_round\stype\flipscan2\%s.txt' % r['label']
        ok = os.path.exists(f) and not check(rows(open(f).read()))[0]
        c['models'] += 1; c['consistent'] += ok
        c['three_gen'] += abs(r['net10']) == 3; c['three_gen_consistent'] += ok and abs(r['net10']) == 3
        c['scalar10'] += r['scalar10']
    out[name] = dict(c)
    print(name, dict(c))
g = json.load(open('../search_drivers_12223/gens153.json'))
pm = json.load(open('ploger_per_model.json'))['twisted10_C10_loaded']
c = Counter()
for x in g:
    ok = not pm[x['label'] + '.txt']
    c['models'] += 1; c['consistent'] += ok
    c['three_gen_consistent'] += ok and abs(x['net10']) == 3
    c['six_gen_consistent'] += ok and abs(x['net10']) == 6
out['12223_twisted10'] = dict(c)
print('12223_twisted10', dict(c))
json.dump(out, open('restate.json', 'w'), indent=1)
