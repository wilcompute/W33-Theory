"""Passes 12131-12135: the k_Y law from lattice self-duality, the one-loop moduli potential of S002 and its tachyon-free
window, exotic masses to quartic order, down-sector mixing in the A8 models, and a third Wilson line on S002 (Claude track).

12131 -- if the whole lattice spectrum has quantised charges, q +- lambda lies in Lambda = E8 x E8 (q = a_L/2 + y the charge
  vector, lambda a colour fundamental weight; Lambda self-dual), so N = (q +- lambda)^2 = 1/2 + y^2 + 2/3 is EVEN:
  k_Y = 2 y^2 = 2N - 7/3 = 5/3 + 4n (this is Schellekens's 1990 self-duality argument, specialised). Checked on all 51
  fraction-free hypercharges of 12126: q +- lambda in Lambda with N in {4, 6, 8, 10, 12, 18, 36}. k_Y = 5/3 <=> q +- lambda is a
  ROOT; enumerating all 480 roots gives exactly 24 admissible hypercharges per model and none yields the SM spectrum
  (5/5 models): a fraction-free k_Y = 5/3 is impossible here, not just unfound.
12132 -- S002's one-loop potential (11106 engine) and tachyons (11107 enumerator; controls: model 2 Delta = -0.2113 at
  Im T = 1, none at large radius). Lambda/M^4 > 0 everywhere sampled; it falls as the Wilson-line tori shrink
  (3i: 1475 ... i: 199, 0.8i: 145 -- no T-duality turnaround, so T_WL = i is not a minimum) and is lowest at T* = rho
  among the family-modulus points. Unlike every A8 survivor of 11106/11107 (all tachyonic by Im T_WL = 1 except model 77),
  S002 is TACHYON-FREE along the whole imaginary T_WL axis sampled (3i .. 0.7i). Off the axis a tachyon appears: on the
  arc |T_WL| = 1 between 80 and 75 degrees (56 states; Delta = -0.012 at 75, -0.043 at 65, -1/18 at rho), so the Lambda
  values at the arc point and at rho are void. The Wilson-line moduli roll toward small radius with Lambda > 0; no
  minimum was found, and the dilaton tadpole remains.
12133 -- exotic masses up to quartic order (psi psi <s> with all rules, psi psi <s1><s2> with gauge + space group only, so
  a lift is an upper bound and a remaining light state is robust): T115 goes from 7 light vector-like pairs (trilinear)
  to ONE (a lepton-doublet pair); S002 from 41 to 12, including 9 pairs of charge +-1/3 that stay massless.
12134 -- down-sector mixing in the 104 A8 models (their nsosm hypercharge, local couplings as in 11098): reproduces 11098
  exactly (no tree-level down Yukawa in 77, rank 3 in 27) and mixing changes nothing -- in the 77 models no D-type state
  (chiral or vector-like) has a Q D H coupling; the local trilinear singlet couplings lift all vector-like d^c pairs in only
  8 of the 92 models that have them.
12135 -- NEGATIVE: a third Wilson line on S002 (250 candidates, 78 load) never gives SU(3) x SU(2) x U(1) (no first-E8
  A2 + A1), so S002's Yukawa mechanism and T115's gauge group are not combined by one more line.
"""

import json
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12131_to_12135_kY_law_moduli_exotics.json"
D = ROOT / "analysis" / "search_drivers_12131"


def lam(name):
    return json.loads((D / ("oneloop_N004_F1_03_S002_%s.json" % name)).read_text())["Lambda_over_M4"]


def main():
    checks, res = {}, {}
    k = json.loads((D / "kylaw.json").read_text())
    res["12131"] = k
    checks["12131: all 51 fraction-free hypercharges have q +- lambda in E8 x E8 with even N = 1/2 + y^2 + 2/3"] = (
        sum(v["n_fraction_free"] for v in k.values()) == 51 and all(v["all_in_lattice"] and v["N_matches_formula"] for v in k.values())
        and all(Fr(n) % 2 == 0 for v in k.values() for n in v["N_values"]))
    checks["12131: k_Y = 5/3 root test: 24 admissible roots per model, none gives the SM (5/5)"] = (
        len(k) == 5 and all(v["root_candidates_kY_5_3"] == 24 and v["root_candidates_giving_SM"] == 0 for v in k.values()))
    # 12132
    pts = {n: lam(n) for n in ["3j_rho", "2.5j_rho", "2j_rho", "1.75j_rho", "1.5j_rho", "1.25j_rho", "1j_rho", "0.8j_rho", "2j_1j", "2j_1.5j", "2j_2j"]}
    arc = lam("arc75_rho")
    t1 = json.loads((D / "s002tach.json").read_text())
    t2 = json.loads((D / "s002tach2.json").read_text())
    ta = json.loads((D / "s002arc.json").read_text())
    res["12132"] = dict(Lambda=pts, Lambda_arc_75deg=arc, tachyons_axis=t1, tachyons_more=t2, tachyons_arc=ta)
    axis = [pts[n] for n in ["3j_rho", "2.5j_rho", "2j_rho", "1.75j_rho", "1.5j_rho", "1.25j_rho", "1j_rho", "0.8j_rho"]]
    checks["12132: Lambda > 0 at every sampled point; falls monotonically along T_WL = 3i ... 0.8i (no duality turnaround at i); T* = rho lowest of the family points"] = (
        all(v > 0 for v in pts.values()) and all(a > b for a, b in zip(axis, axis[1:]))
        and pts["2j_rho"] < min(pts["2j_1j"], pts["2j_1.5j"], pts["2j_2j"]))
    checks["12132: controls (model 2: Delta = -0.2113 at Im T = 1, none at large radius); S002 tachyon-free on the imaginary axis 3i..0.7i, tachyonic at T_WL = rho (Delta = -1/18)"] = (
        abs(t1["control_model2_ImT1"] + 0.21132486540518758) < 1e-9 and t1["control_model2_large"] == 0
        and all(v["n"] == 0 for kk, v in t1.items() if kk.startswith("S002"))
        and all(t2[n]["n"] == 0 for n in ["0.9i_rho", "0.8i_rho", "0.7i_rho", "i_i", "2i_i", "1.25i_2i"])
        and t2["rho_rho"]["n"] == 56 and abs(t2["rho_rho"]["Delta"] + 1 / 18) < 1e-9)
    checks["12132: tachyon onset on the arc |T_WL| = 1 between 80 and 75 degrees (85, 80 clean; 75, 70, 65 tachyonic)"] = (
        ta["85"]["n"] == 0 and ta["80"]["n"] == 0 and all(ta[d]["n"] == 56 and ta[d]["Delta"] < 0 for d in ("75", "70", "65")))
    # 12133
    e = json.loads((D / "exomass4.json").read_text())
    s = e["N004_F1_03_S002"]["classes"]["(1, 1, Fraction(1, 3))"]
    checks["12133: light vector-like pairs trilinear -> quartic: T115 7 -> 1, S002 41 -> 12 (9 charge-1/3 pairs stay)"] = (
        e["N008_F1_04_S037_T115"]["light_trilinear"] == 7 and e["N008_F1_04_S037_T115"]["light_up_to_quartic"] == 1
        and e["N004_F1_03_S002"]["light_trilinear"] == 41 and e["N004_F1_03_S002"]["light_up_to_quartic"] == 12 and s["rank_up_to_quartic"] == 0 and s["need"] == 9)
    # 12134
    a = json.loads((D / "a8down.json").read_text())
    checks["12134: A8 down sector: 11098 reproduced (77 none / 27 rank 3); vector-like mixing changes no rank; all vector-like d^c lifted in 8/92"] = (
        len(a) == 104 and all(v["nQ"] == 3 for v in a.values()) and sum(v["rank_light"] == 0 for v in a.values()) == 77
        and sum(v["rank_light"] == 3 for v in a.values()) == 27 and all(v["rank_light"] == v["rank_Yuk_all_D"] for v in a.values())
        and sum(1 for v in a.values() if v["nDb"]) == 92 and sum(1 for v in a.values() if v["nDb"] and v["rank_M"] == v["nDb"]) == 8)
    # 12135
    s4 = json.loads((D / "smwl4_9.json").read_text())
    ld = [r for r in s4 if r["gauge"] != "LOADFAIL"]
    firsts = {r["gauge"].split(" and ")[0].split(" NU1")[0].strip() for r in ld}
    res["12135"] = dict(attempts=len(s4), loaded=len(ld), first_E8_groups=sorted(firsts))
    checks["12135: third Wilson line on S002: 250 attempts, 78 load, no first-E8 A2 + A1"] = len(s4) == 250 and len(ld) == 78 and "A2 + A1" not in firsts
    checks = {kk: bool(v) for kk, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
