"""Pass 12089: spin-statistics from Kramers squared -- adding a split fermion parity to the E6 clock vacuum gives SO(10)
with every spinor 16 odd and every vector 10 even (Claude track; 12077, 12081, 12085).

The E6 clock vacuum is a Klein plane K of clocks (fixed algebra e6 + u(1)^2, 12077). By 12085 a Kramers reversal
squares to a split involution sigma (odd exactly on a half-spinor 128 of so(16)). Adjoin sigma to K. Exact results
(one Klein plane, all 135 splits, plus a second Klein plane as a check):
  * span(K, sigma) fixes so(10) (d5) for exactly 27 of the 135 splits, and a5 + a1 for the other 108.
  * In every one of the 27 SO(10) cases: classify the 200 roots outside the d5 by the norm of their projection onto the
    d5 span -- vector weights (norm 1), spinor weights (norm 5/4), singlets (0). Then sigma is
        ODD on all 128 spinor-weight roots (the 16s: E8 > SO(10) x SU(4), (16,4) + (16bar,4bar)),
        EVEN on all 60 vector-weight roots (the 10s, (10,6)) and on the 12 singlet roots (su(4)).
Reading. With fermion parity taken to be Kramers squared, the SO(10) obtained from the E6 clock vacuum has exactly the
right spin-statistics: every 16 (one generation of matter) is fermionic and every 10 (the Higgs) and the gauge
sector is bosonic. Spin-statistics is not imposed; it is the parity of the split involution on the E8 roots.
Scope: root-level parities; that the split class is Kramers squared is 12085 (classical lift argument).
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12089_fermion_parity_makes_the_16_fermionic.json"


def main():
    checks, res = {}, {}
    g = Gradings()
    R = g.R
    kleins = []
    for a in range(g.n):
        if g.kinds[a] != "clock":
            continue
        for b in range(a + 1, g.n):
            if g.kinds[b] == "clock" and g.kinds[g.key[(g.vecs[a] ^ g.vecs[b]).tobytes()]] == "clock":
                kleins.append([a, b])
                break
        if len(kleins) == 2:
            break
    all_ok, summary = True, []
    for Kp in kleins:
        K = g.span_of(Kp)
        all_ok &= g.typ(g.fixedmask(K)) == ("E6",)
        types, pats = Counter(), Counter()
        for s in range(g.n):
            if g.kinds[s] != "split" or s in K:
                continue
            t = g.typ(g.fixedmask(g.span_of(Kp + [s])))
            types[t] += 1
            if t == ("D5",):
                d5 = set(np.nonzero(g.fixedmask(g.span_of(Kp + [s])))[0].tolist())
                Bd = np.linalg.svd(R[sorted(d5)])[2][:5]
                cnt = Counter()
                for a in range(240):
                    if a in d5:
                        continue
                    nrm = round(float(np.sum((Bd @ R[a]) ** 2)), 3)
                    cnt[({1.0: "10", 1.25: "16", 0.0: "singlet"}.get(nrm, str(nrm)), "odd" if g.vecs[s][a] else "even")] += 1
                pats[tuple(sorted(cnt.items()))] += 1
        summary.append(dict(types={str(k): v for k, v in types.items()}, patterns={str(k): v for k, v in pats.items()}))
        all_ok &= types == Counter({("A1", "A5"): 108, ("D5",): 27})
        all_ok &= pats == Counter({((("10", "even"), 60), (("16", "odd"), 128), (("singlet", "even"), 12)): 27})
    res["klein_planes"] = summary
    checks["E6 Klein vacuum + split sigma: so(10) for exactly 27 of 135 splits (a5+a1 otherwise), two Klein planes"] = bool(all_ok and len(kleins) == 2)
    checks["in every SO(10) case sigma is odd on all 128 spinor-weight roots (16s) and even on the 60 vector (10s) and 12 singlet roots"] = bool(all_ok)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
