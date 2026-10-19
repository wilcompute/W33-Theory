"""Pass 12084: the corpus non-SUSY A8 orbifold uses the split real form -- its Z2 holonomy is a factorisation of
W(3,3), never a clock (Claude track; corpus a8_so16 driver, 11092-11108; 12052, 12078).

The corpus SO(16) x SO(16) completions of the W(3,3) A8 Kac pair (analysis/orbifolder_n0_drivers/a8_so16.py) use the
order-3 shift V1 = (1/6^7, 5/6; 0^7, 2/3) and order-2 shifts V0 = (a; b) with a, b half of norm-4 vectors of E8.
In the 12052 model (same coordinates) a torus element exp(2 pi i a) of order 2 is the inner involution with parity
vector alpha -> [alpha.a in Z + 1/2]. Exact results:
  1. V1a has order 3 (3 V1a in E8) and centraliser A8 (72 roots with p.V1a in Z): the corpus's A8 Kac shift.
  2. All 2160 halves of norm-4 vectors are SPLIT involutions (128 odd roots, fixed so(16)); they fall into all 135 split
     classes, 16 each; none is a clock. Halves of roots, by contrast, are clocks (all 240).
  3. With the A8 shift, the first-factor gauge roots are A7 or A3 + A4; the V0 with a.V1a in Z reach all 45
     factorisations of W(3,3).
Reading. The corpus's non-SUSY heterotic models are built on the split real form E8(8) in each factor -- each Z2 holonomy
is one of the 135 split involutions, i.e. a two-qutrit factorisation with one of its three split real forms -- not on
the clock (one-time) form. By 12078 a split holonomy has vanishing one-loop Hosotani energy (V_B = 0 exactly) and is
the fermion-dominated choice; by 12085 the split involution is the square of a Kramers reversal (fermion parity).
This is consistent with the SO(16) x SO(16) string being the fermion-parity orbifold of E8 x E8.
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

OUT = ROOT / "data" / "w33_pass12084_the_corpus_orbifold_uses_the_split_form.json"
NAMES = {(2, 1): "A1", (6, 2): "A2", (12, 3): "A3", (20, 4): "A4", (30, 5): "A5", (42, 6): "A6", (56, 7): "A7", (72, 8): "A8",
         (24, 4): "D4", (40, 5): "D5", (60, 6): "D6", (84, 7): "D7", (112, 8): "D8", (72, 6): "E6", (126, 7): "E7", (240, 8): "E8"}


def e8_norm(n2):
    out = []
    for half in (False, True):
        rng = [k / 2 for k in range(-5, 6, 2)] if half else list(range(-2, 3))
        for v in itertools.product(rng, repeat=8):
            if abs(sum(x * x for x in v) - n2) < 1e-9 and abs(sum(v) % 2) < 1e-9:
                out.append(np.array(v, float))
    return out


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    kind = {s.tobytes(): k for k, s in invs}
    fac = {s.tobytes(): frozenset(x for x in range(40) if not s[fib[x]].any()) for k, s in invs if k == "split"}
    N4, N2 = e8_norm(4), e8_norm(2)

    def par(a):
        return np.round(2 * (R @ a)).astype(int) % 2 == 1
    V1a = np.array([1 / 6] * 7 + [5 / 6])
    checks["V1a has order 3 and centraliser A8 (72 roots)"] = bool(
        np.allclose(2 * 3 * V1a, np.round(2 * 3 * V1a)) and sum(1 for r in R if abs(r @ V1a - round(r @ V1a)) < 1e-9) == 72)
    c4 = Counter((kind.get(par(v / 2).tobytes()), int(par(v / 2).sum())) for v in N4)
    classes = Counter(par(v / 2).tobytes() for v in N4)
    checks["all 2160 V0 halves are split involutions (128 odd roots): all 135 split classes, 16 each, no clock"] = (
        len(N4) == 2160 and c4 == Counter({("split", 128): 2160}) and len(classes) == 135 and set(classes.values()) == {16})
    checks["halves of the 240 roots are clocks"] = Counter(kind.get(par(v / 2).tobytes()) for v in N2) == Counter({"clock": 240})

    def rs(idx):
        V = R[idx]
        IPm = np.round(V @ V.T).astype(int)
        seen, out = set(), []
        for i in range(len(idx)):
            if i in seen:
                continue
            c, st = {i}, [i]
            while st:
                x = st.pop()
                for y in np.nonzero(IPm[x])[0]:
                    if y not in c:
                        c.add(int(y))
                        st.append(int(y))
            seen |= c
            c = sorted(c)
            out.append(NAMES.get((len(c), int(np.linalg.matrix_rank(V[c]))), "?"))
        return tuple(sorted(out))
    gauge, facs = Counter(), set()
    for v in N4:
        a = v / 2
        kept = [i for i in range(240) if abs(R[i] @ a - round(R[i] @ a)) < 1e-9 and abs(R[i] @ V1a - round(R[i] @ V1a)) < 1e-9]
        gauge[rs(kept)] += 1
        if abs((a @ V1a) - round(a @ V1a)) < 1e-9:
            facs.add(fac[par(a).tobytes()])
    res["first_factor_gauge"] = {str(k): v for k, v in gauge.items()}
    checks["with the A8 shift the first-factor gauge roots are A7 or A3+A4; a.V1a in Z reaches all 45 factorisations"] = (
        set(gauge) == {("A7",), ("A3", "A4")} and len(facs) == 45)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
