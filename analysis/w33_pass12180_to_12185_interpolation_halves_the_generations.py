"""Passes 12180-12185: Scherk-Schwarz interpolation of the Z6-II W(3,3) Standard Models halves their odd-sector generations;
clock Witten shifts are tachyonic on every family; the clock instability is not the Hagedorn one (Claude track).

12180 -- Scherk-Schwarz (super-no-scale) census on Z6-II, the family that admits an order-2 translation (Pass 12177).
  Parents: the 128 supersymmetric Z6-II W(3,3) Standard Models (Pass 10960 archive); 70 have W6 = 0, so t = e6/2 carries no
  Wilson line.  Witten shifts: split x split V0 (the tachyon-free SO(16)^2 endpoint, Pass 12174) with V0.V, V0.W integral.
  Method (exact): at large radius each supersymmetric multiplet is split by its left-moving character chi = exp(2 pi i p.V0)
  -- bosons kept for chi = +1, fermions for chi = -1 -- which is exactly the Witten-untwisted (m = 0) projection of the non-free
  Z2W x Z6-II model with the same V0 (non-supersymmetric orbifolder, Geometry_Z6-II_1_1); in the sectors that rotate the
  translated plane (theta, theta^3, theta^5) the translation pairs fixed points and each pair keeps one boson and one fermion.
  So n_B - n_F (large R) = [bosons - fermions] over m = 0, even Z6 power, + 2 NU1.  Control: each multiplet contributes half its
  states whatever chi is, so the total m = 0 count must be independent of V0 -- it is, in 70/70 parents.
  Result: 70 parents x 20 V0 = 1400 interpolations; n_B - n_F in [-80, 464], always a multiple of 8; EXACT degeneracy
  n_B = n_F in 3 (all in parent Z6II_59 SM_20260917_1105; one, v12, keeps an SU(3) x SU(2)-type factor and is tachyon-free as
  a non-free model).
12180b -- the generations.  Every one of the 70 parents carries net quark doublets (even, odd) = (1, 2): one generation in an
  even sector, two in the translated (odd) sectors.  The translation halves the odd ones, so at large radius at most
  1 + 2/2 = 2 quark generations survive, for EVERY V0.  The degenerate point v12 has net 2 (1 even with chi = -1, plus 2/2).
  So on this class super-no-scale and three generations exclude each other.  Dimension-weighted census of all 128 parents
  (a first count by multiplet lines missed a family-triplet multiplet): (even, odd) = (1, 2) x 117, (2, 1) x 10, (3, 0) x 1.
  The one exception, Z6II_24 SM_20260917_2751, has all three quark doublets in one untwisted family triplet; it carries
  Wilson lines on both order-2 directions, so its interpolation needs 2 V0 = W_t mod Gamma (an order-4 Witten shift), outside
  the non-free method used here.  Its species census (q, u, d, l, e) has zero net chirality in every odd sector, so the
  halving does not obstruct it -- but the space-group consistency of g = (t, V0) does: theta reverses the order-2 plane, so
  g^{-1} theta g theta^{-1} is the lattice translation -2t, whose gauge embedding computes to V0 - V0 = 0 and must equal -W_{2t};
  hence a Scherk-Schwarz translation requires W_{2t} = 0 mod Gamma.  For SM_2751, W5, W6 and W5 + W6 all lie outside Gamma: no
  consistent translation exists.  CLOSURE: no Z6-II W(3,3) Standard Model has a three-generation Scherk-Schwarz
  interpolation (the translations all lie on the order-2 plane by Pass 12177).
12181 -- clock Witten shifts on the other families: Z6-I, Z3xZ3, Z12-I (6 bases each): every clock V0 model tachyonic at the
  orbifold point, 0/5400 tachyon-free with random Wilson lines -- the theorem of Pass 12178 (zero-winding p = V0, p^2 = 1,
  kept by every admissible shift and line) on every family.
12182 -- twisted 10_H, enlarged sample: 150 more draws (second Wilson line on the third torus, seed 31) give 53 SU(5) x U(1)
  models, 21 three-generation, all tachyon-free, scalar 10: 0 (cumulative 0/238 with Passes 12161/12163; fermion 10s present as
  the non-vacuous control).  Still a sample, not a theorem.
12183 -- the nine-dimensional interpolations by class (thermal.py; a state is physical iff level matched, n w = 1/2 - p^2/2 - N):
  V = 0 is the thermal ensemble, tachyonic for 2 - sqrt2 < R < 2 + sqrt2 (the heterotic Hagedorn radius, control);
  clock x clock and split x 0: tachyon p = V0 (n = 0) for ALL R < 2 sqrt2 (the 10D endpoint is tachyonic);
  split x split: never tachyonic, one massless point at R = sqrt2.  The clock instability is therefore not the Hagedorn
  instability: other momentum (p = V0 vs p = 0), smaller critical radius (ratio (2 + sqrt2)/(2 sqrt2) = 1.207), no upper edge.
12184 -- which factorisation the vacuum picks as fermion parity: answered by Pass 12089 (cited, not re-derived): on the E6
  clock (trinification centraliser) vacuum, 27 of the 135 split parities -- the factorisations through the event -- leave
  SO(10) with 16 odd and 10 even; the other 108 leave SU(6) x SU(2).
12185 -- synthesis: the only W(3,3) family/route that admits interpolation (Z6-II) has its generations split 1 + 2 across the
  sectors the translation does and does not pair; Bose-Fermi degeneracy is reachable (3/1400) but never with three generations.
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12180_to_12185_interpolation_halves_the_generations.json"
D0 = ROOT / "analysis" / "search_drivers_12180"
D1 = ROOT / "analysis" / "search_drivers_12181"
D4 = ROOT / "analysis" / "search_drivers_12174"
BOS, FER = {8, 9, 13, 14, 15, 16, 17, 18}, {19, 20}


def main():
    checks, res = {}, {}
    recs, ctrl_bad = [], 0
    for f in sorted(D0.glob("ss20_part*.json")):
        for lab, v in json.loads(f.read_text()).items():
            tots = set()
            for r in v["v0"]:
                recs.append((lab, r))
                tots.add(sum(c for k, c in r["counts"].items() if "_w0_" in k and int(k.split("_")[0][4:]) in BOS | FER) + 2 * r["NU1"])
            ctrl_bad += len(tots) > 1
    d = [r["SS_diff"] for _, r in recs]
    zeros = [(lab, r["V0"], r["gauge"], r["tachyons"]) for lab, r in recs if r["SS_diff"] == 0]
    res["12180"] = dict(parents=len({l for l, _ in recs}), runs=len(recs), min=min(d), max=max(d), zeros=zeros,
                        histogram=sorted(Counter(d).items()))
    checks["12180: 70 parents x 20 V0 = 1400 interpolations; V0-independent total (control) 70/70; n_B - n_F in 8Z, 3 exact zeros"] = (
        len({l for l, _ in recs}) == 70 and len(recs) == 1400 and ctrl_bad == 0 and all(x % 8 == 0 for x in d) and len(zeros) == 3)
    sc = json.loads((D0 / "sscontent.json").read_text())
    res["12180b_v12"] = sc["12"]
    checks["12180b: the degenerate v12 point: parent net 3 quark doublets (control), large-R net 2"] = (
        sc["12"]["content"]["Q"]["parent_net"] == 3 and sc["12"]["content"]["Q"]["ss_large_R_net_fermions"] == 2)
    og = json.loads((D0 / "oddgen.json").read_text())
    labs = {l.replace("_SM_", "__SM_") for l, _ in recs}
    dist = Counter((og[k].get("even", 0), og[k].get("odd", 0)) for k in labs)
    res["12180b_generations"] = dict(w6zero={str(k): n for k, n in dist.items()}, all128={str(k): n for k, n in Counter((v.get("even", 0), v.get("odd", 0)) for v in og.values()).items()})
    checks["12180b: all 70 W6 = 0 parents have net quark doublets (even, odd) = (1, 2) -> at most 2 generations survive interpolation"] = (
        dist == Counter({(1, 2): 70}))
    allev = sorted(k for k, v in og.items() if v.get("odd", 0) == 0)
    res["12180b_all_even_parents"] = allev
    checks["12180b: dimension-weighted census sums to 3 in all 128 parents; exactly one (Z6II_24 SM_2751, untwisted family triplet) has no odd-sector generation, and it is not a W6 = 0 parent"] = (
        all(sum(v.values()) == 3 for v in og.values()) and allev == ["Z6II_24__SM_20260917_2751"] and "Z6II_24__SM_20260917_2751" not in labs)
    from fractions import Fraction as Fr

    def in_e8(v):
        ints = all(x.denominator == 1 for x in v)
        halves = all(x.denominator == 2 for x in v)
        return (ints or halves) and sum(v) % 2 == 0

    W5 = [Fr(x) for x in "-1/4 -1/4 1/4 1/4 1/4 -1/4 -3/4 3/4 -1/4 -1/4 3/4 3/4 -3/4 1/4 9/4 -3/4".split()]
    W6 = [Fr(x) for x in "-2 -3/2 -1 1/2 1 2 0 1 5/4 5/4 -5/4 9/4 -5/4 -1/4 -5/4 -3/4".split()]
    opts = {"W5": W5, "W6": W6, "W5+W6": [a + b for a, b in zip(W5, W6)]}
    res["12180c_SM2751"] = {k: in_e8(w[:8]) and in_e8(w[8:]) for k, w in opts.items()}
    checks["12180c: SM_2751 (the only all-even parent) has no translation with W_2t in Gamma -> no three-generation interpolation"] = (
        not any(res["12180c_SM2751"].values()))
    fam = {}
    for f in sorted(D1.glob("clock_*.json")):
        fam[f.stem] = json.loads(f.read_text())
    res["12181"] = fam
    rr = [r for v in fam.values() for r in v.values() if r]
    checks["12181: clock V0 on Z6-I, Z3xZ3, Z12-I: 18 bases, all tachyonic at the orbifold point, 0/5400 tachyon-free"] = (
        len(rr) == 18 and all(r["tachyons"] != "T_NFIELDS 0" for r in rr) and sum(r["ok"] for r in rr) == 5400
        and sum(r["tachyon_free"] for r in rr) == 0)
    fs = json.loads((D0 / "flipscan2_31_third.json").read_text())
    a4 = [x for x in fs if "net10" in x]
    res["12182"] = dict(draws=len(fs), su5=len(a4), three_gen=sum(abs(x["net10"]) == 3 for x in a4), scalar10=sum(x["scalar10"] for x in a4))
    checks["12182: 53 new SU(5)xU(1) models (21 three-generation), scalar 10: 0; fermion 10s present (control)"] = (
        len(a4) == 53 and res["12182"]["three_gen"] == 21 and res["12182"]["scalar10"] == 0)
    th = json.loads((D4 / "thermal.json").read_text())
    res["12183"] = {k: v["window"] for k, v in th.items()}
    s2 = 2 ** 0.5
    checks["12183: thermal window = Hagedorn (2 -+ sqrt2); clock/split x 0 tachyonic below 2 sqrt2; split x split never"] = (
        abs(th["0x0"]["window"][0] - (2 - s2)) < 1e-3 and abs(th["0x0"]["window"][1] - (2 + s2)) < 1e-3
        and abs(th["clockxclock"]["window"][1] - 2 * s2) < 1e-3 and abs(th["splitx0"]["window"][1] - 2 * s2) < 1e-3
        and th["splitxsplit"]["window"] is None)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
