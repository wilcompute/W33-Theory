#!/usr/bin/env python3
"""Pass 4231 -- do our checkers catch faults they were not built from?

Both LaTeX checkers in this repo were written by staring at faults that had already
happened.  That is the right way to start and the wrong place to stop: a checker validated
only against the bugs that inspired it has unknown recall.  It might be matching the exact
byte sequence of the one instance it was shown.

So plant fresh instances -- different variable names, different numbers, different
surrounding prose -- and require each family to fire.  A family that misses its own planted
fault is not a checker, it is a memory of one commit.

    py -3 scripts/test_checker_recall.py

Exit 0 if every family has recall 1.0; exit 1 naming the families that missed.
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_tex_insert_pitfalls as chk  # noqa: E402

BS = chr(92)
FF = chr(12)

# Each planted fault is written fresh: different symbols and numbers from the real
# instances, so a checker that memorised the originals will miss these.
PLANTS = {
    "row-bracket": (
        "Consider the four codes and their duals:\n"
        "\\[\n\\begin{array}{c|c|c}\n"
        "[m,k,w]&w^\\perp&\\gamma\\\\ \\hline\n"
        "[9,4,3]&5&7\\\\\n"
        "[21,7,6]&2&19\\\\\n"
        "[33,11,9]&8&5\n"
        "\\end{array}\n\\]\nwith weights computed exactly.\n"),
    "double-sub": (
        "The decomposition\n\\[\n"
        "\\mathbb G_5^7 = \\mathbb H_7^2_{\\rm even}\\oplus\\mathbb K_4\n"
        "\\]\nis equivariant.\n"),
    "ctrl-byte": (
        "The calibrated coupling gives\n\\[\n"
        "B_z = Q|z\\rangle\\langle z|Q = " + FF + "rac{49}{128}|w_z\\rangle\\langle w_z|.\n"
        "\\]\nHolding the phase fixed.\n"),
    "undef-env": (
        "\\section{A planted section}\n"
        "\\begin{proposition}[Planted]\nEvery planted claim is false.\n"
        "\\end{proposition}\n"),
    "needs-pkg": (
        "\\section{Another planted section}\n"
        "\\begin{tikzcd}\nA \\arrow{r} & B\n\\end{tikzcd}\n"),
    # Added at Pass 4285.  This family did not exist when the checker was written, and
    # its absence let two inserts through that then failed to compile -- a reminder that
    # planted-fault recall measures the families you HAVE, never the ones you lack.
    "bare-underscore": (
        "The comparator emits rows marked PENDING_VERDICT until tolerances land.\n"
        "Escaped ones like FOO\\_BAR and $x_{i}$ and \\texttt{a_b} must NOT fire,\n"
        "nor must a hash inside verbatim:\n"
        "\\begin{verbatim}\nRUN_TAG deadbeef\n\\end{verbatim}\n"),
}
# Which family label each plant must produce (prefix match).
EXPECT = {"row-bracket": "row-bracket", "double-sub": "double-sub",
          "ctrl-byte": "ctrl-byte", "undef-env": "undef-env", "needs-pkg": "needs-pkg",
          "bare-underscore": "bare-underscore"}

# A clean file that must NOT fire: the honest form of the sentence Pass 4213 corrected.
CLEAN = (
    "\\section{A clean planted section}\n"
    "The walk is doubly stochastic, so the stationary distribution is uniform and\n"
    "\\[\n  |\\lambda_2| = 0.712345,\\qquad t_{\\mathrm{mix}} = 11 .\n\\]\n"
    "Every opcode is a bijection on the frames.\n")


def run_family_tests() -> tuple[dict, dict]:
    have, thms = chk.preamble_packages(), chk.preamble_theorems()
    hits, misses = {}, {}
    with tempfile.TemporaryDirectory() as td:
        for name, body in PLANTS.items():
            p = Path(td) / f"planted_{name}_insert.tex"
            p.write_text(body, encoding="utf-8")
            found = chk.scan(p, have, thms)
            kinds = [k for _, k, _ in found]
            ok = any(k.startswith(EXPECT[name]) for k in kinds)
            (hits if ok else misses)[name] = kinds
        # false-positive check
        p = Path(td) / "planted_clean_insert.tex"
        p.write_text(CLEAN, encoding="utf-8")
        clean_hits = [k for _, k, _ in chk.scan(p, have, thms)]
    return hits, {"misses": misses, "clean_false_positives": clean_hits}


def run_sweep_test() -> dict:
    """Pass 4226's manuscript sweep: plant a sentence that grades the instruction graph
    against a regular-graph bound, phrased differently from the one it was built on, and
    require the NEEDS REVIEW bucket to catch it."""
    FRAME = ("frame", "instruction", "opcode", "isa")
    GRADE = ("\\le", "bound", "short of", "misses", "optimal", "threshold", "%")
    WITHDRAWN = ("withdrawn", "corrected", "wrong", "not trustworthy", "it does not",
                 "none to miss", "not a question", "not gradable", "is not defined",
                 "does not satisfy", "not merely unproven", "has no optimum",
                 "without regularity", "no vertex degree", "not the kind of thing")
    pat = re.compile(r"ramanujan|k?-?regular|2\\sqrt|ihara|zeta|\\lambda_2", re.I)

    planted = (
        "The opcode network is a 6-regular expander on the frame register.\n"
        "Its second eigenvalue sits at 0.77, against a Ramanujan bound of\n"
        "$2\\sqrt5/6 = 0.745$, so the instruction fabric falls 3.4% short of\n"
        "the optimal value for its degree.\n").splitlines()

    flagged = []
    for i, ln in enumerate(planted):
        if not pat.search(ln):
            continue
        window = " ".join(planted[max(0, i - 8):i + 7]).lower()
        if (any(w in window for w in FRAME) and not any(w in window for w in WITHDRAWN)
                and any(w in window for w in GRADE)):
            flagged.append(i + 1)
    return {"planted_lines": len(planted), "flagged": flagged, "caught": bool(flagged)}


def main() -> int:
    print("=" * 78)
    print("Pass 4231 -- checker recall against freshly planted faults")
    print("=" * 78)
    hits, info = run_family_tests()
    misses, fps = info["misses"], info["clean_false_positives"]

    print("  check_tex_insert_pitfalls.py")
    for name in PLANTS:
        state = "CAUGHT" if name in hits else "MISSED"
        kinds = hits.get(name, misses.get(name, []))
        print(f"    {name:14s} {state:7s}  reported: {kinds if kinds else 'nothing'}")
    print(f"    recall: {len(hits)}/{len(PLANTS)}")
    print(f"\n    clean file (must stay silent): "
          f"{'SILENT' if not fps else 'FALSE POSITIVE ' + str(fps)}")

    sweep = run_sweep_test()
    print("\n  Pass 4226 manuscript sweep")
    print(f"    planted a differently-worded regular-graph grading: "
          f"{'CAUGHT at line ' + str(sweep['flagged']) if sweep['caught'] else 'MISSED'}")

    ok = (not misses) and (not fps) and sweep["caught"]
    print(f"""
  {'ALL FAMILIES HAVE RECALL 1.0 ON FRESH INSTANCES.' if ok else 'AT LEAST ONE FAMILY FAILED -- see above.'}
  The plants deliberately share no numbers, symbols or surrounding prose with the faults
  the checkers were written from: different code parameters, a different fraction inside
  the formfeed, a theorem-like environment nobody has used here, and a grading sentence
  phrased with '6-regular' and '3.4%' rather than the original wording.  A checker that had
  merely memorised its origin commit would miss these.

  The clean file matters as much as the plants.  It carries the honest form of the very
  sentence Pass 4213 corrected -- a measured second eigenvalue and a mixing time, reported
  and not graded -- and the checkers must stay silent on it.  A checker that fires on
  correct prose gets switched off, which is the failure mode that costs the most.""")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
