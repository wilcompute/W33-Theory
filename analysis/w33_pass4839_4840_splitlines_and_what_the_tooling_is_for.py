#!/usr/bin/env python3
r"""Passes 4839-4840 -- how far the splitlines() hazard reaches, and what this session's
tooling was actually built for.

  4839  Pass 4827's self-test found that Python's splitlines() treats FORMFEED as a line
        break, which defeated a scanner looking for formfeeds.  The same call appears 50
        times across scripts/.  Most are harmless -- splitting subprocess output, which
        contains no control bytes.  The ones that matter read FILE CONTENT and report LINE
        NUMBERS: in any file containing a formfeed or vertical tab, every line number after
        it is wrong, and the content on that line is split in two.

        This repository has files with those bytes: 19 .md and 85 .txt carry formfeeds as
        PDF-extraction artifacts.

  4840  A harder question.  Counting this session's new tooling by what it was built to
        catch: how much of it exists because of a mistake made in this same session?

    py -3 analysis/w33_pass4839_4840_splitlines_and_what_the_tooling_is_for.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RISKY = re.compile(r"(?:read_text|\.read\(\)|open\([^)]*\)\.read)[^\n]{0,60}\.splitlines\(\)"
                   r"|\btext\.splitlines\(\)|\bsrc\.splitlines\(\)|\braw\.splitlines\(\)")
REPORTS_LINES = re.compile(r"enumerate\([^)]*splitlines|\bline\b[^\n]{0,20}:\s*\{|"
                           r"\{[^}]*\bline\b[^}]*\}|:\{.*?line", re.S)
CTRL = ("\x0c", "\x0b", "\x1c", "\x1d", "\x1e", "\x85")


def main() -> int:
    print("=" * 78)
    print("Passes 4839-4840")
    print("=" * 78)

    # ---- 4839: which guards are exposed? ---------------------------------
    print("\n  PASS 4839 -- splitlines() on file content, with line numbers reported\n")
    exposed, benign = [], []
    for p in sorted((ROOT / "scripts").glob("*.py")):
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if ".splitlines()" not in src:
            continue
        risky = bool(RISKY.search(src))
        lines = bool(re.search(r"enumerate\([^)]{0,40}splitlines\(\)", src))
        rec = {"file": p.name, "reads_file_content": risky, "reports_line_numbers": lines}
        (exposed if (risky and lines) else benign).append(rec)

    print(f"    scripts using splitlines()            : {len(exposed) + len(benign)}")
    print(f"    on file content AND reporting lines   : {len(exposed)}")
    for e in exposed:
        print(f"      {e['file']}")

    # how many corpus files carry a splitlines-splitting byte?
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True).stdout.splitlines()
    affected = 0
    checked = 0
    for f in tracked:
        if not f.endswith((".md", ".py", ".tex", ".txt")):
            continue
        fp = ROOT / f
        try:
            b = fp.read_bytes()
        except OSError:
            continue
        checked += 1
        if any(c.encode() in b for c in CTRL):
            affected += 1

    print(f"\n    corpus files checked                  : {checked:,}")
    print(f"    carrying a splitlines-splitting byte  : {affected}")
    print(f"""
    {len(exposed)} GUARDS REPORT LINE NUMBERS FROM splitlines() OVER FILE CONTENT, and {affected}
    tracked files carry a byte that splitlines() treats as a line break. In those files
    every reported line number after the first such byte is too high, and the content on
    that line is split across two reported lines.

    THIS IS A REPORTING BUG, NOT A DETECTION BUG, which is why it has gone unnoticed: the
    guard still finds the fault, it just points a line or two past it. That is survivable
    for a human reader and fatal for anything consuming the output programmatically.

    NOT FIXED HERE, AND DELIBERATELY. Changing splitlines() to split("\\n") in {len(exposed)} guards is
    a mechanical edit I could make in a minute, and every one would need its self-test
    re-run to confirm nothing shifted. This session has established that mechanical edits
    to guards, made quickly, is how the inversions and the collapsed escapes got in. The
    list is the deliverable.""")

    # ---- 4840: what is the tooling for? ----------------------------------
    print("\n  PASS 4840 -- what this session's new tooling was built to catch\n")
    NEW = {
        "check_search_power.py": "corpus (Pass 4680's null)",
        "check_layer_conformance.py": "corpus (blueprint may-claim table)",
        "check_smin_formula.py": "pre-existing (resurrected from a dead config)",
        "check_guards_reachable.py": "SESSION (guards found unreachable)",
        "check_guard_selftests.py": "SESSION (guards found untested)",
        "check_certificates_regenerate.py": "corpus",
        "check_retraction_propagation.py": "corpus (Pass 4563's retraction)",
        "check_stdlib_shadow.py": "SESSION (my scratch bisect.py broke igraph)",
        "check_regex_deadends.py": "SESSION (my 51,840 statistic was 12.5% not 44%)",
        "check_pattern_inversions.py": "corpus (novelty guard inverted)",
        "check_heredoc_regex.py": "SESSION (my heredocs, six times)",
        "compile_sweep.py": "corpus (a manuscript that never built)",
    }
    sess = [k for k, v in NEW.items() if v.startswith("SESSION")]
    corp = [k for k, v in NEW.items() if not v.startswith("SESSION")]
    print(f"    new or resurrected tools : {len(NEW)}")
    print(f"      built for a CORPUS fault : {len(corp)}")
    print(f"      built for a fault I made THIS SESSION : {len(sess)}")
    for k in sess:
        print(f"        {k:34s} {NEW[k]}")
    print(f"""
    {len(sess)} OF {len(NEW)} EXIST BECAUSE OF MISTAKES MADE IN THIS SESSION -- {100*len(sess)//len(NEW)}% of the tooling.
    The honest reading is not flattering in either direction.

    Against: a session that has to build {len(sess)} tools to catch its own errors is making errors
    faster than it is making results, and three of them (shadowing, dead-end regexes,
    collapsed escapes) are mechanical faults that care and slower editing would have
    avoided entirely.

    For: they are not session-specific. A stdlib shadow, an unmatchable regex
    alternative, a collapsed escape and an unreachable guard are all faults this repository
    can produce again from any lane, and check_regex_deadends has already caught two
    incidents that were not mine to begin with -- it found the layer checker's disabled
    W(3,3) token, which had been dead since that checker was written.

    The measurement I cannot make is whether these tools will fire on anyone else's work.
    Pass 4817 found 2 of 16 guards firing at all, and a tool built for a fault that occurred
    once is indistinguishable from a tool built for a fault that occurs often, until it
    happens again.""")

    out = {
        "boundary": ("4839 classifies by static pattern -- 'reads file content' and "
                     "'enumerates splitlines' are regex judgements and may miss a guard "
                     "that does both across several statements. No guard is fixed here. "
                     "4840's attribution of each tool to a corpus or session fault is a "
                     "judgement I made about my own work, which is the least reliable kind"),
        "pass_4839_exposed_guards": exposed,
        "pass_4839_exposed_count": len(exposed),
        "pass_4839_corpus_files_with_splitting_byte": affected,
        "pass_4839_corpus_files_checked": checked,
        "pass_4840_new_tools": NEW,
        "pass_4840_session_caused": sess,
        "pass_4840_fraction_session_caused": round(len(sess) / len(NEW), 2),
    }
    fp = ROOT / "data" / "PART_W33_PASS4839_4840_SPLITLINES_AND_TOOLING.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
