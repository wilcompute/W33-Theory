"""Passes 7205-7212 -- where alpha(W(3,q)) stands, with the method's reliability measured.

  7205  LNS reliability at a size where the answer is known: 6/6.
  7206  How it degrades with q, and what that does to each conclusion.
  7207  q=11 and q=13: lower bounds only, and honestly weak ones.
  7208  The certified basin, restated as a statement about ALL 52-sets.
  7209  Why spectral methods provably cannot improve the upper bound here.
  7210  The Pauli reading, and what is prior art in it.
  7211  Everything this week that was already the repo's.
  7212  Scope.

    py -3 analysis/w33_pass7205_7212_where_alpha_stands.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main() -> int:
    print("=" * 78)
    print("Passes 7205-7212 -- where alpha(W(3,q)) stands")
    print("=" * 78)

    print("\n  PASS 7205-7206 -- the method's reliability, MEASURED not assumed\n")
    print(f"    {'q':>3s}  {'points':>7s}  {'LNS result':>22s}  {'reliability':>28s}")
    rows = [
        (7, 400, "33 = the true optimum", "6/6 seeds, 25s each"),
        (9, 820, "51, never improved", "4 seeds; 16,624 iterations"),
        (11, 1464, "65, still creeping", "two move regimes, both stall"),
        (13, 2380, "83, still creeping", "one run, not converged"),
    ]
    for q, n, res, rel in rows:
        print(f"    {q:3d}  {n:7d}  {res:>22s}  {rel:>28s}")
    print("""
    THE q=7 ROW IS THE ONE THAT LICENSES THE OTHERS. Six independent seeds each hit the exact
    published optimum of 33 within 25 seconds. So at 400 points the method is not merely good,
    it is reliable.

    AND IT DEGRADES WITH SIZE, which is the honest caveat. At 820 points it still converges in
    about three seconds and then never moves in sixteen thousand iterations -- the same
    signature as q=7. At 1464 it is still improving when the budget ends, and two different
    destroy regimes (k = 6..22 with slow exact repairs, k = 3..7 with 63,959 fast ones) both
    stall near 65. That is the signature of a search that has NOT converged.

    SO THE CONCLUSIONS ARE NOT EQUALLY STRONG. 51 at q=9 carries the q=7 signature and four
    independent confirmations. 65 at q=11 and 83 at q=13 carry neither and are weak lower
    bounds that should not be used to fit anything.""")

    print("\n  PASS 7207 -- so q=11 does NOT discriminate yet\n")
    print(f"      {'':10s} {'q=11':>8s}  {'q=13':>8s}")
    print(f"      {'if a(9)=51':10s} {71:8d}  {92:8d}")
    print(f"      {'if a(9)=52':10s} {75:8d}  {102:8d}")
    print(f"      {'LNS has':10s} {65:8d}  {83:8d}")
    print("""
    The discriminating gap at q=11 is 71 versus 75, and the search is at 65 -- below both, and
    by more than the gap between them. It cannot separate the hypotheses until it converges,
    and Pass 7206 says it has not. Reporting that rather than reading the gap as evidence.""")

    print("\n  PASS 7208 -- the basin, restated globally\n")
    print("""    The radius-9 certificate is often described as local. It is not. "No 52-set agrees
    with S in >= 42 points" quantifies over ALL 52-sets, so the theorem is:

        EVERY 52-point partial ovoid of W(3,9), if one exists, meets our specific 51-set
        in AT MOST 41 points.

    That is a statement about the whole solution space, obtained from ten ILP infeasibility
    proofs (d = 0..9); d = 10 did not resolve in 900s. It still does not bound alpha: a 52-set
    far from S remains possible.

    WHY THE RADIUS CANNOT SIMPLY BE PUSHED. A point p outside S can join a 52-set only if all
    of its S-neighbours are removed, so only points with tangent <= d are ever candidates. At
    q=9 the maximum tangent is exactly 10, so at d = 10 the restriction becomes vacuous and
    the reduction that makes small d cheap stops existing. The wall at d = 10 is structural,
    not a matter of more time.""")

    print("\n  PASS 7209 -- spectral methods provably cannot help\n")
    print(f"      {'bound':34s} {'q=7':>6s} {'q=9':>6s}")
    print(f"      {'Hoffman ratio = Delsarte LP':34s} {50:6d} {82:6d}")
    print(f"      {'Tallini q^2-q+1':34s} {43:6d} {73:6d}")
    print(f"      {'ILP dual bound after 240s':34s} {46:6d} {'--':>6s}")
    print(f"      {'best known lower bound':34s} {33:6d} {51:6d}")
    print("""
    THE SPECTRAL BOUNDS ARE WORSE THAN TALLINI AT BOTH q. The collinearity graph is an SRG, so
    the Hoffman ratio bound and the two-class Delsarte LP coincide, and both give q^2+1 --
    the ovoid size, which Tallini already beats by q-1. Anyone reaching for theta, Delsarte or
    the ratio bound here is wasting the run, and that is worth recording as a dead end rather
    than rediscovering it.

    The ILP dual bound does converge -- 50 to 46 at q=7 in 240 seconds -- but had not passed
    43 when measured. It is the only one of these that CAN beat Tallini, since it is not
    limited by the spectrum.""")

    print("\n  PASS 7210-7211 -- what was already the repo's\n")
    print("""    THIS IS THE PART THAT MATTERS MOST, and it was found by searching for results
    rather than topics, twice:

      * scripts/w33_ovoid_stabiliser_exact.py (Pass 6285-6300) already had the exact q=3
        stabiliser order 18, and already CONJECTURED that these stabilisers are tiny "so
        group-orbit constructions cannot work". Pass 7192 PROVED that conjecture; it did not
        discover it, and my commit message for 7187-7194 presented the consequence as new;
      * w33_pass5351_5352 already carried the commuting/anticommuting Pauli dictionary at
        q=2, with a correct disclaimer that it is code geometry and not a physics claim.

    WHAT WAS ACTUALLY NEW: the proof (exact ILPs, caps 30/15/15 against a representable 33);
    |Stab| <= 2 at q=7 and q=9; the certified radius-9 basin; the extension of the Pauli
    dictionary to odd q with a matrix-level control at q=2; and the independent confirmation
    of the other lane's four E8/D4 counts.""")

    print("\n  PASS 7212 -- scope\n")
    print("""    alpha(W(3,9)) IS NOT DETERMINED. The interval remains 51 <= alpha <= 73, with 51
    supported by a method measured 6/6 reliable one size down, and 73 unimproved since Tallini.
    My earlier prediction of 52 stays downgraded and unrefuted.

    NOT DONE: alpha at q = 9, 11, 13; any improvement on Tallini; a 52-set; a proof of 51;
    the d = 10 basin step.""")

    out = {
        "boundary": (
            "alpha(W(3,9)) is NOT determined; 51 <= alpha <= 73 stands. LNS is measured 6/6 "
            "reliable at q=7 where the answer is known, converges with the same signature at "
            "q=9, and has NOT converged at q=11 or q=13 -- so 65 and 83 are weak lower bounds "
            "that must not be used to fit a formula"),
        "reliability": {"q7": {"points": 400, "result": 33, "seeds_hitting_optimum": "6/6",
                               "time": "25s each"},
                        "q9": {"points": 820, "result": 51, "iterations": 16624,
                               "improvements_after_3s": 0},
                        "q11": {"points": 1464, "result": 65, "converged": False,
                                "regimes_tried": ["k=6..22 exact repair",
                                                  "k=3..7, 63959 iterations"]},
                        "q13": {"points": 2380, "result": 83, "converged": False}},
        "q11_does_not_discriminate": {
            "if_alpha9_51": {"q11": 71, "q13": 92},
            "if_alpha9_52": {"q11": 75, "q13": 102},
            "lns_has": {"q11": 65, "q13": 83},
            "why": "below both predictions by more than the gap between them"},
        "basin_is_global": {
            "statement": ("every 52-point partial ovoid of W(3,9), if one exists, meets our "
                          "51-set in at most 41 points"),
            "method": "ten ILP infeasibility proofs, d = 0..9; d=10 unresolved in 900s",
            "why_the_wall_is_structural": (
                "a point outside S can join only if all its S-neighbours are removed, so only "
                "points with tangent <= d are candidates; the maximum tangent at q=9 is 10, "
                "so at d=10 the restriction is vacuous"),
            "still_not_a_bound": "a 52-set far from S remains possible"},
        "spectral_dead_end": {
            "hoffman_eq_delsarte": {"q7": 50, "q9": 82},
            "tallini": {"q7": 43, "q9": 73},
            "verdict": ("spectral bounds are WORSE than Tallini at both q, because the SRG "
                        "ratio bound is q^2+1; only the ILP dual bound can beat Tallini"),
            "ilp_dual_observed": {"q7_after_240s": 46}},
        "already_the_repos": [
            {"what": "the conjecture that these stabilisers are tiny, so group-orbit "
                     "constructions cannot work",
             "where": "scripts/w33_ovoid_stabiliser_exact.py, Pass 6285-6300",
             "my_error": "Pass 7187-7194's commit message presented the consequence as new"},
            {"what": "the commuting/anticommuting Pauli dictionary at q=2",
             "where": "w33_pass5351_5352"}],
        "actually_new": ["the proof that no order-3 element stabilises the q=7 optimum",
                         "|Stab| <= 2 at q=7 and q=9",
                         "certified basin radius 9",
                         "the Pauli dictionary at odd q, controlled at q=2 with matrices",
                         "independent confirmation of the other lane's four E8/D4 counts"],
        "not_done": ["alpha at q = 9, 11, 13", "any improvement on Tallini's 73",
                     "a 52-set", "a proof of 51", "the d=10 basin step"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7205_7212_WHERE_ALPHA_STANDS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
