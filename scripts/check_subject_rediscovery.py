"""Guard: would this commit's SUBJECT LINE have found prior art, if searched?

WHY THIS GUARD AND NOT THE EXISTING ONE. scripts/check_rediscovery.py scans STAGED FILES for
code parameters that exist elsewhere uncited. It is calibrated and it works. But it missed two
rediscoveries in one session, both with the same shape:

  * "the 36 spreads and the 36 double sixes are the SAME graph" -- already MCCCXCIII/MCCCXCIV/
    MCCCXCV, which had the scheme, an EXPLICIT isomorphism, and |Aut| = 51840 and 1440;
  * "the points of W(3,3) are the A2 subsystems of E8" -- BT1750 already had the 40 hexagons
    and their Coxeter 5-cycle structure.

In both cases the diff contained no colliding code parameter, so the file guard was silent.
What WOULD have caught the FIRST is searching the corpus for the claim as stated in the commit
SUBJECT, before committing -- guard the sentence, not the numbers.

IT WOULD NOT HAVE CAUGHT THE SECOND, and the selftest says so. BT1750 calls those objects
"hexagons"; I called them "A2 subsystems". Same objects, disjoint vocabulary. Word matching
cannot bridge a rename, so this guard covers rediscoveries that REUSE the prior art's words
and provably not those that rename the object. Half a guard, honestly labelled.

HOW IT WORKS. Take the subject line, drop boilerplate (pass numbers, track tags), extract
content phrases, and grep the corpus for each. Report any file that matches two or more
independent content words from the subject. WARN ONLY -- like the existing guard, because
blocking trains --no-verify.

    py -3 scripts/check_subject_rediscovery.py --selftest
    py -3 scripts/check_subject_rediscovery.py "your commit subject here"
"""

from __future__ import annotations

import re
import subprocess  # noqa: F401
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STOP = {
    "the", "and", "are", "was", "were", "is", "a", "an", "of", "in", "on", "to", "for",
    "with", "that", "this", "it", "its", "at", "by", "from", "not", "no", "but", "or",
    "as", "so", "same", "after", "before", "than", "then", "into", "out", "up", "down",
    "add", "adds", "added", "fix", "fixes", "fixed", "reserve", "reserved", "pass",
    "passes", "track", "glue", "my", "own", "one", "two", "three", "i", "we", "our",
    "be", "been", "have", "has", "had", "all", "any", "more", "most", "only", "just",
    "now", "new", "old", "does", "do", "did", "can", "cannot", "will", "would", "what",
    "which", "who", "when", "where", "why", "how", "if", "correction", "corrected",
}


def content_words(subject: str) -> list[str]:
    s = re.sub(r"Pass\s*\d+[-–]?\d*", " ", subject, flags=re.I)
    s = re.sub(r"\(.*?\)", " ", s)
    toks = re.findall(r"[A-Za-z][A-Za-z0-9_,()]*|\d{2,}", s)
    out = []
    for t in toks:
        w = t.strip(",()").lower()
        if len(w) < 3 or w in STOP:
            continue
        out.append(w)
    return out


def search_corpus(words: list[str], exclude: str = "") -> dict[str, int]:
    """Count how many of the words each corpus file matches.

    Pure Python: ripgrep is NOT on PATH in this environment, and the first version of
    this guard shelled out to `rg` and silently returned zero hits -- failing its own
    selftest, which is the only reason the bug was visible.
    """
    pats = [re.compile(re.escape(w), re.I) for w in words]
    hits: dict[str, int] = {}
    roots = [ROOT / d for d in ("analysis", "manuscripts", "scripts", "docs")]
    for r in roots:
        if not r.is_dir():
            continue
        for f in list(r.rglob("*.md")) + list(r.rglob("*.py")):
            if "__pycache__" in str(f):
                continue
            if f.name == Path(__file__).name:
                continue          # never match this guard's own selftest text
            if exclude and exclude in f.name:
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            n = sum(1 for pat in pats if pat.search(txt))
            if n:
                hits[f.name] = n
    return hits


def report(subject: str, exclude: str = "", threshold: int = 3) -> list[str]:
    words = content_words(subject)
    if len(words) < 2:
        return []
    hits = search_corpus(words, exclude)
    ranked = sorted(hits.items(), key=lambda kv: -kv[1])
    out = []
    for name, n in ranked[:6]:
        if n >= threshold:
            out.append(f"{name} matches {n}/{len(words)} content words of the subject")
    return out


def selftest() -> int:
    print("  selftest -- would the subject have found the prior art?\n")
    cases = [
        ("the 36 spreads and the 36 double sixes are the SAME graph",
         "w33_pass7245", True,
         "MCCCXCIII/MCCCXCIV/MCCCXCV exist and were missed"),
        # KNOWN BLIND SPOT, and the reason it is listed as want=False. BT1750 calls
        # these objects "hexagons"; I called them "A2 subsystems". Same objects,
        # disjoint vocabulary, so word matching CANNOT bridge it. The guard catches
        # rediscoveries that reuse the prior art's words, and provably not those that
        # rename the object. Stating the limit rather than pretending coverage.
        ("the points of W(3,3) ARE the A2 subsystems of E8",
         "w33_pass7221", False, "BLIND SPOT: BT1750 says 'hexagons', not 'A2 subsystems'"),
        ("zzzqqq nonexistent widget frobnicator",
         "", False, "nothing in the corpus should match"),
    ]
    ok = True
    for subj, excl, want, why in cases:
        found = report(subj, excl)
        got = bool(found)
        ok &= got == want
        print(f"    {subj[:52]:54s} got={str(got):5s} want={str(want):5s} "
              f"{'ok' if got == want else 'FAIL'}")
        print(f"      ({why})")
        for f in found[:2]:
            print(f"        -> {f}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    subject = " ".join(a for a in argv if not a.startswith("-"))
    if not subject:
        try:
            subject = subprocess.run(["git", "log", "-1", "--format=%s"], cwd=ROOT,
                                     capture_output=True, text=True).stdout.strip()
        except Exception:
            subject = ""
    if not subject:
        print("  no subject given and no HEAD commit to read")
        return 0
    print(f"  subject: {subject}")
    words = content_words(subject)
    print(f"  content words: {words}\n")
    found = report(subject)
    if not found:
        print("  no corpus file matches 3+ content words -- no obvious prior art")
    else:
        print("  POSSIBLE PRIOR ART, read before claiming novelty:")
        for f in found:
            print(f"    {f}")
    print("\n  (warn only; this never blocks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
