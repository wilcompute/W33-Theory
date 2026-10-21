import sys, json
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H
lat = json.load(open('latff_control.json'))
out = {}
for m in ['N008_F1_03_S033', 'N008_F1_02_S053', 'N008_F1_04_S037_T115', 'N004_F1_03_S002']:
    fac, u1, fields = H.parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col, L = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0], r['L']
    aL = fac[L][1][0]
    roots = [rt for _, rts in fac for rt in rts]
    allf = [f for f in fields if f['m'] in (19, 15, 16)]
    latset = {tuple(Fr(x) for x in y) for y in lat[m]['ys']}
    strict_ff = strict_comm = strict_comm_in_lat = 0
    for s in r['sols']:
        if not H.is_sm(s['net']):
            continue
        y = s['y']
        if any((abs(H.dsgn(f['dim'][col])) == 1 and (H.dot(aL, w) / 2 + H.dot(y, w)).denominator != 1)
               or (abs(H.dsgn(f['dim'][col])) == 3 and ((3 * (H.dot(aL, w) / 2 + H.dot(y, w))).denominator != 1 or (H.dot(aL, w) / 2 + H.dot(y, w)).denominator == 1))
               for f in allf for w in f['W']):
            continue
        strict_ff += 1
        if all(H.dot(y, rt) == 0 for rt in roots):
            strict_comm += 1
            strict_comm_in_lat += tuple(y) in latset or tuple(-v for v in y) in latset
    out[m] = dict(strict_fraction_free=strict_ff, strict_commuting=strict_comm, strict_commuting_found_by_lattice=strict_comm_in_lat, lattice=lat[m]['n'])
    print(m, out[m], flush=True)
json.dump(out, open('latctrl.json', 'w'), indent=1)
