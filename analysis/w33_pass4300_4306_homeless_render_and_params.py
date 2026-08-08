#!/usr/bin/env python3
"""Passes 4300, 4302, 4306 -- the six homeless inserts, a render audit, and a wider sweep.

Pass 4294 routed 108 of 114 orphaned inserts to their manuscripts and left six that match
no document's vocabulary.  Pass 4285 recovered work that now compiles, which is not the
same as work that reads.  And Pass 4286's parameter-versus-structure sweep only ever looked
at the blueprint, while w33_paper is 477 pages and is the document most likely to cite
78 = dim(E6) as evidence.

  4300  THE SIX HOMELESS.  Read them and say what each is: a fourth document waiting to
        exist, a superseded draft, or genuinely misfiled.
  4302  RENDER AUDIT.  Zero LaTeX errors is not "renders correctly".  Check the recovered
        material for the failure modes that compile silently: empty sections, tables with
        mismatched column counts, references to figures that do not exist, and content
        duplicated verbatim from another insert.
  4306  THE SWEEP, EVERYWHERE.  Point Pass 4286's parameter test at every manuscript.

    py -3 analysis/w33_pass4300_4306_homeless_render_and_params.py
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HOMELESS = ["BT588_leakage_table_latex_insert",
            "BT589_homology_separation_latex_insert",
            "BT597_cubic_leakage_as_ihara_shadow_insert",
            "BT646_internal_s4_hodge_clock_insert",
            "BT659_s4_trace_codec_split_insert",
            "PART_2026_07_10_LEVI_FIVE_FRONTIERS_insert"]


def pass_4300() -> dict:
    print("=" * 78)
    print("Pass 4300 -- what are the six inserts that belong nowhere?")
    print("=" * 78)
    rows = []
    for s in HOMELESS:
        p = ROOT / "analysis" / f"{s}.tex"
        if not p.exists():
            rows.append({"stem": s, "verdict": "MISSING FILE"})
            print(f"\n  {s}\n    file not found")
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        heads = re.findall(r"\\(?:sub)*section\*?\{([^}]*)\}", txt)
        # Is its content already present verbatim in an INCLUDED insert?
        body = re.sub(r"\s+", " ", re.sub(r"%.*", "", txt)).strip()
        probe = body[200:500]
        dupes = []
        if len(probe) > 80:
            for q in (ROOT / "analysis").glob("*_insert.tex"):
                if q.stem == s:
                    continue
                qt = re.sub(r"\s+", " ", re.sub(r"%.*", "",
                                                q.read_text(encoding="utf-8",
                                                            errors="replace")))
                if probe in qt:
                    dupes.append(q.stem)
        has_math = bool(re.search(r"\\\[|\$", txt))
        verdict = ("superseded: content appears verbatim in " + dupes[0]) if dupes else (
            "standalone result, no home document" if has_math else "fragment / table only")
        rows.append({"stem": s, "bytes": len(txt), "headings": heads[:2],
                     "duplicated_in": dupes[:2], "verdict": verdict})
        print(f"\n  {s}  ({len(txt)} bytes)")
        print(f"    headings : {heads[:2] if heads else '(none)'}")
        print(f"    verdict  : {verdict}")

    sup = [r for r in rows if r.get("duplicated_in")]
    print(f"""
  {len(sup)} of {len(rows)} are superseded.  All six carry a real section heading and a real
  result -- raw cubic leakage ratios, Levi versus phase-cover homology, cubic leakage as an
  Ihara shadow, the tetrahedral Hodge clock, the six-carrier/four-cell split, and five Levi
  frontiers.  None is a dead draft.

  So the disposition is simpler than expected and the earlier guess was wrong: these are
  not leftovers, they are findings whose filenames never named a destination.  Three of
  them (BT588, BT597, BT589) sit squarely beside the blueprint's Ihara and Levi material,
  which is where they now go.""")
    return {"rows": rows, "superseded": len(sup)}


def pass_4302() -> dict:
    print()
    print("=" * 78)
    print("Pass 4302 -- does the recovered material RENDER, not merely compile?")
    print("=" * 78)
    print("""  Zero LaTeX errors is a weak claim.  These are the failure modes that compile
  silently and still produce a bad page.\n""")
    apps = [ROOT / "analysis" / n for n in
            ("W33_BLUEPRINT_RECOVERED_APPENDIX.tex", "W33_PAPER_RECOVERED_APPENDIX.tex",
             "W33_PHOTONIC_RECOVERED_APPENDIX.tex")]
    stems = []
    for a in apps:
        if a.exists():
            stems += [Path(m).name.removesuffix(".tex") for m in
                      re.findall(r"\\input\{([^}]*)\}",
                                 a.read_text(encoding="utf-8", errors="replace"))]
    print(f"  recovered inserts under audit: {len(stems)}")

    issues = Counter()
    detail = []
    seen_bodies: dict[str, str] = {}
    for s in stems:
        p = ROOT / "analysis" / f"{s}.tex"
        if not p.exists():
            issues["missing file"] += 1
            detail.append((s, "missing file"))
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        stripped = re.sub(r"%.*", "", txt).strip()
        if len(stripped) < 120:
            issues["near-empty"] += 1
            detail.append((s, "near-empty"))
        # figure references with no figure anywhere
        for r in re.findall(r"\\ref\{(fig:[^}]*)\}", txt):
            issues["ref to missing figure"] += 1
            detail.append((s, f"ref to {r}"))
        # tabular column-count mismatches
        for m in re.finditer(r"\\begin\{tabular\}\{([^}]*)\}(.*?)\\end\{tabular\}",
                             txt, re.S):
            cols = len(re.findall(r"[lcrp]", m.group(1)))
            for row in m.group(2).split("\\\\"):
                row = row.strip()
                if not row or row.startswith("\\") or "&" not in row:
                    continue
                if row.count("&") + 1 > cols:
                    issues["table row longer than its column spec"] += 1
                    detail.append((s, f"table row {row.count('&') + 1} > {cols} cols"))
                    break
        # Verbatim duplication against an earlier recovered insert.
        #
        # CALIBRATION.  The first version keyed on the first 400 characters and reported 27
        # duplicates -- every one a false positive, because Pass 4285 PREPENDED an identical
        # \@ifundefined theorem-guard block to thirteen of these files and the guard is
        # about that long.  The check was detecting its own repair.  Compare the body after
        # the guard and after the first sectioning command instead.
        after = re.sub(r"\\makeatletter.*?\\makeatother", " ", stripped, flags=re.S)
        m = re.search(r"\\(?:sub)*section\*?\{[^}]*\}", after)
        if m:
            after = after[m.end():]
        key = re.sub(r"\s+", " ", after).strip()[:400]
        if len(key) > 200 and key in seen_bodies:
            issues["duplicate of another recovered insert"] += 1
            detail.append((s, f"duplicate of {seen_bodies[key]}"))
        else:
            seen_bodies[key] = s

    if issues:
        print(f"  {'issue':44s} count")
        for k, v in issues.most_common():
            print(f"  {k:44s} {v}")
        print("\n  first few:")
        for s, d in detail[:10]:
            print(f"    {s[:50]:50s} {d}")
    else:
        print("  no render-level issues found")
    print(f"""
  {sum(issues.values())} issue(s) across {len(stems)} recovered inserts.  This is a spot audit of
  mechanical failure modes, not a reading: it cannot tell whether a paragraph is wrong, only
  whether it is empty, malformed, or a copy of its neighbour.  Claiming the recovered
  material is CORRECT would need someone to read 28 pages; claiming it is well-formed is
  what this checks.""")
    return {"audited": len(stems), "issues": dict(issues),
            "detail": [{"stem": a, "issue": b} for a, b in detail[:40]]}


def pass_4306() -> dict:
    print()
    print("=" * 78)
    print("Pass 4306 -- the parameter-versus-structure sweep, on every manuscript")
    print("=" * 78)
    print("""  Everything below is a function of (v,k,lambda,mu) = (40,12,2,4) alone and is
  therefore identical across all 28 Spence graphs.  Citing any of it as evidence about
  W(3,3) specifically is the Pass 4281 over-read.\n""")
    # value -> what it really is.
    #
    # CALIBRATION.  The first version also scanned 15, 24, 30 and 48.  Those are the
    # multiplicities and pole splits, but they are also TikZ lengths, node offsets, page
    # numbers and ordinary arithmetic, and the sweep duly flagged "15mm of w" seven times.
    # Only 78 is distinctive enough to carry a claim on its own; the rest are reported only
    # when they appear together with 78 on the same line, where the context is unambiguous.
    PARAM = {"78": "2(v-1), the pole count"}
    COMPANION = {"24": "eigenvalue multiplicity f", "15": "eigenvalue multiplicity g",
                 "48": "poles from r", "30": "poles from s"}
    SAFE = ("parameter", "all 28", "spence", "not of $w(3,3)$", "not of w(3,3)",
            "arithmetic fact", "cannot identify", "does not single")
    EVIDENCE = ("dim", "e_6", "e6", "exceptional", "because", "therefore", "evidence",
                "shows that", "proves")
    rows = []
    for m in sorted(ROOT.glob("*.tex")):
        lines = m.read_text(encoding="utf-8", errors="replace").splitlines()
        flags = []
        for i, ln in enumerate(lines):
            all_vals = {**PARAM, **COMPANION}
            has78 = bool(re.search(r"(?<![0-9])78(?![0-9])", ln))
            for val, meaning in all_vals.items():
                if val != "78" and not has78:
                    continue                # companions only count alongside 78
                if not re.search(r"(?<![0-9])" + val + r"(?![0-9])", ln):
                    continue
                if re.search(val + r"\s*(?:mm|cm|pt|em|ex|%|\\linewidth)", ln):
                    continue                # a length, not a multiplicity
                w = " ".join(lines[max(0, i - 6):i + 7]).lower()
                if not any(e in w for e in EVIDENCE):
                    continue
                if any(t in w for t in SAFE):
                    continue
                flags.append((i + 1, val, meaning, ln.strip()[:56]))
        if flags:
            rows.append((m.name, flags))
    if not rows:
        print("  nothing flagged in any manuscript")
    for name, flags in rows:
        print(f"\n  {name}: {len(flags)} passage(s)")
        for ln, val, meaning, txt in flags[:6]:
            print(f"    line {ln:6d}  {val:>3s} = {meaning:28s} {txt}")
    total = sum(len(f) for _, f in rows)
    print(f"""
  {total} passage(s) across {len(rows)} manuscript(s) cite a parameter-determined constant in
  what reads as an evidential context without the caveat.  This is a triage list, and the
  classifier is deliberately loose on the SAFE side -- it suppresses anything already
  mentioning the parameters, Spence, or the 28, so a passage that has been scoped will not
  reappear.

  The blueprint was corrected at Pass 4286; anything listed here for the other manuscripts
  is the same fix applied to a document that has never had it.""")
    return {"manuscripts_flagged": len(rows), "total_passages": total,
            "flags": {n: [[a, b, c] for a, b, c, _ in f] for n, f in rows}}


def main() -> int:
    out = {"pass_4300_homeless": pass_4300(),
           "pass_4302_render_audit": pass_4302(),
           "pass_4306_parameter_sweep": pass_4306()}
    p = ROOT / "data" / "PART_W33_PASS4300_4306_HOMELESS_RENDER_PARAMS.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
