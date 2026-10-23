"""Passes 12223-12228: the twisted-10 models include 58 three-generation SU(5) x U(1) models; with two Wilson lines twisted 10s are 12x
commoner but still fermions; the twisted 10 momenta carry a constant split-parity character; translation or radius on the T6/Z3 Narain
lattice with cross-plane moduli (Claude track).

12223 -- generation content of the 153 consistent twisted-10 models of 12217 (non-SUSY engine): net (10, 5bar) = (+-3, +-3) in 58 and
  (+-6, +-6) in 95; all anomaly-free, all tachyon-free, all with scalar 5s; the twisted sectors contribute +-3 (or more) to the chiral
  10s.  Three-generation models whose families partly live in twisted sectors -- but still with no scalar 10, so no field-theoretic
  SU(5) breaking (Wen-Witten).
12224 -- two A4-type Wilson lines (W1 on torus 2, W2 on torus 3): naive random sampling never meets the admissibility (one line passes
  0.65% of the time); sampled correctly -- each line from the exhaustive admissible list of 12217, both lines leaving the same A4 (16
  A4 classes per base), 3 W1.W2 integral -- the density of configurations with a twisted 10-type massless vector is 2.1% (63/3000,
  95% Wilson interval 1.6-2.7%), twelve times the one-line density 0.18%.  Built in the engine: 9 of the 63 load, all SU(5) x U(1),
  tachyon-free; their 30 10-fields are all fermions (14 Witten-twisted, 4 Witten-untwisted twisted, 12 untwisted), scalar 10s: 0.
  A sample (9 consistent models), not a theorem.
12225 -- the mechanism, as data: the 4050 twisted 10-type massless momenta of the 405 one-line configurations ALL lie in Witten-twisted
  cosets (w = 1) and ALL have integral split-parity character P.V0; the Witten projection therefore sees a single left-moving phase and
  selects a single right-mover class, which the engine reports as fermionic in 153/153 (that pairing is the inferred step).  With two
  lines Witten-untwisted twisted 10s appear (12224), still as fermions.
12226 -- translation or radius on the Narain lattice of T6/Z3 at its enhanced point ((II(2,2) at rho)^3): for all 2^3 symmetric /
  asymmetric assignments of the Z3 on the three planes, order-2 translations exist exactly on asymmetric planes; with the FULL 12 x 12
  generalized metric (cross-plane moduli included: up to 18 invariant moduli), no invariant deformation changes the length of any
  translation lift to first order (t^T S t = 0 on the kernel basis and its pairwise sums).  General reason per plane: an asymmetric
  twist has no invariant Hom(V_L, V_R) (all moduli frozen), a symmetric one has det(1 - g) = 9, odd (no translation).
12227 -- cross-track: a continuity task (ticket) could not be filed (Pro feature); the question is logged as a decision for the other
  track (tags cross-track, narain, codex).
12228 -- synthesis.
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12223_to_12228_twisted_tens_three_generations_and_radius.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    g = json.loads((A / "search_drivers_12223" / "gens153.json").read_text())
    dist = Counter((abs(x["net10"]), abs(x["net5bar"])) for x in g)
    res["12223"] = dict(models=len(g), generations={str(k): n for k, n in dist.items()}, anomaly_ok=sum(x["anomaly_ok"] for x in g),
                        tachyon_free=sum(x["tachyons"] == 0 for x in g), with_scalar5=sum(x["scalar5"] > 0 for x in g))
    checks["12223: 153 twisted-10 models: 58 three-generation (net 10 = net 5bar = 3), 95 six-generation; all anomaly- and tachyon-free"] = (
        len(g) == 153 and dist == Counter({(6, 6): 95, (3, 3): 58}) and res["12223"]["anomaly_ok"] == 153 and res["12223"]["tachyon_free"] == 153)
    t2 = json.loads((A / "search_drivers_12224" / "twoline2_5.json").read_text())
    b2 = json.loads((A / "search_drivers_12224" / "build2_results.json").read_text())
    c = Counter()
    for x in b2:
        for k, v in x.get("tens", {}).items():
            c[k] += v
    res["12224"] = dict(sampling=t2, built=len(b2), loaded=sum(1 for x in b2 if x["gauge"] != "LOADFAIL"), tens=dict(c))
    checks["12224: two lines: density 63/3000 (95% CI 1.6-2.7%), 12x the one-line density; 9 consistent models, all 10s fermions, 0 scalars"] = (
        t2["draws"] == 3000 and t2["hits"] == 63 and 0.016 < t2["wilson95"][0] < 0.017 and len(b2) == 63 and res["12224"]["loaded"] == 9
        and not any(k.startswith("scalar") for k in c) and sum(c.values()) == 30)
    ch = json.loads((A / "search_drivers_12225" / "character.json").read_text())
    res["12225"] = ch["stats"]
    checks["12225: all 4050 twisted 10-type momenta (one line) are Witten-twisted with integral P.V0"] = ch["stats"] == {"1|0": 4050}
    pf = json.loads((A / "search_drivers_12226" / "product_full.json").read_text())
    res["12226"] = pf
    checks["12226: (II(2,2) at rho)^3, all 8 sym/asym assignments: translations only on asymmetric planes, no translation length varies (cross-plane moduli included)"] = (
        len(pf) == 8 and all(not v["some_translation_radius_runs"] for v in pf.values())
        and pf["sym-sym-sym"]["translations"] == 0 and pf["asym-asym-asym"]["translations"] == 6 and pf["sym-sym-sym"]["invariant_moduli"] == 18)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
