"""12281: chirality proxy for control vs W6-odd brother -- net (left - right) fermion multiplicity per non-abelian representation
(sector-summed), and the largest net multiplicity of a doublet-triplet bifundamental-type rep (both an SU(3)-type '3' and an
SU(2)-type '2' entry), i.e. a quark-doublet proxy.  12180 predicts at most 2 for the Scherk-Schwarz endpoint."""
import re, json, collections, os
def net(p):
    c = collections.Counter()
    for l in open(p):
        m = re.match(r'FIELD \d+ m=(19|20) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) ', l)
        if m:
            c[m.group(2)] += 1 if m.group(1) == '19' else -1
    return c
def qproxy(c):
    best = 0
    for d, v in c.items():
        parts = [x.lstrip('-') for x in d.split(',') if x]
        if '3' in parts and '2' in parts:
            best = max(best, abs(v))
    return best
idx = json.load(open('census_index.json'))
done = lambda p: os.path.exists(p) and open(p, errors='ignore').read().rstrip().endswith('END')
tab = collections.Counter(); rows = []
for e in idx:
    a, b = e['files']['ctrl'][:-4] + '.nsoq', e['files'].get('w6odd', 'x')[:-4] + '.nsoq'
    if not (done(a) and done(b)):
        continue
    qa, qb = qproxy(net(a)), qproxy(net(b))
    tab[(qa, qb)] += 1
    rows.append(dict(model=e['model'], ctrl_q=qa, w6odd_q=qb))
print(sorted(tab.items()))
json.dump(dict(table={str(k): v for k, v in tab.items()}, rows=rows), open('chirality.json', 'w'), indent=1)
