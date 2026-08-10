#!/usr/bin/env python3
"""Passes 4710-4712 -- verify the fact this whole arc rests on, then find where else I made
the parameter-equality mistake.

  4710  W(3,q) is self-dual iff q is even.  Passes 4682, 4693, 4694, 4709 and the whole
        three-track convergence rest on it, and every one of them CITED it.  A cited fact
        carrying that much weight should be checked at least where checking is cheap:
        build W(3,q) and Q(4,q) and decide isomorphism outright at q = 2 and q = 3.

  4712  Pass 4693 found that Pass 4685 compared parameter-determined quantities and read
        agreement as evidence.  That error is MECHANICALLY DETECTABLE -- a spectral or
        trace quantity compared between two strongly regular graphs with equal parameters
        cannot distinguish them, ever.  Sweep the corpus for it.

    py -3 analysis/w33_pass4710_4712_selfduality_verified_and_a_vacuity_sweep.py
"""

from __future__ import annotations

import importlib.util
import itertools
import re
import sys
from pathlib import Path

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P57 = _load("p57", "w33_pass4456_4457_bass_reduction_and_gq_sweep.py")
P63 = _load("p63", "w33_pass4563_w33_is_not_self_dual.py")


def graph_of(pts, lines):
    G = nx.Graph()
    G.add_nodes_from(range(len(pts)))
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            G.add_edge(u, v)
    return G


def dual(pts, lines):
    """Points of the dual are the lines; two are collinear iff they meet."""
    n = len(lines)
    dpts = list(range(n))
    sets = [set(L) for L in lines]
    dlines = []
    for i in range(len(pts)):
        thru = [j for j in range(n) if i in sets[j]]
        if len(thru) > 1:
            dlines.append(thru)
    return dpts, dlines


def main() -> int:
    print("=" * 78)
    print("Passes 4710-4712")
    print("=" * 78)

    print("\n  PASS 4710 -- is W(3,q) really self-dual iff q is even?\n")
    print(f"  {'q':>2s} {'parity':>6s} {'points':>7s} {'W(3,q) vs its dual':>20s} "
          f"{'predicted':>12s} {'agrees':>7s}")
    rows = []
    for q in (2, 3):
        pts, lines = P57.symplectic_w3(q)
        G = graph_of(pts, lines)
        dp, dl = dual(pts, lines)
        H = graph_of(dp, dl)
        if G.number_of_nodes() != H.number_of_nodes() or \
                G.number_of_edges() != H.number_of_edges():
            iso = False
        else:
            iso = nx.is_isomorphic(G, H)
        pred = (q % 2 == 0)
        rows.append({"q": q, "even": bool(q % 2 == 0), "points": G.number_of_nodes(),
                     "isomorphic_to_dual": bool(iso), "predicted": bool(pred),
                     "agrees": bool(iso == pred)})
        print(f"  {q:2d} {'even' if q%2==0 else 'odd':>6s} {G.number_of_nodes():7d} "
              f"{str(iso):>20s} {str(pred):>12s} {str(iso == pred):>7s}")

    ok = all(r["agrees"] for r in rows)
    print(f"""
    DECIDED BY ISOMORPHISM TESTING, NOT BY CITATION. At q = 2 the quadrangle IS isomorphic
    to its dual; at q = 3 it is NOT. That is the fact Passes 4682, 4693, 4694 and 4709 all
    lean on, and until now every one of them took it from the literature. It is true, and it
    is now true here.

    NOTE WHAT THIS DOES NOT COVER: q = 4 and q = 5 are not tested. Isomorphism testing an
    85- or 156-vertex strongly regular graph is where the cheap method stops, and the
    prediction recorded at Pass 4695 lives at exactly those q. So the framework is verified
    where verification is cheap and remains cited where it is not -- which is the honest
    boundary, not a complete one.""")

    # ---- 4712: sweep for the vacuous comparison --------------------------
    print("\n  PASS 4712 -- where else did I compare parameter-determined quantities?\n")

    # NO OUTER \b on these two. Found by scripts/check_regex_deadends.py (Pass 4742): with
    # a trailing \b the alternatives tr\(A, trace\(, np\.trace and SRG\( are UNMATCHABLE --
    # each ends in an escaped non-word literal, and there is no word boundary between '('
    # and whatever follows it. The four most specific tokens in the spectral vocabulary and
    # the single most specific one in the SRG vocabulary all silently never fired, so the
    # candidate count this pass first reported was too low.
    SPECTRAL = re.compile(
        r"(?:tr\(A|trace\(|np\.trace|\beigenvalue\b|\beigenvalues\b|\bspectrum\b|"
        r"\bspectra\b|\bcharpoly\b|\bcharacteristic polynomial\b|\bmatrix_power\b)", re.I)
    SRGPAIR = re.compile(
        r"(?:SRG\(|\bstrongly regular\b|\bsame parameters\b|\bidentical parameters\b|"
        r"\bparameter-equal\b|\bequal parameters\b)", re.I)
    COMPARE = re.compile(
        r"\b(?:agree|agrees|match|matches|identical|equal|same|differ|distinguish|"
        r"separate)\b", re.I)

    hits = []
    files = sorted(list((ROOT / "analysis").rglob("*.py")) +
                   list((ROOT / "analysis").rglob("*.md")))
    for p in files:
        t = p.read_text(encoding="utf-8", errors="replace")
        lines_t = t.splitlines()
        for i, line in enumerate(lines_t):
            if not SPECTRAL.search(line):
                continue
            lo, hi = max(0, i - 5), min(len(lines_t), i + 6)
            ctx = "\n".join(lines_t[lo:hi])
            if SRGPAIR.search(ctx) and COMPARE.search(ctx):
                hits.append({"file": p.relative_to(ROOT).as_posix(), "line": i + 1,
                             "text": line.strip()[:100]})
                break           # one hit per file is enough to flag it for reading

    print(f"    scanned {len(files)} files, {len(hits)} carry a spectral comparison")
    print(f"    in the vicinity of an SRG-parameter statement\n")
    for h in hits[:14]:
        print(f"      {h['file']}:{h['line']}")
        print(f"        {h['text']}")

    print(f"""
    THESE ARE CANDIDATES FOR READING, NOT FINDINGS. The flag fires on co-occurrence, and
    co-occurrence is exactly what a CORRECT pass looks like too: Pass 4693 itself is a
    spectral comparison beside an SRG-parameter statement, and it is the pass that got this
    right. So the sweep cannot separate the error from its own diagnosis, and a count here
    is not a defect count.

    WHAT IT IS GOOD FOR is narrowing {len(files)} files to {len(hits)}. The rule to apply while reading
    each one is a single question: IF THE TWO OBJECTS HAVE THE SAME (v,k,lambda,mu), COULD
    THIS COMPARISON HAVE COME OUT ANY OTHER WAY? If not, the comparison is a restatement of
    the parameters and proves nothing about the objects. That question has no regex.""")

    out = {
        "boundary": ("4710 decides isomorphism outright at q = 2 and q = 3 only; q = 4 and "
                     "q = 5 are NOT tested and the Pass 4695 prediction lives there, so the "
                     "self-duality rule remains cited for the cases that matter most to it. "
                     "4712 is a triage filter, not a defect detector: it flags co-occurrence "
                     "of a spectral comparison with an SRG-parameter statement, which "
                     "correct passes also exhibit, and its output is a reading list"),
        "pass_4710_selfduality": {"rows": rows, "prediction_holds_where_tested": bool(ok),
                                  "untested": [4, 5]},
        "pass_4712_sweep": {"files_scanned": len(files), "candidates": len(hits),
                            "hits": hits,
                            "reading_rule": ("if the two objects have the same "
                                             "(v,k,lambda,mu), could this comparison have "
                                             "come out any other way? if not it restates "
                                             "the parameters")},
    }
    p = ROOT / "data" / "PART_W33_PASS4710_4712_SELFDUALITY_AND_VACUITY.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
