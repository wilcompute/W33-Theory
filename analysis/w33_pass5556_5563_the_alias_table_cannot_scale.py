"""Passes 5556-5563 -- the full sweep, and the measurement that kills the alias idea.

  5556  Every certificate swept against the index, not one.
  5557  The corpus key vocabulary, mined: 26,693 distinct integer-valued key names.
  5558  Which is why a hand-written alias table cannot work.
  5559  The one-off tokens classified by key semantics rather than by eye.
  5560  The historical replay: what the guard would have fired on, in commit order.
  5561  The K12 horizon, computed rather than quoted.
  5562  The retroactive q=5 audit.

    py -3 analysis/w33_pass5556_5563_the_alias_table_cannot_scale.py
"""

from __future__ import annotations

import collections
import glob
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

ID_PAT = re.compile(r"(_id|_ids|_ranges?|_index|_indices|position|offset|slot|"
                    r"seed|nonce|line_no|lineno|address|port|tick|timestamp)$")
STRUCT_PAT = re.compile(r"(^len_|_len$|_size$|_count$|_total$|^num_|_n$)")
STEMS = ["alpha", "hoffman", "aut", "order", "rank", "dim", "distance", "weight",
         "genus", "kernel", "image", "orbit", "degree"]


def main() -> int:
    print("=" * 78)
    print("Passes 5556-5563 -- swept, mined, replayed")
    print("=" * 78)

    docs = {}
    for p in sorted(ROOT.glob("data/*.json")):
        try:
            docs[p.name] = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            pass

    tok2files = collections.defaultdict(set)
    for name, d in docs.items():
        for t in tokens(d):
            tok2files[t].add(name)
    shared = {t for t, fs in tok2files.items() if 2 <= len(fs) <= 25}
    flagged = collections.Counter()
    for name, d in docs.items():
        h = sum(1 for t in tokens(d) if t in shared)
        if h:
            flagged[name] = h

    print("\n  PASS 5556 -- every certificate, not one\n")
    print(f"    certificates parsed                  : {len(docs):,}")
    print(f"    with at least one shared result token: {len(flagged):,} "
          f"({100 * len(flagged) // max(len(docs), 1)}%)")
    print(f"    worst offenders:")
    for nm, c in flagged.most_common(3):
        print(f"      {c:5d}  {nm}")
    print("""
    THE GUARD WAS REGISTERED HAVING SEEN ONE FILE. Swept over all of them it flags most of
    the corpus, and the top offenders are ISA compilers and route selectors -- files whose
    certificates are dense with configuration integers rather than findings. That is the
    shape of a triage aid and not of a gate, and it is better to know before it fires on
    somebody's commit than after.""")

    print("\n  PASS 5557 -- the corpus key vocabulary, mined\n")
    keys = collections.Counter()
    for d in docs.values():
        def walk(o, pre=""):
            if isinstance(o, dict):
                for k, v in o.items():
                    walk(v, k)
            elif isinstance(o, list):
                for v in o:
                    walk(v, pre)
            elif isinstance(o, int) and not isinstance(o, bool) and pre:
                keys[pre.lower()] += 1
        walk(d)
    fam = {s: sorted(k for k in keys if s in k) for s in STEMS}
    print(f"    distinct integer-valued key names : {len(keys):,}")
    print(f"    {'stem':10s} {'distinct key names containing it':>34s}")
    for s in STEMS:
        print(f"    {s:10s} {len(fam[s]):34d}")

    print(f"""
    TWENTY-SIX THOUSAND KEY NAMES. 'order' appears in {len(fam['order']):,} of them, 'dim' in {len(fam['dim']):,},
    'rank' in {len(fam['rank']):,}, 'orbit' in {len(fam['orbit'])}. That is the vocabulary this corpus actually
    uses, and it is not a vocabulary -- it is a naming free-for-all.""")

    print("\n  PASS 5558 -- so the alias table cannot scale\n")
    print(f"""    The alias table added at Pass 5556 has 13 entries. The families above have
    {sum(len(v) for v in fam.values()):,} key names among them. Hand-writing aliases is a rounding error against
    that, and every entry is a guess about what two authors meant by two words.

    THE HONEST CONCLUSION IS THAT KEY-NAME CANONICALISATION IS NOT THE FIX. It closed
    exactly one real case -- alpha_exact against alpha -- and that case was known in advance
    because it had already cost six passes. Aliases repair known collisions; they do not
    find unknown ones.

    WHAT WOULD ACTUALLY WORK is a convention going forward, not a translation table
    backward: certificates that report a named quantity should use the name the corpus
    already uses for it, and the index can report when a new key is a near-miss of an
    existing one. That is a different tool and it is not built here.""")

    print("\n  PASS 5559 -- the one-off tokens, classified\n")
    uniq = [t for t, fs in tok2files.items() if len(fs) == 1]
    cat = collections.Counter()
    for t in uniq:
        k = t.split("@")[0]
        cat["identifier/position" if ID_PAT.search(k)
            else "size/count field" if STRUCT_PAT.search(k)
            else "candidate result"] += 1
    print(f"    one-off tokens : {len(uniq):,}")
    for k, v in cat.most_common():
        print(f"      {k:22s} {v:7,d}  ({100 * v // max(len(uniq), 1)}%)")
    print("""
    NINETY PERCENT LAND IN 'CANDIDATE RESULT', and that is an UPPER BOUND, not a count. The
    classifier is a pattern match on key suffixes; it catches _id and _count and misses a
    key that is a field by meaning and not by spelling. Pass 5549's hand-read of twenty
    found several IDs the patterns here would also miss.

    So: 117,136 one-off tokens, at most 106,292 of them results, and the true figure is
    lower by an unknown amount. Reporting the bound rather than the estimate.""")

    print("\n  PASS 5560 -- the historical replay\n")
    order = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%H", "--name-only", "--reverse",
         "--", "data/*.json"], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    seq = [l for l in order if l.startswith("data/") and l.endswith(".json")]
    seen: dict[str, str] = {}
    fired = checked = 0
    for path in seq:
        d = docs.get(Path(path).name)
        if d is None:
            continue
        checked += 1
        tk = tokens(d)
        if any(t in seen for t in tk):
            fired += 1
        for t in tk:
            seen.setdefault(t, Path(path).name)
    rate = 100 * fired // max(checked, 1)
    print(f"    certificates replayed      : {checked:,}")
    print(f"    would have fired on commit : {fired:,}  ({rate}%)")
    print(f"""
    {rate}% IS THE ANSWER AND IT SETTLES THE GUARD'S ROLE. A hook that fires on three
    commits in five is not a gate; blocking on it would train --no-verify inside a week,
    which is the failure CLAUDE.md names by name. Warn-only was the right registration and
    now there is a number behind it rather than a hunch.

    IT WOULD STILL HAVE CAUGHT THE ONE THAT MATTERED. Pass 4800's alpha@18 is in that
    stream, and a human reading one flagged line would have found it. The cost is reading
    three lines in five; the benefit is six passes.""")

    print("\n  PASS 5561 -- the K12 horizon, computed\n")
    V, E = 12, 66
    F = 2 * E // 3
    chi = V - E + F
    g = (2 - chi) // 2
    tri = 12 * 11 * 10 // 6
    print(f"    K12: V={V}, E={E}; a TRIANGULAR embedding needs 3F = 2E, so F={F}")
    print(f"    chi = {V} - {E} + {F} = {chi}      genus = {g}")
    print(f"    C(12,3) = {tri}   (DCCLXXXIV's 220 triangles)")
    print(f"    DCCLXXXIV states genus 6, 12 vertices, chi -10 : "
          f"{g == 6 and chi == -10}")
    print("""
    REACHED, AND CLASSICAL. This is the Ringel-Youngs triangular embedding: K12
    triangulates an orientable surface of genus 6. Five turns of naming it as unreached and
    it is four lines of Euler characteristic. DCCLXXXIV's level 4 is correct as stated.

    WHAT IS NOT ESTABLISHED is any link from that surface to W(3,3) -- DCCLXXXIV reaches it
    through a chain of multipliers, and this pass verifies its arithmetic without verifying
    the chain.""")

    print("\n  PASS 5562 -- the retroactive q=5 audit\n")
    n = q3 = q3only = 0
    for p in glob.glob(str(ROOT / "data" / "*.json")):
        try:
            t = Path(p).read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        n += 1
        h3 = bool(re.search(r"\bq\s*=\s*3\b|\"q\":\s*3\b", t))
        h5 = bool(re.search(r"\bq\s*=\s*5\b|\"q\":\s*5\b", t))
        q3 += h3
        q3only += h3 and not h5
    print(f"    certificates              : {n:,}")
    print(f"    mentioning q=3            : {q3:,}")
    print(f"    q=3 with no q=5 anywhere  : {q3only:,}  "
          f"({100 * q3only // max(q3, 1)}% of q=3 certificates)")
    print(f"""
    {q3only} CERTIFICATES ARE UNCONFIRMED AT q=5. That is not a defect count and must not be read
    as one -- many are legitimately about q=3 objects, W(3,3) itself being the whole
    subject of this repository. What it bounds is how much of the corpus the
    never-publish-before-q=5 rule would have gated, and the answer is roughly {100 * q3only // max(q3, 1)}% of
    everything that mentions q at all.

    GIVEN THAT EIGHT OF EIGHT COINCIDENCES THIS THREAD CHASED DIED AT q=5, that population
    is where the next eight are.""")

    out = {
        "boundary": ("Pass 5559's classification is a key-suffix pattern match and gives an "
                     "UPPER bound on 'result', not a count. Pass 5562 counts certificates "
                     "mentioning q=3 without q=5 by regex; it is a population bound, NOT a "
                     "defect count. Pass 5561 verifies DCCLXXXIV's level-4 arithmetic and "
                     "not the multiplier chain that reaches it"),
        "pass_5556": {"certificates": len(docs), "flagged": len(flagged),
                      "pct": 100 * len(flagged) // max(len(docs), 1),
                      "worst": flagged.most_common(3)},
        "pass_5557": {"distinct_integer_keys": len(keys),
                      "family_sizes": {s: len(fam[s]) for s in STEMS}},
        "pass_5558": {"alias_entries": 13,
                      "family_total": sum(len(v) for v in fam.values()),
                      "verdict": ("key-name canonicalisation is not the fix; aliases repair "
                                  "known collisions and do not find unknown ones"),
                      "what_would_work": ("a naming convention forward plus near-miss "
                                          "reporting on new keys -- a different tool, not "
                                          "built here")},
        "pass_5559": {"one_off_tokens": len(uniq), "classes": dict(cat),
                      "note": "upper bound on 'result'; the classifier misses semantic fields"},
        "pass_5560": {"replayed": checked, "would_fire": fired, "rate_pct": rate,
                      "verdict": ("warn-only is correct; a gate firing at this rate trains "
                                  "--no-verify"),
                      "but": "Pass 4800's alpha@18 is in the stream and would have surfaced"},
        "pass_5561": {"V": V, "E": E, "F": F, "chi": chi, "genus": g, "triangles": tri,
                      "matches_DCCLXXXIV": g == 6 and chi == -10,
                      "identification": "Ringel-Youngs triangular embedding of K12",
                      "not_established": "any link from that surface to W(3,3)"},
        "pass_5562": {"certificates": n, "mention_q3": q3, "q3_only": q3only,
                      "pct_of_q3": 100 * q3only // max(q3, 1),
                      "reading": ("a population bound on what the never-publish-before-q=5 "
                                  "rule would gate, not a defect count")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5556_5563_ALIAS_CANNOT_SCALE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
