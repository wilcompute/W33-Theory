"""Passes 12156-12161: thresholds cannot rescue k_Y = 17/3, the Fricke duality permutes multiplicities, an audit under the full
rule set, the corpus status of the k_Y = 5/3 route, and the Wen-Witten obstruction with the SU(5) escape tested (Claude track).

12156 -- one-loop gauge thresholds. The volume-growing (beta-sector, 10D-like) thresholds are UNIVERSAL: for every norm shell of
  E8 and of every SO(16) conjugacy class (0, v, s, c) the lattice sum of (p.y)^2 equals |y|^2 x count x N/8 exactly (Weyl
  irreducibility), so the insertion is proportional to k_a, and the two SO(16) halves enter symmetrically; T^6/Z3 has no N = 2
  sectors, so there are no large moduli-dependent (DKL) thresholds either. The non-universal threshold needed at the heterotic
  scale is Delta_Y - k_Y Delta_2 = -246 for k_Y = 5/3 (24% of the tree-level k_Y/alpha_U) but -2636 for k_Y = 17/3 (77%):
  the fraction-free route cannot be rescued; the canonical route needs a large but not absurd correction.
12157 -- the fractional-charge question is already settled in the corpus WITH the calibrated rules: Pass 11097 used gauge,
  Witten Z2, point group, space group AND H-momentum (exact cubic, mod 3 higher), and found all fractional fermions massive in
  33 of the 104 A8 models (hidden group unbroken); 11101/11102 narrowed to 12 survivors with a heavy top (charm-up degenerate,
  protected by an AG(3,3) reflection). So the viable line is k_Y = 5/3 with fractional states lifted -- not fraction-free.
12158 -- the Fricke duality T_WL -> -1/(3 T_WL): S002's Witten-sector LEVEL VALUES map exactly onto each other (all four levels
  below Delta = 0.3 agree to 1e-9 at 0.52i and 0.641i) but two MULTIPLICITIES are swapped (272 <-> 104 at Delta = 0.1519 / 0.1869);
  the untwisted beta-insertion block is Fricke-invariant up to 6e-8 at tau_2 = 2.5 while the Witten-twisted blocks differ by ~1%.
  The duality maps the model to a partner with the same levels and permuted degeneracies -- which is why Lambda is only
  approximately invariant while the lowest (equal-multiplicity) level is exact.
12159 -- audit of 12121-12150 under the full rule set. Valid (exact cubic H-momentum or exact symmetry): 12122, 12128, 12134,
  12142, 12145, 12147 (|V_tb| = 1), 12148, 12153. Corrected in 12155: 12133, 12146 (quartic lifts). 12138: its 'protected'
  conclusion holds a fortiori (extra rules only remove couplings). NEW correction here: 12147's 'up rank 1 -> 3 at quartic order'
  becomes 1 -> 1 with H-momentum in all 16 models -- charm and up stay massless through quartic order (cf. the AG(3,3)
  protection of 11102).
12160 -- other geometries: Pass 11100 found only T^6/Z3 tachyon-free with the W(3,3) shifts (sample); no new computation.
12161 -- Wen-Witten. The 12150 congruence is an instance of Wen and Witten (1985): a GUT broken by Wilson lines leaves fractionally
  charged states (generalised by Schellekens 1990). Escape = field-theoretic breaking at level 1 (flipped SU(5) by 10_H, or
  Pati-Salam). Tested: a targeted scan of the 864/6561 A4-type second Wilson lines on the e6+a2 bases gives 64 SU(5) x U(1)
  models, 22 with exactly three chiral generations (net +-3 10 and 5bar), all tachyon- and anomaly-free -- but NONE with a scalar
  10 (0/64), and the first one found (N001_F1_04_S023) has no 10_H or 24: the SU(5) cannot be broken at level 1 on this route.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12156_to_12161_thresholds_fricke_audit_wenwitten.json"
D = ROOT / "analysis" / "search_drivers_12156"


def main():
    checks, res = {}, {}
    th = json.loads((D / "thresh.json").read_text())
    need = th["needed_thresholds_heterotic_Ms"]
    res["12156"] = dict(isotropic=th["isotropic"], needed=need)
    checks["12156: (p.y)^2 lattice sums isotropic on every E8 shell and SO(16) class (volume thresholds universal)"] = bool(th["isotropic"])
    checks["12156: needed non-universal threshold -246 (k_Y = 5/3, 24%) vs -2636 (k_Y = 17/3, 77%)"] = (
        abs(need["1.6667"]["Delta_Y_minus_kY_Delta_2"] + 246.34) < 0.5 and abs(need["5.6667"]["Delta_Y_minus_kY_Delta_2"] + 2635.85) < 1)
    fl = json.loads((D / "fricke_levels.json").read_text())
    a, b = fl["0.5200"], fl["0.6410"]
    fb = json.loads((D / "fricke_blocks.json").read_text())
    res["12158"] = dict(levels=fl, block_deviation=fb)
    checks["12158: Fricke-paired level VALUES equal (4/4), multiplicities 272 <-> 104 swapped; beta-insertion block invariant at large tau_2"] = (
        set(a) == set(b) and sorted(a.values()) == sorted(b.values()) and sum(1 for k in a if a[k] != b[k]) == 2
        and fb["(0.05+2.5j)"]["(0, 1)"] < 1e-6 and fb["(0.05+2.5j)"]["(1, 0)"] > 1e-3)
    ch = json.loads((D / "crossflavor_hm.json").read_text())
    res["12159"] = {k: v["up"]["rank_with_quartic"] for k, v in ch.items()}
    checks["12159: with H-momentum the quartic up rank stays 1 in all 16 crossed models (12147 'charm at next order' retracted)"] = (
        len(ch) == 16 and all(v["up"]["rank_with_quartic"] == 1 for v in ch.values()))
    fs = json.loads((D / "flipscan_11.json").read_text())
    a4 = [r for r in fs if "net10" in r]
    three = [r for r in a4 if abs(r["net10"]) == 3 and abs(r["net5bar"]) == 3]
    res["12161"] = dict(attempts=len(fs), su5_models=len(a4), three_generation=len(three), with_scalar_10=sum(1 for r in a4 if r["scalar10"]))
    checks["12161: 64 SU(5)xU(1) models, 22 three-generation (tachyon- and anomaly-free), none with a scalar 10"] = (
        len(a4) == 64 and len(three) == 22 and all(r["tachyonic"] == 0 and r["anomaly_ok"] for r in three) and all(r["scalar10"] == 0 for r in a4))
    q = (D / "S023.q").read_text()
    sc10 = [l for l in q.split("\n") if l.startswith("FIELD") and (" m=15 " in l or " m=16 " in l) and ("dim=10," in l or "dim=-10," in l or "dim=24" in l)]
    checks["12161: N001_F1_04_S023 (3 x (10 + 5bar)) has no scalar 10 or 24"] = len(sc10) == 0
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
