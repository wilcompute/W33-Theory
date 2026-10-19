"""Pass 12085: Kramers squared is fermion parity -- the observers' time reversals square to the split involution of E8,
which is odd exactly on the half-spinor 128 (Claude track; 12080, 12084).

  1. W(E8) level (12080): the 72 Kramers reversals are antilinear Weyl elements e with e^2 = -1, the central element of
     W(E8) acting as alpha -> -alpha; the 1080 bosonic CPs have e^2 = +1.
  2. Lift to E8. Every lift n of -1 in W(E8) to the normaliser of the torus satisfies (n t)^2 = n^2 (since -1 inverts
     the torus), and one lift is the Chevalley involution (e_alpha -> -e_{-alpha}, h -> -h). So every lift of -1 is an
     involution conjugate to the Chevalley involution, whose fixed algebra has dimension |Phi+| = 120: the SPLIT class
     (the inner involutions of E8 have fixed dimension 136 for clocks and 120 for splits, 12052). Hence the square of any
     lift of a Kramers reversal is a split involution. (Classical: Chevalley involution; Kac's classification.)
  3. For every one of the 135 split classes: the fixed algebra is so(16) = 8 + 112 even roots, and the 128 odd roots
     form one minuscule W(D8)-orbit (<odd, even root> in {0, +-1}): 248 = 120 + 128 with the half-spinor 128 odd.
Reading. A Kramers reversal (an observer's time reversal, J^2 = -1) squares, inside E8, to the involution that is +1 on
so(16) and -1 on its spinor 128: a fermion-parity operator for the E8 = so(16) + 128 decomposition. The flavour CPs
square to the identity. The corpus's non-SUSY heterotic models use exactly this split involution as their Z2 holonomy
(12084), as in the construction of the SO(16) x SO(16) string as a fermion-parity orbifold of E8 x E8.
Scope: the Lie-level step is the classical lift argument; the W-level and root-level statements are computed.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402
from w33_pass12080_cp_compatible_clocks import inverting_involution  # noqa: E402

OUT = ROOT / "data" / "w33_pass12085_kramers_squared_is_fermion_parity.json"


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    G = sp43_from_ticks(tick)
    w = perm(inverting_involution(C, refl))
    neg = perm(-np.eye(8))
    ptof = np.empty(240, int)
    for x in range(40):
        for i in fib[x]:
            ptof[i] = x
    sq = Counter()
    for g in G:
        e = w[g]
        pp = np.array([ptof[e[fib[x][0]]] for x in range(40)])
        if not np.array_equal(pp[pp], np.arange(40)):
            continue
        nf = int(np.sum(pp == np.arange(40)))
        s = e[e]
        sq[(nf, "-1" if np.array_equal(s, neg) else ("+1" if np.array_equal(s, np.arange(240)) else "other"))] += 1
    checks["W level: 72 Kramers with e^2 = -1 (central, alpha -> -alpha), 1080 CPs with e^2 = +1"] = sq == Counter({(0, "-1"): 72, (8, "+1"): 1080})
    checks["-1 acts on roots as negation (central in W(E8))"] = bool(np.array_equal(R[neg], -R))
    fixed_dims = Counter(8 + int((~s).sum()) for k, s in invs)
    checks["inner involutions: fixed dimension 136 (120 clocks) or 120 (135 splits); 120 = |Phi+| singles out the split class"] = (
        fixed_dims == Counter({136: 120, 120: 135}) and 120 == 240 // 2)
    key = {tuple(np.round(r * 2).astype(int)): i for i, r in enumerate(R)}
    ok = True
    for k, s in invs:
        if k != "split":
            continue
        even, odd = np.nonzero(~s)[0], np.nonzero(s)[0]
        ipv = np.round(R[odd] @ R[even].T).astype(int)
        seen, st = {int(odd[0])}, [int(odd[0])]
        while st:
            a = st.pop()
            for b in even:
                r = R[a] - (R[a] @ R[b]) * R[b]
                j = key[tuple(np.round(r * 2).astype(int))]
                if j not in seen:
                    seen.add(j)
                    st.append(j)
        ok &= len(even) == 112 and len(odd) == 128 and set(np.unique(ipv)) <= {-1, 0, 1} and len(seen) == 128
    checks["every split class: so(16) = 8 + 112 even roots; the 128 odd roots are one minuscule W(D8)-orbit (half-spinor)"] = bool(ok)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
