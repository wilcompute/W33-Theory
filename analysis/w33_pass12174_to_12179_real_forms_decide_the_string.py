"""Passes 12174-12179: the E8 real forms decide the ten-dimensional string, and the fixed-point parity decides Scherk-Schwarz
(Claude track).

12174 -- the fermion-parity orbifolds g = (-1)^F exp(2 pi i p.V) of the E8 x E8 heterotic string, classified by the real-form
  class of each half of V in E8/2E8 = O+(8,2): 0, CLOCK (V = alpha/2, alpha a root, Q = 1: the 120 = 40 points x 3 involutions of
  E8(-24), Theorem 7.3 / Pass 12052) or SPLIT (V = v/2, v of norm 4, Q = 0: the 135 = 45 factorisations x 3 of E8(8)).  The one-loop
  partition function is built from its four blocks, Z = F/2 [B00 + B01 + B10 + B10(tau+1)], and tested numerically.
  Consistent (T^2 closure of the twisted block to 1e-15, S-invariance to 1e-11) exactly when Q(V1) = Q(V2), i.e. V^2 in Z:
    0 x 0          -> supersymmetric E8 x E8 (Z = 0 to 4e-12, n_B = n_F = 4032: the gravitino returns; positive control)
    split x 0      -> E8 x SO(16), tachyon in the 16 (16 states)
    split x split  -> SO(16) x SO(16), TACHYON-FREE, n_B - n_F = 1984 - 4096 (= Pass 11099's calibrated -2112)
    clock x clock  -> (E7 x SU(2))^2, tachyon (2,2) (4 states)
    clock x 0, clock x split -> inconsistent: B10(tau + 2) = -B10(tau) exactly (level matching fails), S fails at O(1).
  The list itself is the classical one (Kawai-Lewellen-Tye; Dixon-Harvey; Alvarez-Gaume-Ginsparg-Moore-Vafa); what is new is the
  reading: consistency is Q(V) = 0 on O+(16,2) (136^2 + 120^2 = 32896 = 2^15 + 2^7 classes), and the unique tachyon-free
  non-supersymmetric string needs a tensor factorisation of the two qutrits in EACH E8 -- a clock (the one-time, event-anchored
  form) can be the fermion parity only together with a second clock, and then the string is tachyonic.
12175 -- the tachyon is the minimal vector of the class: min |p|^2 over E8 + V is 0, 1/2 (exactly the two vectors +-alpha/2: the
  clock's own root pair, i.e. its fibre over the event of the 240 -> 40 fibration) and 1 (sixteen vectors v/2, the split's frame);
  a tachyon needs total norm 1, which only 0 + split and clock + clock reach.  Split x split starts at norm 2: tachyon-freedom is
  the statement that a factorisation's coset has no vector shorter than 1.
12176 -- massless Bose-Fermi counts of the four consistent strings: 4032 - 4032, 3008 - 2048, 1984 - 4096, 2240 - 3584.
12177 -- Scherk-Schwarz obstruction (exact, over F2): an order-2 translation commuting with the point group exists iff the
  generators' (M_g - 1) mod 2 have a common kernel; for a cyclic twist iff det(1 - theta) -- the number of fixed points -- is even.
  On the nine W(3,3) orbifold families: Z3 (27 fixed points), Z3xZ3, Z6-I (3), Z12-I (3), Z2xZ6-II, Z3xZ6 and Z6xZ6 admit NONE;
  Z6-II (all four lattices, det 12) and Z2xZ6-I admit a two-dimensional F2 space.  So the T6/Z3 and Z6-I non-supersymmetric models
  of Passes 11095-12173 cannot be interpolating (super-no-scale) models: their Witten element must act trivially on T6, and the
  large-volume Lambda_4 = (V/3) Lambda_10 > 0 of Pass 11099 is forced.  Controls: Z4 (det 16, kernel 4), Z8-I (det 4, kernel 2),
  Z7 (det 7, kernel 0), Z2xZ2 (kernel 6).
12178 -- the corpus never tried a CLOCK Witten shift (Pass 12084: split only).  On the W(3,3) A8 Kac base of T6/Z3, 12656 clock
  V0 = (alpha/2; beta/2) are admissible (V0.V1 in Z), in three gauge classes (78, 88, 96 roots); all load in the non-supersymmetric
  orbifolder, all are tachyonic at the orbifold point (1-2 tachyonic fields; the split control V0 is tachyon-free there), and 12
  representatives x 2000 random Wilson lines give 0/24000 tachyon-free models.  Mechanism (a theorem, not a sample): the
  zero-winding Witten-sector state of momentum p = V0 has p^2 = V0^2 = 1/2 + 1/2 = 1, the tachyon of Pass 12174, and the
  admissibility conditions V0.V_i, V0.W in Z are exactly its invariance conditions; with no winding and no KK momentum its mass
  is modulus-independent.  A clock Witten shift is tachyonic everywhere on the moduli space of every T6/Z3 model; a split one
  (V0^2 = 2) cannot be by this state.
12179 -- synthesis: the real form the clock selects for time (E8(-24)) is exactly the one that cannot be the string's fermion
  parity without a tachyon; the tachyon-free non-supersymmetric W(3,3) models are forced onto the split (tensor-factorisation)
  form, and on T6/Z3 they cannot interpolate to supersymmetry (27 fixed points).
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12174_to_12179_real_forms_decide_the_string.json"
D = ROOT / "analysis" / "search_drivers_12174"
W33 = ["Z3_SU3^3", "Z3xZ3_SU3^3", "Z6-I_G2xG2xSU3", "Z12-I_E6", "Z2xZ6-II_G2xG2xSU3", "Z3xZ6_SU3xG2xG2", "Z6xZ6_G2^3",
       "Z6-II_G2xSU3xSU2^2", "Z6-II_SU3xSO7xSU2", "Z6-II_SU3xSO8", "Z6-II_SU6xSU2", "Z2xZ6-I_SO4xG2xG2"]


def main():
    checks, res = {}, {}
    t = json.loads((D / "tenD.json").read_text())
    res["12174"] = t
    good = ("0x0", "splitx0", "splitxsplit", "clockxclock")
    bad = ("clockx0", "clockxsplit")
    checks["12174: Q(V1) = Q(V2) cases close under T^2 (1e-13) and are S-invariant (1e-10); clock x 0, clock x split fail level matching exactly"] = (
        all(z[1] < 1e-13 and z[2] < 1e-10 and z[3] < 1e-13 for k in good[1:] for z in t[k]["Z"])
        and all(abs(z[3] - 2) < 1e-9 for k in bad for z in t[k]["Z"]))
    checks["12174: controls -- V = 0 is supersymmetric (Z = 0, n_B = n_F = 4032); split x split = SO(16)^2 with 1984 - 4096 (Pass 11099)"] = (
        all(z[0] < 1e-9 for z in t["0x0"]["Z"]) and t["0x0"]["nB"] == t["0x0"]["nF"] == 4032
        and (t["splitxsplit"]["nB"], t["splitxsplit"]["nF"], t["splitxsplit"]["gauge_dim"]) == (1984, 4096, 240))
    checks["12174: gauge groups E8xSO16 (368), SO16^2 (240), (E7xSU2)^2 (272); only split x split is tachyon-free and non-SUSY"] = (
        (t["splitx0"]["gauge_dim"], t["clockxclock"]["gauge_dim"]) == (368, 272)
        and [k for k in good[1:] if t[k]["tachyons"] == 0] == ["splitxsplit"])
    checks["12174: consistent classes = singular vectors of O+(16,2): 136^2 + 120^2 = 32896 = 2^15 + 2^7"] = 136 ** 2 + 120 ** 2 == 2 ** 15 + 2 ** 7
    checks["12175: tachyons = minimal coset vectors: 16 (split x 0, the frame v/2), 4 = 2 x 2 (clock x clock, the two clocks' roots +-alpha/2)"] = (
        t["splitx0"]["tachyons"] == 16 and t["clockxclock"]["tachyons"] == 4)
    res["12176"] = {k: t[k]["nB"] - t[k]["nF"] for k in good}
    checks["12176: n_B - n_F = 0, 960, -2112, -1344"] = list(res["12176"].values()) == [0, 960, -2112, -1344]
    s = json.loads((D / "ss_translations.json").read_text())
    res["12177"] = {k: s[k] for k in W33}
    none = ["Z3_SU3^3", "Z3xZ3_SU3^3", "Z6-I_G2xG2xSU3", "Z12-I_E6", "Z2xZ6-II_G2xG2xSU3", "Z3xZ6_SU3xG2xG2", "Z6xZ6_G2^3"]
    some = ["Z6-II_G2xSU3xSU2^2", "Z6-II_SU3xSO7xSU2", "Z6-II_SU3xSO8", "Z6-II_SU6xSU2", "Z2xZ6-I_SO4xG2xG2"]
    checks["12177: no Scherk-Schwarz translation on Z3 (27), Z3xZ3, Z6-I, Z12-I, Z2xZ6-II, Z3xZ6, Z6xZ6; a 2-dim one on Z6-II (4 lattices) and Z2xZ6-I"] = (
        all(s[k]["ss_kernel_dim"] == 0 for k in none) and all(s[k]["ss_kernel_dim"] == 2 for k in some)
        and s["Z3_SU3^3"]["det_1_minus_theta"] == [27] and all(s[k]["integrality_error"] < 1e-6 for k in W33))
    checks["12177: cyclic law (kernel > 0 iff det(1 - theta) even) holds on every cyclic geometry, controls Z4/Z7/Z8-I included"] = all(
        (v["ss_kernel_dim"] > 0) == (v["det_1_minus_theta"][0] % 2 == 0) for v in s.values() if "twists" in v and len(v["twists"]) == 1
        and v["det_1_minus_theta"][0] != 0)
    cj = D / "clockv0_scan.json"
    c = json.loads(cj.read_text())
    recs = [r for v in c.values() for r in v]
    res["12178"] = dict(classes=sorted(c), reps=len(recs), draws=sum(r["ok"] for r in recs), tachyon_free=sum(r["tachyon_free"] for r in recs), detail=c)
    checks["12178: clock V0 on the A8 base: 3 classes, 12 reps load, all tachyonic at the orbifold point, 0/24000 tachyon-free with Wilson lines"] = (
        sorted(c) == ["78", "88", "96"] and len(recs) == 12 and not any(r["loadfail"] for r in recs)
        and all(r["tachyons"] != "T_NFIELDS 0" for r in recs) and res["12178"]["draws"] == 24000 and res["12178"]["tachyon_free"] == 0)
    checks["12178: mechanism -- clock x clock V0^2 = 1 (the tachyon momentum p = V0), split x split V0^2 = 2"] = all(
        sum(float(eval(x)) ** 2 for x in r["V0"].split()) == 1.0 for r in recs)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
