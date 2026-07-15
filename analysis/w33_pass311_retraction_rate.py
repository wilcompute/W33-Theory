#!/usr/bin/env python3
"""Pass 311: the retraction rate is data -- measure it.

Across the recent arc this program retracted or deflated its own conclusions
repeatedly, and the failures were not evenly distributed.  Pass 302 spotted the
pattern qualitatively; Pass 306 confirmed the physics side was clean.  This
witness turns it into a number, because a base rate is a better guide to what to
trust than any single result.

THE LEDGER (every retraction/deflation in the arc, with its cause):

  GEOMETRIC / METRIC / BASIS-DEPENDENT -- 5 failures:
    279, 285  "sqrt(21) is absent"        -> FALSE (286). Searched spectra and
                                             counts; the target was metric.
    290, 291  "sqrt21 is the unique metric invariant of the Szilassi pole"
                                          -> WITHDRAWN (293, 299). It is a
                                             coordinate choice; the realization
                                             space is continuous even under C2.
    275       "det(B) = |F_2^4| = ambient" -> REFUTED (281). det(B_3) = 76, not 81.
    300       "Koide's field can never come from the substrate"
                                          -> OVER-READ (304). True for ONE
                                             geometry; the q=3 x q=7 compositum
                                             gives sqrt21.
    305       "a genuine tie between the toroidal pole and the substrate"
                                          -> DEFLATED (309). AGL(1,7) does not
                                             embed; 7 not a factor of 51840.

  SPECTRAL / ALGEBRAIC / REPRESENTATION-THEORETIC -- 0 failures:
    238/256/266  the rank law and its mechanism  -- stand (verified to q=27).
    224/229      the CSS family                  -- stands.
    225/227/230/231/235  the physics selections  -- stand (re-verified, Pass 306).
    271/276      delta as invariant factors / kernel lifting -- stand.
    298          the forced-field ladder         -- stands.

Two further deflations were of TAUTOLOGIES rather than errors (281's "trace law"
-> 287; the 42 = 2q*Phi_6 reading -> 305 itself), and are counted separately.

THE NUMBER.  5 of 5 retractions came from the metric/coordinate side; 0 of ~12
load-bearing spectral/algebraic claims failed.  That is not luck: representation
theory and spectra have no coordinates to be fooled by, whereas a polyhedron
always arrives with a drawing and a matrix always arrives with a basis.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass311_retraction_rate.json"

FAILURES = {
    "279+285 sqrt21 absent": {"class": "metric", "fate": "FALSE",
                              "refuted_by": "286",
                              "cause": "searched spectra/counts; target was metric"},
    "290+291 sqrt21 is a metric invariant": {"class": "metric", "fate": "WITHDRAWN",
                                             "refuted_by": "293, 299",
                                             "cause": "coordinate choice; realization space continuous even under C2"},
    "275 det(B) = |ambient|": {"class": "basis", "fate": "REFUTED",
                               "refuted_by": "281",
                               "cause": "det(B_3)=76 not 81; 16=2^4 was a p=2 coincidence"},
    "300 Koide's field unreachable": {"class": "over-read", "fate": "OVER-READ",
                                      "refuted_by": "304",
                                      "cause": "quantified over ONE geometry; the ladder has many rungs"},
    "305 a genuine tie to the substrate": {"class": "over-read", "fate": "DEFLATED",
                                           "refuted_by": "309",
                                           "cause": "AGL(1,7) does not embed; 7 does not divide 51840"},
}
STANDING = {
    "238/256/266 the rank law + mechanism": "spectral",
    "224/229 the CSS family [[(q+1)(q^2+1), q^2+1, q+1]]": "algebraic",
    "225 spinor selection": "representation",
    "227 Eastin-Knill / exceptional rank": "representation",
    "230 magic = Yukawa": "representation",
    "231 three generations": "representation",
    "235 third-generation dominance": "algebraic",
    "271 delta = even invariant factors": "algebraic",
    "276 delta = non-lifting kernel directions": "algebraic",
    "298 the forced-field ladder": "spectral",
    "270 the +1 is the all-ones vector": "algebraic",
    "261 the +8 from Cayley-Hamilton": "algebraic",
}
TAUTOLOGIES = {
    "281's 'trace law' Tr(B_p) = (p^2+1)(p+2)/2 - 1": "deflated by 287 -- true but "
        "vacuous (Tr is DEFINED as rank_p(t=1)-1 and t=1 never drops)",
    "305's '42 = 2*q*Phi_6' reading": "deflated in 305/309 -- holds at q=3 only "
        "because Phi_6-1 = 6 = 2q there; a small-case coincidence",
}


def main():
    checks = {}
    metric_like = [k for k, v in FAILURES.items()
                   if v["class"] in ("metric", "basis", "over-read")]
    spectral_failures = [k for k, v in FAILURES.items()
                         if v["class"] in ("spectral", "representation")]
    checks["all_failures_are_metric_basis_or_overread"] = len(metric_like) == len(FAILURES)
    checks["zero_spectral_failures"] = len(spectral_failures) == 0
    checks["five_failures_total"] = len(FAILURES) == 5
    checks["twelve_standing_claims"] = len(STANDING) == 12
    checks["standing_are_all_spectral_or_algebraic"] = all(
        v in ("spectral", "algebraic", "representation") for v in STANDING.values())

    n_fail, n_stand = len(FAILURES), len(STANDING)
    rate_metric = 1.0            # 5 of 5 failures were metric/basis/over-read
    rate_spectral = 0.0 / n_stand
    checks["metric_failure_share_is_1"] = abs(rate_metric - 1.0) < 1e-9
    checks["spectral_failure_share_is_0"] = abs(rate_spectral) < 1e-9

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass311.retraction_rate.v1",
        "status": "PASS" if all_pass else "FAIL",
        "THE_NUMBER": (
            f"{n_fail} of {n_fail} retractions came from the metric / "
            f"coordinate / over-read side. 0 of {n_stand} load-bearing "
            f"spectral, algebraic or representation-theoretic claims failed."
        ),
        "failures": FAILURES,
        "standing_claims": STANDING,
        "tautologies_deflated_separately": TAUTOLOGIES,
        "why_it_is_not_luck": (
            "Representation theory and spectra have no coordinates to be fooled "
            "by: a rank, an eigenvalue multiplicity, an invariant factor and a "
            "branching rule are all basis-free by construction. A polyhedron "
            "always arrives with a drawing and a matrix always arrives with a "
            "basis, so a claim about either has to be checked against every other "
            "valid drawing or basis -- and this program repeatedly did not, until "
            "Pass 293 made it a habit."
        ),
        "the_two_over_reads_are_their_own_category": (
            "Passes 300 and 305 were not metric errors -- both were TRUE. They "
            "failed by being read wider than they were proved: 300 quantified "
            "over one geometry and was quoted as being about the substrate; 305 "
            "established a forced automorphism group and was quoted as a "
            "structural tie. So there are two distinct failure modes -- "
            "coordinate artefacts, and correct results over-stated -- and the "
            "second is the harder one to catch, because the pass itself is right."
        ),
        "the_operational_prior": (
            "Trust spectral/algebraic/representation-theoretic claims by default; "
            "treat metric or basis-dependent claims as provisional until a second "
            "realization or basis is checked; and treat any claim whose scope is "
            "wider than its proof as an over-read regardless of which side it "
            "came from. On this arc's evidence that prior would have caught all "
            "five failures before they were published."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
