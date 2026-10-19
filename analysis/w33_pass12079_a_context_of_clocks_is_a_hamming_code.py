"""Pass 12079: the su(2)^8 left by a context of clocks is the Hamming-code E8 on a pair of skew lines
(Claude track; 12071, 12069, 12080).

For each of the 81 choices of one clock at each event of a context L, the fixed algebra is su(2)^8 (12071). Exact:
  1. Its 16 roots are 8 mutually orthogonal pairs +-r_i. The glue code {S : (1/2) sum_{i in S} +-r_i in E8} is the
     extended Hamming code [8,4,4] (weights 0:1, 4:14, 8:1), and E8 = 16 frame roots + 224 glue roots.
  2. The 8 frame roots lie in 8 fibres: the 4 events of L and the 4 events of a line L' disjoint from L. Every one of the
     27 lines disjoint from L occurs, each for exactly 3 of the 81 choices.
  3. Read as sets of events, the 14 weight-4 codewords are: 6 unions of two collinear (matched) pairs across L, L', and
     4 + 4 copies of L or L' with one event swapped for its partner. There is a labelling of the 8 events by
     AG(3,2) = F_2^3 in which the 14 codewords are exactly the 14 affine planes (found by exhaustive search).
  4. L u L' is exactly the fixed set of a bosonic CP (12069); 12080 shows that the CP-compatible clocks on L leave this
     su(2)^8 on the CP's own fixed set.
Reading. A context of clocks breaks E8 to the Hamming-code su(2)^8 -- a three-qubit (AG(3,2)) structure -- carried by
two disjoint measurement contexts, i.e. by the fixed set of a flavour-type CP. Classical: E8 from the Hamming code
(Conway-Sloane ch. 8); new: its realisation by clock involutions on W(3,3) and the link to bosonic CP.
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12079_a_context_of_clocks_is_a_hamming_code.json"


def inE8(v):
    v2 = np.round(2 * v).astype(int)
    if not np.allclose(2 * v, v2):
        return False
    if np.all(v2 % 2 == 0):
        return (v2 // 2).sum() % 2 == 0
    if np.all(v2 % 2 != 0):
        return (v2.sum() // 2) % 2 == 0
    return False


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    cp = {}
    for k, s in invs:
        if k == "clock":
            ev = {x for x in range(40) if not s[fib[x]].any()}
            cp.setdefault(next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == ev), []).append(s)
    ptof = {i: x for x in range(40) for i in fib[x]}
    p, q = 0, int(np.nonzero(Adj[0])[0][0])
    line = ([p, q] + [int(r) for r in np.nonzero(Adj[p])[0] if Adj[q, r]])[:4]
    skew = [L for L in itertools.combinations(range(40), 4) if all(Adj[a, b] for a in L for b in L if a != b)]
    skew = [set(L) for L in skew if not set(L) & set(line)]
    ok1, ok3, Lps = True, True, Counter()
    plane_ok = True
    planes = [set(v for v in itertools.product(range(2), repeat=3) if (np.dot(a, v) % 2) == c)
              for a in itertools.product(range(2), repeat=3) if any(a) for c in (0, 1)]
    for ch in itertools.product(range(3), repeat=4):
        even = np.ones(240, bool)
        for x, c in zip(line, ch):
            even &= ~cp[x][c]
        idx = list(np.nonzero(even)[0])
        reps = []
        for i in idx:
            if not any(np.allclose(R[i], -R[j]) for j in reps):
                reps.append(i)
        V = R[reps]
        code = [S for m in range(9) for S in itertools.combinations(range(8), m)
                if (not S and True) or any(inE8(0.5 * sum(s * V[i] for s, i in zip(sg, S))) for sg in itertools.product((1, -1), repeat=len(S)))]
        glue = sum(1 for i in range(240) if np.sum(np.abs(V @ R[i] / 2) > 1e-9) == 4)
        ok1 &= len(reps) == 8 and np.allclose(V @ V.T, 2 * np.eye(8)) and Counter(len(S) for S in code) == Counter({0: 1, 4: 14, 8: 1}) and glue == 224
        ev = [ptof[i] for i in reps]
        Lp = set(ev) - set(line)
        Lps[frozenset(Lp)] += 1
        ok1 &= len(set(ev)) == 8 and set(line) <= set(ev) and Lp in skew
        if ch == (0, 0, 0, 0):
            match = {a: next(b for b in Lp if Adj[a, b]) for a in line}
            words = [set(ev[i] for i in S) for S in code if len(S) == 4]
            cls = Counter((len(w & set(line)), sum(1 for a in line if a in w and match[a] in w)) for w in words)
            ok3 &= cls == Counter({(2, 2): 6, (3, 0): 4, (1, 0): 4})
            found = None
            for img in itertools.permutations(list(itertools.product(range(2), repeat=3))):
                lab = dict(zip(ev, img))
                if all({lab[e] for e in w} in planes for w in words):
                    found = {int(k): list(v) for k, v in lab.items()}
                    break
            plane_ok = found is not None
            res["AG32_labelling"] = found
    checks["81 choices: 8 orthogonal frame roots, glue code = extended Hamming [8,4,4], 16 + 224 = 240 roots"] = bool(ok1)
    checks["frame fibres = L u L' with L' disjoint from L; all 27 disjoint lines occur, 3 choices each"] = (
        len(Lps) == 27 and set(Lps.values()) == {3} and len(skew) == 27)
    checks["codewords: 6 unions of two matched pairs, 4 + 4 swapped copies of L, L'"] = bool(ok3)
    checks["an AG(3,2) labelling of the 8 events makes the 14 codewords exactly the affine planes"] = bool(plane_ok)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
