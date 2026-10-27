"""12282: are the 12 new Z2xZ6-I SM brothers different from their parents independently of the SM identification?  specdump labels
(q, u, d, ...) and hypercharge depend on which SM embedding the analysis picks; the multiset of (sector k, multiplet type, non-abelian
representation) does not.  Compare that multiset, and the gauge group (number of U(1)s)."""
import json, re, collections
def reps(p):
    c = collections.Counter(); nu1 = None
    for l in open(p):
        if l.startswith('NU1 '):
            nu1 = int(l.split()[1])
        m = re.match(r'S \S+ k=(\S+) susy=(\S+) dim=(\S*) ', l)
        if m:
            c[(m.group(1), m.group(2), m.group(3))] += 1
    return c, nu1
new = json.load(open('new_sm.json')); idx = {e['model']: e for e in json.load(open('index.json'))}
res = {}
for n in new:
    e = idx[n['model']]
    a, na = reps(e['files']['ctrl'][:-4] + '.sd'); b, nb = reps(e['files']['odd'][:-4] + '.sd')
    res[n['model']] = dict(identification_independent_difference=a != b, fields=(sum(a.values()), sum(b.values())), NU1=(na, nb),
                           only_parent=sum((a - b).values()), only_brother=sum((b - a).values()))
    print(n['model'], res[n['model']])
json.dump(res, open('robust.json', 'w'), indent=1)
print(sum(v['identification_independent_difference'] for v in res.values()), 'of', len(res))
