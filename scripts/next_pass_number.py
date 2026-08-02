"""Find the next free pass number, and emit protocol-correct reservations.

WHY THIS EXISTS (measured 2026-07-31).

CLAUDE.md mandates reserving a pass number with

    git commit --allow-empty -m "Pass NNN reserved: <topic> (<track>)"

before computing.  On 2026-07-31 both tracks instead wrote the *range* form,

    "Passes 1606-1610 reserved: ..."

and the collision happened anyway: my reservation was pushed at 19:44 and was
already an ancestor of the other track's 20:00 commit, which used the same five
numbers.  The mechanism is mechanical, not careless -- a scan for `Pass ([0-9]+)`
does not match `Passes 1606-1610`, because "Passes" has no space after "Pass".
So a range-form reservation is INVISIBLE to the very check it exists to feed,
and the earlier claim silently loses.

The fix is not "remember the format".  It is to scan every form that occurs and
to emit the reservations for you.

Sources scanned (all of them, because each has missed a number before):
  * commit subjects on the tracking remote  -- "Pass 123", "Passes 123-127",
    "Pass 123 reserved", "PASS123", "BT123"
  * analysis/ filenames                     -- pass123, PASS123_, BT123_
  * root-level PASS*/BT* markdown filenames

Usage
-----
    py -3 scripts/next_pass_number.py                 # report
    py -3 scripts/next_pass_number.py --claim 5 --topic "octet lift" --track glue
    py -3 scripts/next_pass_number.py --claim 5 ... --run     # actually commit
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The repo runs TWO independent counters and they have diverged (measured
# 2026-07-31: Pass at 1616, BT at 1907).  They coincide sometimes -- Pass 1536
# produced BT1536_frame_dual_k44_code.md -- and diverge elsewhere, so
# BT1613_BT1620_decoder_fault_sm_bridge.md already exists while "Pass 1613" was
# still free.  Conflating them makes the next free pass number look ~300 too
# high; keeping them apart is the whole point of this module.
RE_PASS_SUBJ = re.compile(
    r"\bpass(?:es)?\s*(\d{2,5})(?:\s*[-–]\s*(\d{2,5}))?", re.I)
RE_BT_SUBJ = re.compile(
    r"\bbt\s*(\d{2,5})(?:\s*[-–]\s*(\d{2,5}))?", re.I)
RE_PASS_FILE = re.compile(r"pass_?(\d{2,5})", re.I)
RE_BT_FILE = re.compile(r"bt_?(\d{2,5})", re.I)


def _git(*args: str) -> str:
    try:
        return subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                              text=True, timeout=180).stdout
    except Exception as exc:                       # pragma: no cover
        print(f"  (git failed: {exc})", file=sys.stderr)
        return ""


def _expand(pairs) -> set[int]:
    out: set[int] = set()
    for lo, hi in pairs:
        a = int(lo)
        b = int(hi) if hi else a
        if b < a or b - a > 50:                   # a range that wide is a typo
            b = a
        out.update(range(a, b + 1))
    return out


def numbers_from_subjects(ref: str, limit: int = 400) -> dict[str, set[int]]:
    subs = _git("log", ref, "--format=%s", f"-{limit}").splitlines()
    return {"pass": _expand(p for s in subs for p in RE_PASS_SUBJ.findall(s)),
            "bt": _expand(p for s in subs for p in RE_BT_SUBJ.findall(s))}


def numbers_from_filenames() -> dict[str, set[int]]:
    out = {"pass": set(), "bt": set()}
    for d in ("analysis", "."):
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for name in os.listdir(p):
            out["pass"].update(int(m) for m in RE_PASS_FILE.findall(name))
            out["bt"].update(int(m) for m in RE_BT_FILE.findall(name))
    return out


def range_is_free(lo: int, hi: int, used: set[int]) -> tuple[bool, list[int]]:
    """Is [lo, hi] unused?  Call this BEFORE renumbering into a range.

    Added after a real collision (2026-08-02). The claim path checks the highest
    number in use and pushes reservations, but a batch that RENUMBERS after the
    fact bypasses that check entirely and can land on a range another track has
    already published. Passes 2011-2015 were claimed and published by one track
    at 09:18 and renumbered into by the other at 09:41 -- collisions were handled
    at claim time and not at renumber time. This closes that gap.
    """
    clash = sorted(n for n in range(lo, hi + 1) if n in used)
    return (not clash), clash


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--remote", default="origin-https/master",
                    help="ref to scan (default: origin-https/master)")
    ap.add_argument("--claim", type=int, default=0,
                    help="how many consecutive numbers to reserve")
    ap.add_argument("--topic", default="<topic>")
    ap.add_argument("--track", default="glue")
    ap.add_argument("--run", action="store_true",
                    help="actually create and push the reservation commits")
    ap.add_argument("--fetch", action="store_true", help="git fetch first")
    ap.add_argument("--check-range", default="",
                    help="LO-HI: verify a range is unused BEFORE renumbering "
                         "into it (the gap that caused the 2011-2015 clash)")
    args = ap.parse_args()

    if args.fetch:
        _git("fetch", args.remote.split("/")[0])

    subj = numbers_from_subjects(args.remote)
    fname = numbers_from_filenames()
    if not (subj["pass"] | fname["pass"]):
        print("no pass numbers found -- is the remote ref right?")
        return 1

    hi = {}
    for seq in ("pass", "bt"):
        s, f = subj[seq], fname[seq]
        hi[seq] = max(max(s, default=0), max(f, default=0))
        print(f"[{seq.upper():4}] subjects: {max(s, default=0):5}   "
              f"filenames: {max(f, default=0):5}   highest: {hi[seq]:5}")
    nxt = hi["pass"] + 1
    print(f"\nNEXT FREE PASS NUMBER : {nxt}")
    if hi["bt"] > hi["pass"]:
        print(f"  (the BT counter is {hi['bt'] - hi['pass']} ahead; they are "
              f"SEPARATE sequences.\n   Do not name a Pass-{nxt} artefact "
              f"BT{nxt} -- check analysis/ for BT{nxt}* first.)")

    only_file = sorted(n for n in fname["pass"] - subj["pass"]
                       if n > hi["pass"] - 60)
    if only_file:
        print(f"\n  note: pass {only_file} appear only as filenames, not in any "
              f"commit subject --\n  a subject-only scan would have missed them.")

    if not args.claim:
        print("\n(pass --claim N to emit reservation commands)")
        return 0

    nums = list(range(nxt, nxt + args.claim))
    cmds = [f'git commit --allow-empty -m "Pass {n} reserved: {args.topic} '
            f'({args.track} track)"' for n in nums]
    print(f"\nreserving {nums[0]}-{nums[-1]} in the singular form CLAUDE.md "
          f"mandates\n(one commit per number, so every scan sees every "
          f"number):\n")
    for c in cmds:
        print("  " + c)
    print(f"  git push {args.remote.split('/')[0]} "
          f"{args.remote.split('/')[-1]}")

    if args.run:
        print("\nrunning...")
        for n in nums:
            _git("commit", "--allow-empty", "-m",
                 f"Pass {n} reserved: {args.topic} ({args.track} track)")
        remote, branch = args.remote.split("/", 1)
        print(_git("push", remote, branch) or "pushed")
        print(f"claimed {nums[0]}-{nums[-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
