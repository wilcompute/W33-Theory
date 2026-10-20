"""Passes 12121-12125: hypercharge, Yukawas, vacuum energy and the gauge-group limit of the three-generation models
(Claude track; continues 12111-12120).

PRIOR ART, read first. Pass 11095 already holds 104 tachyon-free non-supersymmetric three-generation Standard-Model-like
models on the same T^6/Z3 geometry (A8 shift, SO(16) x SO(16), canonical k_Y = 5/3); Pass 11098 their tree-level
Yukawas (no single heavy top); Passes 11099/11106 their one-loop vacuum energy (positive, runs away; Itoyama-Taylor).
SM-like tachyon-free SO(16) x SO(16) orbifolds are known in the literature in large numbers (Perez-Martinez, Ramos-Sanchez,
Vaudrevange, arXiv:2105.03460). The passes below are about the OTHER route -- the e6+a2 three-family shift with the split
fermion parity as the Witten Z2 (12111) -- and compare it with 11095.

12121 -- hypercharge. A new field dumper (nsoq.cpp: every left-mover weight, right-mover weight, oscillator, fixed point,
  U(1) charge) and an exact rational branch search over Y in span(U(1)s, SU(2)_R Cartan), with (3,2) at Y = +-1/6,
  colour triplets at quark values and doublets at +-1/2: in each of the four left-right models of 12116 there are
  hypercharges (2, 29, 64, 30) under which the net chiral spectrum is EXACTLY three Standard-Model generations with all
  exotics vector-like, every one orthogonal to the anomalous U(1). But the normalisation is never the GUT one:
  k_Y = 2 Y.Y >= 25/3, 14/3, 13/3, 11/3 (canonical 5/3, which the A8 models of 11095 have).
12122 -- Yukawas (gauge, Witten Z2, point group, space group, H-momentum; the exact rule sum R = 0 of 11098 and the
  weaker mod-3 rule give the same quark results). The three chiral quark doublets (the untwisted three-plane triple) have
  NO gauge-invariant Q q^c H coupling at all. Twisted U x T2 x T1 couplings exist for the vector-like doublet (15, 6, 0,
  6), and in three models the untwisted singlet coupling Q_chiral Qbar_vl S mixes it into the light states: one light
  combination carries all quark Yukawas, so the quark mass matrices have rank one at renormalisable order. In S002 the
  mixed doublet couples to u^c AND d^c (one heavy up-type and one heavy down-type quark); in S033 and S053 to d^c only;
  S037 has no quark Yukawa. Contrast 11098: the A8 models never give a single heavy top at tree level.
12123 -- vacuum energy. Massless N_B - N_F < 0 in all 75 loaded models of both scans (-454 .. -186; the four left-right
  models -390, -356, -320, -284). With the 11099 normalisation (Lambda_10 > 0 for N_B - N_F = -2112) the large-volume
  term (Itoyama-Taylor, proportional to N_F - N_B) is positive in every model: no super-no-scale (N_B = N_F) model, the
  volume runs away as in 11099.
12124 -- NEGATIVE: the second Wilson line in W(3,3). The colour A2 is an event fibre in 0/4 models (baseline 54/2160);
  SU(2)_L and SU(2)_R sit on collinear points in 3/4 (baseline 1296/2160). The line is generic.
12125 -- the gauge-group limit. Every order-3 element lambda/3 (6561, lambda in E8 mod 3E8) restricted to the so(10) of each
  of the 7 base models fixes D5 / D4 / A1+A3 / A1+A1+A2 / A3 / A4 = 27 / 270 / 1080 / 2160 / 2160 / 864 (Kac: so(10-2b) +
  u(b)); A2+A1 never occurs, so ONE extra Z3 line cannot give the SM group directly (classical). A third line (120
  candidates, 56 load) does: N008_F1_04_S037_T115 has first-E8 gauge group SU(3) x SU(2) x U(1)s, net three quark
  doublets, no tachyons, anomalies cancelled, 20 exact three-generation hypercharges (k_Y >= 17/3) -- but no quark Yukawa
  at renormalisable order (no vector-like doublet to mix with).
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

OUT = ROOT / "data" / "w33_pass12121_to_12125_hypercharge_yukawas_vacuum.json"
D11 = ROOT / "analysis" / "search_drivers_12111"
D16 = ROOT / "analysis" / "search_drivers_12116"
D21 = ROOT / "analysis" / "search_drivers_12121"
LR = ["N004_F1_03_S002", "N008_F1_03_S033", "N008_F1_04_S037", "N008_F1_02_S053"]
T115 = "N008_F1_04_S037_T115"
BASES = ["N001_F1_04", "N004_F1_03", "N004_F1_04", "N004_F1_05", "N008_F1_02", "N008_F1_03", "N008_F1_04"]
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])


def nbnf(text):
    b = f = 0
    for m in re.finditer(r"^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]*) x(\d+)", text, re.M):
        c, k = int(m.group(1)), int(m.group(3))
        for e in m.group(2).split(","):
            if e:
                k *= int(re.match(r"-?(\d+)", e).group(1))
        b += k if c in (8, 9, 13, 14, 15, 16, 17, 18) else 0
        f += k if c in (19, 20) else 0
    return b, f


def main():
    checks, res = {}, {}
    # 12121
    hy = json.loads((D21 / "hyper3_5.json").read_text())
    res["12121_hypercharge"] = {m: {k: v for k, v in hy[m].items() if k != "y_good"} for m in LR + [T115]}
    checks["12121: exact three-generation hypercharges 2/29/64/30 in the four left-right models, all orthogonal to the anomalous U(1)"] = (
        [hy[m]["n_exact"] for m in LR] == [2, 29, 64, 30] and all(hy[m]["n_exact_orth_anomalous"] == hy[m]["n_exact"] for m in LR))
    checks["12121: minimal k_Y = 25/3, 14/3, 13/3, 11/3 -- never the canonical 5/3"] = (
        [hy[m]["k_Y_min_good"] for m in LR] == ["25/3", "14/3", "13/3", "11/3"] and all(Fr(hy[m]["k_Y_min_good"]) > Fr(5, 3) for m in LR + [T115]))
    # 12122
    yk = json.loads((D21 / "yuk_5_exact.json").read_text())
    mx = json.loads((D21 / "yukmix_5_exact.json").read_text())
    ymod3 = json.loads((D21 / "yuk_4_mod3.json").read_text())
    nq = [len(yk[m]["quark"]) for m in LR + [T115]]
    no_direct = all(not any(re.match(r"gauge B\(-?3,1\) S\(1,2\)", k) for k in mx[m]) for m in LR + [T115])
    mixing = {m: any(re.match(r"ALLOWED B\(-?3,2\) S\(1,1\)", k) for k in mx[m]) for m in LR + [T115]}
    kinds = {}
    for m, chiral_y in [("N004_F1_03_S002", "1/6"), ("N008_F1_03_S033", "-1/6"), ("N008_F1_02_S053", "1/6")]:
        kinds[m] = sorted({"up" if abs(Fr(q["cy"][0])) == Fr(2, 3) else "down" for q in yk[m]["quark"] if q["Qy"] == chiral_y})
    res["12122_yukawa"] = dict(quark_couplings=dict(zip(LR + [T115], nq)), mixing=mixing, light_doublet_couples_to=kinds)
    checks["12122: chiral quark doublets have no gauge-invariant Q q^c H coupling (all five models)"] = no_direct
    checks["12122: vector-like-doublet Yukawas U x T2 x T1 = 15, 6, 0, 6, 0; exact and mod-3 H-momentum agree"] = (
        nq == [15, 6, 0, 6, 0] and [len(ymod3[m]["quark"]) for m in LR] == nq[:4]
        and all(all(q["Qsec"] == "U" and q["csec"] == "T2" and q["Hsec"] == "T1" for q in yk[m]["quark"]) for m in LR))
    checks["12122: chiral-to-vector-like mixing in S002, S033, S053 only; mixed doublet couples to u^c and d^c (S002), d^c only (S033, S053)"] = (
        [mixing[m] for m in LR + [T115]] == [True, True, False, True, False]
        and kinds == {"N004_F1_03_S002": ["down", "up"], "N008_F1_03_S033": ["down"], "N008_F1_02_S053": ["down"]})
    # 12123 (recomputed from the engine outputs)
    outs = sorted((D16 / "smwl").glob("*.out")) + sorted((D21 / "smwl3").glob("*.out"))
    bf = {}
    for p in outs:
        t = p.read_text()
        if "GAUGE" in t:
            b, f = nbnf(t)
            bf[p.stem] = b - f
    res["12123_NB_minus_NF"] = dict(n_loaded=len(bf), min=min(bf.values()), max=max(bf.values()),
                                    left_right=[bf[m] for m in LR], T115=bf[T115])
    checks["12123: N_B - N_F < 0 in all 75 loaded models (-454..-186): positive large-volume vacuum energy, no super-no-scale model"] = (
        len(bf) == 75 and max(bf.values()) == -186 and min(bf.values()) == -454 and [bf[m] for m in LR] == [-390, -356, -320, -284])
    # 12124
    w = json.loads((D21 / "wl2w33.json").read_text())
    c = json.loads((D21 / "wl2col.json").read_text())
    checks["12124: colour A2 an event fibre in 0/4 (baseline 54/2160); L,R collinear 3/4 (baseline 1296/2160)"] = (
        sum(w[m]["colour_is_fibre"][0] for m in LR) == 0 and all(w[m]["baseline"]["colour A2 is a fibre"] == 54 for m in LR)
        and sum(c[m]["LR_collinear"] for m in LR) == 3 and all(c[m]["baseline_collinear"] == 1296 for m in LR))
    # 12125 (Kac classification recomputed)
    g = Gradings()
    R = g.R
    lams = np.array(list(itertools.product(range(3), repeat=8))) @ SIMPLE
    integ = lambda a: np.abs(a - np.round(a)) < 1e-9  # noqa: E731
    kac = {}
    for base in BASES:
        rows = (D11 / (base + "_9.txt")).read_text().split("Shifts and Wilsonlines:")[1].split("end model")[0].strip().split("\n")
        v = [np.array([float(Fr(x)) for x in r.split()[:8]]) for r in rows]
        d5 = next(cc for cc in g.comps(integ(R @ v[0]) & integ(R @ v[1]) & integ(R @ v[3])) if len(cc) == 40)
        P = integ(R[d5] @ lams.T / 3)
        t = Counter()
        for j in range(lams.shape[0]):
            mk = np.zeros(240, bool)
            mk[np.array(d5)[P[:, j]]] = True
            t[" + ".join(g.typ(mk))] += 1
        kac[base] = dict(t)
    want = {"D5": 27, "D4": 270, "A1 + A3": 1080, "A1 + A1 + A2": 2160, "A3": 2160, "A4": 864}
    res["12125_order3_on_so10"] = kac
    checks["12125: order-3 elements on so(10): D5/D4/A1+A3/A1+A1+A2/A3/A4 = 27/270/1080/2160/2160/864, never A2+A1 (7/7 models)"] = all(kac[b] == want for b in BASES)
    s3 = json.loads((D21 / "smwl3_7.json").read_text())
    loaded = [r for r in s3 if r["gauge"] != "LOADFAIL"]
    sm = [r for r in loaded if r["gauge"].split(" and ")[0].split(" NU1")[0].strip() == "A2 + A1" and abs(r["net32"]) == 3]
    res["12125_third_line"] = dict(attempts=len(s3), loaded=len(loaded), direct_sm=sm)
    checks["12125: third Wilson line: 120 attempts, 56 load, exactly one SU(3) x SU(2) x U(1)s model with net 3 quark doublets, tachyon- and anomaly-free, 20 exact hypercharges, no quark Yukawa"] = (
        len(s3) == 120 and len(loaded) == 56 and [r["label"] for r in sm] == [T115] and sm[0]["tachyonic"] == 0 and sm[0]["anomaly_ok"]
        and hy[T115]["n_exact"] == 20 and len(yk[T115]["quark"]) == 0)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
