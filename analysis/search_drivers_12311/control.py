"""12311 control: the translation rule must be live.  Shift one partner's fixed-point label by e5 (torus 3: (1 - theta^k) = 2 for odd k,
0 for even k, so a unit e5 can never be absorbed) -> every pairing must fail; by e1 (torus 1: det(1 - theta) = 1) -> pairings that
involve a theta-sector field may still pass."""
import sys, json, itertools, copy
sys.argv = ['x']
src = open('vacuum.py').read().split('conj = lambda')[0]
exec(src)
conj = lambda d: [(-x if abs(x) in (3, 8, 28, 56) else x) for x in d]
res = {'e5': [0, 0], 'e1': [0, 0]}
for i, j in itertools.combinations(range(len(Fr)), 2):
    A_, B_ = Fr[i], Fr[j]
    if conj(A_['dims']) != B_['dims'] or A_['y'] + B_['y'] != 0:
        continue
    for key, idx in (('e5', 4), ('e1', 0)):
        A2 = copy.deepcopy(A_); A2['lat'][idx] += 1
        ok = pair_allowed(A2, B_) is not None
        res[key][0 if ok else 1] += 1
print({k: dict(allowed=v[0], rejected=v[1]) for k, v in res.items()})
json.dump({k: dict(allowed=v[0], rejected=v[1]) for k, v in res.items()}, open('control.json', 'w'), indent=1)
