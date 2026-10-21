"""Passes 12136-12140: the end of S002's tachyon-free valley, the one-loop engine on three Wilson-line tori (T115), T115's
protected doublet, the complete lattice search for fraction-free hypercharges, and the transverse structure of S002's axis
(Claude track; engines of Passes 11106/11107).

12136 -- S002 below Im T_WL = 0.7 (T* = rho; winding cut-off checked: K = 2 and 3 agree to 1e-8 at 0.8i). Lambda/M^4 on the
  imaginary axis: 0.9i 170.1, 0.8i 145.3, 0.6i 115.8, 0.55i 115.4, 0.5i 119.6, 0.4i 149.0 -- a MINIMUM near Im T_WL = 0.55,
  still positive. The 11107 enumerator (cut-offs raised; control model 2 Delta = -0.2113 reproduced) finds the whole axis
  3i ... 0.3i tachyon-free.
12140 -- but the axis is not a valley. Off the axis the same level turns tachyonic, linearly in |Re T_WL|: Delta = -0.025,
  -0.047, -0.110, -0.131 at Re T_WL = 0.05, 0.1, 0.3, 0.5 (Im 0.55); at Im 0.9 the strip is wider (Re 0.1 clean, Re 0.2
  tachyonic) and Lambda falls off the axis (170.1 -> 168.5 at Re 0.1). The level is MARGINAL exactly on the axis, so the
  B-field direction is tachyonic there: the axis minimum is a saddle, and the off-axis Lambda < 0 values (0.3 + 0.55i: -132,
  0.5 + 0.55i: -441) are void (tachyonic region; their integrand grows).
12137 -- the 11106 engine generalised to t Wilson-line tori (WLPartN; control: S002 with its free torus as a third torus with
  W = 0 reproduces the two-torus engine to 2e-10) and the 11107 enumerator to three tori (control: S002's 56 states at rho
  with Delta = -1/18, none at 2i). T115 (all three tori carry Wilson lines): integrand modular invariant to 1e-13;
  Lambda/M^4 = +987.6 at T_WL = (2i,2i,2i) and +663.8 at 1.75i; tachyon-free at 3i, 2i, 1.75i, tachyonic at 1.5i (10 states,
  Delta = -0.067) and 1.25i (12 states, -0.139); the value at (i,i,i) (Lambda < 0) is void, its integrand grows.
12138 -- T115's last light doublet pair: adding quintic psi psi <s><s><s> terms (gauge + space group) leaves the rank at 5 of 6;
  the allowed-entry pattern has STRUCTURAL rank 5 (Hall deficiency), so no coefficients lift it at any order these rules allow
  up to quintic -- a selection-rule block structure protects one vector-like lepton doublet.
12139 -- the complete fraction-free search (12131 criterion: v = q +- lambda in E8 x E8, v.r fixed for every nonabelian root,
  all lattice vectors with N <= 12, halves hash-joined on the colour-singlet charge residues; E8 shells 1, 240, ..., 60480
  exact). Control: every strict (12121-type) fraction-free hypercharge commuting with all nonabelian factors is recovered
  (19/19). CORRECTION to 12126: its fraction-free counts (11/22/4/14, 'none in S002') were complete only inside the strict
  search class -- the lattice search finds 4 / 45 / 59 commuting ones in S033 / S053 / T115 and THREE in S002 (k_Y = 41/3),
  all on the k_Y = 5/3 + 4n law. The 104 A8 models of 11095: fraction-free hypercharges exist in 102 (10920 to N <= 12), all
  with k_Y >= 17/3 -- none at 5/3. So on BOTH routes charge quantisation costs k_Y >= 17/3, and the canonical k_Y = 5/3 of the A8
  models always comes with fractionally charged states.
"""

import json
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12136_to_12140_valley_three_tori_quintic_lattice.json"
D = ROOT / "analysis" / "search_drivers_12136"
D31 = ROOT / "analysis" / "search_drivers_12131"


def lam(p):
    return json.loads(p.read_text())["Lambda_over_M4"]


def main():
    checks, res = {}, {}
    ax = {"0.9j": lam(D / "oneloop_N004_F1_03_S002_0.9j_rho_K2.json"), "0.8j": lam(D / "oneloop_N004_F1_03_S002_0.8j_rho_K3.json"),
          "0.6j": lam(D / "oneloop_N004_F1_03_S002_0.6j_rho_K3.json"), "0.55j": lam(D / "oneloop_N004_F1_03_S002_0.55j_rho_K4.json"),
          "0.5j": lam(D / "oneloop_N004_F1_03_S002_0.5j_rho_K4.json"), "0.4j": lam(D / "oneloop_N004_F1_03_S002_0.4j_rho_K4.json")}
    k2 = lam(D31 / "oneloop_N004_F1_03_S002_0.8j_rho.json")
    t3 = json.loads((D / "s002tach3.json").read_text())
    res["12136"] = dict(Lambda_axis=ax, K2_vs_K3_at_08i=[k2, ax["0.8j"]], tachyons=t3)
    checks["12136: winding cut-off converged (K = 2 vs 3 at 0.8i, 1e-6 relative)"] = abs(k2 / ax["0.8j"] - 1) < 1e-6
    checks["12136: Lambda on the axis has a positive minimum near Im T_WL = 0.55 (0.6i > 0.55i < 0.5i, all > 0)"] = (
        ax["0.6j"] > ax["0.55j"] < ax["0.5j"] < ax["0.4j"] and ax["0.9j"] > ax["0.8j"] > ax["0.6j"] and min(ax.values()) > 0)
    checks["12136: control Delta = -0.2113 reproduced; S002 tachyon-free on the axis 0.8i .. 0.3i"] = (
        abs(t3["control_model2_ImT1"] + 0.21132486540518758) < 1e-9 and all(t3[k]["n"] == 0 for k in ("0.8i", "0.6i", "0.5i", "0.4i", "0.3i")))
    # 12140
    tc = json.loads((D / "tachC.json").read_text())
    te = json.loads((D / "tachE.json").read_text())
    off = {"0.1+0.9j": lam(D / "oneloop_N004_F1_03_S002_0.1+0.9j_rho_K2.json"), "0.2+0.9j": lam(D / "oneloop_N004_F1_03_S002_0.2+0.9j_rho_K2.json"),
           "0.3+0.55j": lam(D / "oneloop_N004_F1_03_S002_0.3+0.55j_rho_K4.json"), "0.5+0.55j": lam(D / "oneloop_N004_F1_03_S002_0.5+0.55j_rho_K4.json")}
    res["12140"] = dict(tachyons_055=dict(tc, **te), tachyons_09={k: t3[k] for k in ("0.1+0.9i", "0.2+0.9i")}, Lambda_off_axis=off)
    d = [te["0.05+0.55i"]["Delta"], tc["0.1+0.55i"]["Delta"], tc["0.3+0.55i"]["Delta"], tc["0.5+0.55i"]["Delta"]]
    checks["12140: at Im 0.55 the axis is the only tachyon-free line: Delta < 0 at Re 0.05, 0.1, 0.3, 0.5 (monotone in |Re|), 0 on the axis"] = (
        tc["0.55i"]["n"] == 0 and all(x < 0 for x in d) and d[0] > d[1] > d[2] > d[3])
    checks["12140: at Im 0.9 Re 0.1 clean and lower than the axis (168.5 < 170.1: a ridge), Re 0.2 tachyonic; off-axis Lambda < 0 points are tachyonic (void)"] = (
        t3["0.1+0.9i"]["n"] == 0 and off["0.1+0.9j"] < ax["0.9j"] and t3["0.2+0.9i"]["n"] > 0
        and off["0.3+0.55j"] < 0 and off["0.5+0.55j"] < 0 and tc["0.3+0.55i"]["n"] > 0 and tc["0.5+0.55i"]["n"] > 0)
    # 12137
    w3 = json.loads((D / "wl3_control.json").read_text())
    mc = json.loads((D / "oneloop3_T115_modcheck.json").read_text())
    tt = json.loads((D / "tach3.json").read_text())
    L2 = json.loads((D / "oneloop3_T115_2j_2j_2j.json").read_text())
    L175 = json.loads((D / "oneloop3_T115_1.75j_1.75j_1.75j.json").read_text())
    L1 = json.loads((D / "oneloop3_T115_1j_1j_1j.json").read_text())
    res["12137"] = dict(control=w3, modcheck=mc, tachyons=tt, Lambda={"2i": L2["Lambda_over_M4"], "1.75i": L175["Lambda_over_M4"], "i (void)": L1["Lambda_over_M4"]})
    checks["12137: three-torus engine = two-torus engine on S002 (2e-10); T115 integrand modular invariant (1e-13)"] = (
        list(w3.values())[0]["rel"] < 1e-9 and max(mc.values()) < 1e-12)
    checks["12137: three-torus tachyon enumerator control (S002: 56 at rho, Delta -1/18; none at 2i)"] = (
        tt["control_S002_rho"]["n"] == 56 and abs(tt["control_S002_rho"]["Delta"] + 1 / 18) < 1e-9 and tt["control_S002_2i"] == 0)
    checks["12137: T115 Lambda/M^4 = +987.6 (2i), +663.8 (1.75i); tachyon-free 3i/2i/1.75i, tachyonic 1.5i/1.25i; (i,i,i) value void (growing integrand)"] = (
        abs(L2["Lambda_over_M4"] - 987.58) < 0.1 and abs(L175["Lambda_over_M4"] - 663.84) < 0.1
        and all(tt["T115_" + k]["n"] == 0 for k in ("3i", "2i", "1.75i")) and tt["T115_1.5i"]["n"] == 10 and tt["T115_1.25i"]["n"] == 12
        and L1["I_beta"]["c_top"] > 1000 and L2["I_beta"]["c_top"] < 0)
    # 12138
    e5 = json.loads((D / "exomass5.json").read_text())["N008_F1_04_S037_T115"]["classes"]["(1, 2, Fraction(1, 2))"]
    pat = json.loads((D / "t115_doublet_pattern.json").read_text())
    checks["12138: T115 doublet class: rank 5 of 6 up to quintic (24 quintic entries), structural rank of the allowed pattern = 5"] = (
        e5["need"] == 6 and e5["rank_up_to_quintic"] == 5 and e5["n_quintic_entries"] == 24 and pat["structural_rank"] == 5)
    # 12139
    lc = json.loads((D / "latctrl.json").read_text())
    lf = json.loads((D / "latff_control.json").read_text())
    res["12139_control"] = lc
    res["12139_e6a2_lattice"] = {m: dict(n=v["n"], kY=v["kY"]) for m, v in lf.items()}
    checks["12139: control -- every strict fraction-free hypercharge commuting with all nonabelian factors is found (19/19)"] = (
        sum(v["strict_commuting"] for v in lc.values()) == 19 and all(v["strict_commuting"] == v["strict_commuting_found_by_lattice"] for v in lc.values()))
    checks["12139: lattice search finds 4/45/59/3 commuting fraction-free hypercharges (S033/S053/T115/S002), all k_Y = 5/3 + 4n"] = (
        [lf[m]["n"] for m in ("N008_F1_03_S033", "N008_F1_02_S053", "N008_F1_04_S037_T115", "N004_F1_03_S002")] == [4, 45, 59, 3]
        and all((Fr(k) - Fr(5, 3)) % 4 == 0 and Fr(k) > Fr(5, 3) for v in lf.values() for k in v["kY"]))
    a8p = D / "latff_a8.json"
    if a8p.exists():
        a8 = json.loads(a8p.read_text())
        nff = sum(1 for v in a8.values() if v["n_fraction_free"])
        res["12139_a8"] = dict(models=len(a8), with_fraction_free=nff, kY=sorted({k for v in a8.values() for k in v["kY"]}, key=Fr))
        checks["12139: A8 models (N <= 12, 104/104): fraction-free hypercharges in 102 (10920 total), every k_Y = 5/3 + 4n, minimum 17/3 -- never 5/3"] = (
            len(a8) == 104 and nff == 102 and sum(v["n_fraction_free"] for v in a8.values()) == 10920
            and all((Fr(k) - Fr(5, 3)) % 4 == 0 for v in a8.values() for k in v["kY"])
            and min(Fr(k) for v in a8.values() for k in v["kY"]) == Fr(17, 3))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
