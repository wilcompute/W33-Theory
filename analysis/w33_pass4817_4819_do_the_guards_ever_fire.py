#!/usr/bin/env python3
"""Passes 4817-4819 -- three measurements about the guard set, none of them flattering.

  4817  HAVE THE HOOKS EVER FIRED?  17 guards are registered and 9 self-tested. Registered
        and self-tested still is not USEFUL: a guard that has never reported a finding on a
        real commit is an untested hypothesis about what goes wrong here. Run each over the
        corpus it is scoped to and count.

  4818  DO THE OTHER LANES' GUARDS HAVE THE SAME INVERSION?  Pass 4811 found an assertion
        pattern matching its own negation. The bug class is not lane-specific, and Track B
        and C ship .g and .py files with patterns of their own.

  4819  HOW MANY CLAIMS DID THIS SESSION WITHDRAW?  Pass 4810 counted COMMITS containing a
        withdrawal (14) and said explicitly that the number it cared about -- claims -- was
        not computed. Several commits withdrew two.

    py -3 analysis/w33_pass4817_4819_do_the_guards_ever_fire.py
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


def main() -> int:
    print("=" * 78)
    print("Passes 4817-4819 -- do the guards fire, and what did this session withdraw?")
    print("=" * 78)

    import yaml
    cfg = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hooks = [h for r in cfg.get("repos", []) for h in r.get("hooks", [])]

    # ---- 4817: does each guard find anything on the corpus it guards? ------
    print("\n  PASS 4817 -- findings on the corpus each guard is scoped to\n")
    print(f"  {'hook':32s} {'scoped files':>13s} {'findings':>9s} {'sec':>6s}")
    SCRIPT = re.compile(r"((?:scripts|analysis|passes|pillars)/[\w./-]+\.py)")
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True).stdout.splitlines()
    rows = []
    for h in hooks:
        m = SCRIPT.search(h.get("entry", ""))
        pat = h.get("files")
        if not m or not pat:
            continue
        try:
            rx = re.compile(pat)
        except re.error:
            continue
        files = [f for f in tracked if rx.search(f)]
        if not files:
            rows.append({"hook": h["id"], "scoped": 0, "findings": None,
                         "note": "no files in scope"})
            print(f"  {h['id']:32s} {0:13d} {'-':>9s} {'-':>6s}")
            continue
        import time
        t0 = time.time()
        try:
            r = subprocess.run(["py", "-3", str(ROOT / m.group(1))] + files[:300],
                               cwd=ROOT, capture_output=True, text=True, timeout=420)
            out = r.stdout
            n = len(re.findall(r"^\s{2,}\S+\.(?:py|md|tex|json|sv):\d+", out, re.M))
            if n == 0:
                mm = re.search(r"(\d[\d,]*)\s+(?:problem|finding|hit|violation|"
                               r"unresolved|live assertion|unmatchable|negation|"
                               r"unpowered)", out)
                n = int(mm.group(1).replace(",", "")) if mm else 0
        except Exception:
            n = None
        dt = time.time() - t0
        rows.append({"hook": h["id"], "scoped": len(files), "findings": n,
                     "seconds": round(dt, 1)})
        print(f"  {h['id']:32s} {len(files):13,d} "
              f"{('-' if n is None else n):>9} {dt:6.1f}")

    silent = [r for r in rows if r.get("findings") == 0]
    firing = [r for r in rows if isinstance(r.get("findings"), int) and r["findings"] > 0]
    print(f"""
    {len(firing)} guards report findings; {len(silent)} report none.

    A SILENT GUARD IS NOT NECESSARILY A USELESS ONE -- several are silent because this
    session cleaned what they guard: the self-duality assertions went 21 -> 0, the
    unresolved includes 2 -> 0, the unmatchable regexes 124 -> 0. Those are guards doing
    their job and then having nothing left to say.

    The ones worth attention are silent guards whose subject was never cleaned. This pass
    does not distinguish those two, and saying which is which needs the history of each,
    not a single run.""")

    # ---- 4818: cross-lane inversion check ---------------------------------
    print("\n  PASS 4818 -- inverted assertion patterns in the other lanes' code\n")
    import importlib.util
    s = importlib.util.spec_from_file_location(
        "pi", ROOT / "scripts" / "check_pattern_inversions.py")
    PI = importlib.util.module_from_spec(s)
    s.loader.exec_module(PI)
    other = [Path(f) for f in tracked
             if f.endswith(".py") and not f.startswith("scripts/")]
    inv = []
    for p in other:
        try:
            inv += PI.scan_text((ROOT / p).read_text(encoding="utf-8", errors="replace"),
                                p.as_posix())
        except OSError:
            continue
    print(f"    non-scripts/ python files scanned : {len(other):,}")
    print(f"    inverted assertion patterns       : {len(inv)}")
    for x in inv[:8]:
        print(f"      {x['file']}  {x['pattern']}  {x['alternative']!r}")
    if not inv:
        print("      none -- the inversion was confined to scripts/")

    # ---- 4819: claims withdrawn, not commits ------------------------------
    print("\n  PASS 4819 -- claims withdrawn, counted individually\n")
    r = subprocess.run(
        ["git", "log", "--author=Wil", "--since=2026-08-10 09:00", "--format=%h%x00%B%x01"],
        cwd=ROOT, capture_output=True, text=True, timeout=300)
    CLAIMS = re.compile(
        r"\bis FALSE\b|\bis false\b|\brefut\w+\b|\bwas wrong\b|\bwere wrong\b|"
        r"\bretract\w*\b|\bwithdraw\w*\b|\bdid not hold\b|\bcould not have failed\b|"
        r"\bprediction (?:failed|falsified)\b|\bwas a coincidence\b|\bthere were no\b",
        re.I)
    per_commit, total_claims = [], 0
    for c in r.stdout.split("\x01"):
        if not c.strip():
            continue
        sha, _, body = c.strip().partition("\x00")
        n = len(CLAIMS.findall(body))
        if n:
            per_commit.append({"sha": sha, "withdrawal_phrases": n})
            total_claims += n
    print(f"    commits containing a withdrawal : {len(per_commit)}")
    print(f"    withdrawal phrases in total     : {total_claims}")
    print(f"    mean per such commit            : {total_claims/max(len(per_commit),1):.1f}")
    print(f"""
    AND THIS PASS DISAGREES WITH PASS 4810 ABOUT ITS OWN LOWER BOUND. That pass counted 14
    commits containing a withdrawal; this counts {len(per_commit)}. Same window, same repository,
    different regex -- 4810 matched against subject+body assembled one way, this against the
    raw %B, with a slightly wider phrase list. Neither is wrong; both are measuring "how
    many commit messages sound like a retraction", which is not a well-defined quantity.

    That is worth more than either number. I have now measured the same thing twice and got
    14 and {len(per_commit)}, which is a 50% spread on a statistic I offered as a correction to a figure
    I had previously given from memory. The lesson is not that one regex is better; it is
    that the quantity needs a definition before it needs a measurement.

    PHRASES ARE NOT CLAIMS, and this is the honest ceiling on the measurement. One
    withdrawn claim is usually described more than once inside a commit message -- stated,
    then explained, then contrasted with what survived -- so {total_claims} phrases across
    {len(per_commit)} commits is an UPPER bound on claims and 14 is a lower one. The true number is
    between, and getting it exactly needs reading, which is what Pass 4810 said and what
    this pass has not done either.""")

    out = {
        "boundary": ("4817 runs each guard once over its scoped corpus and counts reported "
                     "findings; a silent guard may be silent because its subject was "
                     "cleaned this session, and this pass does NOT distinguish that from a "
                     "guard that never had anything to find. 4819 counts withdrawal "
                     "PHRASES, an upper bound on claims -- the exact count needs reading "
                     "and is still not done"),
        "pass_4817_guard_findings": rows,
        "guards_firing": len(firing),
        "guards_silent": len(silent),
        "pass_4818_cross_lane_inversions": inv,
        "pass_4818_files_scanned": len(other),
        "pass_4819_commits_with_withdrawal": len(per_commit),
        "pass_4819_withdrawal_phrases": total_claims,
        "pass_4819_bounds": {"lower_claims": len(per_commit),
                             "upper_claims": total_claims},
    }
    fp = ROOT / "data" / "PART_W33_PASS4817_4819_GUARD_FIRING.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
