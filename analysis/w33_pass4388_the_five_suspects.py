#!/usr/bin/env python3
"""Pass 4388 -- the five suspects, read; and the section-level immune system they revealed.

Pass 4380 read twenty of Pass 4375's 216 flagged passages and graded five SUSPECT, with the
honest caveat that "worth a reader" is not "wrong".  This is that reader.  Each of the five
was read with its whole enclosing section and, where the sentence depended on it, the whole
file.  Verdicts below are mine and are stated with the evidence so they can be disputed.

The result of the reading is one confirmed over-read out of five.  It also produced a
structural hypothesis -- four of the five sit under headings like "Relation to ...",
"Connection between ...", "Geometric reading", and three of the five files close with an
explicit "Honest boundary" section naming the part that was actually proved.  The tempting
conclusion was that Pass 4375 had been measuring the size of the corpus's DECORATIVE
sections rather than a backlog in its claims.

PART 2 TESTED THAT ACROSS ALL 216 AND IT IS FALSE.  Of the flags whose enclosing heading
carries any section-type word at all, 19 are decorative and 20 are load-bearing: no
concentration whatsoever.  The hypothesis was formed from five cases and died on the sixth
through two-hundred-and-sixteenth, which is the outcome CLAUDE.md's rule about running the
falsifying computation exists to produce.

WHAT THE FALSIFYING RUN FOUND INSTEAD IS WORTH MORE THAN THE HYPOTHESIS WAS.  The "Honest
boundary" convention is real but it is not the corpus's -- it is ONE ARC's, and it stopped:

    2026-05 arc     86 of 98 files (88%)  close with an "Honest boundary" section
    2026-06 arc      0 of 15 ( 0%)
    2026-07 arc      0 of 69 ( 0%)
    everything else 22 of 1427 ( 2%)

Three of my five suspects are 2026-05 files.  I was not sampling the corpus; I was sampling
the month with the best hygiene, and mistook a house style for a property of the whole.  The
recommendation at the end of this pass follows from that and costs one heading per file.

    py -3 analysis/w33_pass4388_the_five_suspects.py

"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Part 1 -- the five, read.
# ---------------------------------------------------------------------------
# verdict vocabulary, refined from Pass 4380's by the act of reading:
#   OVER-READ  -- the sentence claims more than the construction supports.  CONFIRMED.
#   DECORATIVE -- the signature is real, but the file's own theorem and honest boundary
#                 exclude the passage, so nothing downstream rests on it.
#   SOUND      -- on reading, the map IS named; the sweep missed it.
#   EXEMPLARY  -- the passage is the PREMISE of an inference the same file then REFUTES.
SUSPECTS = [
    {
        "file": "2026-07-07_pass69_three_perpendicular_tracks.md", "line": 132,
        "text": "All three tracks point to the same number: sqrt(97).",
        "section": "Connection Between All Three Tracks",
        "verdict": "OVER-READ",
        "finding":
            "lambda_2 = (1+sqrt 97)/2 is ONE eigenvalue of ONE adjacency matrix. Track 1 "
            "uses it for the Ramanujan violation; Track 2's HOM dip tau = 16 pi/(sqrt 97 "
            "- 5) is DERIVED from lambda_2 - lambda_3; Track 3's spectral gap is that "
            "same spectrum. The three tracks do not converge on sqrt(97) -- they consume "
            "it. The sentence reads as independent confirmation and the construction "
            "cannot supply any.",
        "remedy":
            "three CONSEQUENCES of one eigenvalue, not three routes to it. Track 2's "
            "prediction is still genuinely falsifiable, but measuring tau confirms the "
            "shared spectrum, not the two other tracks.",
        "load": "the file's Track-1 theorem does not use the sentence; the harm is framing",
    },
    {
        "file": "2026-05-18_toroidal_metric_parity_taylor.md", "line": 176,
        "text": "79 = 160 - 81 matches the signed phase-frame kernel.",
        "section": "Relation to the spectrum",
        "verdict": "DECORATIVE",
        "finding":
            "one of four ad-hoc arithmetic decompositions in a row (48 = 2*24, 504/7 = 72, "
            "401 = 320+81, 79 = 160-81). 79 is prime and small; there are many ways to "
            "write it. This IS the signature.",
        "remedy":
            "none needed to the mathematics. The file's theorem is the exact Taylor "
            "identity P(t) = 12u + 48u^2 + 0u^3 + 4u^4 + u^5 + 3u^6, which is proved and "
            "uses none of the four; its honesty boundary already says 'it does not prove "
            "physical' anything.",
        "load": "zero -- excluded by the file's own honesty boundary",
    },
    {
        "file": "2026-05-31_polarity_chirality_orientation_duality.md", "line": 131,
        "text": "This cleanly matches the toroidal duality.",
        "section": "Relation to toroidal duality",
        "verdict": "SOUND",
        "finding":
            "the sweep saw 'matches the' and no licence in four lines. The licence is on "
            "line 141: 'Fano polarity implements the dual swap' -- the map is NAMED, which "
            "is precisely what CLAUDE.md's rule asks for. Line 125, six lines ABOVE, is an "
            "explicit refusal of the stronger claim: 'it is not meaningful, at this "
            "abstract F2-incidence level, to claim that polarity preserves or reverses "
            "Euclidean chirality.'",
        "remedy": "none. Upgrade from SUSPECT; the window was too narrow, not the passage.",
        "load": "n/a",
    },
    {
        "file": "2026-05-30_ordered_spread_transport_orbits.md", "line": 51,
        "text": "So the count matches the full linear symplectic order exactly.",
        "section": "Setup",
        "verdict": "EXEMPLARY",
        "finding":
            "40*36*36 = 51840 = |Sp(4,3)| is arithmetic and true. The line is the SETUP "
            "for 'the tempting stronger claim' stated on line 11 -- and the rest of the "
            "file REFUTES it: PSp(4,3) does not act with one regular orbit, the triples "
            "split by incidence type, and the file's corrected statement demands the "
            "missing sign/orientation datum.",
        "remedy":
            "none. This is failure mode 6 handled correctly, at length, in 2026-05-30.",
        "load": "the file exists to remove the load",
    },
    {
        "file": "2026-05-29_q4_fano_chain_complex_homology.md", "line": 133,
        "text": "This matches the known signed phase-frame rank: rank(AA^T/160) = 81.",
        "section": "Geometric reading (trailing clause of the compressed theorem)",
        "verdict": "DECORATIVE",
        "finding":
            "3^4 = 81 from four qutrit phase modes, and a matrix rank that is also 81. No "
            "map is named between them. It appears in the compressed theorem, but as a "
            "trailing 'matching' clause after the proved part.",
        "remedy":
            "the proved part is the homology computation (H0,H1,H2) = (1,0,7) full and "
            "(1,0,3) after antipodal quotient, and the file's honest boundary claims "
            "exactly that -- 'this proves the finite chain-complex homology bridge'. The "
            "81 = 81 clause is outside it.",
        "load": "zero by the file's own boundary; would be mode 6 if anything rested on it",
    },
]

# ---------------------------------------------------------------------------
# Part 2 -- the falsifying run.  Pass 4375's detector, rerun, with each hit attributed
# to its enclosing markdown heading; plus the "Honest boundary" convention by arc.
# ---------------------------------------------------------------------------
COUNTING = re.compile(
    r"\b(both (?:have|are|carry|give)|the same (?:size|order|number|count|dimension)|"
    r"also has|matches the|coincid\w+|equal(?:s|ly)? in (?:size|number|order)|"
    r"same cardinality|identical (?:size|count|order))\b", re.I)
LICENSED = re.compile(
    r"\b(character|conjugat\w+|isomorph\w+|equivariant|stabiliser|stabilizer|"
    r"permutation character|G-set|gset|as (?:a )?G-set|non-conjugate|inequivalent|"
    r"up to isomorphism|structure|bijection)\b", re.I)

# A section is LOad-bearing if the file's claim lives there, DEcorative if the file has
# parked the evocative material under its own heading.  These are the corpus's own words.
LOAD_BEARING = re.compile(
    r"\b(theorem|proof|verifier|verification|result|setup|computation|certificate|"
    r"lemma|corollary|construction|test|check)\b", re.I)
DECORATIVE = re.compile(
    r"\b(relation|connection|meaning|reading|interpretation|why this|dictionary|"
    r"physical|analogy|picture|context|remark|discussion|outlook|speculat)\w*\b", re.I)
BOUNDARY = re.compile(r"^#+\s*(honest\w*|honesty)\s+boundary", re.I | re.M)


def enclosing_heading(lines: list[str], i: int) -> str:
    for j in range(i, -1, -1):
        if lines[j].startswith("#"):
            return lines[j].lstrip("# ").strip()
    return ""


def main() -> int:
    print("=" * 78)
    print("Pass 4388 -- the five suspects, read")
    print("=" * 78)

    c = Counter(s["verdict"] for s in SUSPECTS)
    for s in SUSPECTS:
        print(f"\n  {s['verdict']:11s} {s['file'][:52]}:{s['line']}")
        print(f"    section : {s['section']}")
        print(f"    passage : \"{s['text']}\"")
        for k in ("finding", "remedy", "load"):
            body = " ".join(s[k].split())
            print(f"    {k:8s}: {body[:88]}")
            for k2 in range(88, len(body), 88):
                print(f"              {body[k2:k2 + 88]}")

    print(f"""
  FIVE READ: {c['OVER-READ']} confirmed over-read, {c['DECORATIVE']} decorative, {c['SOUND']} sound on reading,
  {c['EXEMPLARY']} exemplary (the premise of an inference its own file refutes).  ZERO mathematical
  errors: every number in all five is correct.

  THE ONE CONFIRMED FINDING is the sqrt(97) sentence, and it is failure mode 2 (over-read),
  not mode 6.  Nothing is miscounted; the word "tracks" implies three independent routes
  to a value that all three in fact take as input from the same adjacency matrix.""")

    # ---- part 2 -----------------------------------------------------------
    print("\n" + "=" * 78)
    print("Part 2 -- the falsifying run, over all 216")
    print("=" * 78)

    kinds: Counter[str] = Counter()
    head_hits: Counter[str] = Counter()
    with_boundary = 0
    total = 0
    files_seen: set[str] = set()
    for f in sorted((ROOT / "analysis").glob("*.md")):
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = raw.splitlines()
        hits = []
        for i, ln in enumerate(lines):
            if not COUNTING.search(ln):
                continue
            if LICENSED.search(" ".join(lines[max(0, i - 4):i + 5])):
                continue
            hits.append(i)
        if not hits:
            continue
        has_boundary = bool(BOUNDARY.search(raw))
        for i in hits:
            total += 1
            files_seen.add(f.name)
            h = enclosing_heading(lines, i)
            head_hits[h.lower()[:44] or "(no heading)"] += 1
            dec, lb = bool(DECORATIVE.search(h)), bool(LOAD_BEARING.search(h))
            kinds["decorative" if dec and not lb else
                  "load-bearing" if lb and not dec else
                  "both/ambiguous" if lb and dec else "unclassified"] += 1
            with_boundary += has_boundary

    print(f"\n  HYPOTHESIS (from the five): flags concentrate under decorative headings.")
    print(f"\n  flagged passages re-detected : {total}  (across {len(files_seen)} files)")
    print(f"  distinct enclosing headings  : {len(head_hits)}")
    print(f"\n  {'enclosing section kind':22s} {'count':>6s} {'share':>7s}")
    for k in ("decorative", "load-bearing", "both/ambiguous", "unclassified"):
        print(f"  {k:22s} {kinds[k]:6d} {100 * kinds[k] / max(total, 1):6.0f}%")

    dec, lb = kinds["decorative"], kinds["load-bearing"]
    clf = dec + lb
    print(f"""
  HYPOTHESIS REFUTED.  Among the {clf} flags whose heading carries any section-type word,
  {dec} are decorative and {lb} are load-bearing -- a {dec / max(lb, 1):.2f}:1 ratio, which is no
  concentration at all.  The other {kinds['unclassified']} sit under {len(head_hits)} mostly-unique headings that are
  pass titles or content titles and carry no section-type signal to read.

  I formed this from five cases and it died on the two hundred and eleven others.  That is
  the outcome the rule is for: run the computation that would break the claim, and run it
  before recording the claim, not after.""")

    # --- the falsifying run's own finding: the convention is one arc's, and it stopped ---
    by_arc: Counter[str] = Counter()
    arc_boundary: Counter[str] = Counter()
    for f in sorted((ROOT / "analysis").glob("*.md")):
        m = re.match(r"(\d{4}-\d{2})", f.name)
        arc = m.group(1) if m else "not date-named"
        by_arc[arc] += 1
        try:
            if BOUNDARY.search(f.read_text(encoding="utf-8", errors="replace")):
                arc_boundary[arc] += 1
        except OSError:
            pass
    print(f"\n  {'arc':16s} {'files':>6s} {'closes with Honest boundary':>28s} {'share':>7s}")
    for arc in sorted(by_arc):
        print(f"  {arc:16s} {by_arc[arc]:6d} {arc_boundary[arc]:28d} "
              f"{100 * arc_boundary[arc] / by_arc[arc]:6.0f}%")
    tot_b, tot_f = sum(arc_boundary.values()), sum(by_arc.values())
    print(f"  {'TOTAL':16s} {tot_f:6d} {tot_b:28d} {100 * tot_b / tot_f:6.0f}%")

    print(f"""
  AND HERE IS WHAT THE FALSIFYING RUN FOUND, WHICH IS WORTH MORE THAN THE HYPOTHESIS WAS.

  The "Honest boundary" section -- one heading, one or two sentences, naming exactly what
  the file proved and what it did not -- is a convention of the 2026-05 arc.  {arc_boundary['2026-05']} of its {by_arc['2026-05']}
  files carry it.  The next two arcs carry it {arc_boundary['2026-06'] + arc_boundary['2026-07']} times in {by_arc['2026-06'] + by_arc['2026-07']} files.  It did not spread
  and it did not survive; it was simply dropped, and nothing replaced it.

  THAT ALSO EXPLAINS MY SAMPLE.  Three of my five suspects are 2026-05 files, and they read
  well because that arc states its own scope.  I was not sampling the corpus -- I was
  sampling the month with the best hygiene, and generalising a house style to 1611 files.

  THE RECOMMENDATION, AND IT IS CHEAP.  Reinstate the section.  Failure mode 2 (over-read)
  and failure mode 6 (untested premise) are both, in the end, requests for one sentence
  stating the scope the witness establishes.  The 2026-05 arc wrote that sentence under a
  standard heading, which makes it greppable, auditable, and impossible to omit silently.
  It is the only practice in this repository that addresses the two most common failure
  modes at once, it is already proven here, and it was abandoned without being replaced.""")

    out = {
        "suspects_read": len(SUSPECTS),
        "verdicts": {s["file"] + ":" + str(s["line"]): s["verdict"] for s in SUSPECTS},
        "detail": SUSPECTS,
        "confirmed_over_reads": c["OVER-READ"],
        "mathematical_errors": 0,
        "reflagged_total": total,
        "distinct_headings": len(head_hits),
        "section_kind": dict(kinds),
        "hypothesis": "flags concentrate under decorative headings",
        "hypothesis_verdict": "REFUTED",
        "decorative_vs_load_bearing": [dec, lb],
        "honest_boundary_by_arc": {a: [by_arc[a], arc_boundary[a]] for a in sorted(by_arc)},
        "conclusion": (
            "one confirmed over-read of five (sqrt(97) framed as three convergent routes "
            "to one eigenvalue all three consume); zero mathematical errors; the "
            "decorative-concentration hypothesis is REFUTED at 19:20; and the falsifying "
            "run found that the 'Honest boundary' convention is 88% of the 2026-05 arc "
            "and ~0% after it -- a proven in-repo remedy for failure modes 2 and 6 that "
            "was dropped without replacement"),
    }
    p = ROOT / "data" / "PART_W33_PASS4388_FIVE_SUSPECTS.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
