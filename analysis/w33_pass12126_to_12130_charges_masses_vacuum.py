"""Passes 12126-12130: charge quantisation versus k_Y, the size of the rank-one Yukawas, exotic masses, the A8 models'
mixing channels, and the full one-loop vacuum energy (Claude track; continues 12121-12125, cites 11095-11106).

12126 -- the canonical hypercharge is absent. Y restricted to the Cartan of the parent so(10), orthogonal to SU(3)_c and
  SU(2)_L (a 2-plane containing the k_Y = 5/3 direction), with exotics allowed ANY charge if vector-like: no member gives
  the Standard-Model spectrum in any of the five models (27-74 candidates each; control: the evaluator accepts every
  strict solution of 12121). So 12121's 'k_Y never 5/3' is not an artefact of its strict search. Charge quantisation:
  fraction-free three-generation hypercharges (no fractionally charged state in the whole massless spectrum) exist in 4/5
  models (11, 22, 4, 14 of them; none in S002) and ALL have k_Y in {17/3, 29/3, 41/3, ...} = 5/3 + 4n, n >= 1: every pairwise
  difference of fraction-free hypercharges is integral on every state and of even norm (383/383 pairs). The smaller k_Y
  (11/3, 13/3, 14/3) always come with fractional charges. Contrast the A8 models (11095): k_Y = 5/3 with 144 fractional
  colourless states. In these models a fraction-free spectrum costs k_Y >= 17/3 (cf. Schellekens 1990, cited in 11024).
12127 -- S002's rank-one Yukawas: every up- and down-type coupling is U x T2 x T1 with u^c/d^c and the Higgs at the SAME
  fixed point (unsuppressed, gauge strength), the up-type Higgs at the 3 fixed points with first-torus label 0, the
  down-type at 6 with label 1 or 2, distinct scalars (no conjugate pair). So y_t ~ y_b ~ g and m_t/m_b = v_u/v_d, a
  ratio of vevs on geometrically separated fixed points; the chiral-vector-like mixing factor cancels in the ratio.
12128 -- exotic masses at trilinear order (psi psi <s>, SM-singlet scalars, all selection rules; numerical rank at random
  couplings, which BOUNDS the true rank from above): the direct SU(3) x SU(2) x U(1) model T115 has no fractional
  charge under its minimal-k_Y hypercharge; its vector-like d^c pair lifts, but 2 of 6 lepton-doublet pairs and 5 of 33
  charged-singlet pairs stay massless at this order. S002 leaves 41 pairs light, including fractional charges -5/3, 1/3, 2/3.
12129 -- the 104 A8 models of 11095, on their own hypercharge (nsosm): net 3 quark doublets in 104/104, NO vector-like
  Y = 1/6 doublet and NO vector-like u^c in any model (confirms 11098: the top-charm degeneracy cannot be lifted by
  renormalisable mixing); vector-like d^c pairs in 95/104; 41 models carry (3,2)_{-+5/6} pairs (X/Y-boson quantum numbers).
12130 -- vacuum energy. Correction: the field dumps omit the U(1) gauge bosons (as found in 11106 for 11099), so
  N_B - N_F gains 2 N_U1: corrected range over the 75 models [-432, -160] (four left-right models -372, -336, -300, -264;
  T115 -260; the SO(10) parents of 12117 -672..-480), still never zero. Full one-loop integral (11106 engine, all 36
  sectors) at T_WL = 2i, T* = rho: Lambda_4/M^4 = +677.6 for S002 (I_beta = -1274.5, I_twisted = -80.7), integrand modular
  invariant to 1e-11; control: 11106 model 2 gives 657.63 (11106: 657.6). Positive beyond the massless term.
"""

import json
import re
import sys
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12126_to_12130_charges_masses_vacuum.json"
D = ROOT / "analysis" / "search_drivers_12126"
D11 = ROOT / "analysis" / "search_drivers_12111"
D16 = ROOT / "analysis" / "search_drivers_12116"
D21 = ROOT / "analysis" / "search_drivers_12121"
LR = ["N004_F1_03_S002", "N008_F1_03_S033", "N008_F1_04_S037", "N008_F1_02_S053"]
T115 = "N008_F1_04_S037_T115"


def count(t):
    b = f = 0
    for m in re.finditer(r"^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]*) x(\d+)", t, re.M):
        c, k = int(m.group(1)), int(m.group(3))
        for e in m.group(2).split(","):
            if e:
                k *= int(re.match(r"-?(\d+)", e).group(1))
        b += k if c in (8, 9, 13, 14, 15, 16, 17, 18) else 0
        f += k if c in (19, 20) else 0
    return b + 2 * int(re.search(r"NU1 (\d+)", t).group(1)) - f


def a8():
    res = {}
    for fn in sorted((D / "a8").glob("*.sm")):
        t = fn.read_text()
        facs = re.findall(r"^FACTOR (\d+) (\w+)", t, re.M)
        a2 = [int(i) for i, n in facs if n == "A2"]
        a1 = [int(i) for i, n in facs if n == "A1"]
        raw = [(m.group(1), m.group(2).split(","), [float(x) for x in m.group(3).split(",")]) for m in re.finditer(r"^L (\S+) dim=(\S+) q=(\S+)", t, re.M)]
        qf = [r for r in raw if r[0] == "q"]
        yi = next(i for i in range(len(qf[0][2])) if all(abs(abs(r[2][i]) - 1 / 6) < 1e-9 for r in qf))
        L = [(dims, Fr(qs[yi]).limit_denominator(36)) for _, dims, qs in raw]
        best = None
        for c in a2:
            for l in a1:
                cnt = Counter()
                for dims, Y in L:
                    dc, dl = int(dims[c]), int(dims[l])
                    if abs(dc) in (1, 3):
                        rest = 1
                        for k, e in enumerate(dims):
                            if k not in (c, l):
                                rest *= abs(int(re.match(r"-?\d+", e).group(0)))
                        cnt[(dc, dl, Y)] += rest
                q = max(cnt.get((3, 2, Fr(1, 6)), 0) - cnt.get((-3, 2, Fr(-1, 6)), 0), cnt.get((-3, 2, Fr(1, 6)), 0) - cnt.get((3, 2, Fr(-1, 6)), 0), key=abs)
                if best is None or abs(q) > abs(best[0]):
                    best = (q, cnt)
        q, cnt = best
        vl = {}
        for name, key in (("Q", (3, 2, Fr(1, 6))), ("u", (-3, 1, Fr(-2, 3))), ("d", (-3, 1, Fr(1, 3))),
                          ("Q", (-3, 2, Fr(1, 6))), ("u", (3, 1, Fr(-2, 3))), ("d", (3, 1, Fr(1, 3)))):
            conj = (-key[0], key[1], -key[2])
            vl[name] = max(vl.get(name, 0), min(cnt.get(key, 0), cnt.get(conj, 0)))
        x56 = any(abs(dc) == 3 and dl == 2 and abs(Y) == Fr(5, 6) for (dc, dl, Y) in cnt)
        res[fn.stem] = dict(netQ=abs(q), vl=vl, x56=x56)
    return res


def main():
    checks, res = {}, {}
    # 12126
    ys = json.loads((D / "ystd.json").read_text())
    ff = json.loads((D / "fracdiff.json").read_text())
    fc = json.loads((D / "fraccheck.json").read_text())
    res["12126_so10_plane"] = {m: dict(candidates=v["n_candidates"], sm=v["n_sm"]) for m, v in ys.items()}
    res["12126_fraction_free"] = fc
    checks["12126: no hypercharge in the so(10)-Cartan plane (contains k_Y = 5/3) gives the SM spectrum, 5/5 models"] = (
        len(ys) == 5 and all(v["n_sm"] == 0 and v["n_candidates"] > 0 for v in ys.values()))
    kys = {k for v in fc.values() for k in v["kY_of_fraction_free"]}
    checks["12126: fraction-free hypercharges in 4/5 models (11/22/4/14, none in S002), all with k_Y = 5/3 + 4n, n >= 1"] = (
        [fc[m]["n_no_fractional"] for m in LR + [T115]] == [0, 11, 22, 4, 14]
        and all((Fr(k) - Fr(5, 3)) % 4 == 0 and Fr(k) > Fr(5, 3) for k in kys))
    checks["12126: every difference of two fraction-free hypercharges is integral on all states and of even norm (383 pairs)"] = (
        sum(v["pairs"] for v in ff.values()) == 383 and all(v["integral_differences"] == v["pairs"] == v["even_norm_differences"] for v in ff.values()))
    # 12127
    sy = json.loads((D / "s002yuk.json").read_text())
    up = [c for c in sy["couplings"] if c["kind"] == "up"]
    dn = [c for c in sy["couplings"] if c["kind"] == "down"]
    same_fp = all(all((a + b) % 3 == 0 for a, b in zip(c["c_fp"], c["H_fp"])) for c in sy["couplings"])
    checks["12127: S002 Yukawas all local (same fixed point); up Higgs at 3 points (torus-1 label 0), down at 6 (label 1,2); distinct scalars"] = (
        same_fp and len(up) == 3 and len(dn) == 6 and {c["H_fp"][0] for c in up} == {0} and {c["H_fp"][0] for c in dn} == {1, 2}
        and not sy["conjugate_pairs"] and not set(sy["up_higgs"]) & set(sy["down_higgs"]))
    # 12128
    ex = json.loads((D / "exomass.json").read_text())
    t = ex[T115]["classes"]
    res["12128_exotic_masses"] = {m: dict(unlifted=v["unlifted_pairs"]) for m, v in ex.items()}
    checks["12128: T115 at trilinear order: d^c pair lifts, 2/6 doublet pairs and 5/33 charged-singlet pairs stay light; S002 leaves 41"] = (
        t["(3, 1, Fraction(-1, 3))"]["ok"] and t["(1, 2, Fraction(1, 2))"]["need"] - t["(1, 2, Fraction(1, 2))"]["rank"] == 2
        and t["(1, 1, Fraction(-1, 1))"]["need"] == 33 and t["(1, 1, Fraction(-1, 1))"]["rank"] == 28 and ex["N004_F1_03_S002"]["unlifted_pairs"] == 41)
    # 12129 (recomputed from the frozen nsosm dumps)
    am = a8()
    res["12129_a8"] = dict(models=len(am), vl_Q=Counter(v["vl"]["Q"] for v in am.values()), vl_u=Counter(v["vl"]["u"] for v in am.values()),
                           vl_d_models=sum(1 for v in am.values() if v["vl"]["d"]), x56_models=sum(v["x56"] for v in am.values()))
    checks["12129: A8 models: net Q = 3 in 104/104, no vector-like Y=1/6 doublet or u^c anywhere, vector-like d^c in 95, (3,2)_5/6 pairs in 41"] = (
        len(am) == 104 and all(v["netQ"] == 3 for v in am.values()) and all(v["vl"]["Q"] == 0 and v["vl"]["u"] == 0 for v in am.values())
        and res["12129_a8"]["vl_d_models"] == 95 and res["12129_a8"]["x56_models"] == 41)
    # 12130 (recount, U(1) gauge bosons included)
    bf = {}
    for p in sorted((D16 / "smwl").glob("*.out")) + sorted((D21 / "smwl3").glob("*.out")):
        tx = p.read_text()
        if "GAUGE" in tx:
            bf[p.stem] = count(tx)
    par = {b: count((D11 / (b + "_9.out")).read_text()) for b in ["N001_F1_04", "N004_F1_03", "N004_F1_04", "N004_F1_05", "N008_F1_02", "N008_F1_03", "N008_F1_04"]}
    res["12130_NB_minus_NF_corrected"] = dict(range=[min(bf.values()), max(bf.values())], left_right=[bf[m] for m in LR], T115=bf[T115], so10_parents=par)
    checks["12130: corrected N_B - N_F (with U(1) gauge bosons) in [-432, -160] over 75 models, never zero; LR -372/-336/-300/-264"] = (
        len(bf) == 75 and min(bf.values()) == -432 and max(bf.values()) == -160 and [bf[m] for m in LR] == [-372, -336, -300, -264])
    ol = {p.stem: json.loads(p.read_text()) for p in sorted(D.glob("oneloop_*_2j.json"))}
    mc = json.loads((D / "oneloop_S002_modcheck.json").read_text())
    res["12130_one_loop"] = {k: dict(I_beta=v["I_beta"]["I"], I_twisted=v["I_twisted"]["I"], Lambda_over_M4=v["Lambda_over_M4"]) for k, v in ol.items()}
    ctrl = next(v for k, v in ol.items() if "model2" in k)
    s002 = next(v for k, v in ol.items() if "S002" in k)
    checks["12130: control -- 11106 model 2 at T_WL = 2i, T* = rho reproduced (Lambda/M4 = 657.6 within 1%)"] = abs(ctrl["Lambda_over_M4"] - 657.6) < 6.6
    checks["12130: S002 integrand modular invariant (Gamma_1(6) seed, S on beta part, S and T on twisted part) to 1e-11"] = max(mc.values()) < 1e-11
    checks["12130: S002 full one-loop Lambda/M^4 = +677.6 > 0 at T_WL = 2i, T* = rho"] = abs(s002["Lambda_over_M4"] - 677.63) < 0.1
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
