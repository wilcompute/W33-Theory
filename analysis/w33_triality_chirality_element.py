"""Item 4: is the antiunitary element that realises odd triality on a split's three entangled 8-MUB classes the same as the chirality flip?
The chirality flip over a codeword is the reflection s_alpha in its double-six root (Pass 12636).  The three entangled classes of a
split = the three orthogonal frames of its D4 (Pass 12636 add. 2 + 12637).  Test in E6: for every D4 and every root alpha:
(a) if alpha in D4: s_alpha preserves D4, fixes the frame containing alpha and swaps the other two (a transposition);
(b) if alpha not in D4: s_alpha does not preserve D4 (or acts otherwise) - recorded;
(c) each root lies in exactly 15 D4's, so one reflection = chirality flip over its codewords AND odd triality on 15 factorisations.
usage: py -3 analysis/w33_triality_chirality_element.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pass12634_naruki_fan.py")}
exec(open(os.path.join(HERE, "w33_pass12634_naruki_fan.py"), encoding="utf-8").read().split("# --- Check 1")[0], g)
POS, IP, PI, key = g["POS"], g["IP"], g["PI"], g["key"]
def refl(a):
    al = POS[a]
    return [PI[key(POS[i] - (2 * (POS[i] @ al) // (al @ al)) * al)] for i in range(36)]
def span_roots(S):
    M = POS[sorted(S)].astype(float); Pm = M.T @ np.linalg.pinv(M.T)
    return frozenset(i for i in range(36) if np.allclose(Pm @ POS[i], POS[i]))
frames4 = []
def ext(S, start):
    if len(S) == 4: frames4.append(frozenset(S)); return
    for k in range(start, 36):
        if all(IP[k, x] == 0 for x in S): ext(S + [k], k + 1)
ext([], 0)
D4 = {}
for F in frames4:
    D4.setdefault(span_roots(F), []).append(F)
assert len(D4) == 45 and all(len(v) == 3 for v in D4.values())
stats = Counter(); per_root = Counter()
for D, frames in D4.items():
    for a in range(36):
        s = refl(a)
        img = frozenset(s[x] for x in D)
        if img != D:
            stats[("alpha_in_D4", a in D, "preserves", False)] += 1
            continue
        perm = tuple(frames.index(frozenset(s[x] for x in F)) for F in frames)
        fixed = sum(1 for i in range(3) if perm[i] == i)
        own = next(i for i, F in enumerate(frames) if a in F) if a in D else None
        stats[("alpha_in_D4", a in D, "fixed_frames", fixed, "fixes_own_frame", own is not None and perm[own] == own)] += 1
        if a in D:
            per_root[a] += 1
res = dict(stats={str(k): v for k, v in stats.items()}, D4_per_root=sorted(set(per_root.values())))
print("(alpha in D4?, effect): count")
for k, v in sorted(stats.items(), key=str):
    print("  ", k, v)
print("number of D4 containing each root:", res["D4_per_root"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_triality_chirality_element.json"), "w"), indent=1)
