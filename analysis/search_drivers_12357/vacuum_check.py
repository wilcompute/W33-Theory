"""12360 verification from scratch (no cache): the 6-singlet set gives full structural rank in every block, and removing any one of
the six breaks some block (minimality); random control: 6 random singlets drawn from the same 80 (100 draws) -- how often do they suffice?"""
import sys, json, random
sys.path.insert(0, '.')
from vacuum import all_edges, rank_ok, NS
vac = json.load(open('vacuum.json'))['vacuum']
def full(allowed):
    ok = rank_ok(all_edges(allowed)); return all(a >= b for a, b in ok.values()), ok
mask = [s in vac for s in range(NS)]
f0, ok0 = full(mask); print('fresh check', f0, ok0)
drop = {}
for s in vac:
    m = list(mask); m[s] = False; f, ok = full(m); drop[s] = dict(full=f, broken=[k for k, (a, b) in ok.items() if a < b])
print('drop one:', drop)
random.seed(7); hits = 0; N = 100
for _ in range(N):
    r = random.sample(range(NS), 6); hits += full([s in r for s in range(NS)])[0]
print('random 6-sets that suffice:', hits, '/', N)
json.dump(dict(fresh=f0, drop_one=drop, random_hits=hits, random_draws=N), open('vacuum_check.json', 'w'), indent=1)
