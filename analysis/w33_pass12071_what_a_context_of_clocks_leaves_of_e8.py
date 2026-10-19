"""Pass 12071: what a context of clocks leaves of E8 (Claude track; 12052, 12062, 12068).

Several clock involutions (inner, in one torus, hence commuting) fix the subalgebra h + span(roots even under all of
them). Exact, in the 12052 root model, over every choice of clock at each event:
  one clock                         e7 + a1                (136)
  two collinear clocks (9 choices)   d6 + 2 a1              (72)
  two non-collinear clocks           e6 + u(1)^2 (80) for the 6 choices whose product is a clock (12062),
                                     d6 + 2 a1 (72) for the 3 whose product is split
  the three clocks at one event      e6 + u(1)^2            (80)
  three clocks on a line (27)        d4 + 4 a1              (40)
  a whole context, 4 clocks (81)     8 a1 = su(2)^8         (24, rank 8)
Reading. The context condensate that a tick capacity selects (12068) would leave su(2)^8 of E8 -- the A1^8 of the
Hamming-code construction of E8 -- and no su(3): a context of clocks does not leave a Standard-Model algebra. Two
incompatible clocks whose product is a third clock leave e6 + u(1)^2, the grand-unified algebra of E6(p) (12056).
Scope: fixed subalgebras of commuting inner involutions in the 12052 model; which clocks a tick condensate picks is
the open tick-to-clock map (12068, 12072).
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

OUT = ROOT / "data" / "w33_pass12071_what_a_context_of_clocks_leaves_of_e8.json"
NAMES = {(2, 1): "A1", (6, 2): "A2", (12, 3): "A3", (20, 4): "A4", (30, 5): "A5", (42, 6): "A6", (56, 7): "A7", (72, 8): "A8",
         (24, 4): "D4", (40, 5): "D5", (60, 6): "D6", (84, 7): "D7", (112, 8): "D8", (72, 6): "E6", (126, 7): "E7", (240, 8): "E8"}


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    cp = {}
    for k, s in invs:
        if k == "clock":
            ev = {x for x in range(40) if not s[fib[x]].any()}
            cp.setdefault(next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == ev), []).append(s)

    def rootsys(idx):
        V = R[list(idx)]
        IP = np.round(V @ V.T).astype(int)
        seen, out = set(), []
        for i in range(len(idx)):
            if i in seen:
                continue
            st, c = [i], {i}
            while st:
                a = st.pop()
                for b in np.nonzero(IP[a])[0]:
                    if b not in c:
                        c.add(int(b))
                        st.append(int(b))
            seen |= c
            c = sorted(c)
            out.append(NAMES.get((len(c), int(np.linalg.matrix_rank(V[c]))), "?"))
        return tuple(sorted(out))

    def fixed(lst):
        even = np.ones(240, bool)
        for s in lst:
            even &= ~s
        idx = np.nonzero(even)[0]
        return 8 + len(idx), rootsys(idx)
    p = 0
    q = int(np.nonzero(Adj[p])[0][0])
    line = ([p, q] + [int(r) for r in np.nonzero(Adj[p])[0] if Adj[q, r]])[:4]
    far = next(x for x in range(40) if x != p and not Adj[p, x])
    T = {}
    T["one"] = Counter(fixed([cp[p][a]]) for a in range(3))
    T["collinear_pair"] = Counter(fixed([cp[p][a], cp[q][b]]) for a in range(3) for b in range(3))
    T["far_pair"] = Counter(fixed([cp[p][a], cp[far][b]]) for a in range(3) for b in range(3))
    T["three_at_p"] = Counter([fixed(cp[p])])
    T["three_on_line"] = Counter(fixed([cp[x][c] for x, c in zip(line[:3], ch)]) for ch in itertools.product(range(3), repeat=3))
    T["context"] = Counter(fixed([cp[x][c] for x, c in zip(line, ch)]) for ch in itertools.product(range(3), repeat=4))
    res["fixed_subalgebras"] = {k: {str(a): b for a, b in v.items()} for k, v in T.items()}
    E7, D6, E6, D4, A8 = ("A1", "E7"), ("A1", "A1", "D6"), ("E6",), ("A1",) * 4 + ("D4",), ("A1",) * 8
    checks["one clock: e7 + a1 (136)"] = T["one"] == Counter({(136, E7): 3})
    checks["two collinear clocks: d6 + 2a1 (72), all 9 choices"] = T["collinear_pair"] == Counter({(72, D6): 9})
    checks["two non-collinear clocks: e6 + u(1)^2 (80) x6, d6 + 2a1 (72) x3"] = T["far_pair"] == Counter({(80, E6): 6, (72, D6): 3})
    checks["three clocks at one event: e6 + u(1)^2 (80)"] = T["three_at_p"] == Counter({(80, E6): 1})
    checks["three clocks on a line: d4 + 4a1 (40), all 27 choices"] = T["three_on_line"] == Counter({(40, D4): 27})
    checks["a whole context of clocks: su(2)^8 (24, rank 8), all 81 choices"] = T["context"] == Counter({(24, A8): 81})
    # the far-pair split: e6 cases are exactly those where the product is a clock (12062)
    ok = True
    for a in range(3):
        for b in range(3):
            prod = cp[p][a] ^ cp[far][b]
            is_clock = 240 - int(prod.sum()) == 128
            ok &= (fixed([cp[p][a], cp[far][b]])[0] == 80) == is_clock
    checks["far pair: e6 + u(1)^2 exactly when the product is a clock (12062)"] = bool(ok)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
