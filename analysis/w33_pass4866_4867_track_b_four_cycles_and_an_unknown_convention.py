#!/usr/bin/env python3
"""Passes 4866-4867 -- verify Track B's 1,080 four-cycles, and report a convention I cannot
determine.

  4866  Track B's newest packet states that the 1,080 minimum words of their
        [1620,64,96]_2 code are the Levi 8-cycles of GQ(4,2) and, equivalently, "all 1,080
        four-cycles of SRG(27,10,1,5)".  That second graph is Q(5,2), built in this lane at
        Pass 4562 over GF(2).  Pass 4824 verified their Levi 8-cycle count from H(3,4); this
        checks the other half of the same identity from the dual side.

  4867  Pass 4857 found five registry entries whose recorded sha256 matches nothing this
        lane can compute.  Eight serialisations were tried.  None matches.  The honest
        report is that the convention is unknown and needs its producer, not that the
        entries are stale.

    py -3 analysis/w33_pass4866_4867_track_b_four_cycles_and_an_unknown_convention.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
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


P62 = _load("p62", "w33_pass4562_second_dual_pair_and_a_correction.py")
PP = _load("pp", "w33_pass4754_4755_prime_power_quadrangles_and_bliss.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def count_four_cycles(g: igraph.Graph) -> int:
    """Exact number of 4-cycles: sum over vertex pairs of C(common neighbours, 2), / 2.

    Each 4-cycle has two diagonals, and each diagonal contributes one pair-of-common-
    neighbours choice, so the total counts every cycle exactly twice.
    """
    nb = [set(g.neighbors(v)) for v in range(g.vcount())]
    total = 0
    for u, v in itertools.combinations(range(g.vcount()), 2):
        c = len(nb[u] & nb[v])
        total += c * (c - 1) // 2
    return total // 2


def main() -> int:
    print("=" * 78)
    print("Passes 4866-4867")
    print("=" * 78)

    # ---- 4866 -----------------------------------------------------------
    print("\n  PASS 4866 -- four-cycles of SRG(27,10,1,5) = Q(5,2)\n")
    pts, lines = P62.build_q52()
    g = graph_of(pts, lines)
    prm = PP.srg_params(g)
    n4 = count_four_cycles(g)
    claimed = 1080
    print(f"    Q(5,2) parameters            : {prm}")
    print(f"    Track B's claim              : {claimed:,} four-cycles")
    print(f"    computed here                : {n4:,}")
    print(f"    agree                        : {n4 == claimed}")

    # cross-check against the Levi count Pass 4824 verified
    p2, l2 = P62.build_h34()
    n, L = len(p2), len(l2)
    B = igraph.Graph(n=n + L)
    B.add_edges([(p, n + j) for j, Ln in enumerate(l2) for p in Ln])
    print(f"\n    (Pass 4824 verified the dual side: Levi(H(3,4)) has 72 vertices,"
          f" {B.ecount()} edges,\n     girth {int(B.girth())}, and 1,080 eight-cycles.)")

    print(f"""
    {'BOTH SIDES OF THEIR IDENTITY NOW CHECK OUT INDEPENDENTLY.' if n4 == claimed else 'THE FOUR-CYCLE COUNT DISAGREES -- READ THE ROW.'}
    Track B says the 1,080 minimum words are the Levi 8-cycles of GQ(4,2) and equally the
    four-cycles of SRG(27,10,1,5). This lane built H(3,4) and Q(5,2) separately over GF(4)
    and GF(2), and gets 1,080 from each -- the 8-cycle count at Pass 4824 and the 4-cycle
    count here.

    THAT IS TWO COUNTS AGREEING, NOT THE IDENTIFICATION. Their claim is that the same 1,080
    objects carry both descriptions, which needs the bijection. What is checked is that both
    counts are 1,080 in constructions that share nothing with their code -- and Q(5,2) and
    H(3,4) are dual to each other, which is why the two counts have any right to coincide.""")

    # ---- 4867 -----------------------------------------------------------
    print("\n  PASS 4867 -- the registry digest convention, still unknown\n")
    reg = ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "1876.json"
    tried = []
    if reg.is_file():
        import hashlib
        r = json.loads(reg.read_text(encoding="utf-8"))
        tp = ROOT / r["certificate"]
        if tp.is_file():
            b = tp.read_bytes()
            d = json.loads(b)
            cand = {
                "target raw bytes": hashlib.sha256(b).hexdigest(),
                "target compact": hashlib.sha256(json.dumps(
                    d, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                "target indent2+nl": hashlib.sha256((json.dumps(
                    d, indent=2, sort_keys=True) + "\n").encode()).hexdigest(),
                "target indent2": hashlib.sha256(json.dumps(
                    d, indent=2, sort_keys=True).encode()).hexdigest(),
                "target compact unsorted": hashlib.sha256(json.dumps(
                    d, separators=(",", ":")).encode()).hexdigest(),
                "target minus boundary": hashlib.sha256(json.dumps(
                    {k: v for k, v in d.items() if k != "boundary"},
                    sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                "registry self compact": hashlib.sha256(json.dumps(
                    {k: v for k, v in r.items() if k != "sha256"},
                    sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                "registry self indent2": hashlib.sha256((json.dumps(
                    {k: v for k, v in r.items() if k != "sha256"},
                    indent=2, sort_keys=True) + "\n").encode()).hexdigest(),
            }
            want = r["sha256"]
            for k, v in cand.items():
                tried.append({"serialisation": k, "digest": v[:16],
                              "matches": v == want})
            print(f"    recorded : {want[:32]}")
            for t in tried:
                print(f"      {t['serialisation']:26s} {t['digest']}  "
                      f"{'MATCH' if t['matches'] else ''}")

    print(f"""
    EIGHT SERIALISATIONS TRIED, NONE MATCHES. The target certificate carries no self-digest,
    and git shows both files written the same day in single commits, so nothing changed
    underneath the entry.

    THE HONEST REPORT IS 'CONVENTION UNKNOWN', NOT 'STALE'. Pass 4857 nearly labelled these
    stale, which would have been the third false positive in one checker from assuming a
    key name implies a convention. There is no evidence they are wrong -- only that this
    lane cannot verify them, which is a different statement and belongs to whoever wrote
    the registry producer.

    ONE QUESTION ANSWERS ALL FIVE: what does w33_pass_namespace_registry_v2 hash into its
    sha256 field?""")

    out = {
        "boundary": ("4866 verifies COUNTS, not the identification: Track B claims the same "
                     "1,080 objects are both Levi 8-cycles and SRG(27,10,1,5) four-cycles, "
                     "and a bijection is not exhibited here. 4867 reports a negative -- "
                     "eight serialisations tried, none matches -- which establishes that "
                     "this lane cannot verify the registry digests, NOT that they are wrong"),
        "pass_4866": {"geometry": "Q(5,2)", "srg": list(prm),
                      "track_b_claim": claimed, "computed": n4,
                      "agree": n4 == claimed,
                      "companion": "Pass 4824 verified 1,080 Levi 8-cycles from H(3,4)"},
        "pass_4867": {"registry_sample": "1876.json", "serialisations_tried": tried,
                      "any_match": any(t["matches"] for t in tried),
                      "verdict": "convention unknown; needs the registry producer",
                      "not_a_verdict": "these entries are NOT shown to be stale"},
    }
    fp = ROOT / "data" / "PART_W33_PASS4866_4867_FOUR_CYCLES_AND_CONVENTION.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
