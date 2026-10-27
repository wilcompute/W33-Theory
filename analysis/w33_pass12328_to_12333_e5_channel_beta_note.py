"""Passes 12328-12333: the e5 winding channel's candidates, the k_Y obstruction confirmed with the full spectrum, a standalone note
(Claude track).

12328 -- the e5-winding tachyon channel (12322) of the SM_810 lineage: 16 left-movers P in E8 x E8 + V0 + W5 with P^2 = 1 in each of
  v9, v4 (parent and brother); 8 have e5 phase 0 (zero e5 momentum allowed) and e6 phase 0 (no e6 momentum shift, even in the
  brother) -- the channel's translation conditions are met, so R_5 >~ sqrt(2 alpha') stands unless the theta^2 / statistics projections
  remove those 8 (not computed).  The R_6 < 0.61 sqrt(alpha') window itself needs no projection: its channels are closed by level minima.
12329 -- the one-loop potential in the string-scale window: not computed.  It needs the brother's states with half-integer e6 momentum
  (those the torsion moves off the zero mode), which the engine never produces; required extension: an engine dump of the states
  removed only by the e6 translation phase.
12330 -- one-loop beta coefficients of the candidate's full massless spectrum (Y = T3R + Y' per component): b3 = 7, b2 = 16,
  bY = 148/3 (not asymptotically free).  SM below a common threshold M_X and the full spectrum above, M_X = 1e3 ... 1e16 GeV: 43
  perturbative alpha_2 = alpha_3 crossings, k_Y needed in [0.21, 1.28] -- never 8/3.  The k_Y = 8/3 obstruction holds within one-loop
  running with a common threshold.
12331 -- standalone note papers/wilson_line_torsion (formula, tests incl. the pre-registered 124/124, Z3 proposition, routes, the
  Scherk-Schwarz window with computed vs argued, the obstructions, the record of corrections).
12332 -- the backed-up testbenches: two differ from the repo only by a trailing blank line; for tb_w33_linebus_phase_frame_random the
  user chose the repo version (6380f6794).  (An earlier report had the two versions' wording reversed: the LOCAL copy is the cautious
  'certification still requires Icarus' one.)
12333 -- synthesis.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12328_to_12333_e5_channel_beta_note.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    e5 = json.loads((A / "search_drivers_12328" / "e5chan.json").read_text())
    res["12328"] = e5
    checks["12328: 16 candidates per model, 8 with e5 and e6 phases 0 (parent and brother)"] = all(
        x["candidates"] == 16 and x["phases"].get("phi5=0 phi6=0") == 8 for v in e5.values() for x in v.values())
    bt = json.loads((A / "search_drivers_12330" / "beta.json").read_text())
    sc = json.loads((A / "search_drivers_12330" / "scan.json").read_text())
    res["12330"] = dict(b=bt["b_full"], k_range=sc["perturbative_k_range"], reaches_8_3=sc["reaches_8_3"])
    checks["12330: b = (7, 16, 148/3); perturbative k_Y needed in [0.21, 1.28], never 8/3"] = (
        bt["b_full"] == {"b3": "7", "b2": "16", "bY": "148/3"} and not sc["reaches_8_3"]
        and 0.2 < sc["perturbative_k_range"][0] < 0.22 and 1.27 < sc["perturbative_k_range"][1] < 1.29)
    note = (ROOT / "papers" / "wilson_line_torsion" / "main.tex").read_text(encoding="utf-8")
    checks["12331: the note states the formula, the 124/124 test and the record of corrections"] = (
        "124/124" in note and "Record of corrections" in note and "sigma_g" in note)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
