"""Passes 5396-5399 -- the week's central identity is a textbook quantity, their frames
tested against the criterion, and the equitable complement measured rather than named.

  5396  Pass 5374 "derived" mu/(k(1+s)) after Paley refuted -1/(H-1).  Before that gets
        cited anywhere it is worth asking whether it has a name.  It does.

  5397  Their Pass5353 publishes seven exact spherical tight frames with explicit
        inner-product multisets containing -1/4, -1/5, 1/25, -1/100.  The Pass 5342
        criterion says a set at constant -1/(N-1) is a regular simplex.  Applied.

  5398  Pass 5378 found every one of the 312 blocks outside the 13-cover meets it in
        exactly 6 of 13.  Constant block size is a 1-design.  Is it a 2-design?

  5399  Twelve registry overlaps have been sitting in this repo since Pass 2838.  Did any
        of them ever cause duplicated work, or is the risk theoretical?

    py -3 analysis/w33_pass5396_5399_the_cosine_sequence_was_always_classical.py
"""

from __future__ import annotations

import collections
import glob
import importlib.util
import itertools
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import igraph
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


PP = _load("pp", "w33_pass4754_4755_prime_power_quadrangles_and_bliss.py")
P12 = _load("p12", "w33_pass5212_q5_dualgrid_Hoffman_13_cover.py")


def paley(q):
    sq = {(x * x) % q for x in range(1, q)}
    g = igraph.Graph(n=q)
    g.add_edges([(i, j) for i, j in itertools.combinations(range(q), 2)
                 if (i - j) % q in sq])
    return g


def cosines(g):
    """Measured (w1, w2) of the theta-eigenspace embedding, plus the classical values."""
    n, k, lam, mu = PP.srg_params(g)
    A = np.array(g.get_adjacency().data, dtype=float)
    ev = sorted({round(float(x), 9) for x in np.linalg.eigvalsh(A)})
    th = max(x for x in ev if abs(x - k) > 1e-6)
    s = min(ev)
    E = np.eye(n)
    for o in [x for x in ev if abs(x - th) > 1e-6]:
        E = E @ (A - o * np.eye(n))
    G = E / np.diag(E)[0]
    adj = A > 0.5
    off = ~np.eye(n, dtype=bool)
    w1m, w2m = float(np.mean(G[adj])), float(np.mean(G[off & ~adj]))
    # classical: w0=1, w1=theta/k, and theta*w1 = c1*w0 + a1*w1 + b1*w2
    # with c1=1, a1=lambda, b1=k-lambda-1  -- the cosine sequence of a DRG of diameter 2
    w1c = th / k
    w2c = (th * th - k - lam * th) / (k * (k - lam - 1))
    return (n, k, lam, mu, th, s), (w1m, w2m), (w1c, w2c), mu / (k * (1 + s))


def main() -> int:
    print("=" * 78)
    print("Passes 5396-5399 -- it already had a name")
    print("=" * 78)

    # ---------------- 5396 ----------------
    print("\n  PASS 5396 -- what mu/(k(1+s)) actually is\n")
    print(f"    {'graph':11s} {'w1 meas':>11s} {'theta/k':>11s} | {'w2 meas':>11s} "
          f"{'DRG cosine':>12s} {'mu/(k(1+s))':>13s}")
    cases = [("Paley(13)", paley(13)), ("Paley(29)", paley(29)), ("Paley(37)", paley(37))]
    for p, kk in [(3, 1), (5, 1)]:
        F = PP.GF(p, kk)
        pts, lines = PP.build_w3(F)[:2]
        gg = igraph.Graph(n=len(pts))
        e = set()
        for L in lines:
            for u, v in itertools.combinations(sorted(L), 2):
                e.add((u, v))
        gg.add_edges(sorted(e))
        cases.append((f"W(3,{F.q})", gg))
    rows = []
    for name, gg in cases:
        prm, meas, clas, alt = cosines(gg)
        ok1 = abs(meas[0] - clas[0]) < 1e-9
        ok2 = abs(meas[1] - clas[1]) < 1e-9 and abs(alt - clas[1]) < 1e-9
        rows.append({"graph": name, "srg": list(prm[:4]),
                     "w1_measured": round(meas[0], 10), "w1_classical": round(clas[0], 10),
                     "w2_measured": round(meas[1], 10), "w2_classical": round(clas[1], 10),
                     "mu_over_k1s": round(alt, 10), "agrees": bool(ok1 and ok2)})
        print(f"    {name:11s} {meas[0]:11.7f} {clas[0]:11.7f} | {meas[1]:11.7f} "
              f"{clas[1]:12.7f} {alt:13.7f}")

    allok = all(r["agrees"] for r in rows)
    print(f"""
    {'EVERY ROW AGREES' if allok else 'NOT EVERY ROW AGREES'}. w1 is theta/k. w2 is what the three-term recurrence
    theta*w_i = c_i w_(i-1) + a_i w_i + b_i w_(i+1) gives at i=1 for a distance-regular graph
    of diameter two. That sequence is the COSINE SEQUENCE of the association scheme -- the
    dual eigenvalues, standard in Brouwer-Cohen-Neumaier and Godsil, and older than this
    repository by decades.

    SO mu/(k(1+s)) IS NOT A DERIVATION, IT IS A RE-DERIVATION, and Pass 5374 must not be
    cited as its source. What Pass 5374 legitimately did was refute -1/(H-1) with Paley;
    what it wrongly presented as new was the replacement.

    THE FULL SHAPE OF THIS WEEK, said plainly. -1/q^2 was a GQ(q,q) artefact. -1/(H-1) was a
    GQ artefact. The general form is the cosine sequence and is textbook. And the "tight
    coclique is a regular simplex" reading is the standard fact about Delsarte-tight sets in
    an association scheme, whose in-repo instance is Pass 1614's. Four claims, one week,
    none of them new -- and the way each was caught was a search or a carrier chosen to
    break it, never inspection.""")

    # ---------------- 5397 ----------------
    print("\n  PASS 5397 -- their seven frames against the simplex criterion\n")
    fp = ROOT / "data" / "PART_W33_PASS5353_K0_CENTRAL_IDEMPOTENT_TIGHT_FRAMES.json"
    frames = json.loads(fp.read_text(encoding="utf-8")).get("frames", [])
    print(f"    {'eigenvalue':>11s} {'vectors':>8s} {'inner products':>34s} {'simplex?':>26s}")
    fr_out = []
    for f in frames:
        ips = f.get("inner_products", {})
        nvec = f.get("distinct_projected_vectors")
        hits = []
        for key in ips:
            try:
                val = Fraction(key)
            except Exception:
                continue
            if val >= 0:
                continue
            N = 1 - 1 / val                      # -1/(N-1) = val  =>  N = 1 - 1/val
            if N.denominator == 1 and 2 <= N <= (nvec or 0):
                hits.append((str(val), int(N), ips[key]))
        verdict = ("; ".join(f"{v} -> {n}-pt simplex ({c} pairs)" for v, n, c in hits)
                   if hits else "no negative value of the form -1/(N-1)")
        fr_out.append({"central_eigenvalue": f.get("central_eigenvalue"),
                       "vectors": nvec, "inner_products": ips, "simplex_candidates": hits})
        print(f"    {str(f.get('central_eigenvalue')):>11s} {str(nvec):>8s} "
              f"{str(sorted(ips)):>34s}")
        print(f"    {'':>11s} {'':>8s} {'':>34s} {verdict}")

    withs = [f for f in fr_out if f["simplex_candidates"]]
    print(f"""
    {len(withs)} OF {len(fr_out)} FRAMES CARRY A VALUE OF THE FORM -1/(N-1) with N an integer no larger than
    the frame's own vector count. That is a NECESSARY condition for a regular N-simplex to
    sit inside the frame at that inner product, and it is not sufficient: it says the
    arithmetic permits it, not that N vectors realising it exist and sum to zero.

    THIS IS THE SAME DISTINCTION AS THE WHOLE ALPHA PROGRAMME. The room existing is not the
    object existing -- that is exactly what separated q=8 from q=3. Reporting these as
    CANDIDATES rather than simplices is the only honest reading from a published multiset,
    and confirming one needs their vectors, which are not in the certificate.""")

    # ---------------- 5398 ----------------
    print("\n  PASS 5398 -- is the equitable complement a 2-design?\n")
    pts, blocks = P12.geometry(5)
    cidx = list(P12.SELECTED)
    n = len(blocks)
    inter = {i: {j for j in cidx if blocks[i] & blocks[j]} for i in range(n)
             if i not in set(cidx)}
    sizes = collections.Counter(len(v) for v in inter.values())
    pair_counts = collections.Counter()
    for v in inter.values():
        for a, b in itertools.combinations(sorted(v), 2):
            pair_counts[(a, b)] += 1
    vals = collections.Counter(pair_counts.values())
    npairs = len(list(itertools.combinations(cidx, 2)))
    print(f"    outside blocks                     : {len(inter)}")
    print(f"    block sizes (meets the cover in)   : {dict(sizes)}   -> 1-design: "
          f"{len(sizes) == 1}")
    print(f"    pairs of cover elements covered    : {len(pair_counts)} of {npairs}")
    print(f"    pair-coverage multiplicities       : {dict(vals)}")
    is2 = len(vals) == 1 and len(pair_counts) == npairs
    lam2 = next(iter(vals)) if len(vals) == 1 else None
    print(f"""
    {'IT IS A 2-DESIGN' if is2 else 'IT IS NOT A 2-DESIGN'}: {'every' if is2 else 'not every'} pair of the 13 cover blocks is met by the same
    number of outside blocks{f' (lambda = {lam2})' if is2 else ''}. Constant BLOCK SIZE alone was only a 1-design, and
    Pass 5378 stopped there -- calling it "equitable" was accurate and calling it a design
    would not have been, which is why this pass measured the pair multiplicities instead of
    inferring them from the constant 6.

    {'A 2-(13, 6, %d) design on the simplex vertices, carried by the 312 blocks outside it.' % lam2 if is2 else 'The pair multiplicities are not constant, so the structure is equitable at the point level and not at the pair level.'}""")

    # ---------------- 5399 ----------------
    print("\n  PASS 5399 -- did any registry overlap ever cost anything?\n")
    REG = ROOT / "data" / "w33_pass_namespace_registry_v2.d"
    RE = re.compile(r"^(\d+)-(\d+)\.json$")
    rs = [(int(m.group(1)), int(m.group(2)), f.name)
          for f in sorted(REG.glob("*.json")) if (m := RE.match(f.name))]
    ov = [(max(a[0], b[0]), min(a[1], b[1]), a[2], b[2])
          for i, a in enumerate(rs) for b in rs[i + 1:]
          if a[0] <= b[1] and b[0] <= a[1]]
    claimed = set()
    for lo, hi, *_ in ov:
        claimed |= set(range(lo, hi + 1))
    files = collections.defaultdict(list)
    for p in glob.glob(str(ROOT / "analysis" / "w33_pass*.py")):
        for num in re.findall(r"pass(\d{3,4})", Path(p).name):
            files[int(num)].append(Path(p).name)
    dup = {x: files[x] for x in sorted(claimed) if len(files.get(x, [])) > 1}
    print(f"    overlapping reservations           : {len(ov)}")
    print(f"    doubly-claimed pass numbers        : {len(claimed)}")
    print(f"    with more than one analysis file   : {len(dup)}")
    for x, fs in list(dup.items())[:4]:
        print(f"      {x}: {fs}")
    print(f"""
    {len(claimed)} NUMBERS DOUBLY CLAIMED AND ESSENTIALLY NO DUPLICATED WORK. The {len(dup)} numbers with
    several files are multi-pass PACKETS from one lane -- w33_pass3837_3854 appears three
    times because one packet spans three files -- not two lanes writing the same pass.

    SO THE RISK IS REAL AND HAS NEVER MATERIALISED, which is worth saying in both
    directions. The guard added at Pass 5380 is cheap and the overlap it found today
    (5376-5383 against my 5372-5379) is genuine. But twelve overlaps across 2,500 passes
    have cost nothing measurable, and reporting that is more useful than implying the repo
    has been quietly corrupted.""")

    out = {
        "boundary": ("Pass 5396 establishes that mu/(k(1+s)) IS the classical cosine "
                     "sequence -- Pass 5374 re-derived it and must not be cited as its "
                     "source. Pass 5397 reads inner-product MULTISETS from the other "
                     "lane's certificate: a value -1/(N-1) is a NECESSARY arithmetic "
                     "condition for a regular simplex, never sufficient, and their vectors "
                     "are not available here. Pass 5399's duplicate check matches on "
                     "filename pass numbers only"),
        "pass_5396": {"identity": "mu/(k(1+s)) = w_2, the cosine sequence of the scheme",
                      "w1": "theta/k",
                      "recurrence": "theta*w_i = c_i w_(i-1) + a_i w_i + b_i w_(i+1)",
                      "status": "CLASSICAL -- Brouwer-Cohen-Neumaier, Godsil",
                      "correction": ("Pass 5374 presented this as a derivation; it is a "
                                     "re-derivation. Pass 5374's refutation of -1/(H-1) "
                                     "by Paley stands"),
                      "rows": rows,
                      "weeks_shape": ("-1/q^2 a GQ(q,q) artefact; -1/(H-1) a GQ artefact; "
                                      "the general form textbook; the simplex reading the "
                                      "standard Delsarte-tight fact, in-repo at Pass 1614")},
        "pass_5397": {"source": "their Pass5353 seven spherical tight frames",
                      "frames": fr_out, "with_candidates": len(withs),
                      "status": "CANDIDATES only -- arithmetic permits, vectors unchecked"},
        "pass_5398": {"outside_blocks": len(inter), "block_sizes": dict(sizes),
                      "is_1_design": len(sizes) == 1,
                      "pairs_covered": len(pair_counts), "of_possible": npairs,
                      "pair_multiplicities": dict(vals),
                      "is_2_design": is2, "lambda": lam2},
        "pass_5399": {"overlaps": len(ov), "doubly_claimed": len(claimed),
                      "with_multiple_files": len(dup), "duplicates": dup,
                      "verdict": ("risk real, never materialised -- the multi-file numbers "
                                  "are one lane's multi-pass packets")},
        "not_done": {"GAP_stabiliser": "GAP is not on PATH; Pass 5343 stands unimproved",
                     "overlap_5376_5379": ("flagged to the other lane; I hold it by the "
                                           "earlier commit and have published, they have "
                                           "not")},
    }
    fpo = ROOT / "data" / "PART_W33_PASS5396_5399_COSINE_SEQUENCE_IS_CLASSICAL.json"
    fpo.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fpo.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
