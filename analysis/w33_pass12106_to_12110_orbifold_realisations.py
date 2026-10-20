"""Passes 12106-12110: realising the clock gradings as heterotic orbifolds (Claude track; 12091-12105).

12106 -- the non-SUSY realisation. Z2W x Z3 (Witten Z2 = (-1)^F x split shift, Z3 twist (1/3,1/3,-2/3)), corpus N = 0
  engine (patched orbifolder 1.2.1, nsdump_v2). V0 = (sigma lift; split lift) -- the split fermion parity of 12085 in
  both E8s, as in the corpus SO(16)^2 route -- and V1 = a three-family e6+a2 order-3 shift (12091) + second-E8 part.
  Control: the stock Z3_1_1 model gives SO(10) x SU(3) x SO(16) x U(1) and net 36 left-handed 16s (known).
  Scan (24 attempts, 13 loaded): every loaded model with an SO(10) x SU(3) factor (6 of 13, in either E8) has net
  left-handed (16, 3bar) = 3 copies, i.e. 9 chiral 16s; the other 7 (SU(6) x SU(2)^2 in both E8s) have no 16 at all.
  So the untwisted per-plane count of 12091 (N = 3) survives the full orbifold, multiplied by the three untwisted planes:
  three copies of a family TRIPLET (16, 3bar), not three generations. Tachyon content was not checked (the engine dump
  has no tachyon code).
12107 -- where the family number lives. In the non-SUSY models the total (9) equals the untwisted count (3 per plane x 3
  planes), so the twisted sectors add only vector-like matter. In the SUSY Z6-II models of 12101 (re-counted with
  representation dimensions) the totals are 0 or +-1 -- there the twisted sectors cancel the untwisted chirality.
12108 -- OPEN: the 24 Z6-II models rejected by the orbifolder ('orbifold group ill-defined') satisfy every global and
  every local level-matching condition N_loc(V_loc^2 - v_loc^2) in 2Z for all (theta^k, n5 e5 + n6 e6) that I tested;
  the separating condition is not one of these and remains unidentified.
12109 -- the corpus's Standard Models ARE clock/split gradings. All 87 distinct corpus Z6-I non-SUSY/SUSY A8 Standard
  Models (~/orb/ns87, frozen copies in search_drivers_12109): the order-2 part 3V of the order-6 shift is a CLOCK in one
  E8 and a SPLIT in the other (never two clocks, two splits or trivial), and the order-3 Wilson line has fixed algebra
  e6 + a2 -- the three-family type -- in both E8s.
12110 -- the (27, 6bar) family Higgs cannot be massless at level 1. With h = C2/(2(k + h^vee)) (roots of norm 2):
  h(27 of E6) = (4/3 + 16)/26 = 2/3, h(6bar of SU(3)) = (8/3 + 4)/8 = 5/6, so h(27, 6bar) = 3/2 > 1; by contrast
  h(27, 3) = 2/3 + 1/3 = 1 (massless). The family masses that 11271 says need a (27, 6bar) must therefore come from
  higher-dimension operators or higher-level embeddings (classical level-1 rule: Font-Ibanez-Quevedo; Dienes).
"""

import itertools
import json
import re
import sys
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12106_to_12110_orbifold_realisations.json"
D6 = ROOT / "analysis" / "search_drivers_12106"
D9 = ROOT / "analysis" / "search_drivers_12109"


def nsdump_counts(text):
    gauge = re.search(r"GAUGE (.*)", text)
    left16 = 0
    for m in re.finditer(r"F m=(\d+) dim=([^ ]+) x(\d+)", text):
        mult, dims, k = int(m.group(1)), m.group(2).split(","), int(m.group(3))
        if mult != 2:
            continue
        for pos, d in enumerate(dims):
            if d.lstrip("-") == "16":
                w = 1
                for q, e in enumerate(dims):
                    if q != pos:
                        w *= int(re.match(r"-?(\d+)", e).group(1))
                left16 += k * w if not d.startswith("-") else -k * w
    return gauge.group(1).strip() if gauge else None, left16


def main():
    checks, res = {}, {}
    g0, n0 = nsdump_counts((D6 / "control_z3_standard.out").read_text())
    checks["12106 control: stock Z3_1_1 gives D5 + A2 and D8 (SO(10) x SU(3) x SO(16) x U(1)) and net 36 left-handed 16s"] = (
        g0 == "D5 + A2 and D8 NU1 1" and n0 == 36)
    rows = {}
    for lab in ("N001", "N004", "N008", "N010", "N011", "N019", "N003"):
        rows[lab] = nsdump_counts((D6 / (lab + ".out")).read_text())
    res["12106_models"] = {k: dict(gauge=v[0], net_left_16=v[1]) for k, v in rows.items()}
    so10 = [k for k, v in rows.items() if "D5 + A2" in v[0]]
    checks["12106: every frozen model with SO(10) x SU(3) has net 9 left-handed 16s (= 3 x (16,3bar)); SU(6)xSU(2)^2 model has none"] = (
        len(so10) == 6 and all(rows[k][1] == 9 for k in so10) and rows["N003"][1] == 0)
    scan = json.loads((D6 / "nsscan_5.json").read_text())
    loaded = [r for r in scan if r["gauge"] != "LOADFAIL"]
    checks["12106: scan 24 attempts, 13 loaded, 6 with an SO(10) x SU(3) factor"] = (
        len(scan) == 24 and len(loaded) == 13 and sum("D5 + A2" in r["gauge"] for r in loaded) == 6)
    z6 = json.loads((D6 / "z6recount_3.json").read_text())
    checks["12107: SUSY Z6-II accepted models, dimension-weighted: net 16s/27s only 0 or +-1"] = all(
        all(abs(v) <= 1 for v in r[2].values()) for r in z6) and len(z6) == 12
    # 12109
    g = Gradings()
    R = g.R
    kind = {s.tobytes(): k for k, s in zip(g.kinds, g.vecs)}
    models = set()
    for f in sorted(D9.glob("susy_*.txt")):
        t = f.read_text()
        for blk in t.split("begin model")[1:]:
            rws = blk.split("Shifts and Wilsonlines:")[1].split("end model")[0].strip().split("\n")
            models.add(tuple(tuple(Fr(x.strip()) for x in r.split(",")) for r in rws))

    def z2class(v8):
        a = np.array([float(x) for x in v8])
        par = np.round(2 * (R @ a)).astype(int) % 2 == 1
        return "trivial" if not par.any() else kind.get(par.tobytes(), "other")

    def z3fixed(v8):
        a = np.array([float(x) for x in v8])
        return g.typ(np.round(3 * (R @ a)).astype(int) % 3 == 0)
    tab = Counter()
    for m in models:
        V, W = m[0], m[6]
        z2 = tuple(sorted(z2class([3 * x for x in V[p]]) for p in (slice(0, 8), slice(8, 16))))
        wl = tuple(z3fixed(list(W[p])) for p in (slice(0, 8), slice(8, 16)))
        tab[(z2, wl)] += 1
    res["12109"] = {str(k): v for k, v in tab.items()}
    checks["12109: all 87 corpus A8 Standard Models: Z2 part = one clock + one split; Wilson line e6 + a2 in both E8s"] = (
        len(models) == 87 and tab == Counter({(("clock", "split"), (("A2", "E6"), ("A2", "E6"))): 87}))
    # 12110
    A2 = np.array([v for v in itertools.product([-1, 0, 1], repeat=3) if sum(v) == 0 and sum(x * x for x in v) == 2], float)
    mu = np.array([2 / 3, -1 / 3, -1 / 3])
    lam6 = 2 * mu
    pos = [a for a in A2 if (a @ np.array([3, 2, 1])) > 0]
    C2_6 = float(lam6 @ lam6) + float(sum(lam6 @ a for a in pos))
    h6 = Fr(C2_6).limit_denominator(100) / (2 * (1 + 3))
    C2_3 = float(mu @ mu) + float(sum(mu @ a for a in pos))
    h3 = Fr(C2_3).limit_denominator(100) / (2 * (1 + 3))
    h27 = (Fr(4, 3) + 16) / (2 * (1 + 12))
    res["12110"] = dict(h27=str(h27), h6=str(h6), h3=str(h3), h_27_6bar=str(h27 + h6), h_27_3=str(h27 + h3))
    checks["12110: h(27) = 2/3, h(6bar) = 5/6, h(27,6bar) = 3/2 > 1 (never massless at level 1); h(27,3) = 1"] = (
        h27 == Fr(2, 3) and h6 == Fr(5, 6) and h3 == Fr(1, 3) and h27 + h6 == Fr(3, 2) and h27 + h3 == 1)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
