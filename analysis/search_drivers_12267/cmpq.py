"""12267: compare two nsoq dumps field by field: gauge factors, U(1) directions and the multiset of (multiplet, sector, fixed point,
dimensions, U(1) charges)."""
import sys, re, collections
def load(p):
    t = open(p).read().split('\n')
    head = [l for l in t if l.startswith(('GAUGE', 'FACTOR', 'U1 '))]
    fields = collections.Counter()
    for l in t:
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ (m=\S+ k=\S+ mm=\S+ n=\S+ lat=\S+ dim=\S+ q=\S+)', l)
            fields[m.group(1)] += 1
    return head, fields
h1, f1 = load(sys.argv[1]); h2, f2 = load(sys.argv[2])
print('gauge/U1 header identical:', h1 == h2, len(h1))
print('fields', sum(f1.values()), sum(f2.values()), 'identical multiset:', f1 == f2)
d1, d2 = f1 - f2, f2 - f1
print('only in first', sum(d1.values()), 'only in second', sum(d2.values()))
for k in list(d1)[:5]: print(' <', k)
for k in list(d2)[:5]: print(' >', k)
