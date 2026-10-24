"""12267: compare, for every lenient-only model, the stock engine's spectrum of the original input with the strict engine's spectrum of
each lattice-shift repair: gauge factors + U(1) directions, and the multiset of fields (multiplet, sector, fixed point, dimensions,
U(1) charges).  Also counts 10-type fields and bosons (m label) so a change in the physics content is visible."""
import json, re, collections, os
def load(p):
    if not os.path.exists(p):
        return None
    t = open(p, errors='ignore').read().split('\n')
    if any(l.startswith('LOADFAIL') for l in t):
        return 'LOADFAIL'
    rnd = lambda l: re.sub(r'-?\d+\.\d+(e-?\d+)?', lambda m: f'{round(float(m.group(0)), 9) + 0.0:.9f}', l)
    head = tuple(rnd(l) for l in t if l.startswith(('GAUGE', 'FACTOR', 'U1 ')))
    full = collections.Counter(); inv = collections.Counter()
    for l in t:
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ m=(\S+) k=(\S+) mm=(\S+) n=(\S+) lat=(\S+) dim=(\S*) q=(\S*)', l)
            if m is None:
                raise ValueError('unparsed FIELD line in ' + p + ': ' + l[:120])
            full[m.groups()] += 1
            inv[(m.group(1), m.group(3), m.group(4), m.group(6))] += 1
    return head, full, inv
def main():
  idx = json.load(open('census_index.json'))
  res = collections.Counter(); rows = []
  for i, rec in enumerate(idx):
      o = load(f'census/{i:04d}_o.nsoq')
      r = dict(name=rec['name'], shifts=[])
      for j, s in enumerate(rec['shifts']):
          x = load(f'census/{i:04d}_s{j}.nsoq')
          if o is None or x is None or o == 'LOADFAIL' or x == 'LOADFAIL':
              v = 'missing' if (o is None or x is None) else 'loadfail'
          elif o[0] == x[0] and o[1] == x[1]:
              v = 'identical'
          elif o[2] == x[2]:
              v = 'same sectors+dims, charges/basis differ'
          else:
              v = 'different spectrum'
          r['shifts'].append(dict(tori=s['tori'], verdict=v))
          res[(j, v)] += 1
      rows.append(r)
  pair = collections.Counter(tuple(s['verdict'] for s in r['shifts']) for r in rows)
  print(res); print(pair)
  json.dump(dict(summary={str(k): v for k, v in res.items()}, per_model=rows), open('census_compare.json', 'w'), indent=1)

if __name__ == '__main__':
    main()
