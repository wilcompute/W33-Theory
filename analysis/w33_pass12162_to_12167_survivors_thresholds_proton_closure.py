"""Passes 12162-12167: the survivors' exotic thresholds, proton decay at the fitted scales, the scalar-10 search on the other torus,
the Fricke partner, and the closure of the T^6/Z3 SO(16)xSO(16) W(3,3) route (Claude track; survivors of 11101/11106).

12162 -- intermediate-scale thresholds of the 12 survivors (one-loop b_a of the full massless spectrum on their own hypercharge,
  Delta b = total - SM). (a) M_s fixed at the heterotic value g_U 5.27e17 GeV, coloured and colourless exotics at independent
  scales: the three couplings then require EVERY survivor's exotics ABOVE M_s (M_c, M_l > M_s, 12/12) -- the exotics push the
  couplings the wrong way. (b) one common exotic scale, M_s free: consistent (0 <= ln M_s/M_X <= ln M_s/M_Z) only for survivors
  2, 15, 77, at M_s ~ 1.2e13, 1.1e12, 3.6e11 GeV with M_X ~ 1e6-2e8 GeV -- far below the perturbative heterotic scale.
12166 -- and that low-scale escape is closed by the proton: in all three, 6 colour-triplet scalar components (Y = -+1/3) carry BOTH a
  diquark and a leptoquark trilinear coupling under the full rules (exact H-momentum); exchanged at 1e6-1e8 GeV they give a
  proton lifetime of years, against > 1e34 yr. With the triplets pushed to >~ 1e15 GeV the fit reverts to (a).
12163 -- the scalar-10 search on the third torus: 121 SU(5) x U(1) models, 52 with three generations, scalar 10: 0/121 (with 12161:
  0/185) -- the flipped-SU(5) Higgs never appears on the e6+a2 route.
12164 -- the Fricke partner (12158) is NOT a sign flip: S002 with W -> -W (both tori), W -> 2W, W -> -W on the family or the second
  torus alone, all reproduce S002's own multiplicities at 0.52i (272 at 0.1519, 104 at 0.1869), not the swapped ones of 0.641i.
  The duality T -> -1/(3T) maps S002 to a model outside these simple transformations (open).
12165 -- charm-up: with the calibrated rules the up-type rank stays 1 through quartic order in all 16 crossed models (12159),
  consistent with the all-order AG(3,3) protection of 11102; lifting it needs spontaneous breaking of that reflection by the
  scalar potential, which is not computed here.
12167 -- CLOSURE of the T^6/Z3 SO(16) x SO(16) W(3,3) route as a realistic Standard Model, on three independent grounds:
  (i) fraction-free hypercharges have k_Y >= 17/3 and fail the Weinberg angle (12154, 12156);
  (ii) canonical k_Y = 5/3 with fractional states lifted (11097-11102): no threshold at the heterotic scale from the exotics
  (12162a), and the only low-scale fits need light leptoquark-diquark scalars (12166);
  (iii) the Wen-Witten escape (field-theoretic GUT breaking) needs a 10_H that never appears (12161, 12163).
  What survives as structure: three chiral generations from the e6+a2 shift, the Fricke-symmetric Witten levels, Witten-parity
  protection, and k_Y = 5/3 + 4n from self-duality.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12162_to_12167_survivors_thresholds_proton_closure.json"
D = ROOT / "analysis" / "search_drivers_12162"


def main():
    checks, res = {}, {}
    s2 = json.loads((D / "survthresh2.json").read_text())
    s1 = json.loads((D / "survthresh.json").read_text())
    res["12162a"] = {k: dict(Ms=v["Ms_GeV"], Mc=v["Mc_GeV"], Ml=v["Ml_GeV"]) for k, v in s2.items()}
    checks["12162: M_s at the heterotic scale -> every survivor needs its exotics above M_s (12/12 inconsistent)"] = (
        len(s2) == 12 and all(not v["consistent"] for v in s2.values()) and all(v["Mc_GeV"] > v["Ms_GeV"] or v["Ml_GeV"] > v["Ms_GeV"] for v in s2.values()))
    good = sorted(k for k, v in s1.items() if v["fit"]["consistent"])
    res["12162b"] = {k: dict(Ms=s1[k]["fit"]["Ms_GeV"], MX=s1[k]["fit"]["MX_GeV"]) for k in good}
    checks["12162: single exotic scale consistent only for survivors 2, 15, 77, with M_s < 2e13 GeV and M_X < 1e9 GeV"] = (
        good == ["15", "2", "77"] and all(s1[k]["fit"]["Ms_GeV"] < 2e13 and s1[k]["fit"]["MX_GeV"] < 1e9 for k in good))
    pt = json.loads((D / "protonT.json").read_text())
    res["12166"] = {k: {kk: v for kk, v in x.items() if kk != "detail"} for k, x in pt.items()}
    checks["12166: in 2, 15, 77 six colour-triplet scalar components couple both as diquark and leptoquark (full rules)"] = (
        sorted(pt) == ["15", "2", "77"] and all(x["both"] == 6 for x in pt.values()))
    f3 = json.loads((D / "flipscan2_21_third.json").read_text())
    a4 = [r for r in f3 if "net10" in r]
    res["12163"] = dict(su5_models=len(a4), three_generation=sum(1 for r in a4 if abs(r["net10"]) == 3), scalar10=sum(r["scalar10"] for r in a4))
    checks["12163: third torus: 121 SU(5)xU(1) models, 52 three-generation, no scalar 10"] = (
        len(a4) == 121 and res["12163"]["three_generation"] == 52 and res["12163"]["scalar10"] == 0)
    pj = D / "partner.json"
    if pj.exists():
        p = json.loads(pj.read_text())
        orig = p["orig@0.5200"]
        swapped = p["orig@0.6410"]
        flips = {k: v for k, v in p.items() if not k.startswith("orig")}
        res["12164"] = p
        checks["12164: no sign-flip candidate reproduces the swapped (partner) multiplicities; all equal S002's own at 0.52i"] = (
            orig != swapped and all(v == orig for v in flips.values()) and len(flips) >= 4)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
