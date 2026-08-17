#!/usr/bin/env python3
"""Pass5703: W(3,9) reconstruction with explicit rediscovery correction.

Pass5226--5227 already owns the W(3,9) construction, a randomized-greedy
baseline of 46, a stronger independent-set witness of size 50, and the Hoffman
upper bound 82.  The former Pass5703 prose incorrectly advertised unsupported
bounds 51 <= alpha <= 80 and reclaimed the baseline 46.

This corrected producer only rebuilds the graph independently over
F_9 = F_3[a]/(a^2+1), verifies SRG(820,90,8,10), and checks the prior owner's
frozen 50 <= alpha(W(3,9)) <= 82 boundary.  It performs no time-dependent search
and claims no new independence result.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'data/PART_W33_PASS5703_W39_INDEPENDENCE_REPLICATION.json'
OWNER = ROOT/'data/PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json'

def f9mul(x, y): return ((x[0]*y[0]-x[1]*y[1]) % 3, (x[0]*y[1]+x[1]*y[0]) % 3)
def f9add(x, y): return ((x[0]+y[0]) % 3, (x[1]+y[1]) % 3)
F9all = [(i, j) for i in range(3) for j in range(3)]
F9m = [x for x in F9all if x != (0, 0)]
def f9inv(x):
    for y in F9m:
        if f9mul(x, y) == (1, 0): return y
F9I = {x: f9inv(x) for x in F9m}
vec9 = [v for v in itertools.product(F9all, repeat=4) if v != ((0,0),)*4]
def canon9(v):
    for x in v:
        if x != (0, 0):
            s = F9I[x]
            return tuple(f9mul(xi, s) for xi in v)
pts9 = sorted(set(canon9(v) for v in vec9))
N = len(pts9); assert N == 820
def omega9(u, v):
    acc = (0, 0)
    for a, b in ((0, 2), (1, 3)):
        acc = f9add(acc, f9add(f9mul(u[a], v[b]), tuple((-x) % 3 for x in f9mul(u[b], v[a]))))
    return acc

def main():
    adj = [set() for _ in range(N)]
    for i in range(N):
        ui = pts9[i]
        for j in range(i+1, N):
            if omega9(ui, pts9[j]) == (0, 0):
                adj[i].add(j); adj[j].add(i)
    assert set(len(a) for a in adj) == {90}
    adjacent_common = {len(adj[i] & adj[j])
                       for i in range(N) for j in range(i+1, N) if j in adj[i]}
    nonadjacent_common = {len(adj[i] & adj[j])
                          for i in range(N) for j in range(i+1, N) if j not in adj[i]}
    assert adjacent_common == {8}
    assert nonadjacent_common == {10}
    owner = json.loads(OWNER.read_text(encoding='utf-8'))
    q9 = next(row for row in owner['pass_5226']['rows'] if row['q'] == 9)
    assert q9['alpha_established'] == 50
    assert q9['hoffman'] == 82
    assert q9['bound_settled'] == 'lower only'
    out = {
      'pass': 5703,
      'status': 'REDISCOVERY_CORRECTED_TO_PASS5226_5227_PRIOR_OWNERSHIP',
      'graph': {'field': 'F_9 = F_3[a]/(a^2+1)', 'points_PG39': 820,
                'srg': [820, 90, 8, 10]},
      'prior_owner': {'file': 'data/PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json',
                      'randomized_greedy_baseline': q9['restart_greedy'],
                      'certified_lower_witness': q9['alpha_established'],
                      'hoffman_upper_bound': q9['hoffman']},
      'repo_bounds': {'lower_witness': 50, 'upper_hoffman': 82,
                      'exact_alpha_settled': False},
      'legacy_claim_withdrawn': ('The former 51 <= alpha <= 80 claim had no cited certificate, and the '
                                 'reported baseline 46 was already present in Pass5226--5227.'),
      'verdict': 'Independent graph reconstruction only; no new independence-number result.',
      'physics_boundary': 'Pure finite combinatorial reconstruction; no optimization or physics claim.'
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps(out, indent=2, sort_keys=True))
if __name__ == '__main__': main()
