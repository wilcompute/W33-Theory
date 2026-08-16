"""Passes 5635-5642 -- the third recalibration failed for the reason the first two did,
and a test left open on 2026-05-29 resolves negative.

  5635  The routing blocklist, A/B tested on one corpus.
  5636  Why all three recalibrations failed: I ranked tokens and measured files.
  5637  Reranking per file, and what it surfaces.
  5638  The 16-codec adjacency test, open since 2026-05-29, resolves NEGATIVE.
  5639  Coincidence nine: the two 192s are not the same 192.
  5640  The tomotope's 192 flags are two torsors, not one.
  5641  alpha(W(3,9)) is still open, and why.
  5642  My own guards, turned on my own passes.

    py -3 analysis/w33_pass5635_5642_the_sixteen_codecs_are_not_a_hypercube.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Measured in this pass; see the docstring runs.
AB = {"corpus": 5056, "off_pct": 70.8, "on_pct": 70.7, "delta_certificates": -2,
      "shared_tokens_off": 15127, "shared_tokens_on": 12887}
ROUTER_FILES = 10
STEMS_BY_FILE = [("depth", 538, 1155), ("tomotope_flag", 190, 939),
                 ("line", 272, 802), ("support", 238, 601),
                 ("value", 105, 583), ("tick", 70, 526)]
GUARDS = {"check_spectral_overreach": 0, "check_convention_fixed_form": 1,
          "check_order_coincidence": 1}


def q4() -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(16))
    for a in range(16):
        for b in range(4):
            g.add_edge(a, a ^ (1 << b))
    return g


def codec16() -> nx.Graph:
    """The 16 codecs of the 2026-05-29 file: 2 tetrahedron halves, 7 Csaszar
    vertices, 7 Szilassi faces, each family with the adjacency it carries."""
    g = nx.Graph()
    g.add_nodes_from([("tet", i) for i in range(2)])
    g.add_nodes_from([("cs", i) for i in range(7)])
    g.add_nodes_from([("sz", i) for i in range(7)])
    for i, j in itertools.combinations(range(7), 2):
        g.add_edge(("cs", i), ("cs", j))   # Csaszar skeleton is K7
        g.add_edge(("sz", i), ("sz", j))   # Szilassi face-adjacency is K7
    return g


def main() -> int:
    print("=" * 78)
    print("Passes 5635-5642 -- the 16 codecs are not a hypercube")
    print("=" * 78)

    print("\n  PASS 5635 -- the blocklist, A/B tested on ONE corpus\n")
    print(f"    corpus                : {AB['corpus']:,} certificates")
    print(f"    blocklist OFF         : {AB['off_pct']}% fire, "
          f"{AB['shared_tokens_off']:,} shared tokens")
    print(f"    blocklist ON          : {AB['on_pct']}% fire, "
          f"{AB['shared_tokens_on']:,} shared tokens")
    print(f"    delta                 : {AB['delta_certificates']:+d} certificates")
    print(f"""
    IT MOVED TWO CERTIFICATES OUT OF {AB['corpus']:,}. And the 60% -> 68% -> 70%
    sequence I have been reporting across three passes was never a trend: those were
    three different corpora and bands compared as though they were one measurement.
    On a single corpus the blocklist does essentially nothing.""")

    print("\n  PASS 5636 -- why all three recalibrations failed\n")
    print(f"    certificates containing router keys : {ROUTER_FILES} of {AB['corpus']:,}"
          f"  ({100 * ROUTER_FILES / AB['corpus']:.1f}%)")
    print("""
    I RANKED TOKENS AND MEASURED FILES. Pass 5580 ranked stems by DISTINCT TOKENS, saw
    `chart` at 538, and concluded the firing rate was driven by routing infrastructure.
    But those 538 tokens live in TEN files. A per-file firing rate cannot be moved by
    suppressing tokens that appear in 0.2% of the corpus, so the blocklist could not
    have worked, and it did not.

    THAT IS ALSO WHY PASS 5573 FAILED. Excluding dense certificates raised the rate
    because density is a per-file property being used against a per-token diagnosis.
    Three recalibrations, one error, repeated: the unit I diagnosed in was never the
    unit I measured in.""")

    print("\n  PASS 5637 -- reranked by file-hits\n")
    print(f"    {'stem':22s} {'distinct tokens':>16s} {'file-hits':>11s}")
    for s, t, f in STEMS_BY_FILE:
        print(f"    {s:22s} {t:16,d} {f:11,d}")
    print("""
    `tomotope_flag` IS THE SECOND-BIGGEST HUB IN THE CORPUS by the unit that matters --
    939 file-hits across 63 certificates. Ranked by tokens it was invisible behind the
    routing keys. That reranking is what sent this pass to the tomotope.""")

    print("\n  PASS 5638 -- the test left open on 2026-05-29\n")
    Q, G = q4(), codec16()
    print(f"    Q4                   : 4-regular, bipartite={nx.is_bipartite(Q)}, "
          f"triangles={sum(nx.triangles(Q).values()) // 3}")
    print(f"    16-codec graph       : degrees "
          f"{sorted(set(dict(G.degree()).values()))}, "
          f"bipartite={nx.is_bipartite(G)}, "
          f"triangles={sum(nx.triangles(G).values()) // 3}")
    print(f"    isomorphic to Q4     : {nx.is_isomorphic(G, Q)}")
    print("""
    NEGATIVE, AND THE OBSTRUCTION IS INVARIANT. analysis/2026-05-29_flag_codec_toroidal_
    hypercube_boundary.md closes with its own next test: "build the explicit 16-codec
    adjacency graph and compare it to Q4 / toroidal-knight adjacency." Built: Csaszar's
    vertex-adjacency and Szilassi's face-adjacency are each K7, so the codec graph is
    6-regular with 70 triangles while Q4 is 4-regular, bipartite and triangle-free.

    NO ASSIGNMENT CAN FIX IT. Bipartiteness and triangle-freeness are invariants of the
    codec graph, not of which codec sits at which Q4 vertex, so the failure survives
    every relabelling.

    WHAT SURVIVES is the arithmetic: 192 = 16 x 12 = (2+7+7) x 12 = 24+84+84 is a correct
    flag count. What does not survive is the architectural sentence "Q4 supplies the
    toroidal boundary layout for all 16 codecs". Q4 supplies sixteen SLOTS -- a set of
    the right size -- and the codecs inherit none of its adjacency.""")

    print("\n  PASS 5639 -- coincidence nine\n")
    print("    |Rot(Q4)| = 192   and   tomotope flags = 192")
    print("""
    NOT THE SAME 192, killed on structure rather than by another carrier. A group of
    order 192 acting regularly on 192 points is TRANSITIVE. The 192 flags carry an
    Aut-invariant partition into unequal parts -- 24 + 84 + 84 by source object -- and
    transitive is incompatible with that. This is the ninth coincidence this thread has
    killed, and the second killed on structure rather than by running at another q.""")

    print("\n  PASS 5640 -- and the certificate says so independently\n")
    print("    bt1371: 192-row address table, orbit_sizes_are_two_96s = True,")
    print("            gap_iso_maps_all_96_group_elements = True")
    print("""
    TWO TORSORS, NOT ONE. The tomotope group has order 96 and acts on the 192 flags with
    two regular orbits of 96. So the flag set is a torsor pair under an order-96 group,
    never a torsor under an order-192 group -- a second, independent refutation of the
    coincidence, and one already committed in a certificate since bt1371.

    THIS ALSO CONFIRMS THE DCCLXXXIV ERRATA I appended at Pass 5585: 96 is the polytope's
    automorphism group. It is the group that acts here, and 576 remains the
    configuration's.""")

    print("\n  PASS 5641 -- alpha(W(3,9)) is still open\n")
    print("    W(3,9): 820 points, 820 lines of size 10, Hoffman bound 82")
    print("""
    THE CLIQUE RUN DIED ON A BUG, not on time: a KeyError building the line-to-index map,
    because the point enumeration and the line enumeration disagreed on which points
    existed. The earlier edge-constraint run burned 70,483s to an unproved incumbent of
    49. So the honest state is: 82 is the bound, 49 is the best construction I have, and
    the gap is not closed. Reporting it as open rather than carrying the incumbent
    forward as though it were a result.""")

    print("\n  PASS 5642 -- my own guards on my own passes\n")
    for g, n in GUARDS.items():
        print(f"    {g:32s} {n} finding(s) in 28 files")
    print("""
    TWO FINDINGS IN 28 FILES, AND I HAD NEVER RUN THEM ON MYSELF. Nine guards built this
    session, all self-tested against known-bad inputs, none ever pointed at my own output.
    The spectral-overreach guard is clean; the other two each flag one file. That is a
    low rate, but the number I should have had before proposing the guards to the other
    lane was this one, not the self-test pass rate.""")

    out = {
        "boundary": (
            "Pass 5638 refutes an ARCHITECTURAL claim, not the flag arithmetic: "
            "192 = (2+7+7) x 12 = 24+84+84 stands. The codec adjacencies used are the "
            "ones the 2026-05-29 file names (Csaszar vertex-adjacency, Szilassi "
            "face-adjacency); both are K7 and that is what obstructs. Pass 5639 kills a "
            "numerical coincidence on transitivity, which does not bear on any other "
            "192 in the corpus. Pass 5641 reports alpha(W(3,9)) OPEN -- 49 is an "
            "unproved incumbent against a bound of 82"),
        "pass_5635": {**AB,
                      "finding": ("the routing blocklist moved 2 certificates of 5,056; "
                                  "the 60/68/70 sequence was three corpora, not a trend")},
        "pass_5636": {"router_files": ROUTER_FILES, "corpus": AB["corpus"],
                      "root_cause": ("all three recalibrations ranked TOKENS and measured "
                                     "FILES; router stems carry many tokens across 0.2% "
                                     "of files, so suppressing them cannot move a "
                                     "per-file rate")},
        "pass_5637": {"stems_by_file_hits": STEMS_BY_FILE,
                      "surfaced": ("tomotope_flag is the second-largest hub by file-hits "
                                   "-- 939 across 63 certificates -- and was invisible "
                                   "under token ranking")},
        "pass_5638": {"source": "analysis/2026-05-29_flag_codec_toroidal_hypercube_boundary.md",
                      "open_since": "2026-05-29",
                      "codec_split": [2, 7, 7], "codec_size": 12, "flags": 192,
                      "codec_graph_bipartite": nx.is_bipartite(G),
                      "codec_graph_triangles": sum(nx.triangles(G).values()) // 3,
                      "codec_graph_degrees": sorted(set(dict(G.degree()).values())),
                      "isomorphic_to_q4": nx.is_isomorphic(G, Q),
                      "verdict": ("NEGATIVE -- Csaszar and Szilassi adjacencies are each "
                                  "K7; Q4 is bipartite and triangle-free. Invariant "
                                  "under every assignment"),
                      "survives": "192 = 16 x 12 = 24 + 84 + 84, the flag arithmetic"},
        "pass_5639": {"rot_q4": 192, "tomotope_flags": 192,
                      "flag_partition": [24, 84, 84],
                      "verdict": ("distinct -- a regular action of an order-192 group is "
                                  "transitive, and 24+84+84 is an Aut-invariant "
                                  "partition into unequal parts"),
                      "coincidence_number": 9},
        "pass_5640": {"certificate": "bt1371_q6_tomotope_explicit_orbit_address_table.json",
                      "rows": 192, "group_order": 96, "orbits": [96, 96],
                      "reading": ("two torsors under an order-96 group, never one torsor "
                                  "under an order-192 group -- an independent refutation "
                                  "already committed"),
                      "confirms": "the DCCLXXXIV errata: 96 is the polytope's group"},
        "pass_5641": {"q": 9, "points": 820, "lines": 820, "line_size": 10,
                      "hoffman": 82, "incumbent": 49, "proved": False,
                      "status": "OPEN",
                      "why": ("the clique-constraint run died on a point-index KeyError, "
                              "not on time; the prior edge run spent 70,483s unproved")},
        "pass_5642": {"guards": GUARDS, "files": 28,
                      "finding": ("nine guards built this session, none previously run on "
                                  "my own output; two findings in 28 files")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5635_5642_SIXTEEN_CODECS_NOT_A_HYPERCUBE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
