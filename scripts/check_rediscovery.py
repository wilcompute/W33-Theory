#!/usr/bin/env python3
"""Pre-commit guard against REDISCOVERY (failure mode 5).

WHY THIS IS A HOOK AND NOT A NOTE. "Search the corpus before claiming anything
new" was already in the standing instructions and in the agent memory. It failed
twice anyway, at a cost of ~19 passes: the rank law (Pass 322) and the CSS code
(Pass 323) were both re-derived while already proved in-repo AND published. An
instruction that has failed twice is not an instruction, it is a wish. So this
runs at commit time, where it cannot be skipped by forgetting.

WHAT IT DOES. For each staged pass/analysis file, it extracts the RESULTS the
file asserts -- distinctive integers, code parameters [[n,k,d]] / [n,k,d], and
slash-sequences -- and looks them up in RESULTS_INDEX.md. If a result already
appears in files the staged file does not cite, it WARNS with the prior locations.

WHY IT WARNS AND DOES NOT BLOCK. A collision is not proof of rediscovery -- the
same integer legitimately recurs (51840 is the group order; every pass may name
it). Blocking would train people to pass --no-verify, which is worse than no
hook. The hook's job is to put the prior file in front of your eyes at the moment
you would otherwise not look. Reading it is still yours.

Usage:
    py -3 scripts/check_rediscovery.py <files...>      # pre-commit passes these
    py -3 scripts/check_rediscovery.py --all           # sweep everything staged
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "RESULTS_INDEX.md"

RE_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|$")
RE_FILE = re.compile(r"`([^`]+)`")
RE_CSS = re.compile(r"\[\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]\]")
RE_LIN = re.compile(r"\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]")
# vocabulary that makes a single-bracket triple a CODE parameter (Pass 1407)
RE_CODEWORD = re.compile(
    r"(?i)\b(code|CSS|stabili[sz]er|qubit|qutrit|distance|parameters|self-dual|quantum|linear|BCH|quadratic residue|minimum weight)\b")
RE_INT = re.compile(r"(?<![\d.\-])(\d{3,7})(?![\d.])")
RE_SEQ = re.compile(r"\b\d+(?:/\d+){2,}\b")

# NAMED OBJECTS -- added at Pass 348, which found the blind spot the hard way.
# The guard extracted ZERO tokens from Pass 347, whose rediscovered claim was
# "A2 = the q=3 hexagonal lattice = the GKP base" (already in
# w33_eisenstein_grand_synthesis.py, FACE 4). A2 is not a code parameter, not a
# distinctive integer, not a sequence -- so a numbers-only guard is structurally
# blind to it. Results-as-NAMES rediscover exactly as easily as results-as-NUMBERS.
#
# Kept to a hand-curated lexicon of load-bearing objects, NOT open-ended
# capitalized-word extraction: the Pass 328 calibration showed that a guard which
# flags everything is a guard nobody reads. Each entry is an object this repo
# builds theories ON, so a collision is worth forty seconds of a human's time.
NAMED = [
    "Witting polytope", "GKP tower", "GKP code tower", "Heawood", "doily",
    "Csaszar", "Szilassi", "Barnes-Wall", "Leech", "Golay", "tetracode",
    "Eisenstein tower", "Shephard-Todd", "Weil representation", "Weil module",
    "Smith group", "critical group", "Baer subgeometry", "Singer cycle",
    "extraspecial", "trinification", "Hesse", "Steiner system", "Levi graph",
]
RE_NAMED = re.compile("|".join(re.escape(n) for n in NAMED), re.IGNORECASE)
# lattice/root-system names need word boundaries or they match everything
RE_ROOT = re.compile(r"\b(A2|D4|E6|E7|E8|F4|G2|A_2|D_4|E_6|E_8)\b")

# ---------------------------------------------------------------------------
# COMPOUNDS (Pass 349). Pass 348 measured a floor and called it the floor: the
# rediscovery in Pass 347 collided on "A2", which lives in 169 files and is
# therefore a TOPIC, dropped by the >10-file cut. Named objects alone rescued
# only 4 of 28 tokens.
#
# The floor lifts. Measured over 3,555 files: single atoms are usable (<=10
# files) 24% of the time; CO-OCCURRING PAIRS are usable 80% of the time. And the
# decisive case works -- ('a2','eisenstein') appears in exactly 9 files, so the
# ORIGINAL Pass 347 (recovered from git at 39b09db30, before its citation was
# added) WOULD have been flagged against w33_eisenstein_grand_synthesis.py.
#
# The principle: A PAIR OF TOPICS IS A RESULT. "A2" is what the corpus is about;
# "Eisenstein" is what the corpus is about; "A2 AND Eisenstein in one file" is a
# specific claim someone made. Atoms name the subject, compounds name the work.
ATOMS = [
    "Eisenstein", "Witting", "GKP", "Heawood", "doily", "Csaszar", "Szilassi",
    "Leech", "Golay", "tetracode", "hexagonal", "qutrit", "Weil", "Baer",
    "Singer", "extraspecial", "trinification", "Hesse", "Steiner", "Levi",
    "Smith group", "Barnes-Wall", "Shephard-Todd", "moonshine", "Monster",
    "Koide", "PMNS", "Cabibbo", "tomotope", "Clifford", "Bockstein", "torsor",
]
RE_ATOM = re.compile(r"\b(?:" + "|".join(re.escape(a) for a in ATOMS) + r")\b",
                     re.IGNORECASE)



# ---------------------------------------------------------------------------
# NOUN-NUMBER PAIRS (Pass 1107).  Added after a real miss.
#
# Pass 1098 rediscovered two results BT818 already owned -- the maximum partial
# ovoid of W(3,3) is 7, and 36 of the 40 contexts are simultaneously satisfiable.
# The guard could not see either, and neither could the index, for a reason
# sharper than "bare integers are noisy": RESULTS_INDEX's integer pattern is
# `\d{3,9}`, so ONE- AND TWO-DIGIT INTEGERS ARE NEVER INDEXED AT ALL.  Pinning
# `7` as a bare token would not help either, since it occurs in most files.
#
# What is distinctive is not the number but the number ATTACHED TO ITS NOUN.
# "partial ovoid ... 7" and "36 ... contexts" are rare; "7" and "36" are not.
# So a small vocabulary of geometry nouns is paired with any 1-3 digit integer
# occurring within a short window, giving tokens like `ovoid@7`.
#
# Calibrated the same way as every other class here: the flag rate over the pass
# witnesses is measured before this is enabled, not assumed.  See
# scripts/calibrate_index_cut.py.
GEOM_NOUNS = (
    # DELIBERATELY NARROW.  The first version also included the generic nouns
    # frame / block / context / orbital / suborbit / eigenvalue / valency.  Those
    # words appear in nearly every file here, so pairing them with any nearby
    # small integer pushed the measured flag rate from 30.9% to 39.9% -- nine
    # points of noise for tokens that are not distinctive.  The nouns kept below
    # name specific finite-geometry objects, and `ovoid@7` (the token that would
    # have caught the Pass 1098 / BT818 collision) survives the narrowing.
    "ovoid", "heptad", "tritangent", "double-six", "polar pair",
    "partial spread", "hyperbolic line", "totally isotropic", "spread",
)
RE_NOUN = re.compile(r"(?i)\b(" + "|".join(re.escape(n) for n in GEOM_NOUNS) + r")\b")
RE_SMALL = re.compile(r"(?<![\d.\w])(\d{1,3})(?!\d)(?!\.\d)")

# ---------------------------------------------------------------------------
# SIGNED vs UNSIGNED EDGE ACTION (Pass 1428).  Added after a full pass was spent
# on a category error.
#
# This corpus carries TWO different 240-dimensional edge modules:
#
#   * the UNSIGNED permutation module, where Aut permutes the 240 edges;
#   * the orientation-SIGNED module, where Aut acts by signed permutations and
#     the signed-turn operator K lives.
#
# Both are written "240", "edge module", "Q^240".  Pass 1412 decomposed the
# unsigned one and compared multiplicities against ker(K-10I), which is not a
# submodule of it at all -- so a true statement about the permutation module was
# applied to the wrong object, and the conclusion ("not forced") was void.
# Passes 1416-1420 then closed the question with an explicit intertwiner.
#
# `edge240:signed` and `edge240:unsigned` make the two distinguishable to every
# tool that consumes this grammar, so a file asserting one can collide with a
# file asserting the other instead of looking identical.
RE_SIGNED = re.compile(
    r"(?i)\b(signed[- ]turn|oriented edge|orientation[- ]signed|signed permutation"
    r"|directed edge|edge chain|\\partial|Y_?480)\b")
RE_UNSIGNED = re.compile(
    r"(?i)\b(edge permutation|unsigned (?:edge|incidence)|permutation module"
    r"|OnSets|edge set)\b")


def edge_action_tokens(text: str) -> set[str]:
    """Tag which 240-edge action a file is talking about, when it says 240."""
    if not re.search(r"(?<![\d.])240(?![\d.])", text):
        return set()
    out = set()
    if RE_SIGNED.search(text):
        out.add("edge240:signed")
    if RE_UNSIGNED.search(text):
        out.add("edge240:unsigned")
    return out


def noun_number_pairs(text: str) -> set[str]:
    """Tokens `noun@n` for a geometry noun and every small integer near it.

    A window is scanned around each noun occurrence rather than taking the first
    number after it: regex alternation is non-overlapping, so a single pattern
    silently drops the second and later numbers attached to the same noun, which
    is exactly where the interesting one usually sits ("maximum partial ovoid has
    size 7" -- the 7 is last, not first).
    """
    out: set[str] = set()
    for m in RE_NOUN.finditer(text):
        noun = m.group(1).lower().replace(" ", "-")
        lo = max(0, m.start() - 30)
        hi = min(len(text), m.end() + 30)
        for d in RE_SMALL.finditer(text[lo:hi]):
            n = int(d.group(1))
            if n >= 2:                       # 0 and 1 carry no signal
                out.add(f"{noun}@{n}")
    return out


RE_SMALLGROUP = re.compile(r"(?i)\b(?:small|id)group\s*[\[(]\s*(\d+)\s*,\s*(\d+)\s*[\])]")
RE_CLASSICAL = re.compile(
    r"\b(PGSp|PSp|PGL|PSL|PSU|GL|SL|SU|Sp|Sz|U|O)\s*\(?\s*(\d+)\s*,\s*(\d+)\s*\)?")
RE_ATOMIC = re.compile(r"\b([AS])_?(\d{1,2})\b|\b([QD])_?(\d{1,2})\b|\bO_h\b|\b2([TOI])\b")
# A semidirect/direct product, written any of the half-dozen ways this repo does.
#
# ANCHORED AND BOUNDED ON PURPOSE.  The first version matched the whole product
# in one pattern, with a `(?:\s*[x×]\s*...)*` group between two optional-space
# runs.  On `analysis/2026-07-15_pass81_monster_sp43_boundary.md` that backtracks
# catastrophically -- it did not finish in 200 s on a 4 KB file, which silently
# hung the whole boundary sweep (and would have hung the CI hook).  So instead:
# find the separator first, then match each side inside a SHORT window with the
# repetition bounded, which makes the worst case per separator constant.
RE_SEP = re.compile(r"[:⋊]")
RE_LEFT = re.compile(
    r"\(?[CZ]?(\d+)(?:\^(\d+))?\)?"
    r"((?:\s?[x×]\s?\(?[CZ]?\d+(?:\^\d+)?\)?){0,6})\s?$")
RE_RIGHT = re.compile(r"^\s?\(?([CZAS]?)(\d+)")


def _pow_of(base: str, extra: str) -> str:
    """`C2 x C2 x C2` and `2^3` are the same group; write both as `2^3`."""
    n = 1 + len(re.findall(r"[x×]", extra or ""))
    return f"{base}^{n}" if n > 1 else base


def group_tokens(text: str) -> set[str]:
    """Canonical tokens for GROUP-THEORETIC results.

    WHY THIS EXISTS (measured, 2026-07-31).  BT781's boundary section reads

        BT782 should build the explicit bridge functor
        Aut(Q3)=2^3:S3 --> Gamma(T)'=2^4:C3

    and BT782/BT783 answer it directly.  Running the boundary sweep on it
    extracted **zero** tokens, so the sweep could not possibly fire, and Pass
    1127 re-derived BT783's obstruction from scratch.  The cause is not the
    threshold: it is that the entire grammar -- code parameters, slash
    sequences, noun@number -- is blind to `2^3:S3`, which is the single most
    common way a result is stated in this corpus.

    The normalisation matters as much as the matching.  This repo writes one
    group five ways -- `2^3:S3`, `C2^3 : S3`, `(C2 x C2 x C2):S3`,
    `SmallGroup[48,48]`, `C2 x S4` -- so the tokens below collapse cyclic
    factor lists to powers and drop the C/Z prefix, letting a file that says
    `C2^4 : C3` match one that says `2^4:C3`.
    """
    out: set[str] = set()
    for n, k in RE_SMALLGROUP.findall(text):
        out.add(f"grp:{n}.{k}")
    for fam, d, q in RE_CLASSICAL.findall(text):
        out.add(f"grp:{fam.lower()}({d},{q})")
    for sep in RE_SEP.finditer(text):
        i = sep.start()
        lm = RE_LEFT.search(text[max(0, i - 32):i])      # short window, anchored
        rm = RE_RIGHT.match(text[i + 1:i + 10])
        if not (lm and rm):
            continue
        base, exp, extra = lm.groups()
        kind, deg = rm.groups()
        # A bare `n:m` is far more often a dict entry or a ratio than a group.
        # `{1:1, 2:19, 3:8}` (an element-order census) produced tokens like
        # `grp:2:19` in the first sweep. Require SOME group syntax: an exponent,
        # a product, or a C/Z/S/A letter on one side.
        if not (exp or extra.strip() or kind):
            continue
        left = f"{base}^{exp}" if exp else _pow_of(base, extra)
        out.add(f"grp:{left}:{(kind or '').upper()}{deg}".replace("C", ""))
    for m in RE_ATOMIC.finditer(text):
        g = m.group(0).replace("_", "").strip()
        # S0/S1/S2 and A0..A3 are state labels far more often than groups here
        # (BT1856 produced grp:S0..grp:S3 from tape-state names), and the small
        # symmetric/alternating groups carry no signal anyway.
        d = re.search(r"(\d+)", g)
        if g and not (g[0] in "SA" and d and int(d.group(1)) < 4):
            out.add(f"grp:{g}")
    return out


def compounds(text: str) -> set[str]:
    """Co-occurring pairs of central objects, as sorted 'x+y' tokens."""
    from itertools import combinations
    found = {m.lower() for m in RE_ATOM.findall(text)}
    found |= {m.lower() for m in RE_ROOT.findall(text)}
    return {f"{x}+{y}" for x, y in combinations(sorted(found), 2)}

NOISE = {str(y) for y in range(1900, 2100)} | {
    "100", "1000", "200", "300", "400", "500", "600", "700", "800", "900",
    "128", "256", "512", "1024", "2048", "4096",
}
# results so ubiquitous that a hit carries no signal
SKIP = {"51840", "25920", "196883"}

WATCHED = ("analysis/", "passes/", "exploration/")


def load_index() -> dict[str, list[str]]:
    if not INDEX.exists():
        return {}
    out: dict[str, list[str]] = {}
    for line in INDEX.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = RE_ROW.match(line.strip())
        if m:
            out[re.sub(r"\s+", "", m.group(1))] = RE_FILE.findall(m.group(2))
    return out


def results_in(text: str) -> set[str]:
    """Extract only the token classes that carry SIGNAL.

    CALIBRATED, not guessed. Pass 328 ran this guard over all 172 pass files and
    measured the flag rate per token class:

        everything (incl. bare integers) ...... 97%   <- noise; flags everything
        bare integers, even rare-only ......... 78%   <- still noise
        code parameters [[n,k,d]] / [n,k,d] ... 20%   <- SIGNAL
        slash-sequences ....................... 2%    <- signal, sparse

    A guard that flags 97% of commits is a guard nobody reads -- it fails exactly
    the way the instruction it replaces failed. Bare integers are dropped: the
    same integer legitimately recurs everywhere (a dimension, a count, a group
    order), so its recurrence carries no information. Code parameters are the
    objects a rediscovery actually duplicates, and 20% is a rate a human will
    still look at.
    """
    got: set[str] = set()
    # `[[n,k,d]]` is unambiguous -- nothing else is written with double brackets.
    for rx in (RE_CSS, RE_SEQ):
        got |= {re.sub(r"\s+", "", m) for m in rx.findall(text)}
    # `[n,k,d]` IS ambiguous, and measurably so (Pass 1407).  The first
    # corpus-wide collision run put these at the head of the list:
    #
    #   data/w33_packet_vm.json vs w33_python_bytecode_packet_lifter.json,
    #     37 shared tokens: [102,103,104] [105,106,107] [108,109,110] ...
    #
    # Those are not code parameters, they are consecutive array rows in a JSON
    # data file.  The pattern matches ANY three-integer list, and this corpus is
    # full of them -- coordinate triples, index blocks, orbit tables.  So a
    # single-bracket triple only counts when the surrounding text says it is a
    # code, exactly the contextual rule already used for noun-number tokens.
    for m in RE_LIN.finditer(text):
        lo = max(0, m.start() - 60)
        hi = min(len(text), m.end() + 60)
        if RE_CODEWORD.search(text[lo:hi]):
            got.add(re.sub(r"\s+", "", m.group(0)))
    # named objects (Pass 348): results-as-NAMES, invisible to the numeric classes
    got |= {m.lower() for m in RE_NAMED.findall(text)}
    got |= {m for m in RE_ROOT.findall(text)}
    # compounds (Pass 349): a pair of topics is a result
    got |= compounds(text)
    # noun-number pairs (Pass 1107): the number attached to its noun
    got |= noun_number_pairs(text)
    got |= edge_action_tokens(text)
    return got - SKIP



def selftest() -> int:
    """Planted results this guard must extract, and text it must stay quiet on.

    Added Pass 4756. CLAUDE.md calls this the core artifact of the two-agent protocol, and
    Pass 4708 found it had no self-test -- so its silence on a staged file proved nothing.
    Pass 4692 had already found it was not even registered as a hook.

    This tests the EXTRACTOR, which is the part that can fail silently: if results_in()
    returns nothing for a file, the guard reports no collisions for the most conclusive
    possible reason, and the report is indistinguishable from a genuinely novel file.
    """
    cases = [
        ("code parameter [[137,1,21]]",
         "We exhibit a [[137,1,21]] stabilizer code on the substrate.", True),
        # These two are DELIBERATELY not extracted, and finding that out is the point of
        # writing the test. CLAUDE.md: the guard is "calibrated to code parameters only --
        # bare integers flag 97% of files and are pure noise (Pass 328 measured every token
        # class before choosing)". So SRG parameters and a bare group order are silent BY
        # DESIGN. I expected both to fire and was wrong about the guard, not the guard
        # about the corpus -- the fix was to this test.
        ("SRG parameters (excluded by design)",
         "Its collinearity graph is SRG(40,12,2,4) with eigenvalues 12, 2, -4.", False),
        ("bare group order (excluded by design)",
         "The automorphism group is Sp(4,3) of order 51840.", False),
        ("prose with no result",
         "This section explains the motivation and reviews the earlier literature.",
         False),
    ]
    ok = True
    print("  selftest -- does the extractor actually see results?\n")
    for name, text, want in cases:
        got = bool(results_in(text))
        good = got == want
        ok &= good
        toks = sorted(results_in(text))[:3]
        print(f"    {name:30s} extracted={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
        if toks:
            print(f"        {toks}")
    print("""
  TWO OF THESE FOUR ARE DELIBERATE SILENCES, AND THAT IS THE CALIBRATION. Pass 328
  measured every token class across 173 pass files: code parameters collide usefully, bare
  integers flag 97% of files. So the guard sees [[137,1,21]] and not SRG(40,12,2,4), and a
  reader who does not know that will read its silence as novelty. This test is where that
  fact now lives in executable form.

  THE LAST CASE IS THE ONE THAT MAKES THIS A TEST. Ordinary prose must yield NO result
  tokens -- a guard that extracted something from every paragraph would collide with
  everything and be ignored, which is the failure mode CLAUDE.md warns about by name when
  it says bare integers flag 97% of files and are pure noise.

  ITS LIMIT: this tests extraction, not the index. A result correctly extracted from a
  staged file still reports nothing if RESULTS_INDEX.md is stale, and nothing here checks
  the index's freshness.""")
    return 0 if ok else 1

def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    files = [a for a in argv if not a.startswith("-")]
    index = load_index()
    if not index:
        print("[rediscovery] RESULTS_INDEX.md missing or empty; "
              "run: py -3 analysis/build_results_index.py")
        return 0

    hits = 0
    for f in files:
        p = Path(f)
        rel = p.as_posix()
        if not any(w in rel for w in WATCHED) or not p.exists():
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for tok in sorted(results_in(txt)):
            prior = [x for x in index.get(tok, []) if x != rel]
            # only warn when the file does NOT already point at the prior art
            prior = [x for x in prior if Path(x).name not in txt]
            if prior:
                if hits == 0:
                    print("\n" + "=" * 72)
                    print("[rediscovery guard] results that already exist elsewhere")
                    print("=" * 72)
                hits += 1
                shown = " ".join(prior[:3]) + (f" (+{len(prior)-3})" if len(prior) > 3 else "")
                print(f"  {rel}")
                print(f"    {tok}  ->  {shown}")

    if hits:
        print("\n  These are CANDIDATES, not verdicts -- the same integer recurs")
        print("  legitimately. But Passes 322/323 lost ~19 passes to exactly this,")
        print("  so: open the prior file and READ it (end to end -- Pass 286 shows")
        print("  shallow reads cause retractions) before asserting novelty.")
        print("  Cite the prior art in the file and this warning goes away.\n")
    return 0        # advisory by design -- see module docstring


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))