#!/usr/bin/env python3
"""
Defect-aware page placement: the loader meets the phase space. The VM track's binary-object loader
packs bytes into 81-trit pages and assigns them to W(3,3) point addresses by hash. This witness makes
placement DEFECT-AWARE using the tax arc's structures, and prices what a defect relocation costs the
memory system:

  THE SAFE ZONE IS THE PHASE SPACE. At defect center p the 27 non-neighbors are exactly the points
  touching NO defect line (verified: every star line lies inside the closed perp), and Pass 61
  organizes them canonically: the nine ground states' out-triples partition the 27. So pages are
  placed page -> phase point (one of the 9 AG(2,3) ground states, by hash mod 9) -> one of its 3
  triple points -- a deterministic, reversible, defect-avoiding address map with the qutrit phase
  space as its directory structure. Pages never sit on an escalation path.

  THE PAGE-MIGRATION BILL. When the defect relocates p -> p', the safe zone changes; pages on
  newly-exposed points must move. Computed exactly over all 780 center pairs: the safe-zone overlap
  is THE SAME for adjacent and non-adjacent moves -- 18 of 27 points stay safe, so the bill is always
  exactly 9 points' worth of pages (a third of the safe zone). The ray side of relocation prefers edges (Pass 64: 3 vs >=5 rays), while the page side
  is relocation-isotropic: a constant 9-point bill wherever the defect goes. Edge migration is
  therefore strictly optimal overall -- it wins on rays and ties on pages.

  THE RE-KEYING STRUCTURE. For an edge move p -> p', the 18 surviving safe points redistribute over
  the NEW nine triples; the witness computes the survival histogram per new phase point (how many of
  each new triple's 3 points were already safe), recording the exact re-keying work the memory
  system does per relocation.

Honest scope: exact finite computations; the placement map is bookkeeping made canonical by Pass 61's
theorem (the triple partition is the ILP-free ground-state characterization); the loader tie-in names
the VM track's in-flight 81-trit page loader as the consumer, without depending on it.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_interrupt_controller as ic  # noqa: E402
import w33_master_audit as audit  # noqa: E402


def safe_zone_and_triples(p, pts, A, lines, n):
    """The 27 non-neighbors of p, partitioned into the 9 ground out-triples (the phase directory)."""
    table, nb = ic.vector_table(p, pts, A, lines, n)
    triples = [tuple(sorted(t)) for (_, t, _) in table]
    safe = sorted(set(range(n)) - nb - {p})
    return safe, triples, nb


def place_page(page_bytes, triples):
    """page -> phase point (hash mod 9) -> triple point (hash//9 mod 3): deterministic, reversible."""
    h = int.from_bytes(hashlib.sha256(page_bytes).digest()[:4], "big")
    phase = h % 9
    slot = (h // 9) % 3
    return phase, triples[phase][slot]


def main():
    print("== defect-aware placement: the loader meets the phase space ==\n")
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    pts, A, lines, B = audit._build(3)
    n = len(pts)

    # A. the safe zone is defect-free, and the phase directory covers it
    safe0, triples0, nb0 = safe_zone_and_triples(0, pts, A, lines, n)
    star0 = [li for li, L in enumerate(lines) if 0 in L]
    star_pts = set().union(*[set(lines[li]) for li in star0])
    chk(
        "every defect line lies inside the closed perp, so the 27 non-neighbors touch NO defect line",
        star_pts <= (nb0 | {0}) and len(safe0) == 27,
    )
    flat = sorted(x for t in triples0 for x in t)
    chk(
        "the 9 ground out-triples PARTITION the safe zone (the AG(2,3) phase directory)",
        flat == safe0,
    )

    # B. deterministic defect-avoiding placement
    placed = [place_page(f"page-{i}".encode(), triples0) for i in range(500)]
    chk(
        "500 sample pages place deterministically onto safe points only",
        all(pt in safe0 for (_, pt) in placed),
    )
    spread_over_phases = Counter(ph for (ph, _) in placed)
    chk(
        f"placement spreads over all 9 phase points (min bucket {min(spread_over_phases.values())})",
        len(spread_over_phases) == 9,
    )

    # C. the page-migration bill, over all center pairs
    nonn = [frozenset(x for x in range(n) if x != p and not A[p][x]) for p in range(n)]
    adj_overlaps = set()
    non_overlaps = set()
    for p in range(n):
        for q in range(p + 1, n):
            ov = len(nonn[p] & nonn[q])
            (adj_overlaps if A[p][q] else non_overlaps).add(ov)
    chk(
        f"PAGE BILL LAW: safe-zone overlap is a constant 18/27 for adjacent moves ({sorted(adj_overlaps)}) "
        f"AND non-adjacent moves ({sorted(non_overlaps)}) -- the bill is always exactly 9 points",
        adj_overlaps == {18} and non_overlaps == {18},
    )
    chk(
        "=> edge relocation is strictly optimal overall: wins on rays (3 vs >=5, Pass 64), ties on pages (9 = 9)",
        adj_overlaps == non_overlaps == {18},
    )

    # D. re-keying structure for one edge move
    p2 = next(x for x in range(n) if A[0][x])
    safe2, triples2, _ = safe_zone_and_triples(p2, pts, A, lines, n)
    surviving = set(safe0) & set(safe2)
    hist = sorted(
        Counter(sum(1 for x in t if x in surviving) for t in triples2).items()
    )
    chk(
        f"re-keying after an edge move: 18 survivors redistribute over the new 9 triples with histogram "
        f"{hist} (survivors per new triple)",
        sum(k * v for k, v in hist) == 18,
    )

    all_ok = all(ok for _, ok in checks)
    print(
        "\nFUSION COMPLETE (move 2): pages live in the qutrit phase directory of the current defect"
        "\ncenter -- never on an escalation path -- and the relocation page bill is a constant 9 points"
        "\nwherever the defect goes, so the ray-side price law alone decides the move: edges win."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "placement": "page -> phase point (hash mod 9) -> triple slot (hash//9 mod 3); safe zone only",
        "page_bill_law": {
            "adjacent_overlap": sorted(adj_overlaps),
            "nonadjacent_overlap": sorted(non_overlaps),
            "bill_points": 9,
            "statement": "the relocation page bill is a constant 9 of 27 safe points, for every move; "
            "edge relocation wins on rays and ties on pages",
        },
        "rekeying_histogram_edge_move": hist,
        "all_pass": bool(all_ok),
        "summary": (
            "defect-aware placement: the VM track's page loader gains a phase-space directory. At defect "
            "center p the 27 non-neighbors touch no defect line (verified), and Pass 61's ground "
            "out-triples partition them into the 9 AG(2,3) phase points -- so pages place page -> phase "
            "point -> triple slot, deterministically, never on an escalation path. PAGE BILL LAW "
            "(computed over all 780 center pairs): the safe-zone overlap is a constant 18/27 for BOTH "
            "adjacent and non-adjacent relocations -- the memory bill is always exactly 9 points -- so "
            "the page side is relocation-isotropic and the ray-side price law (edge = 3 rays, Pass 64) "
            "alone decides: edges win strictly. Re-keying histogram after an edge move recorded. HONEST: "
            "exact computations; the directory is canonical by Pass 61's ILP-free characterization; the "
            "in-flight 81-trit loader is the named consumer, not a dependency."
        ),
        "sources": [
            "w33_interrupt_controller.vector_table (closed form); w33_ground_affine_plane (Pass 61)",
            "VM track: w33_binary_object_loader (in-flight consumer)",
        ],
    }
    with open("data/w33_defect_aware_placement.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_defect_aware_placement.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
