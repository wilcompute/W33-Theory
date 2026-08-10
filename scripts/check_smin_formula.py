#!/usr/bin/env python3
"""Guard the S_min formula: log2(2160) - log2(40) = log2(54), not 2.0704.  Pass 4692.

WHY THIS FILE EXISTS AT ALL
---------------------------
This check was already in the repository, written inline inside `.pre-commit-config.yaml`
as a multi-line `entry: "` scalar whose continuation lines began at column 0.  That is not
valid YAML -- a double-quoted scalar must be indented past its key -- so the scalar ended at
the first newline and the parser hit bare Python where it expected a mapping.

The consequence was not that this one hook failed.  `pre-commit validate-config` could not
load the FILE, so every hook in it was dead: the rediscovery guard that CLAUDE.md calls the
core of the two-agent protocol, the certificate check, the RTL fold check, the novelty
check.  All present, all documented, none running.

That is failure mode 7 one level up from where the repo has been looking for it.  A vacuous
check reports cleanly while broken; a config that cannot parse reports nothing at all, which
is quieter still -- `git commit` prints "pre-commit not found for this environment" and
looks like a note about the environment rather than a dead guard rail.

Moving the script into a file is not a style preference.  An inline `entry:` cannot be
run, tested, or self-tested on its own, and this one was never executed once.

    py -3 scripts/check_smin_formula.py --selftest
    py -3 scripts/check_smin_formula.py <files...>
"""

from __future__ import annotations

import re
import sys

# log2(2160) - log2(40) = log2(54) = 5.7549..., and 2160/40 = 54.  A file quoting 2.07
# has divided the logs instead of subtracting them: log2(2160)/log2(40) = 2.0704.
BAD = re.compile(r"log_?2\s*\(?\s*2160\s*\)?\s*-\s*log_?2\s*\(?\s*40\s*\)?.{0,80}?2\.07",
                 re.S)


def scan(text: str) -> bool:
    return bool(BAD.search(text))


def selftest() -> int:
    cases = [
        ("planted: divided instead of subtracted",
         "We compute log2(2160) - log2(40) = 2.0704 bits per point.", True),
        ("planted: spaced variant",
         "log_2 2160 - log_2 40 gives 2.07 in the table.", True),
        ("clean: correct value",
         "log2(2160) - log2(40) = log2(54) = 5.7549 bits.", False),
        ("clean: unrelated 2.07",
         "The ratio settles at 2.07 after normalisation.", False),
    ]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, text, want in cases:
        got = scan(text)
        ok &= got == want
        print(f"    {name:40s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if got == want else 'FAIL'}")
    print("""
  The second clean case is the one that matters: 2.07 is an ordinary number and the check
  must fire on the log identity, not on the digits. This check ran zero times before today
  because the config it lived in could not be parsed, so it had never been tested at all --
  which is why it ships with a self-test now.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    bad = 0
    for f in argv:
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                txt = fh.read()
        except OSError:
            continue
        if scan(txt):
            print(f"ERROR in {f}: log2(2160)-log2(40)=log2(54)=5.7549, not 2.0704")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
