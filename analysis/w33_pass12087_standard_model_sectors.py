"""Pass 12087: the Standard-Model content of the 16-clock gradings, sector by sector (Claude track; 12081).

Take a dimension-5 subspace V of E8/2E8 (16 clocks + 15 splits) reached by a flag e7+a1 > e6 > so(10) > su(5) >
su(3)+su(2) (12081). Its 32 characters split the 240 roots into Wilson-line sectors. Hypercharge Y is the direction in
the su(5) span orthogonal to su(3)+su(2), normalised so that the su(5) X, Y bosons have Y = +-5/6. Exact results:
  * sector 0: the su(3)+su(2) roots (8); one sector: the X, Y bosons (12 roots, Y = +-5/6);
  * 5 sectors of Q = (3,2)_{1/6} (+ conjugate), 12 roots each;
  * 5 sectors of u^c-type (3bar)_{-2/3} with e^c-type (1)_{1} (+ conjugates), 8 roots each;
  * 10 sectors of d^c-type (3bar)_{1/3} with two neutral singlets, 8 roots each;
  * 10 sectors of L = (1,2)_{-1/2} (+ conjugate), 4 roots each.
Reading. The Wilson-line sectors of a Standard-Model grading carry exactly the Standard-Model representations with the
correct hypercharges, split as in orbifold GUT breaking (Q apart from u, e; d apart from L). The multiplicities are 5
(pieces of the 10) and 10 (pieces of the 5bar), inherited from the commutant SU(5)' of E8 > SU(5) x SU(5)' -- not 3.
Every sector is vector-like (each representation with its conjugate): chirality is not addressed at this level.
"""

import itertools
import json
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12087_standard_model_sectors.json"
NAMES = {2: "A1", 6: "A2", 12: "A3", 20: "A4", 30: "A5", 42: "A6", 56: "A7", 72: "A8", 24: "D4", 60: "D6", 112: "D8", 126: "E7", 240: "E8"}


class Gradings:
    def __init__(self):
        self.R, C, self.fib, refl, perm = build()
        Adj, invs, tick, _ = setup()
        self.vecs = [s for k, s in invs]
        self.kinds = [k for k, s in invs]
        self.key = {s.tobytes(): i for i, s in enumerate(self.vecs)}
        self.n = len(self.vecs)
        self.IP = np.round(self.R @ self.R.T).astype(int)
        self.rkey = {tuple(np.round(r * 2).astype(int)): j for j, r in enumerate(self.R)}

    def span_of(self, els):
        cur = [np.zeros(240, bool)]
        for h in els:
            cur = cur + [c ^ self.vecs[h] for c in cur]
        return frozenset(self.key[c.tobytes()] for c in cur if c.any())

    def fixedmask(self, S):
        m = np.ones(240, bool)
        for h in S:
            m &= ~self.vecs[h]
        return m

    def comps(self, mask):
        idx = np.nonzero(mask)[0]
        sub = self.IP[np.ix_(idx, idx)] != 0
        seen, out = set(), []
        for i in range(len(idx)):
            if i in seen:
                continue
            c, st = {i}, [i]
            while st:
                a = st.pop()
                for b in np.nonzero(sub[a])[0]:
                    if b not in c:
                        c.add(int(b))
                        st.append(int(b))
            seen |= c
            out.append([int(idx[j]) for j in c])
        return out

    def typ(self, mask):
        t = []
        for c in self.comps(mask):
            r = np.linalg.matrix_rank(self.R[c])
            t.append("E6" if (len(c), r) == (72, 6) else ("D5" if (len(c), r) == (40, 5) else NAMES.get(len(c), "?")))
        return tuple(sorted(t))

    def sm_flag(self, seed=7):
        target = [("A1", "E7"), ("E6",), ("D5",), ("A4",), ("A1", "A2")]
        rnd = random.Random(seed)
        while True:
            gens = []
            for t in target:
                S0 = self.span_of(gens) if gens else frozenset()
                cands = [h for h in range(self.n) if h not in S0 and self.typ(self.fixedmask(self.span_of(gens + [h]))) == t]
                if not cands:
                    break
                gens.append(rnd.choice(cands))
            if len(gens) == 5:
                return gens

    def sectors(self, gens):
        R = self.R
        V, V4 = self.span_of(gens), self.span_of(gens[:4])
        cs = self.comps(self.fixedmask(V))
        A2 = next(c for c in cs if len(c) == 6)
        A1 = next(c for c in cs if len(c) == 2)
        su5 = np.nonzero(self.fixedmask(V4))[0]
        B = np.linalg.svd(R[su5])[2][:4]
        Y = np.linalg.svd(R[A2 + A1] @ B.T)[2][-1] @ B
        xy = [i for i in su5 if i not in A2 + A1]
        Y = Y * (5 / 6) / abs(R[xy[0]] @ Y)
        eps = np.array([[int(self.vecs[h][a]) for h in gens] for a in range(240)])
        out = {}
        for ch in itertools.product(range(2), repeat=5):
            idxs = [a for a in range(240) if tuple(eps[a]) == ch]
            cnt = Counter()
            for i in idxs:
                orb, st = {i}, [i]
                while st:
                    a = st.pop()
                    for b in A2 + A1:
                        j = self.rkey[tuple(np.round((R[a] - (R[a] @ R[b]) * R[b]) * 2).astype(int))]
                        if j not in orb:
                            orb.add(j)
                            st.append(j)
                cnt[(len(orb), round(float(R[i] @ Y) * 6))] += 1
            out[ch] = cnt
        return out, Y, xy

    @staticmethod
    def label(ch, cnt):
        ks = set(cnt)
        if not any(ch):
            return "gauge"
        if (6, 5) in ks or (6, -5) in ks:
            return "XY"
        if (6, 1) in ks:
            return "Q"
        if (1, 6) in ks:
            return "ue"
        if (2, 3) in ks:
            return "L"
        return "dN"


def main():
    checks, res = {}, {}
    g = Gradings()
    gens = g.sm_flag()
    V = g.span_of(gens)
    checks["flag-built SM subspace: 31 elements, 16 clocks"] = len(V) == 31 and sum(g.kinds[h] == "clock" for h in V) == 16
    sec, Y, xy = g.sectors(gens)
    checks["X, Y bosons have hypercharge +-5/6"] = sorted(set(np.round(g.R[xy] @ Y * 6).astype(int))) == [-5, 5]
    lab = {ch: g.label(ch, c) for ch, c in sec.items()}
    res["sector_labels"] = dict(Counter(lab.values()))
    expect = {"gauge": {(6, 0): 6, (2, 0): 2}, "XY": {(6, 5): 6, (6, -5): 6}, "Q": {(6, 1): 6, (6, -1): 6},
              "ue": {(3, 4): 3, (3, -4): 3, (1, 6): 1, (1, -6): 1}, "dN": {(3, 2): 3, (3, -2): 3, (1, 0): 2}, "L": {(2, 3): 2, (2, -3): 2}}
    checks["sector contents are exactly the SM pieces with SM hypercharges (6Y in parentheses)"] = all(dict(sec[ch]) == expect[lab[ch]] for ch in sec)
    checks["multiplicities: Q 5, (u,e) 5, (d,N) 10, L 10, plus gauge and X/Y"] = Counter(lab.values()) == Counter(
        {"gauge": 1, "XY": 1, "Q": 5, "ue": 5, "dN": 10, "L": 10})
    res["sm_generators"] = [int(x) for x in gens]
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
