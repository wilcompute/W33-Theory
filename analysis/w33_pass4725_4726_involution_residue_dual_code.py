#!/usr/bin/env python3
"""Passes 4725--4726: the 270 involution residues are the complete H10-dual minimum shell.

4725. Let A_* be the W33 line-intersection adjacency matrix over F2 and let K be
      the span of the 270 four-line residues from Passes 4721--4724. Every
      residue lies in ker(A_*), the residues have rank 30, and rank(A_*)=10.
      Hence

          K = ker(A_*) = im(A_*)^perp,

      a canonical [40,30,4] binary code. Exhaustion of all subsets of sizes
      1,2,3,4 proves that its complete minimum shell consists of exactly the
      270 residue/involution fixed-line masks.

4726. The protected H10 code is im(A_*). Therefore the 270 inner involution
      residues are exactly the complete minimum parity-check shell of H10 and
      reconstruct H10 by orthogonality. Enumerating the 2^10 H10 words and
      applying the binary MacWilliams transform gives the complete weight
      enumerator of K without enumerating 2^30 words.

No representation or physical label is inferred beyond these exact code
identities.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4725_4726_INVOLUTION_RESIDUE_DUAL_CODE.json"


def gf2_basis(masks):
    piv = {}
    for x in masks:
        y = int(x)
        while y:
            p = y.bit_length() - 1
            if p in piv:
                y ^= piv[p]
            else:
                piv[p] = y
                break
    return [piv[p] for p in sorted(piv, reverse=True)]


def gf2_rank(masks):
    return len(gf2_basis(masks))


def row_masks(A):
    return [sum((int(A[i, j]) & 1) << j for j in range(A.shape[1])) for i in range(A.shape[0])]


def mat_vec_zero_mod2(A, mask):
    for i in range(A.shape[0]):
        parity = 0
        row = A[i]
        for j in range(A.shape[1]):
            if ((mask >> j) & 1) and int(row[j]):
                parity ^= 1
        if parity:
            return False
    return True


def thickening(apartment, lines):
    corners = set()
    for i, j in itertools.combinations(apartment, 2):
        z = lines[i] & lines[j]
        if z:
            corners |= z
    assert len(corners) == 4
    out = frozenset(i for i, line in enumerate(lines) if line & corners)
    assert len(out) == 12
    return out


def residue_shell(lines, apartments):
    tmasks = [sum(1 << i for i in thickening(ap, lines)) for ap in apartments]
    assert len(set(tmasks)) == 1620
    nbr = [[] for _ in range(1620)]
    for i in range(1620):
        for j in range(i + 1, 1620):
            if tmasks[i] & tmasks[j] == 0:
                nbr[i].append(j)
                nbr[j].append(i)
    assert set(map(len, nbr)) == {2}
    seen = set()
    residues = []
    all40 = (1 << 40) - 1
    for seed in range(1620):
        if seed in seen:
            continue
        comp = {seed}
        stack = [seed]
        seen.add(seed)
        while stack:
            u = stack.pop()
            for v in nbr[u]:
                if v not in seen:
                    seen.add(v)
                    comp.add(v)
                    stack.append(v)
        assert len(comp) == 3
        union = 0
        for i in comp:
            union |= tmasks[i]
        residues.append(all40 ^ union)
    counts = Counter(residues)
    assert len(counts) == 270 and set(counts.values()) == {2}
    return sorted(counts)


def enumerate_code_from_basis(basis):
    words = Counter()
    n = len(basis)
    for selector in range(1 << n):
        w = 0
        for i, b in enumerate(basis):
            if (selector >> i) & 1:
                w ^= b
        words[w.bit_count()] += 1
    return dict(sorted(words.items()))


def krawtchouk(n, j, w):
    lo = max(0, j - (n - w))
    hi = min(j, w)
    return sum((-1) ** s * math.comb(w, s) * math.comb(n - w, j - s) for s in range(lo, hi + 1))


def macwilliams_binary(primal, n, k):
    dual = {}
    denom = 1 << k
    for j in range(n + 1):
        num = sum(count * krawtchouk(n, j, w) for w, count in primal.items())
        assert num % denom == 0
        coeff = num // denom
        if coeff:
            dual[j] = coeff
    return dual


def main() -> int:
    _pts, _pidx, lines, astar, apartments, _apmasks, _H = geometry()
    residues = residue_shell(lines, apartments)
    assert len(residues) == 270 and set(r.bit_count() for r in residues) == {4}

    arows = row_masks(astar)
    rank_a = gf2_rank(arows)
    rank_r = gf2_rank(residues)
    assert rank_a == 10
    assert rank_r == 30
    assert all(mat_vec_zero_mod2(astar, r) for r in residues)
    # Inclusion plus equal dimensions proves span(residues)=ker(A_*).
    assert 40 - rank_a == rank_r

    # Exhaust all candidate words below and at weight four; this is cheap and
    # turns the 270 orbit into the complete minimum shell, not merely a subset.
    low = {}
    low_weight4 = set()
    for w in range(1, 5):
        count = 0
        for sub in itertools.combinations(range(40), w):
            mask = sum(1 << i for i in sub)
            if mat_vec_zero_mod2(astar, mask):
                count += 1
                if w == 4:
                    low_weight4.add(mask)
        low[w] = count
    assert low == {1: 0, 2: 0, 3: 0, 4: 270}
    assert low_weight4 == set(residues)

    # H10 = im(A_*), because A_* is symmetric; K=ker(A_*)=H10^perp.
    h10_basis = gf2_basis(arows)
    assert len(h10_basis) == 10
    h10_enum = enumerate_code_from_basis(h10_basis)
    expected_h10 = {0: 1, 12: 40, 16: 135, 20: 672, 24: 135, 28: 40, 40: 1}
    assert h10_enum == expected_h10
    assert sum(h10_enum.values()) == 1 << 10

    dual_enum = macwilliams_binary(h10_enum, 40, 10)
    expected_dual = {
        0: 1,
        4: 270,
        6: 6720,
        8: 152685,
        10: 1651392,
        12: 10921000,
        14: 45288000,
        16: 122873490,
        18: 221227200,
        20: 269500308,
        22: 221227200,
        24: 122873490,
        26: 45288000,
        28: 10921000,
        30: 1651392,
        32: 152685,
        34: 6720,
        36: 270,
        40: 1,
    }
    assert dual_enum == expected_dual
    assert sum(dual_enum.values()) == 1 << 30

    # The all-one vector lies in K (A_* has even row degree 12), explaining the
    # symmetric weight-4/weight-36 minimum/complement shells.
    all_one = (1 << 40) - 1
    assert mat_vec_zero_mod2(astar, all_one)
    assert {all_one ^ r for r in residues} == {
        w for w in [all_one ^ r for r in residues] if w.bit_count() == 36
    }

    out = {
        "passes": [4725, 4726],
        "4725_kernel_code": {
            "length": 40,
            "rank_Astar_F2": 10,
            "residue_span_dimension": 30,
            "identity": "span_F2(270 involution residue masks) = ker_F2(A_*) = im_F2(A_*)^perp",
            "parameters": "[40,30,4]",
            "low_weight_kernel_census": {str(k): v for k, v in low.items()},
            "minimum_shell_size": 270,
            "minimum_shell": "exactly the 270 four-line fixed sets of the inner involution class",
        },
        "4726_H10_dual_reconstruction": {
            "H10": "im_F2(A_*)",
            "H10_parameters": "[40,10,12]",
            "H10_weight_enumerator": {str(k): v for k, v in h10_enum.items()},
            "dual_code": "H10^perp = ker_F2(A_*)",
            "dual_parameters": "[40,30,4]",
            "dual_weight_enumerator": {str(k): v for k, v in dual_enum.items()},
            "minimum_parity_checks": 270,
            "reconstruction": "H10 is the common orthogonal kernel of the 270 minimum residue checks",
            "all_one_in_dual": True,
            "complement_shell": "the complements of the 270 weight-4 residues are the 270 weight-36 words",
        },
        "theorem": "The old 270 inner-involution fixed-line orbit is exactly the complete weight-4 shell of the canonical dual H10^perp=[40,30,4]. Equivalently, the 270 involutions are the complete minimum parity-check shell that reconstructs the protected H10=im(A_*) code.",
        "boundary": "Exact binary coding and W33 incidence. The equality is proved by annihilation plus dimension and by exhaustive weight-1..4 census; the full dual enumerator follows from the exact 2^10 H10 enumerator via MacWilliams. No physical meaning is inferred from the code duality.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
