#!/usr/bin/env bash
# Run a GAP script on Windows.  Learned the hard way across three sessions --
# each of these cost a round, so they are written down rather than rederived:
#
#   * gap.bat spawns a DETACHED mintty window, returns exit 0 immediately, and
#     never runs your script.  Its exit code is meaningless.  Do not use it.
#   * gap.exe invoked directly also exits 0 and does nothing: it needs the Cygwin
#     runtime environment that only the runtime's own bash sets up.
#   * stdout does not survive the hand-off.  Have GAP write results with
#     PrintTo/AppendTo to a file and read the file.  A script printing only to
#     stdout looks exactly like a silent failure.
#   * GAP here is a Cygwin build and wants a WINDOWS-style path (C:/foo/bar.g).
#     The MSYS form /c/foo/bar.g is not understood.  This script does NOT
#     translate for you: an attempted translation ate the drive letter and looked
#     like a GAP fault, costing another round.  Pass Windows style.
#   * We must cd into the GAP install dir to invoke ./gap, so GAP's working
#     directory is NOT the repo.  A relative OutputTextFile("data/x.json") writes
#     into the GAP installation -- or, if data/ is absent there, silently returns
#     `fail`, and the next SetPrintFormattingStatus dies with "no method found
#     ... 1st argument is 'fail'".  That error names neither the path nor the
#     directory, which is why it reads as a GAP bug.  This script therefore
#     exports W33_REPO (Windows style); read it in GAP and build absolute paths:
#
#       repo := GAPInfo.SystemEnvironment.W33_REPO;
#       out  := Concatenation(repo, "/data/whatever.json");
#
# Usage:  scripts/run_gap.sh 'C:/path/to/script.g'
#
# Verified working (W(E8) on its 240 roots, 2026-07-25): |W(E8)| = 696729600,
# transitive, root stabiliser 2903040 = |W(E7)|, imprimitive with 120 blocks of
# size 2 -- the antipodal pairs.
set -euo pipefail
GAPROOT="${GAPROOT:-/c/Program Files/GAP-4.16.0}"
BASH_EXE="$GAPROOT/runtime/bin/bash.exe"
VER="$(basename "$GAPROOT" | sed 's/^GAP-//')"
[ $# -ge 1 ] || { echo "usage: $0 'C:/path/to/script.g'" >&2; exit 2; }
[ -x "$BASH_EXE" ] || { echo "no GAP runtime bash at $BASH_EXE" >&2; exit 1; }
case "$1" in
  [A-Za-z]:/*) ;;
  *) echo "error: pass a Windows-style path with forward slashes (got: $1)" >&2; exit 2;;
esac

# Repo root for the script, Windows style, so GAP can write back into the repo.
# analysis/foo.g and scripts/foo.g both resolve to the repo, not to their parent.
SCRIPT_DIR="${1%/*}"
case "${SCRIPT_DIR##*/}" in
  analysis|scripts|tests|exploration) REPO="${SCRIPT_DIR%/*}" ;;
  *) REPO="$SCRIPT_DIR" ;;
esac
REPO="${W33_REPO:-$REPO}"

exec "$BASH_EXE" -l -c "cd /opt/gap-$VER && W33_REPO='$REPO' ./gap -q -b --nointeract '$1'"
