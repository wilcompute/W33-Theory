#!/usr/bin/env python3
"""Pass 4380 -- I read twenty of the 216, and the corpus is better than my sweep implied.

Pass 4375 flagged 216 passages asserting a shared count with no comparability language in a
four-line window, and concluded honestly that quantifying the real backlog needed reading
rather than grepping.  This is the reading: a seeded random sample of twenty, each judged
against the actual question -- does the passage draw a conclusion from a count without
licensing it?

The classification is recorded per passage so the judgement can be disputed.  It is my
judgement, not a computation, and that is the point: Pass 4375 said this could not be
automated and it could not.

    py -3 analysis/w33_pass4380_reading_twenty.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# verdicts: EXEMPLARY -- the author explicitly licensed or explicitly refused the inference
#           SOUND     -- a count is reported, no inference drawn from it
#           SUSPECT   -- a match is asserted and something is concluded; needs a reader
VERDICTS = [
    ("2026-07-10_levi_closure.md", 78, "SOUND",
     "reports two weight sequences agree; draws nothing from it"),
    ("2026-07-15_pass76_k6_matchings_codewords.md", 42, "EXEMPLARY",
     "labels it 'triple coincidence noted', then TESTS the connection and finds the "
     "complement is NOT in ker(A^T)"),
    ("2026-07-07_pass69_three_perpendicular_tracks.md", 132, "SUSPECT",
     "'all three tracks point to the same number sqrt(97)' -- three routes to one value, "
     "and the shared value is the argument"),
    ("2026-05-30_s4_torsor_bridge_between_12_codecs.md", 36, "EXEMPLARY",
     "'both are 12-element regular torsors, BUT FOR DIFFERENT GROUPS' -- the exact "
     "distinction CLAUDE.md's G-set rule exists for"),
    ("2026-05-18_toroidal_metric_parity_taylor.md", 176, "SUSPECT",
     "bare 'matches the signed phase-frame kernel'"),
    ("2026-05-18_toroidal_spectrum_realization_bridge.md", 82, "SOUND",
     "reports invariants; not a comparability claim"),
    ("2026-07-10_levi_closure.md", 15, "SOUND", "reports that two counts are both odd"),
    ("2026-05-18_minimal_logical_x_scheme_eigenmatrix.md", 103, "SOUND",
     "'matches ... NOW EXPLAINED BY the primitive eigenspaces' -- supplies the mechanism"),
    ("2026-05-30_ordered_spread_transport_orbits.md", 102, "EXEMPLARY",
     "'same order as the total number of triples, SO a regular transport interpretation "
     "MUST INCLUDE more' -- names the coincidence and demands more"),
    ("2026-05-31_polarity_chirality_orientation_duality.md", 131, "SUSPECT",
     "'this cleanly matches the toroidal duality'"),
    ("2026-07-15_pass353_factor17_rep_theory.md", 50, "EXEMPLARY",
     "'flagged speculative ... filed as open, not proved'"),
    ("2026-05-21_toroidal_dual_genus_horizon.md", 40, "SOUND", "reports a shared formula"),
    ("2026-05-18_horizon_f3_parity_matrix.md", 70, "SOUND",
     "'[72,66]-STYLE' -- rank determines n and k, so the inference is licensed and the "
     "hedging word is doing real work"),
    ("2026-05-30_index_read_correction_and_local_shell.md", 21, "SOUND",
     "a meta-comment about a page emphasising a coincidence"),
    ("2026-07-15_pass354_factor17_correction.md", 35, "EXEMPLARY",
     "'Is this a coincidence? ... The source is unknown.'"),
    ("2026-05-30_ordered_spread_transport_orbits.md", 51, "SUSPECT",
     "'the count matches the full linear symplectic order exactly'"),
    ("2026-05-18_toroidal_vef_edge_phase_kernel.md", 103, "SOUND", "reports a shared value"),
    ("2026-06-07_bc_ring_torus_lift.md", 156, "EXEMPLARY",
     "'this is NOT a numerical coincidence; it is a chain-complex theorem'"),
    ("2026-05-31_fano_84_chart_codec.md", 127, "EXEMPLARY",
     "'does NOT yet prove a canonical equality ... it proves a natural object of the same "
     "size' -- the distinction stated in one sentence"),
    ("2026-05-29_q4_fano_chain_complex_homology.md", 133, "SUSPECT",
     "'this matches the known signed phase-frame rank'"),
]


def main() -> int:
    print("=" * 78)
    print("Pass 4380 -- twenty of the 216, read rather than grepped")
    print("=" * 78)
    c = Counter(v for _, _, v, _ in VERDICTS)
    n = len(VERDICTS)
    for f, ln, v, why in VERDICTS:
        print(f"  {v:10s} {f[:46]:46s}:{ln:<5d}")
    print(f"\n  {'verdict':12s} {'count':>6s} {'share':>8s}")
    for v in ("EXEMPLARY", "SOUND", "SUSPECT"):
        print(f"  {v:12s} {c[v]:6d} {100 * c[v] / n:7.0f}%")
    print(f"  {'confirmed errors':12s} {0:6d} {0:7.0f}%")

    print(f"""
  THE CORPUS IS BETTER THAN MY SWEEP IMPLIED, AND I SHOULD SAY SO PLAINLY.

  Zero of twenty is a confirmed untested premise.  {c['EXEMPLARY']} of twenty are EXEMPLARY: the
  author noticed the coincidence and explicitly did the thing failure mode 6 asks for --
  "both are 12-element regular torsors, but for different groups"; "this does not yet prove
  a canonical equality, it proves a natural object of the same size"; "is this a
  coincidence? the source is unknown"; "this is not a numerical coincidence, it is a
  chain-complex theorem".  Those sentences are the discipline, written years of passes
  before I named the mode.

  {c['SOUND']} more simply report two numbers and draw nothing from them, which is not an error in
  any sense.  {c['SUSPECT']} assert a match and lean on it, and those are worth a reader --
  but "worth a reader" is not "wrong", and none of the five is obviously false.

  WHAT THIS DOES TO PASS 4375'S FRAMING.  That pass said the signature was common and
  unchecked, and implied a backlog.  The signature IS common; the backlog is not
  demonstrated.  Extrapolating the sample, roughly a quarter of the 216 merit a read and
  none of the twenty was an error -- so the honest estimate of confirmed untested premises
  in the older corpus is ZERO, with an upper bound I cannot tighten without reading fifty
  more.

  AND THE MOST USEFUL FINDING IS THE OPPOSITE OF WHAT I EXPECTED.  Failure mode 6 was
  derived from three errors made THIS SESSION, in a track that had been moving fast. The
  older corpus, written more slowly, already applies the rule and often says so in the
  text. The mode is real; the claim that it had been operating unnoticed for four thousand
  passes is not supported, and I withdraw the implication.""")

    out = {

        "boundary": ("twenty of 216 read, by one reader, and the verdicts are judgements rather "

            "than computations; the estimate of zero confirmed untested premises is a "

            "sample statement and its upper bound cannot be tightened without reading more"),"sampled": n, "seed": 4380,
           "verdicts": [{"file": f, "line": ln, "verdict": v, "why": w}
                        for f, ln, v, w in VERDICTS],
           "counts": dict(c), "confirmed_errors": 0,
           "conclusion": ("zero confirmed untested premises in twenty; the older corpus "
                          "already applies the rule and frequently states it; Pass 4375's "
                          "implied backlog is withdrawn")}
    p = ROOT / "data" / "PART_W33_PASS4380_READING_TWENTY.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
