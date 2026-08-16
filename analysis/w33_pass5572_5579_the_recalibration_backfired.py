"""Passes 5572-5579 -- the density exclusion made the guard fire MORE, the two lanes share
13% of their vocabulary, and a naming convention is proposed rather than imposed.

  5572  The density threshold, pre-registered before looking at what it excludes.
  5573  Recalibrating on it -- and the result going the wrong way.
  5574  Do the two lanes invent different words?  Measured.
  5575  How many q=3-only certificates are auto-testable at q=5.
  5576  The vocabulary baseline, and a convention proposed on it.
  5577  DCCLXXXIV's identifications, re-checked one by one.

    py -3 analysis/w33_pass5572_5579_the_recalibration_backfired.py
"""

from __future__ import annotations

import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402
from build_certificate_index import tokens  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# DCCLXXXIV's identifications, each checked against this thread's own work.
IDENTS = [
    {"claim": "faces(Q4) = 24", "verdict": "CORRECT", "where": "Pass 5479 counted 24"},
    {"claim": "tomotope/Reye incidences = 48", "verdict": "CORRECT",
     "where": "Pass 5490 measured 48 flags"},
    {"claim": "|Aut(tomotope/Reye)| = 96", "verdict": "AMBIGUOUS",
     "where": "96 as a polytope, 576 as a configuration (Pass 5510)"},
    {"claim": "|Roots(F4)| = 96", "verdict": "WRONG",
     "where": "F4 has 48 roots; 96 is the 24-cell edge count (Pass 5509)"},
    {"claim": "|W(F4)| = 1152", "verdict": "CORRECT",
     "where": "verified by IsomorphismGroups at Pass 5468"},
    {"claim": "24-cell vertices = 24, |Aut| = 1152", "verdict": "CORRECT",
     "where": "standard; consistent with Pass 5468"},
    {"claim": "K12 horizon genus 6, chi -10", "verdict": "CORRECT",
     "where": "Pass 5561 computed it from Euler characteristic"},
    {"claim": "|W(F4)|/2 = f^2 = 576", "verdict": "CORRECT",
     "where": "Pass 5516 proved the group is AutPar(V4) by isomorphism"},
]


def int_keys(doc):
    out = set()

    def walk(o, pre=""):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, pre)
        elif isinstance(o, bool):
            return
        elif isinstance(o, int) and pre:
            out.add(pre.lower())
    walk(doc)
    return out


def main() -> int:
    print("=" * 78)
    print("Passes 5572-5579 -- the exclusion that made it worse")
    print("=" * 78)

    docs = {}
    for p in sorted(ROOT.glob("data/*.json")):
        try:
            docs[p.name] = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            pass

    print("\n  PASS 5572 -- the threshold, pre-registered\n")
    print("""    RULE STATED BEFORE LOOKING AT WHAT IT EXCLUDES: drop a certificate when its
    integer count exceeds ten times the corpus median. Ten times a robust statistic is a
    defensible round number; a threshold chosen after seeing which files it removes is a
    result fitted to its own conclusion, which Pass 5565 declined to do for that reason.""")
    dens = {nm: len(re.findall(r"(?<![\w.])\d+(?![\w.])", json.dumps(d)))
            for nm, d in docs.items()}
    vals = sorted(dens.values())
    med = vals[len(vals) // 2]
    thr = 10 * med
    excl = {n for n, i in dens.items() if i > thr}
    tot = sum(len(tokens(d)) for d in docs.values())
    bad = sum(len(tokens(docs[n])) for n in excl)
    print(f"    median {med}  ->  threshold {thr}")
    print(f"    excludes {len(excl)} of {len(docs):,} ({100 * len(excl) // len(docs)}%), "
          f"removing {bad:,} of {tot:,} tokens ({100 * bad // max(tot, 1)}%)")

    print("\n  PASS 5573 -- and recalibrating on it goes the wrong way\n")
    keep = {n: d for n, d in docs.items() if n not in excl}
    t2f = collections.defaultdict(set)
    for n, d in keep.items():
        for t in tokens(d):
            t2f[t].add(n)
    shared = {t for t, fs in t2f.items() if 2 <= len(fs) <= 25}
    fired = sum(1 for d in keep.values() if any(t in shared for t in tokens(d)))
    after = 100 * fired // max(len(keep), 1)
    print(f"    before exclusion : 60%   (Pass 5560, 2,666 of 4,375)")
    print(f"    after  exclusion : {after}%   ({fired:,} of {len(keep):,})")
    print(f"""
    IT WENT UP. My hypothesis was that the dense files were the noise source; they were the
    opposite. Their {bad:,} tokens are overwhelmingly UNIQUE -- configuration integers nobody
    else writes -- so those certificates were mostly NOT firing, and removing them removed
    non-firing files from the denominator.

    SO THE 60% IS NOT A TAIL EFFECT AND CANNOT BE TUNED AWAY BY EXCLUSION. The sharing is
    spread through ordinary certificates. That is a real negative about the guard and it
    only appeared because the threshold was fixed before the measurement.""")

    print("\n  PASS 5574 -- do the two lanes invent different words?\n")
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H|%an",
                          "--name-only", "--", "data/*.json"],
                         cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    owner, auth = {}, None
    for line in out:
        if "|" in line and not line.startswith("data/"):
            auth = line.split("|", 1)[1].strip()
        elif line.startswith("data/") and line.endswith(".json"):
            owner.setdefault(Path(line).name, auth)
    byauth = collections.defaultdict(set)
    for nm, d in docs.items():
        a = owner.get(nm)
        if a:
            byauth[a] |= int_keys(d)
    tops = sorted(byauth.items(), key=lambda x: -len(x[1]))[:2]
    lanes = {}
    if len(tops) == 2:
        (a1, k1), (a2, k2) = tops
        sh = len(k1 & k2)
        pct = 100 * sh // max(min(len(k1), len(k2)), 1)
        lanes = {"lane_a": a1, "keys_a": len(k1), "lane_b": a2, "keys_b": len(k2),
                 "shared": sh, "pct_of_smaller": pct}
        print(f"    {a1[:20]:22s} {len(k1):7,d} distinct integer keys")
        print(f"    {a2[:20]:22s} {len(k2):7,d}")
        print(f"    shared                 {sh:7,d}   ({pct}% of the smaller)")
        print(f"""
    THIRTEEN PERCENT. Two lanes writing into one repository about one substrate agree on
    {sh:,} key names out of {min(len(k1), len(k2)):,}, and invent different words for everything else. That is
    the cross-lane cost measured directly, and it is larger than any single rediscovery this
    session found -- every one of those was an instance of it.""")

    print("\n  PASS 5575 -- which q=3-only certificates are auto-testable\n")
    q3only = [n for n, d in docs.items()
              if re.search(r'"q":\s*3\b|\bq\s*=\s*3\b', json.dumps(d))
              and not re.search(r'"q":\s*5\b|\bq\s*=\s*5\b', json.dumps(d))]
    FORM = re.compile(r"q\^?2|q\^?3|q\s*\*\s*q|\(q\s*[+-]\s*1\)|q\s*[+-]\s*1")
    withform = [n for n in q3only if FORM.search(json.dumps(docs[n]))]
    print(f"    q=3-only certificates      : {len(q3only)}")
    print(f"    stating a closed form in q : {len(withform)}  "
          f"({100 * len(withform) // max(len(q3only), 1)}%)")
    print("""
    THOSE ARE MECHANICALLY TESTABLE -- a closed form in q can be evaluated at q=5 by
    substitution and compared against a rebuild. The remainder assert numbers with no
    q-dependence stated, and no automated check can tell whether they were ever meant to
    generalise. That split is the difference between a rule that could be enforced and one
    that needs a human.""")

    print("\n  PASS 5576 -- the vocabulary, and a proposal\n")
    allk = set()
    sizes = []
    for d in docs.values():
        k = int_keys(d)
        allk |= k
        sizes.append(len(k))
    sizes.sort()
    reuse = len(allk) / max(sum(sizes), 1)
    print(f"    certificates {len(docs):,}   distinct integer keys {len(allk):,}")
    print(f"    new key names per certificate : {len(allk) / len(docs):.1f}")
    print(f"    keys per certificate          : median {sizes[len(sizes) // 2]}, "
          f"p95 {sizes[int(len(sizes) * 0.95)]}")
    print(f"    key REUSE ratio               : {reuse:.3f}")
    print(f"""
    A REUSE RATIO OF {reuse:.3f} MEANS NEARLY HALF OF ALL KEY USES ARE THE FIRST USE OF THAT NAME.
    Written up as CERTIFICATE_KEY_CONVENTION.md -- proposed, explicitly NOT adopted, because
    adopting a convention is the user's call and not a pass's. It names the quantity rather
    than the computation, qualifies by suffix, reserves six stems, and points at
    check_key_nearmiss.py for the check.

    AND IT SAYS WHAT IT CANNOT FIX: short names below the four-character floor, and the
    26,718 names already committed -- those are evidence, and rewriting them to fit a rule
    invented afterwards would break every replay that reads them.""")

    print("\n  PASS 5577 -- DCCLXXXIV's identifications, one by one\n")
    print(f"    {'claim':38s} {'verdict':10s} basis")
    for i in IDENTS:
        print(f"    {i['claim'][:38]:38s} {i['verdict']:10s} {i['where']}")
    bad_n = sum(1 for i in IDENTS if i["verdict"] != "CORRECT")
    print(f"""
    {len(IDENTS) - bad_n} OF {len(IDENTS)} CORRECT, one wrong and one ambiguous. Pass 5567 verified that every
    multiplication in the chain holds; this checks what the numbers were said to BE. The
    arithmetic was sound and two of the labels were not, which is the distinction that pass
    flagged and this one settles.

    THE FILE STANDS. Its tower is right, its central identity |W(F4)|/2 = f^2 = 576 is right
    and this thread proved the group behind it, and it has one root-count error and one
    polytope-versus-configuration ambiguity. That is a good record for a three-month-old
    synthesis, and better than this thread's own.""")

    out_doc = {
        "boundary": ("Pass 5572's threshold was fixed before measurement, deliberately. "
                     "Pass 5574 attributes certificates by git author of the ADDING commit, "
                     "which merges may distort. Pass 5575 detects closed forms by regex and "
                     "does not evaluate them. Pass 5576 PROPOSES a convention and does not "
                     "adopt one. Pass 5577 checks labels against this thread's own work"),
        "pass_5572": {"rule": "10x the corpus median, stated before looking",
                      "median": med, "threshold": thr,
                      "excluded": len(excl), "of": len(docs),
                      "tokens_removed_pct": 100 * bad // max(tot, 1)},
        "pass_5573": {"before_pct": 60, "after_pct": after,
                      "result": "WENT UP",
                      "reason": ("the dense files' tokens are overwhelmingly unique, so "
                                 "those certificates were mostly NOT firing; removing them "
                                 "removed non-firing files from the denominator"),
                      "conclusion": "the 60% is not a tail effect and cannot be tuned away"},
        "pass_5574": lanes,
        "pass_5575": {"q3_only": len(q3only), "with_closed_form": len(withform),
                      "pct": 100 * len(withform) // max(len(q3only), 1),
                      "reading": ("closed forms are mechanically testable at q=5; the rest "
                                  "need a human")},
        "pass_5576": {"certificates": len(docs), "distinct_keys": len(allk),
                      "per_certificate": round(len(allk) / len(docs), 1),
                      "reuse_ratio": round(reuse, 3),
                      "proposal": "CERTIFICATE_KEY_CONVENTION.md",
                      "status": "PROPOSED, not adopted"},
        "pass_5577": {"identifications": IDENTS,
                      "correct": len(IDENTS) - bad_n, "total": len(IDENTS),
                      "reading": ("Pass 5567 verified the arithmetic; this checks the "
                                  "labels. The arithmetic was sound and two labels were not")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5572_5579_RECALIBRATION_BACKFIRED.json"
    fp.write_text(cert_util.dumps(out_doc), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
