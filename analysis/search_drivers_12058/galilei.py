"""Structure of the clock stabiliser H (order 432) modulo its centre <-1> x <t_p>: is it 3^2 : Q8 (affine plane + spin)?"""
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402

Adj, invs, tick, fib = setup()
G = sp43_from_ticks(tick)
cl = next(s for k, s in invs if k == 'clock')
even = [x for x in range(40) if not cl[fib[x]].any()]
p = next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(even))
H = [h.astype(np.int64) for h in G[np.all(cl[G] == cl[None, :], axis=1)]]
print('|H| =', len(H), ' centre point p =', p)
idn = np.arange(240)
key = lambda g: g.astype(np.int16).tobytes()  # noqa: E731
mul = lambda a, b: a[b]  # noqa: E731  (apply b then a)
Hset = {key(h): h for h in H}
cen = [h for h in H if all(np.array_equal(h[g], g[h]) for g in H)]
Z = {key(z) for z in cen}
print('|Z| =', len(Z))
# point action
pt_of = np.empty(240, int)
for q, f in enumerate(fib):
    pt_of[f] = q
def on_points(h):
    return pt_of[h[[f[0] for f in fib]]]
# orbits of H on the 40 points
orbits, seen = [], set()
for q in range(40):
    if q in seen:
        continue
    orb = {int(on_points(h)[q]) for h in H}
    seen |= orb
    orbits.append(sorted(orb))
print('orbits on points:', [len(o) for o in orbits])
nb = set(np.nonzero(Adj[p])[0])
for o in orbits:
    print('   size %2d: collinear with p? %s' % (len(o), {('p' if x == p else ('nb' if x in nb else 'far')) for x in o}))
# quotient H/Z: cosets
cos, cmap = [], {}
for h in H:
    k = key(h)
    if k in cmap:
        continue
    idx = len(cos)
    cos.append(h)
    for z in cen:
        cmap[key(h[z])] = idx
print('|H/Z| =', len(cos))
def order_mod_Z(h):
    g, n = h.copy(), 1
    while key(g) not in Z:
        g = g[h]; n += 1
    return n
ords = Counter(order_mod_Z(h) for h in cos)
print('element orders in H/Z:', dict(sorted(ords.items())))
# normal subgroup of order 9 in H/Z: elements of order 3 (mod Z) together with identity
o3 = [h for h in cos if order_mod_Z(h) == 3]
print('elements of order 3 in H/Z:', len(o3))
# Sylow-2 of H/Z: orders 2,4,8 count -> Q8 has 1 involution and 6 of order 4
print('order-2 elements:', ords.get(2, 0), ' order-4:', ords.get(4, 0), ' order-8:', ords.get(8, 0))
# kernel of the action on the far orbit / nb orbit
for o in orbits:
    ker = [h for h in H if all(on_points(h)[x] == x for x in o)]
    print('   kernel of action on orbit of size %d has order %d' % (len(o), len(ker)))
