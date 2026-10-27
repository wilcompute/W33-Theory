"""12283: the three consistent Z2xZ2 relabellings with B != 0 and an unchanged multiplet table (12274).  Compare the full state
content -- for every field its sector, fixed point, left-moving weight(s) W and right-moving weights R -- between the model and its
relabelling.  Charges/representations equal but states different would mean the torsion sign swaps physically distinct states with
identical quantum numbers; fully equal states would mean the sign acts trivially on the massless level."""
import re, collections, json, sys
R = '../search_drivers_12271/'
def states(p):
    out = collections.Counter(); cur = None; rs = []; ws = []
    def flush():
        if cur is not None:
            out[(cur, tuple(sorted(rs)), tuple(sorted(ws)))] += 1
    for l in open(p):
        if l.startswith('FIELD'):
            flush()
            m = re.match(r'FIELD \d+ (m=\S+ k=\S+ mm=\S+ n=\S+ lat=\S+ dim=\S*)', l)
            cur = m.group(1); rs = []; ws = []
        elif l.startswith('R ') and cur:
            rs.append(l.strip())
        elif l.startswith('W ') and cur:
            ws.append(l.strip())
    flush()
    return out
res = {}
for lab, src in (('ctrl005_r0', 5), ('ctrl024_r0', 24), ('ctrl039_r1', 39)):
    a = states(R + f'even/{src:03d}_s0.nsoq'); b = states(R + f'relabel/{lab}.nsoq')
    d1, d2 = a - b, b - a
    res[lab] = dict(fields=sum(a.values()), differing_states=sum(d1.values()))
    print(lab, 'fields', sum(a.values()), 'states only in model', sum(d1.values()), 'only in relabelling', sum(d2.values()))
    for k in list(d1)[:2]:
        print('  <', k[0], k[1][:2], k[2][:1])
    for k in list(d2)[:2]:
        print('  >', k[0], k[1][:2], k[2][:1])
json.dump(res, open('states.json', 'w'), indent=1)
