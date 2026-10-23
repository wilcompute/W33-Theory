import random, sys, numpy as np
exec(open('twoline.py').read().split("draws = hits = tries = 0")[0].replace("N, SEED = int(sys.argv[1]), int(sys.argv[2])", "N, SEED = 1, 3"))
from collections import Counter
c = Counter()
for t in range(40000):
    base = rnd.choice(BASES); V0, V1, Wf, d5, pool = info[base]
    j1, j2 = rnd.choice(pool), rnd.choice(pool)
    W1 = np.concatenate([L3[j1], L3[rnd.randrange(len(coefs))]]); W2 = np.concatenate([L3[j2], L3[rnd.randrange(len(coefs))]])
    a1, a2 = admissible(W1, V0, V1, Wf), admissible(W2, V0, V1, Wf)
    c['W1 adm'] += a1; c['both adm'] += a1 and a2
    if a1 and a2:
        c['mutual'] += ok3(W1 @ W2)
        mk = np.zeros(240, bool); mk[np.array(d5)[integ(R[d5] @ L3[j1]) & integ(R[d5] @ L3[j2])]] = True
        c['A4 left'] += g.typ(mk) == ('A4',)
        c['A4 left & mutual'] += g.typ(mk) == ('A4',) and ok3(W1 @ W2)
        c['same lambda'] += j1 == j2
print(dict(c))
