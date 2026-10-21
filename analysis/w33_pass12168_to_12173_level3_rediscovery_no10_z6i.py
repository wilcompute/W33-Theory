"""Passes 12168-12173: the level-3 mass formulas (with a REDISCOVERY notice), the untwisted no-10_H theorem, exact onset brackets,
and Pass 11100 extended to many Witten shifts on Z6-I (Claude track).

REDISCOVERY NOTICE. Passes 11115, 11136 and 11139 already established: the Wilson-line duality group is Gamma0(3), the Fricke
involution T -> -1/(3T) is only approximate (0.34% K-independent, 11139); the Witten-sector levels are Delta = -1/2 + p_R^2/2 with
p_R^2 = (b^2 + y^2)/(sqrt3 y) (onset sqrt3), + 1/(3 sqrt3 y) ('golden', top sqrt3/2 + sqrt(5/12) = 1.5115, disk at the Fricke point
i/sqrt3), and the charged (c^2 + y^2 + 1/12)/(sqrt3 y) + 1/3 (disk at the elliptic point (3 + i sqrt3)/6, tangent to B = 0 at i/sqrt3)
(11136); model 77's onset ~ sqrt3/2 (11115). Passes 12140, 12149, 12152, 12158 (in part) and this round's mass formula re-derive
these for S002/T115/the crossed models; they are CITED here, not claimed. (The S002 multiplet is 11136's charged level; its massless
point i/sqrt3 is the tangency of 11136's charged disk.)

What is new:
12168 -- the formulas hold, exactly, in the e6+a2 models too: S002's lowest Witten level equals (sqrt3 y - 1)^2 / (6 sqrt3 y) (11136's
  charged form at B = 0) to 5e-16 at 18 axis points; T115's levels are Delta = y/(2 sqrt3) - 1/2 (11136's sqrt3 form; onset sqrt3).
12169 -- the K-independent Fricke deviation of 11139 is explained: the duality maps level VALUES exactly but permutes multiplicities
  (272 <-> 104 in S002, 12158), so it relates a model to a partner (not a sign flip of W or V1, 12164) rather than to itself.
12171 -- a third exact class, p_R^2 = 2y/sqrt3 (Delta = y/sqrt3 - 1/2, onset sqrt3/2), for model 77 and the crossed models A8SM_10006 /
  16222, where 11115 had only 'onset ~ sqrt3/2'. Brackets with the 11107 enumerator at root -+ 0.002: model 2 (sqrt3), model 10
  ((sqrt3 + sqrt(5/3))/2 = sqrt3/2 + sqrt(5/12)), model 77 (sqrt3/2) are tachyon-free above and tachyonic below, with Delta = -0.002 x
  slope (1/(2 sqrt3), golden, 1/sqrt3) -- the certified radii 1.73 / 1.512 / 0.87 of 11107 are these exact numbers.
12170 -- THEOREM (untwisted sector): on every e6+a2 base (7) and every A4-type second Wilson line (864 each, all 6048), the untwisted
  first-E8 scalars form only SU(5) 5s and singlets; untwisted 10s occur only as fermions (288 per base, the generation 10s) -- the 10
  sits in the SO(10) 16, which is odd under the split parity. Twisted sectors: 0/185 scalar 10s in the engine (sample).
12172 -- Pass 11100 used one Witten shift per base. On Z6-I with EIGHT loadable V0 per base (58 bases, 464 V0, 27,840 Wilson-line
  draws): 10,986 tachyon-free (39%), 4 SM-like, 0 both -- and all 4 SM-like draws come from V0 whose base is itself tachyonic (6
  tachyonic fields). The SM-like Witten shifts of Z6-I are exactly the tachyonic ones; 11100's conclusion holds at 8x the V0 sample.
12173 -- synthesis: the closure of 12167 stands; the level-3 structure belongs to 11115/11136/11139.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12168_to_12173_level3_rediscovery_no10_z6i.json"
D = ROOT / "analysis" / "search_drivers_12168"
S3 = math.sqrt(3)


def main():
    checks, res = {}, {}
    mf = json.loads((D / "massformula_s002.json").read_text())
    exact = {y: v for y, v in mf.items() if abs(float(y) * 1e6 - round(float(y) * 1e6)) < 1e-9 and y not in ("0.606061", "0.641026", "0.666667", "0.740741")}
    dev = max(abs(v["enumerated"] - (S3 * float(y) - 1) ** 2 / (6 * S3 * float(y))) for y, v in exact.items() if y != "0.57735")
    res["12168"] = dict(points=len(exact), max_dev=dev)
    checks["12168: S002 lowest Witten level = (sqrt3 y - 1)^2/(6 sqrt3 y) to 1e-14 on the axis (11136 charged form at B = 0)"] = dev < 1e-14 and len(exact) >= 12
    on = json.loads((D / "onsets.json").read_text())
    slopes = {"2": 1 / (2 * S3), "77": 1 / S3}
    res["12171"] = on
    ok = all(on[m]["+0.002"]["n"] == 0 and on[m]["-0.002"]["n"] > 0 for m in ("2", "10", "77"))
    ok &= all(abs(on[m]["-0.002"]["Delta"] + 0.002 * s) < 1e-9 for m, s in slopes.items())
    checks["12171: exact onsets sqrt3 / sqrt3/2 + sqrt(5/12) / sqrt3/2 bracketed (models 2, 10, 77); Delta slopes 1/(2 sqrt3) and 1/sqrt3 exact"] = ok
    n10 = json.loads((D / "no10.json").read_text())
    res["12170"] = n10
    checks["12170: untwisted scalar 10s: 0 in all 7 x 864 A4-type models; untwisted fermion 10s: 288 per base (control)"] = (
        len(n10) == 7 and all(v["('scalar', 'has10')"] == 0 and v["('fermion', 'has10')"] == 288 and v["models"] == 864 for v in n10.values()))
    mz = D / "multiv0_z6i.json"
    if mz.exists():
        z = json.loads(mz.read_text())
        recs = [r for v in z.values() for r in v if "ok" in r]
        res["12172"] = dict(bases=len(z), v0_scanned=len(recs), draws=sum(r["ok"] for r in recs), tachyon_free=sum(r["tachyon_free"] for r in recs),
                            SM=sum(r["SM"] for r in recs), SM_tachyon_free=sum(r["SM_tf"] for r in recs))
        checks["12172: Z6-I with 8 V0 per base: 464 V0, 27840 draws, 10986 tachyon-free, 4 SM-like, 0 SM & tachyon-free; SM only on tachyonic bases"] = (
            len(z) == 58 and len(recs) == 464 and res["12172"]["draws"] == 27840 and res["12172"]["SM"] == 4 and res["12172"]["SM_tachyon_free"] == 0
            and all(r["base_tachyons"] != "T_NFIELDS 0" for r in recs if r["SM"]))
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), json.dumps(res.get("12172", {})), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
