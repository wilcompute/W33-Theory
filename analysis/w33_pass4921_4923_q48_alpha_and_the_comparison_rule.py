"""Passes 4921-4923 -- alpha for the dual at q=8, a stale certificate reported, and a rule
extracted from three spurious cross-lane disagreements.

  4921  Q(4,8) is the dual of W(3,8), and q = 8 is even, so Pass 4774's parity rule says
        they are isomorphic and alpha follows without recomputation.  That is a prediction
        this lane can check by canonical form at 585 vertices, where the independence
        number itself is unreachable.

  4922  data/w33_pass1872_1876_five_frontiers.json declares a digest that does not match
        its own contents.  Reported precisely rather than repaired, because it belongs to
        another lane.

  4923  Three cross-lane checks this session reported a disagreement that was MY error --
        Pass 4824 (divided by two twice), Pass 4866 (looked up the wrong key), Pass 4913
        (root system not closed under negation).  Each time the other lane's number was
        right.  The fix each time was a one-line invariant statable before running.

    py -3 analysis/w33_pass4921_4923_q48_alpha_and_the_comparison_rule.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import sys
import time
from pathlib import Path

import igraph

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
P95 = _load("p95", "w33_pass4795_the_ovoid_gap_and_the_polarity_coset.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def main() -> int:
    print("=" * 78)
    print("Passes 4921-4923")
    print("=" * 78)

    # ---- 4921 ------------------------------------------------------------
    print("\n  PASS 4921 -- alpha(Q(4,8)) without computing it\n")
    t0 = time.time()
    pts, lines = PP.build_w3(PP.GF(2, 3))
    g = graph_of(pts, lines)
    dp, dl = PP.dual(pts, lines)
    h = graph_of(dp, dl)
    iso = PP.canon(g) == PP.canon(h)
    prm = PP.srg_params(g)
    hb = P95.hoffman(*prm)
    dt = time.time() - t0
    print(f"    W(3,8)                     : SRG{prm}, {g.vcount()} vertices")
    print(f"    Q(4,8) = its dual          : {h.vcount()} vertices, {h.ecount()} edges")
    print(f"    isomorphic (canonical form): {iso}   predicted (q even): True")
    print(f"    Hoffman bound, both        : {hb}")
    print(f"    alpha(W(3,8)) from Pass 4905: 65")
    print(f"    therefore alpha(Q(4,8))    : {65 if iso else 'not transferable'}")
    print(f"    elapsed                    : {dt:.1f}s")
    print(f"""
    {'THE PARITY RULE TRANSFERS THE ANSWER.' if iso else 'THEY ARE NOT ISOMORPHIC -- alpha DOES NOT TRANSFER.'} q = 8 is even, so W(3,8) and its dual
    are the same graph, and Pass 4905's alpha = 65 is Q(4,8)'s too. No independence
    computation was run on either -- 585 vertices is far past what that costs.

    AND THIS IS EXACTLY WHERE THE ODD-q PAIRS DIFFER. At q = 3 and q = 5 the dual is NOT
    isomorphic, so alpha does not transfer: Pass 4797 found 7 against 10 at q = 3, from two
    separate computations. Even q gets the answer free; odd q has to pay twice, and the two
    answers differ.""")

    # ---- 4922 ------------------------------------------------------------
    print("\n  PASS 4922 -- the stale certificate, reported precisely\n")
    tp = ROOT / "data" / "w33_pass1872_1876_five_frontiers.json"
    report = {}
    if tp.is_file():
        d = json.loads(tp.read_text(encoding="utf-8"))
        key = next((k for k in ("sha256_without_hash_field", "sha256", "universe_sha256")
                    if k in d), None)
        if key:
            x = {a: b for a, b in d.items() if a != key}
            recomputed = hashlib.sha256(json.dumps(
                x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            report = {"file": tp.name, "digest_key": key,
                      "declared": d[key], "recomputed": recomputed,
                      "match": d[key] == recomputed,
                      "owner": "outer-doily-five-front-execution-track",
                      "registry_entries_affected": ["1872", "1873", "1874", "1875"]}
            print(f"    file          : {tp.name}")
            print(f"    digest key    : {key}")
            print(f"    declared      : {d[key][:40]}")
            print(f"    recomputed    : {recomputed[:40]}")
            print(f"    match         : {d[key] == recomputed}")
            print(f"    owner         : outer-doily-five-front-execution-track")
            print(f"    registry rows pointing at it: 1872, 1873, 1874, 1875")
    print("""
    NOT REPAIRED HERE. Regenerating another lane's frozen certificate would change their
    artifact on the strength of my reading of their convention, and this session has three
    examples of that reading being wrong. The registry is blameless -- it copied what the
    certificate declared -- and four registry rows inherit the mismatch.""")

    # ---- 4923 ------------------------------------------------------------
    print("\n  PASS 4923 -- three spurious disagreements, one habit\n")
    INCIDENTS = [
        ("4824", "Levi eight-cycles", "reported 540 vs their 1,080",
         "divided by 2 twice -- once for direction of travel, once by mistake",
         "a cycle counted from its least vertex is found exactly twice"),
        ("4866", "registry digest", "reported 5 entries unverifiable",
         "looked up 'sha256' when the target declared 'sha256_without_hash_field'",
         "the file's own SELF_DIGEST_KEYS lists three names"),
        ("4913", "E6 projective roots", "reported 52 pairs vs their 36",
         "root set not closed under negation -- outer sign varied independently",
         "72 roots must give exactly 36 pairs"),
    ]
    print(f"  {'pass':6s} {'object':22s} {'what I reported':32s}")
    for p, obj, rep, cause, inv in INCIDENTS:
        print(f"  {p:6s} {obj:22s} {rep:32s}")
        print(f"         cause    : {cause}")
        print(f"         invariant: {inv}")
    print(f"""
    THREE FOR THREE, AND THE OTHER LANE WAS RIGHT EVERY TIME. Each disagreement came from
    my construction of the comparison object, not from their result -- and in each case a
    single invariant, statable before running anything, would have caught it:

        a cycle found from its least vertex is found twice, not four times
        a digest key is looked up in the canonical list, never assumed
        72 roots give 36 projective pairs

    THE RULE: before comparing against another lane's number, state one invariant your OWN
    object must satisfy and check it. Not the quantity under comparison -- that is what is
    being tested -- but a structural fact you already know.

    A cross-lane check that reports a spurious disagreement is worse than not running one,
    because the natural next move is to doubt the other lane, and I have now generated that
    move three times in a session where they were correct on every occasion.""")

    out = {
        "boundary": ("4921 transfers alpha by ISOMORPHISM, verified by canonical form; no "
                     "independence number is computed at 585 vertices and none could be. "
                     "4922 reports and does not repair -- the certificate belongs to "
                     "another lane and this session has three examples of my reading of "
                     "another lane's convention being wrong. 4923 is a census of my own "
                     "errors and asserts nothing about anyone else's work"),
        "pass_4921": {"q": 8, "srg": list(prm), "self_dual": bool(iso),
                      "hoffman": hb, "alpha_w38": 65,
                      "alpha_q48": 65 if iso else None,
                      "method": "isomorphism transfer, not computation"},
        "pass_4922": report,
        "pass_4923": {"incidents": [{"pass": p, "object": o, "reported": r,
                                     "cause": c, "invariant": i}
                                    for p, o, r, c, i in INCIDENTS],
                      "rule": ("before comparing against another lane's number, state one "
                               "invariant your own comparison object must satisfy and "
                               "check it -- not the quantity under test, a structural fact "
                               "already known")},
    }
    fp = ROOT / "data" / "PART_W33_PASS4921_4923_Q48_AND_COMPARISON_RULE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
