import sys
from collections import Counter

import numpy as np

sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402
import itertools

Adj, invs, tick, fib = setup()
G = sp43_from_ticks(tick)
cl = next(s for k, s in invs if k == 'clock')
even = [x for x in range(40) if not cl[fib[x]].any()]
p = next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(even))
H = [h.astype(np.int64) for h in G[np.all(cl[G] == cl[None, :], axis=1)]]
idn = np.arange(240)
key = lambda g: g.astype(np.int16).tobytes()  # noqa: E731
inv = lambda g: np.argsort(g)  # noqa: E731
def order(h):
    g, n = h.copy(), 1
    while not np.array_equal(g, idn):
        g = g[h]; n += 1
    return n
# Sylow-3 subgroup U: elements of 3-power order generate it; check it is the set of all elements of order 1,3,9
U = [h for h in H if order(h) in (1, 3, 9)]
print('elements of 3-power order:', len(U), Counter(order(h) for h in U))
Uk = {key(u) for u in U}
closed = all(key(a[b]) in Uk for a in U for b in U)
normal = all(key(g[u[inv(g)]]) in Uk for g in H for u in U[::3])
print('U closed:', closed, ' normal:', normal)
ZU = [u for u in U if all(np.array_equal(u[v], v[u]) for v in U)]
tp = tick[p].astype(np.int64)
tp_set = {key(idn), key(tp), key(tp[tp])}
print('|Z(U)| =', len(ZU), ' Z(U) = <t_p>:', {key(z) for z in ZU} == tp_set)
comms = {key(a[b[inv(a)[inv(b)]]]) for a in U for b in U}
print('[U,U] = <t_p>:', comms == tp_set)
# quotient H/U element orders
cos, seen = [], set()
for h in H:
    if key(h) in seen:
        continue
    cos.append(h)
    for u in U:
        seen.add(key(h[u]))
def order_mod(h, S):
    g, n = h.copy(), 1
    while key(g) not in S:
        g = g[h]; n += 1
    return n
print('|H/U| =', len(cos), ' element orders:', dict(sorted(Counter(order_mod(h, Uk) for h in cos).items())))
# commutator pairing on U/Z = F3^2: pick two generators u1,u2 of U/Z; commutator [a,b] = t_p^{c(a,b)}
reps = [u for u in U if key(u) not in tp_set]
u1 = reps[0]
u2 = next(u for u in reps if key(u1[u[inv(u1)[inv(u)]]]) != key(idn))
def coords(u):  # u = u1^i u2^j z  -> (i, j)
    for i in range(3):
        for j in range(3):
            w = np.linalg.matrix_power  # placeholder
            g = idn.copy()
            for _ in range(i):
                g = g[u1]
            for _ in range(j):
                g = g[u2]
            for z in (idn, tp, tp[tp]):
                if np.array_equal(g[z], u):
                    return i, j
    return None
def tpow(c):
    k = key(c)
    return 0 if k == key(idn) else (1 if k == key(tp) else 2)
c12 = tpow(u1[u2[inv(u1)[inv(u2)]]])
ok = True
for a in U[::2]:
    for b in U[::3]:
        ca, cb = coords(a), coords(b)
        lhs = tpow(a[b[inv(a)[inv(b)]]])
        rhs = (c12 * (ca[0] * cb[1] - ca[1] * cb[0])) % 3
        ok &= lhs == rhs
print('commutator = tick^(symplectic area):', ok, ' (base power', c12, ')')
# U action on far points: regular?
pt_of = np.empty(240, int)
for q, f in enumerate(fib):
    pt_of[f] = q
far = [x for x in range(40) if x != p and not Adj[p, x]]
on = lambda h: pt_of[h[[f[0] for f in fib]]]  # noqa: E731
orb = {int(on(u)[far[0]]) for u in U}
stab = [u for u in U if on(u)[far[0]] == far[0]]
print('U-orbit of a far point:', len(orb), ' stabiliser in U:', len(stab))
nbs = sorted(np.nonzero(Adj[p])[0])
print('U-orbits on the 12 neighbours:', sorted(Counter(len({int(on(u)[q]) for u in U}) for q in nbs).items()))
