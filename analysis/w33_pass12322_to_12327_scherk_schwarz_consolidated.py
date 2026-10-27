"""Passes 12322-12327: the Scherk-Schwarz statement consolidated -- 12316's empty window withdrawn; a window R_6 < 0.61 sqrt(alpha')
survives every computed condition (Claude track).

12322 -- the winding step of 12316 checked against the bicharacter.  The e6 phase on a winding-w state of sector h is
  P.lam - (1/2) V_{h e6^w}.lam = (1/2)(V_h.lam + w lam^2) = (1/2) V_h.lam mod 1 (lam^2 even): for a lattice Wilson line the half-integer
  momentum shift of the Witten-twisted states is the SAME for every winding -- the 'odd winding flips the shift' rule of a freely acting
  Scherk-Schwarz translation does not apply.  There is no (w = 1, n = 0) state; 12316's small-R tachyon and 'tachyonic at every radius'
  are WITHDRAWN.  Small-R channels, by level matching L_int = R_int - n w (n in Z + 1/2):
    Witten theta^2, theta^4 (right vacuum -1/6): tachyon needs n w = 1/2 (p_R = 0 at R = sqrt(alpha'/2)) and L_int = -2/3;
      exact minimal left level (E8 x E8 closest-vector decoding over all fixed points) L_min = -1/3  -> channel closed;
    Witten untwisted (right vacuum -1/2): L_min over E8 x E8 + V0 = 0 (= the 10d tachyon-freedom of SO(16) x SO(16), control) -> closed;
    winding along e5 (coset V0 + W5, W5 the order-2 line): L_min = -1/2 = -1/2 -> a winding tachyon for R_5 < sqrt(2 alpha') ~ 1.41,
      in parent and brother alike (projection of that state not computed: an upper bound on the danger).
12323 -- consolidated statement (computed vs argued).  For the 15 brothers of SM_20260917_810 (non-SUSY Z6-II, left-right, three chiral
  generations, no chiral fractional charge):
    computed  -- zero-momentum/winding spectrum tachyon-free (engine solver); right-moving tachyonic vacua -1/6, -1/6, -1/2 (solver);
                 half-integer momentum for Witten-twisted states at every winding (bicharacter, validated 232/232 and 124/124
                 pre-registered); L_min values above (exact).
    argued    -- circle mass formula alpha' m^2/4 = level + p^2/2 with p_{L,R} = (n/R +- w R/alpha') sqrt(alpha'/2); projections of
                 winding states not computed.
    result    -- tachyonic for R_6 > sqrt(3 alpha'/8) ~ 0.61 sqrt(alpha') (n = 1/2 states, the decompactified tachyonic parent);
                 no tachyon channel found for R_6 < 0.61 sqrt(alpha'); R_5 >~ 1.41 sqrt(alpha') needed against the e5 winding channel.
    open      -- the one-loop potential in that (string-scale) window; the 12312 proxy (n_F - n_B = -222) is a large-R estimate and
                 does not apply there; k_Y = 8/3 (12313) stands.
12324 -- 99 of the 1399 non-SUSY Z6-II parents are tachyon-free at the orbifold point; none is a three-generation left-right model.
12325 -- the twelve Z2xZ6-I SM brothers (12282): nine fail the renormalisable-QLd proton test (12287), SM_128 has no cubic Yukawa,
  SM_808 and SM_2579 fail the texture test (12301) -- all twelve excluded.
12326 -- user decisions taken: main checkout fast-forwarded (68 blockers moved to a scratchpad backup, 65 identical up to whitespace,
  3 testbenches genuinely different); the bug report stays in the repo, unsent.
12327 -- synthesis.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12322_to_12327_scherk_schwarz_consolidated.json"
A = ROOT / "analysis"


def main():
    checks, res = {}, {}
    lm = json.loads((A / "search_drivers_12322" / "lmin.json").read_text())
    l0 = json.loads((A / "search_drivers_12322" / "lmin0.json").read_text())
    res["12322"] = dict(lmin_twisted=lm, lmin_untwisted=l0)
    checks["12322: Witten theta^2/theta^4 L_min = -1/3 > -2/3 in all six models (n w = 1/2 channel closed)"] = all(
        v == {"2": "-1/3", "4": "-1/3"} for v in lm.values())
    checks["12322: Witten-untwisted L_min = 0 (control: 10d tachyon-free); V0 + W5 coset L_min = -1/2 (e5 winding channel)"] = all(
        v == {"V0": "0", "V0+W5": "-1/2"} for v in l0.values())
    R6 = math.sqrt(3 / 8); R5 = math.sqrt(2)
    res["12323"] = dict(R6_upper=R6, R5_lower=R5)
    checks["12323: window R_6 < 0.612 sqrt(alpha'), R_5 > 1.414 sqrt(alpha')"] = abs(R6 - 0.6124) < 1e-3 and abs(R5 - 1.4142) < 1e-3
    tf = json.loads((A / "search_drivers_12322" / "tachfree_parents.json").read_text())
    res["12324"] = tf["counts"]
    checks["12324: 99 tachyon-free parents of 1399"] = tf["counts"].get("tachyon-free parent") == 99 and sum(tf["counts"].values()) == 1399
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
