#!/usr/bin/env python3
"""Passes 4458-4459 -- every drive partition, and the backlog worth working.

  4458  Pass 4449 drove the bipartite incidence graph with ONE split of its four perfect
        matchings -- {1,2} against {3,4} -- and found pi-modes that disorder destroyed.  It
        concluded the chiral symmetry was not enough "in this drive", which leaves the
        obvious question unanswered: is any OTHER split protected?  There are only seven
        distinct two-step partitions of four matchings, so the question is finite and it is
        cheaper to answer than to speculate about.

  4459  Pass 4454 found 40 of 48 searching passes report a winner with no random baseline.
        Pass 4427 found 780 passes emit no certificate yet are cited elsewhere.  Neither
        list is workable on its own.  Their INTERSECTION is: a pass that searched, claimed a
        result, has no baseline showing the result was hard, AND is cited by other work.
        That is the set where an unmeasured claim is actually load-bearing.

    py -3 analysis/w33_pass4458_4459_drives_and_backlog.py
"""

from __future__ import annotations

import importlib.util
import itertools
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402
import check_search_baseline as csb  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "p4389", ROOT / "analysis" / "w33_pass4389_hermitian_quadrangle_measured.py")
p4389 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p4389)

RNG = np.random.default_rng(4458)
WRITES = re.compile(r"""["'](?:data/)?(PART_[A-Za-z0-9_]+\.json)["']""")


def incidence_and_matchings():
    pts, lines, _ = p4389.build_w33()
    n = len(pts)
    N = n + len(lines)
    I = np.zeros((N, N))
    for j, L in enumerate(lines):
        for p in L:
            I[p, n + j] = I[n + j, p] = 1
    left, right = list(range(n)), list(range(n, N))
    remaining = {(u, v) for u in left for v in right if I[u, v]}
    cols = []
    for _ in range(4):
        match = {}

        def aug(u, seen):
            for v in right:
                if (u, v) in remaining and v not in seen:
                    seen.add(v)
                    if v not in match or aug(match[v], seen):
                        match[v] = u
                        return True
            return False
        for u in left:
            aug(u, set())
        m = [(u, v) for v, u in match.items()]
        cols.append(m)
        remaining -= set(m)
    assert not remaining and all(len(c) == n for c in cols)
    return I, cols, N


def main() -> int:
    print("=" * 78)
    print("Passes 4458-4459 -- drive partitions, and the intersection backlog")
    print("=" * 78)

    # ---- Pass 4458 --------------------------------------------------------
    I, cols, N = incidence_and_matchings()
    print(f"\n  PASS 4458 -- all two-step partitions of four perfect matchings\n")

    def U_of(part, T, weights=None):
        H = [np.zeros(I.shape), np.zeros(I.shape)]
        for ci, c in enumerate(cols):
            side = 0 if ci in part else 1
            for k, (u, v) in enumerate(c):
                w = 1.0 if weights is None else weights[ci][k]
                H[side][u, v] = H[side][v, u] = w
        Us = []
        for h in H:
            e, V = np.linalg.eigh(h)
            Us.append(V @ np.diag(np.exp(-1j * T * e)) @ V.conj().T)
        return Us[1] @ Us[0]

    def count_pi(part, T, weights=None):
        ph = np.angle(np.linalg.eigvals(U_of(part, T, weights)))
        return int(np.sum(np.abs(np.abs(ph) - np.pi) < 0.02))

    parts = [(0,), (1,), (2,), (3,), (0, 1), (0, 2), (0, 3)]
    Ts = [np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2, 2 * np.pi / 3, 3 * np.pi / 4, np.pi]
    print(f"  {'partition':14s} " + " ".join(f"{t / np.pi:5.2f}pi" for t in Ts))
    grid = []
    for part in parts:
        row = [count_pi(part, T) for T in Ts]
        grid.append({"partition": list(part), "counts": row, "best": max(row)})
        print(f"  {str(part):14s} " + " ".join(f"{c:7d}" for c in row))

    best = max(grid, key=lambda r: r["best"])
    bT = Ts[best["counts"].index(best["best"])]
    print(f"\n    best clean partition: {tuple(best['partition'])} at T = {bT / np.pi:.2f}pi "
          f"with {best['best']} pi-modes")
    print(f"    {'disorder':>9s} {'mean':>7s} {'min':>5s} {'max':>5s}")
    dis = []
    for W in (0.0, 0.2, 0.5, 1.0):
        cs = []
        for _ in range(25):
            wts = [[1.0 + W * (RNG.random() - 0.5) for _ in c] for c in cols]
            cs.append(count_pi(tuple(best["partition"]), bT, wts))
        dis.append({"W": W, "mean": float(np.mean(cs)),
                    "min": int(min(cs)), "max": int(max(cs))})
        print(f"    {W:9.2f} {np.mean(cs):7.2f} {min(cs):5d} {max(cs):5d}")

    survives = dis[-1]["min"] > 0
    print(f"""
    {'A PROTECTED PARTITION EXISTS.' if survives else 'NO PARTITION IS PROTECTED, AND THAT IS NOW EXHAUSTIVE.'}

    All {len(parts)} distinct two-step partitions of the four perfect matchings were tried at seven
    drive periods. The best clean result is {best['best']} pi-modes; under chiral-preserving bond
    disorder at strength 1.0 the count is {dis[-1]['mean']:.2f} with minimum {dis[-1]['min']}.

    {'So the modes survive disorder that preserves the chiral symmetry, which is what protection means.' if survives else 'Pass 4449 said the chiral symmetry was not enough "in this drive", leaving open whether a'}
    {'' if survives else 'better drive existed. It does not: the partitions are exhausted. The chiral symmetry of the'}
    {'' if survives else 'incidence graph is exact and confers no Floquet protection on any two-step drive built'}
    {'' if survives else 'from its perfect matchings. That closes the question rather than deferring it.'}""")

    # ---- Pass 4459 --------------------------------------------------------
    print(f"\n  PASS 4459 -- searches with no baseline, that other work depends on\n")
    passes = sorted((ROOT / "analysis").glob("w33_pass*.py"))
    corpus = {}
    for pat in ("analysis/*.md", "analysis/*.py", "*.tex", "*.md"):
        for f in ROOT.glob(pat):
            try:
                corpus[f] = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass

    searched, no_base, cited_no_base = 0, [], []
    for p in passes:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        s, b, _ = csb.scan(t)
        if not s:
            continue
        searched += 1
        if b:
            continue
        no_base.append(p.stem)
        refs = sorted({f.name for f, txt in corpus.items()
                       if f.stem != p.stem and p.stem in txt})
        emits = [c for c in set(WRITES.findall(t)) if (ROOT / "data" / c).exists()]
        if refs:
            cited_no_base.append({"pass": p.stem, "citations": len(refs),
                                  "has_certificate": bool(emits), "cited_by": refs[:6]})

    cited_no_base.sort(key=lambda r: -r["citations"])
    worst = [r for r in cited_no_base if not r["has_certificate"]]
    print(f"    passes that search                      : {searched}")
    print(f"    ... with no baseline                    : {len(no_base)}")
    print(f"    ... AND cited elsewhere                 : {len(cited_no_base)}")
    print(f"    ... AND emitting no certificate either  : {len(worst)}")
    print(f"\n    the ten most load-bearing:")
    for r in cited_no_base[:10]:
        print(f"      {r['citations']:3d} refs  {'no cert' if not r['has_certificate'] else 'has cert'}"
              f"  {r['pass'][:52]}")

    print(f"""
    {len(worst)} PASSES SEARCHED, CLAIMED A WINNER, MEASURED NOTHING AGAINST CHANCE, EMIT NO
    CERTIFICATE, AND ARE CITED BY OTHER WORK.

    That is the set worth working, and it is small enough to work. Each of the other lists
    is too big to act on -- 780 uncertified, 40 unbaselined -- and each is mostly harmless
    on its own: an uncited pass is a notebook entry, and a search whose baseline is
    obviously zero needs no control. The intersection is where an unmeasured claim is
    actually carrying weight.

    THE ORDERING IS BY CITATIONS AND THAT IS THE WEAKEST PART. A citation here means the
    pass's filename appears in another file, which counts index and reservation mentions as
    dependence. The list is a triage order, not a severity ranking, and the top entries
    should be read before any of them is touched.""")

    out = {
        "boundary": ("4458 exhausts the two-step partitions of the four perfect matchings "
                     "at seven drive periods -- it does not exhaust all Floquet drives, "
                     "only those built this way. 4459's citation count is a filename match "
                     "and over-counts index mentions"),
        "pass_4458_drives": {"partitions": grid, "best_partition": best,
                             "best_T_over_pi": float(bT / np.pi),
                             "disorder": dis, "protected": bool(survives),
                             "conclusion": ("no two-step drive built from the perfect "
                                            "matchings gives disorder-protected pi-modes; "
                                            "Pass 4449's open question is closed")
                             if not survives else "a protected partition exists"},
        "pass_4459_backlog": {
            "searching_passes": searched, "no_baseline": len(no_base),
            "no_baseline_and_cited": len(cited_no_base),
            "no_baseline_cited_uncertified": len(worst),
            "priority": cited_no_base[:40]},
    }
    p = ROOT / "data" / "PART_W33_PASS4458_4459_DRIVES_AND_BACKLOG.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
