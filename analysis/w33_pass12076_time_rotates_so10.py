"""Pass 12076: time rotates SO(10) inside E6 -- the three SO(10)s of a two-clock vacuum and the matter/Higgs swap
(Claude track; 12064, 12066, 12073).

For two non-collinear clocks p, q the 27 of E6(p) is 1+1+1 + 8_v+8_s+8_c, with singlets f_0, f_1, f_2 (the second
clock's monomial) and D4 = the E6 roots orthogonal to all three (12064). Exact results:
  1. Three SO(10)s. For each singlet f_i, the E6 roots orthogonal to f_i form D5 (40 roots, rank 5): E6 > SO(10)_i x U(1).
     The 27 splits by inner product with f_i as 1 (f_i) + 10_i (-2/3) + 16_i (+1/3), with
         10_i = 8_i + f_j + f_k,      16_i = 8_j + 8_k.
     So each choice of singlet is a grand-unified SO(10) whose spinor 16 (one generation) is two of the octets and whose
     vector 10 (the Higgs) is the third octet plus the other two singlets. The three D5 meet in the D4.
  2. The triality ticks of 12066 (at the four common neighbours) permute f_0 -> f_1 -> f_2 cyclically and carry D5_i to
     D5_{i+1}: a tick of time rotates the SO(10) and turns part of the matter 16 into the Higgs 10 (8_j moves from 16_i
     to 10_j).
Reading. The 'families from triality' reading of 12066 is corrected: the three octets are not three generations; the
time ticks rotate WHICH SO(10) is unified, exchanging matter and Higgs octets. One generation is a 16 of whichever
SO(10) the vacuum (the clock choice) singles out. Scope: Weyl-level weights and roots in the 12052 model.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12066_time_turns_triality import model, orbits  # noqa: E402

OUT = ROOT / "data" / "w33_pass12076_time_rotates_so10.json"


def main():
    checks, res = {}, {}
    M = model()
    G, p, nb, far, R, fib, L27, Adj, tick = M["G"], M["p"], M["nb"], M["far"], M["R"], M["fib"], M["L27"], M["Adj"], M["tick"]
    q = far[0]
    K = M["H"](p) & M["H"](q)
    orb = orbits([M["act27"](g) for g in G[K]], 27)
    eights = [sorted(o) for o in orb if len(o) == 8]
    f = sorted(k for o in orb if len(o) == 1 for k in o)
    fam = {fi: next(e for e in eights if all(int(round(3 * L27[fi] @ L27[x])) == -2 for x in e)) for fi in f}
    e6 = [i for x in nb for i in fib[x]]
    ok1, D5 = True, {}
    for i, fi in enumerate(f):
        Ri = [r for r in e6 if abs(R[r] @ L27[fi]) < 1e-9]
        D5[fi] = set(Ri)
        ip = {k: int(round(3 * L27[fi] @ L27[k])) for k in range(27)}
        ten = sorted(k for k in range(27) if ip[k] == -2)
        sixteen = sorted(k for k in range(27) if ip[k] == 1)
        others = [x for x in f if x != fi]
        ok1 &= len(Ri) == 40 and np.linalg.matrix_rank(R[Ri]) == 5
        ok1 &= ten == sorted(fam[fi] + others) and sixteen == sorted(fam[others[0]] + fam[others[1]])
    checks["each singlet: D5 = 40 E6 roots orthogonal (rank 5); 27 = 1 + 10 + 16 with 10_i = 8_i + f_j + f_k, 16_i = 8_j + 8_k"] = bool(ok1)
    d4 = set.intersection(*D5.values())
    common = [x for x in nb if Adj[q, x]]
    checks["the three D5 meet in the D4 of the four common neighbours (24 roots)"] = d4 == set(sum((fib[x] for x in common), []))
    ok2, cyc = True, set()
    for r in common:
        t = tick[r]
        a = M["act27"](t)
        sigma = tuple(f.index(a[fi]) for fi in f)
        cyc.add(sigma)
        for fi in f:
            img = {int(t[x]) for x in D5[fi]}
            ok2 &= img == D5[a[fi]]
    checks["the triality ticks cycle the singlets f_0 -> f_1 -> f_2 and carry D5_i onto D5_{sigma(i)}"] = bool(
        ok2 and cyc <= {(1, 2, 0), (2, 0, 1)} and len(cyc) >= 1)
    res["singlet_permutations_by_ticks"] = [list(c) for c in cyc]
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
