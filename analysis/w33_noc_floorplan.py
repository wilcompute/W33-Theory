#!/usr/bin/env python3
"""
The floorplan: the bisection is exactly 100, so the fabric is non-planar -- it wants light, not wires.
A topology is only as good as it is buildable, so this pass stress-tests the GQ(3,3) fabric as a
physical layout. The decisive number is the BISECTION WIDTH -- the minimum number of links cut to
split the 40 nodes into two halves of 20 -- because it sets both the bandwidth across the machine and,
by Thompson's VLSI theorem, the chip area. For GQ(3,3) it is EXACTLY 100: the spectral lower bound
(n/4)(k - lambda_2) = (40/4)(12 - 2) = 100 is met by an explicit balanced cut of 100 edges (found
here by spectral + Kernighan-Lin partitioning), so the minimum bisection equals the spectral bound,
100. That is enormous -- 100 of the 240 links (42 percent) cross any halving -- so the machine has
huge cross-sectional bandwidth, the hallmark of a good expander. But the SAME number is the cost: by
Thompson's lower bound a 2-D layout needs area at least ~(bisection/2)^2 ~ 2500 wire-crossing units,
and more sharply, a graph with bisection growing like its size cannot be laid out in the plane with
short wires -- an expander is intrinsically NON-PLANAR. Compared at the same scale, a 6x6 torus has
bisection 12 (cheap, planar, but diameter 6) and a hypercube Q6 has bisection 32; GQ(3,3)'s 100 buys
its diameter-2 all-to-all reach at the price of a wiring that does not fit flat. The resolution is the
substrate's own: a high-bisection, non-planar fabric is exactly what a PHOTONIC realisation is for --
light routed in 3-D / free space (or in wavelength) has no planar wire-crossing penalty, so the
optical Holonet is not a convenience but a NECESSITY forced by the bisection. So the floorplan verdict
is: bisection exactly 100 (spectral-optimal), 42 percent of all links across any cut -- a maximally
fat, non-planar fabric whose natural medium is photonic, not 2-D wires.

This stress-tests the GQ(3,3) interconnect as a physical floorplan: it computes the exact bisection
width, the Thompson VLSI area bound, and the resulting non-planarity that forces a photonic medium.

THE FLOORPLAN.
    bisection width      EXACTLY 100: spectral lower bound (n/4)(k - lambda_2) = 10 * 10 = 100, met by
                         an explicit balanced 20|20 cut of 100 edges (spectral + Kernighan-Lin).
    cross-section        100 / 240 = 42% of all links cross any halving -> maximal expander bandwidth.
    Thompson area bound  A >= ~(bisection/2)^2 ~ 2500 wire-crossing units -> expensive in 2-D.
    planarity            bisection ~ size -> NON-PLANAR (an expander cannot be laid out flat short-wire).
    comparison           6x6 torus bisection 12 (planar, diam 6); Q6 bisection 32; GQ(3,3) 100.
    resolution           non-planar high-bisection fabric -> PHOTONIC realisation (3-D / free-space /
                         wavelength routing has no planar crossing penalty) is forced, not optional.

Honest scope: the bisection width is computed EXACTLY here -- the spectral lower bound (n/4)(k-lambda_2)
= 100 (a standard d-regular eigenvalue bound) is matched by an explicit cut of 100 found by spectral +
Kernighan-Lin refinement, so 100 is both a lower and an achieved upper bound. The Thompson area bound
A = Omega(bisection^2) and "expanders are non-planar" are standard VLSI / graph theory. The reading
that this forces a photonic medium is an engineering inference (light avoids the planar wire-crossing
penalty), consistent with the corpus's optical Holonet. So: an exact bisection of 100 and the
non-planarity it implies.

Verifies the spectral eigenvalues {12, 2, -4}, the bisection lower bound 100, an explicit balanced cut
achieving 100, the cross-section fraction, and the Thompson area / non-planarity verdict.
"""
from __future__ import annotations

import itertools
import json
import random

import numpy as np


def build_gq33():
    inv = {1: 1, 2: 2}

    def norm(v):
        for c in v:
            if c != 0:
                return tuple((x * inv[c]) % 3 for x in v)

    pts = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})

    def B(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3

    n = len(pts)
    A = np.zeros((n, n), int)
    for i, p in enumerate(pts):
        for j, q in enumerate(pts):
            if i != j and B(p, q) == 0:
                A[i, j] = 1
    return A


def cut_size(A, part):
    n = A.shape[0]
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] and part[i] != part[j]:
                s += 1
    return s


def kl_refine(A, part):
    """Balanced Kernighan-Lin: repeatedly swap a 0/1 pair that most reduces the cut."""
    n = A.shape[0]
    part = part.copy()
    improved = True
    while improved:
        improved = False
        zeros = [i for i in range(n) if part[i] == 0]
        ones = [i for i in range(n) if part[i] == 1]
        best_gain, best_swap = 0, None
        base = cut_size(A, part)
        for a in zeros:
            for b in ones:
                part[a], part[b] = 1, 0
                gain = base - cut_size(A, part)
                part[a], part[b] = 0, 1
                if gain > best_gain:
                    best_gain, best_swap = gain, (a, b)
        if best_swap:
            a, b = best_swap
            part[a], part[b] = 1, 0
            improved = True
    return part


def main():
    out = {}
    A = build_gq33()
    n = A.shape[0]
    k = int(A.sum(1)[0])
    m = int(A.sum()) // 2
    ev = sorted(np.linalg.eigvalsh(A.astype(float)))
    from collections import Counter

    spec = Counter(int(round(x)) for x in ev)
    lam2 = sorted({round(x, 6) for x in ev})[-2]
    print(
        "== the floorplan: bisection exactly 100 -> non-planar, wants light not wires =="
    )
    print(
        f"  n = {n}, radix k = {k}, links |E| = {m}; spectrum = {dict(spec)} (lambda_2 = {lam2:.0f})"
    )

    # spectral lower bound on bisection
    lb = (n / 4) * (k - lam2)
    print(
        f"\n[bisection]  spectral lower bound (n/4)(k - lambda_2) = ({n}/4)({k} - {lam2:.0f}) = {lb:.0f}"
    )

    # explicit cut: spectral (Fiedler) + Kernighan-Lin, with random restarts
    L = np.diag(A.sum(1)) - A
    w, V = np.linalg.eigh(L)
    order = np.argsort(V[:, 1])
    part = np.zeros(n, int)
    for idx in order[n // 2 :]:
        part[idx] = 1
    part = kl_refine(A, part)
    best = cut_size(A, part)
    random.seed(0)
    for _ in range(30):
        idx = list(range(n))
        random.shuffle(idx)
        p = np.zeros(n, int)
        for i in idx[n // 2 :]:
            p[i] = 1
        p = kl_refine(A, p)
        best = min(best, cut_size(A, p))
    print(f"  best explicit balanced 20|20 cut found = {best} edges")
    print(
        f"  -> minimum bisection = {best} (lower bound {lb:.0f} met) : SPECTRAL-OPTIMAL"
    )
    assert best == int(lb) == 100
    frac = best / m
    print(
        f"  cross-section: {best} / {m} = {frac:.1%} of all links cross any halving (fat expander)"
    )
    out["bisection"] = {
        "spectral_lower_bound": int(lb),
        "formula": "(n/4)(k - lambda_2) = (40/4)(12 - 2) = 100",
        "explicit_cut": best,
        "minimum_bisection": best,
        "is_optimal": True,
        "cross_section_fraction": round(frac, 3),
        "links_total": m,
    }

    # Thompson VLSI area bound + planarity
    area = (best / 2) ** 2
    print(
        f"\n[layout]  Thompson VLSI: 2-D area A >= ~(bisection/2)^2 = {area:.0f} wire-crossing units"
    )
    print(
        f"  bisection ~ size -> NON-PLANAR: an expander cannot be laid out flat with short wires"
    )
    print(
        f"  -> a PHOTONIC realisation (3-D / free-space / wavelength routing) avoids the planar"
    )
    print(
        f"     crossing penalty: the optical Holonet is forced by the bisection, not optional"
    )
    out["layout"] = {
        "thompson_area_bound": area,
        "thompson_note": "A = Omega(bisection^2); ~(B/2)^2 ~ 2500 wire-crossing units",
        "planarity": "non-planar (bisection grows with size -> no short-wire planar layout)",
        "resolution": "photonic / 3-D / free-space / wavelength routing has no planar crossing penalty -> optical Holonet forced",
    }

    comparison = [
        (
            "GQ(3,3)",
            40,
            12,
            2,
            100,
            "diameter-2 all-to-all reach; non-planar; photonic",
        ),
        ("hypercube Q6", 64, 6, 6, 32, "moderate bisection, higher diameter"),
        ("6x6 torus", 36, 4, 6, 12, "planar, cheap wiring, high diameter"),
    ]
    print(
        f"\n[comparison]  {'topology':14s} {'nodes':>5s} {'radix':>5s} {'diam':>4s} {'bisect':>6s}  note"
    )
    rows = []
    for name, nn, rr, dd, bb, note in comparison:
        rows.append(
            {
                "topology": name,
                "nodes": nn,
                "radix": rr,
                "diameter": dd,
                "bisection": bb,
                "note": note,
            }
        )
        print(f"  {name:14s} {nn:5d} {rr:5d} {dd:4d} {bb:6d}  {note}")
    out["comparison"] = rows

    print(
        "\nRESULT: the floorplan verdict is that the fabric is maximally fat and non-planar. The"
    )
    print(
        "  bisection width -- the minimum links cut to split the 40 nodes into two halves of 20 --"
    )
    print(
        "  is EXACTLY 100: the spectral lower bound (n/4)(k - lambda_2) = (40/4)(12 - 2) = 100 is met"
    )
    print(
        "  by an explicit balanced cut of 100 edges, so the minimum bisection equals the spectral"
    )
    print(
        "  bound. That is 100 of the 240 links (42%) across any halving -- huge cross-sectional"
    )
    print(
        "  bandwidth, the hallmark of a good expander. But the same number is the cost: by Thompson's"
    )
    print(
        "  VLSI theorem a 2-D layout needs area >= ~(bisection/2)^2 ~ 2500 wire-crossing units, and a"
    )
    print(
        "  graph whose bisection grows with its size is intrinsically non-planar -- an expander does"
    )
    print(
        "  not fit flat with short wires. Against a 6x6 torus (bisection 12, planar, diameter 6) or a"
    )
    print(
        "  hypercube Q6 (bisection 32), GQ(3,3)'s 100 buys its diameter-2 all-to-all reach at the"
    )
    print(
        "  price of a non-planar wiring. The resolution is the substrate's own: a high-bisection,"
    )
    print(
        "  non-planar fabric is exactly what a PHOTONIC realisation is for -- light routed in 3-D /"
    )
    print(
        "  free space (or in wavelength) has no planar crossing penalty -- so the optical Holonet is"
    )
    print(
        "  forced by the bisection, not a convenience. Honest: the bisection 100 is computed exactly"
    )
    print(
        "  (spectral bound met by an explicit cut); Thompson's area bound and expander non-planarity"
    )
    print("  are standard; the photonic-medium inference is the engineering reading.")

    out["summary"] = (
        "the floorplan: the bisection is exactly 100, so the fabric is non-planar -- it wants light, "
        "not wires. The bisection width (min links cut to split 40 nodes into 20|20) is EXACTLY 100: "
        "the spectral lower bound (n/4)(k - lambda_2) = (40/4)(12-2) = 100 is met by an explicit "
        "balanced cut of 100 edges (spectral + Kernighan-Lin), so minimum bisection = spectral bound = "
        "100 -- 100 of the 240 links (42%) cross any halving, the hallmark of a good expander (huge "
        "cross-section bandwidth). The same number is the cost: Thompson's VLSI theorem gives 2-D area "
        ">= ~(bisection/2)^2 ~ 2500 wire-crossing units, and a graph whose bisection grows with size is "
        "intrinsically NON-PLANAR (an expander cannot be laid out flat with short wires). Vs a 6x6 "
        "torus (bisection 12, planar, diameter 6) or hypercube Q6 (bisection 32), GQ(3,3)'s 100 buys "
        "diameter-2 all-to-all reach at the price of non-planar wiring. Resolution: a high-bisection "
        "non-planar fabric is exactly what a PHOTONIC realisation is for -- light in 3-D / free space / "
        "wavelength has no planar crossing penalty -- so the optical Holonet is FORCED by the "
        "bisection, not optional. HONEST: the bisection 100 is computed exactly (spectral bound met by "
        "an explicit cut, so both a lower and achieved upper bound); Thompson's area bound and expander "
        "non-planarity are standard VLSI/graph theory; the photonic-medium inference is the engineering "
        "reading, consistent with the corpus optical Holonet."
    )
    out["sources"] = [
        "GQ(3,3) = SRG(40,12,2,4), spectrum {12, 2^24, -4^15}; spectral bisection bound (n/4)(k - "
        "lambda_2) for d-regular graphs (standard); Kernighan-Lin partitioning; Thompson VLSI area "
        "lower bound A = Omega(bisection^2); expanders are non-planar (Lipton-Tarjan planar separator "
        "is O(sqrt n), expanders have Omega(n)); optical Holonet realisation (corpus)."
    ]
    with open("data/w33_noc_floorplan.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_noc_floorplan.json")


if __name__ == "__main__":
    main()
