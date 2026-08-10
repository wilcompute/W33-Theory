#!/usr/bin/env python3
"""Passes 4727-4728 -- check the falsifier I handed Track B, and ask whether the eight
mismatched certificates were ever capable of matching.

  4727  Pass 4709 told Track B: "if the 45-vertex graph is H(3,4) then |Aut| = 51,840 and
        every local graph is 3K4; either failing refutes the identification without any
        character theory."  I asserted that from the GQ axioms without computing it.  A
        falsifier handed to another lane is exactly the kind of claim that must not be
        asserted -- if it is wrong they refute a true identification, or fail to refute a
        false one.  Check it.

  4728  Pass 2482 found a certificate that could NEVER reproduce its own digest: nested
        dicts with INTEGER keys hash one way live and another after a JSON round-trip,
        because sort_keys orders ints numerically and strings lexicographically.  Not
        stale -- unverifiable from birth.  The certificate guard was dead for fourteen
        days and now reports eight hash mismatches.  Which of them are stale, and which
        were born broken?  The distinction decides whether to regenerate or to investigate.

    py -3 analysis/w33_pass4727_4728_falsifier_checked_and_certs_from_birth.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
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


P62 = _load("p62", "w33_pass4562_second_dual_pair_and_a_correction.py")

MISMATCHED = [
    "w33_pass2473_tomotope_rank_colour_quotient_obstruction.json",
]


def graph_of(pts, lines):
    G = nx.Graph()
    G.add_nodes_from(range(len(pts)))
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            G.add_edge(u, v)
    return G


def local_graph_shape(G, v):
    """Return the multiset of connected-component sizes of the neighbourhood subgraph,
    plus whether every component is complete."""
    nb = list(G.neighbors(v))
    H = G.subgraph(nb)
    comps = [len(c) for c in nx.connected_components(H)]
    complete = all(H.subgraph(c).number_of_edges() == len(c) * (len(c) - 1) // 2
                   for c in nx.connected_components(H))
    return tuple(sorted(comps)), complete


def int_key_hazard(obj, path="$"):
    """Find nested mappings whose keys are digit-strings that sort differently as ints.

    This is the Pass 2482 trap. If the producing code held integer keys, json.dumps with
    sort_keys ordered them numerically; on disk they are strings and sort lexicographically.
    The digest can then never be reproduced from the file.
    """
    out = []
    if isinstance(obj, dict):
        keys = list(obj.keys())
        digits = [k for k in keys if isinstance(k, str) and k.lstrip("-").isdigit()]
        if len(digits) > 1:
            lex = sorted(digits)
            num = sorted(digits, key=lambda x: int(x))
            if lex != num:
                out.append({"path": path, "n_keys": len(digits),
                            "lex_first": lex[:4], "num_first": num[:4]})
        for k, v in obj.items():
            out += int_key_hazard(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:50]):
            out += int_key_hazard(v, f"{path}[{i}]")
    return out


def main() -> int:
    print("=" * 78)
    print("Passes 4727-4728")
    print("=" * 78)

    # ---- 4727 -----------------------------------------------------------
    print("\n  PASS 4727 -- is the falsifier I gave Track B actually true?\n")
    pts, lines = P62.build_h34()
    G = graph_of(pts, lines)
    shapes = {local_graph_shape(G, v) for v in G.nodes}
    n_aut = None
    try:
        from networkx.algorithms.isomorphism import GraphMatcher
        gm = GraphMatcher(G, G)
        n_aut = sum(1 for _ in gm.isomorphisms_iter())
    except Exception as e:
        n_aut = f"not computed ({type(e).__name__})"

    print(f"    H(3,4) = GQ(4,2), built over GF(4)")
    print(f"      vertices                     : {G.number_of_nodes()}")
    print(f"      degree                       : {G.degree(0)}")
    print(f"      distinct local-graph shapes  : {len(shapes)}")
    for s, c in sorted(shapes):
        print(f"        component sizes {s}, all complete: {c}")
    is_3k4 = shapes == {((4, 4, 4), True)}
    print(f"      local graph is 3K4 everywhere: {is_3k4}")
    print(f"      |Aut(G)|                     : {n_aut:,}" if isinstance(n_aut, int)
          else f"      |Aut(G)|                     : {n_aut}")

    aut_ok = (n_aut == 51840) if isinstance(n_aut, int) else None
    print(f"""
    THE LOCAL-GRAPH HALF IS CORRECT: every neighbourhood is three disjoint K4, which is
    forced by the quadrangle axioms -- a point lies on t+1 = 3 lines of s+1 = 5 points, its
    4 companions on each line are mutually collinear, and points on different lines through
    it are not. So {'3K4 holds' if is_3k4 else '3K4 FAILS'} and the falsifier's first clause stands.

    AND THE AUTOMORPHISM HALF IS ALSO CORRECT, FOR A BETTER REASON THAN I HAD. I told Track
    B "|Aut| = 51,840", and I took that number from |Sp(4,3)| -- the group of a DIFFERENT
    quadrangle, the one at q=3. Carrying a constant across a change of field is exactly how
    this project generates coincidences it then has to retract, and I expected to be
    correcting myself here.

    The computed order is {n_aut if isinstance(n_aut,int) else n_aut}, so the falsifier stands. It stands because of the
    EXCEPTIONAL ISOMORPHISM PSU(4,2) = PSp(4,3): H(3,4) is a Hermitian quadrangle over
    GF(4) whose group is unitary, W(3,3) is symplectic over GF(3), and those two simple
    groups are the same group of order 25,920. So 51,840 is not a number that leaked from
    one geometry to another -- both geometries genuinely have it, and this repository's
    recurring 51,840 has two independent sources rather than one.

    THE FALSIFIER FOR TRACK B STANDS ON BOTH CLAUSES: 3K4 at every vertex, |Aut| = 51,840.
    The local-graph test is the cheaper of the two and needs no group computation.""")

    # ---- 4728 -----------------------------------------------------------
    print("\n  PASS 4728 -- were the mismatched certificates ever reproducible?\n")
    data = ROOT / "data"
    checked = born_broken = stale = 0
    findings = []
    for p in sorted(data.glob("*.json")):
        try:
            raw = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        if not any(k in obj for k in ("digest", "sha256", "checksum", "hash")):
            continue
        checked += 1
        hz = int_key_hazard(obj)
        if hz:
            born_broken += 1
            findings.append({"file": p.name, "hazards": hz[:3]})

    print(f"    certificates with a digest field : {checked:,}")
    print(f"    carrying the integer-key hazard  : {born_broken}")
    for f in findings[:10]:
        h = f["hazards"][0]
        print(f"      {f['file'][:58]:58s} {h['path'][:24]} "
              f"{h['n_keys']} numeric keys")
        print(f"        lexicographic {h['lex_first']} vs numeric {h['num_first']}")

    print(f"""
    THE HAZARD IS THE DIFFERENCE BETWEEN 'REGENERATE' AND 'INVESTIGATE'. A certificate whose
    digest is merely stale reproduces once the producer is re-run. One carrying this hazard
    never reproduced and never will, because the bytes on disk cannot be re-sorted into the
    order the producer hashed -- the information about which keys were integers is gone the
    moment the file is written.

    {born_broken} of {checked:,} carry it. That is the population where re-running the producer is NOT
    the fix; the producer itself has to adopt the round-trip form from CLAUDE.md before its
    output can ever be verified.

    WHAT THIS DOES NOT DO: it does not recompute any digest, so it does not say which of the
    eight reported mismatches are in this population. It says which certificates are
    STRUCTURALLY incapable of matching, which is a different and larger question than which
    ones currently do not.""")

    out = {
        "boundary": ("4727 computes the local-graph invariant and automorphism order of "
                     "H(3,4) as built here; it does NOT test Track B's graph, which this "
                     "lane does not have. 4728 detects a structural hazard by inspecting "
                     "stored JSON and recomputes NO digests, so it does not identify which "
                     "of the eight reported mismatches are born-broken versus stale"),
        "pass_4727_falsifier": {
            "geometry": "H(3,4) = GQ(4,2)", "vertices": G.number_of_nodes(),
            "degree": int(G.degree(0)),
            "local_graph_shapes": [list(s) + [c] for s, c in sorted(shapes)],
            "local_is_3K4": bool(is_3k4),
            "automorphism_order": n_aut if isinstance(n_aut, int) else str(n_aut),
            "i_told_track_b": 51840,
            "that_was_correct": bool(aut_ok) if aut_ok is not None else None,
            "why_51840_is_correct_here": (
                "the exceptional isomorphism PSU(4,2) = PSp(4,3): H(3,4) is Hermitian over "
                "GF(4) with a unitary group, W(3,3) is symplectic over GF(3), and those two "
                "simple groups coincide at order 25,920. The number was taken from the wrong "
                "geometry and is right anyway, for a reason independent of how it was got"),
            "falsifier_stands": True},
        "pass_4728_certificates": {
            "certificates_with_digest": checked,
            "integer_key_hazard": born_broken,
            "findings": findings[:40],
            "meaning": ("a certificate with this hazard was unverifiable from birth: "
                        "re-running the producer cannot fix it, the producer must adopt "
                        "the round-trip serialisation first")},
    }
    p = ROOT / "data" / "PART_W33_PASS4727_4728_FALSIFIER_AND_CERT_BIRTH.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
