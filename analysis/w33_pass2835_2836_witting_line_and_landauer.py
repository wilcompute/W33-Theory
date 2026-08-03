#!/usr/bin/env python3
"""Passes 2835-2836 -- two questions from outside the current programme.

PASS 2835 -- WHAT IS M36, AS A PIECE OF THE MACHINE'S OWN ADDRESS SPACE?
    The 36 magic rays have been treated throughout as an external resource that the
    substrate happens to supply.  But the substrate's address space is the 40 points of
    W(3,3), and 40 - 36 = 4, and a LINE of W(3,3) has exactly 4 points.  That is either a
    coincidence or the whole story.

    The test is concrete.  Adjoin the four coordinate axes e_1..e_4 to the 36 rays and
    ask whether the orthogonality graph on the resulting 40 rays is SRG(40,12,2,4) -- the
    collinearity graph of W(3,3).  In a generalised quadrangle of order (3,3) the lines
    are exactly the 4-cliques, so if the four axes are mutually orthogonal they are a
    line, and

        M36 = the 40 points of W(3,3) with one line deleted.

    If that holds, magic is not an add-on: it is everything in the machine's address
    space except one line, and the deleted line is the stabilizer basis.

PASS 2836 -- WHAT DOES A SUPPORT READOUT COST, IN JOULES?
    The parallel track's Pass 2822 proves support is not an execution congruence and
    Pass 2825-2828 build a support observer.  Neither asks the thermodynamic question:
    a support readout is a many-to-one map on the state, so by Landauer it has a
    non-negotiable energy cost, and that cost is exactly computable because the fibres
    are exactly known.

    py -3 analysis/w33_pass2835_2836_witting_line_and_landauer.py
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, log2
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)


# ===========================================================================
def pass_2835() -> dict:
    print("=" * 78)
    print("Pass 2835 -- is M36 the complement of a LINE in W(3,3)?")
    print("=" * 78)

    w = [1, W, W ** 2]
    rays, tag = [], []
    for mu, nu in product(range(3), repeat=2):
        rays.append([0, 1, -w[mu], w[nu]]);       tag.append("A")
    for mu, nu in product(range(3), repeat=2):
        rays.append([1, 0, -w[mu], -w[nu]]);      tag.append("B")
    for mu, nu in product(range(3), repeat=2):
        rays.append([1, -w[mu], 0, w[nu]]);       tag.append("C")
    for mu, nu in product(range(3), repeat=2):
        rays.append([1, w[mu], w[nu], 0]);        tag.append("D")
    magic = [np.array(r, dtype=complex) / np.linalg.norm(r) for r in rays]

    # the four coordinate axes -- the computational basis, i.e. stabilizer states
    axes = [np.eye(4, dtype=complex)[i] for i in range(4)]
    for a in axes:
        tag.append("axis")
    allr = magic + axes
    n = len(allr)
    print(f"  36 magic rays + 4 coordinate axes = {n} rays")

    R = np.array(allr)
    G = np.abs(R.conj() @ R.T) ** 2
    adj = (G < 1e-9)                                   # orthogonality
    np.fill_diagonal(adj, False)

    deg = adj.sum(axis=1)
    print(f"  orthogonality degrees: {dict(Counter(deg.tolist()))}")

    reg = len(set(deg.tolist())) == 1 and deg[0] == 12
    lam, mu = set(), set()
    for i in range(n):
        for j in range(i + 1, n):
            common = int((adj[i] & adj[j]).sum())
            (lam if adj[i, j] else mu).add(common)
    print(f"  lambda values: {sorted(lam)}    mu values: {sorted(mu)}")

    is_srg = reg and len(lam) == 1 and len(mu) == 1
    params = (n, int(deg[0]), next(iter(lam)), next(iter(mu))) if is_srg else None
    if is_srg:
        print(f"\n  ORTHOGONALITY GRAPH IS SRG{params}")
        print(f"  W(3,3) collinearity graph is SRG(40, 12, 2, 4): "
              f"{params == (40, 12, 2, 4)}")
    else:
        print("\n  not strongly regular")

    # are the four axes a 4-clique, i.e. a line?
    axis_idx = list(range(36, 40))
    clique = all(adj[i, j] for i in axis_idx for j in axis_idx if i != j)
    print(f"\n  the four axes are mutually orthogonal (a 4-clique = a LINE): {clique}")

    # In a GQ(3,3) every point off a line is collinear with EXACTLY ONE point of it.
    # Check that, because it is the defining axiom and it is what makes the four
    # families A/B/C/D a geometric partition rather than a notational one.
    counts = Counter(int(sum(adj[p, a] for a in axis_idx)) for p in range(36))
    print(f"  each magic ray is orthogonal to exactly one axis: "
          f"{dict(counts) == {1: 36}}   ({dict(counts)})")

    fam = Counter()
    for p in range(36):
        a = next(a for a in axis_idx if adj[p, a])
        fam[a - 36] += 1
    print(f"  points per axis (the GQ 'nearest point' partition): {dict(fam)}")

    verdict = bool(is_srg and params == (40, 12, 2, 4) and clique and dict(counts) == {1: 36})
    if verdict:
        print("""
  M36 IS THE COMPLEMENT OF A SINGLE LINE IN W(3,3).

  The machine's address space is 40 points.  Four of them -- one line -- are the
  computational basis, which is exactly the stabilizer part.  THE OTHER THIRTY-SIX ARE
  ALL MAGIC.  Magic is not a resource bolted onto the substrate; it is the generic
  condition of the substrate's own address space, and the stabilizer states are the
  single distinguished line you have to delete to get rid of it.""")

    # How do the Clifford classes sit relative to the geometric families?
    print("\n  cross-tabulating the geometric families against the Clifford classes")
    print("  (Pass 2797 sizes [4, 8, 12, 12]):")
    fam_of = {p: next(a for a in axis_idx if adj[p, a]) - 36 for p in range(36)}
    fstab = None
    try:
        from math import isclose  # noqa: F401
        # rebuild the classes cheaply from the file-local geometry: rays in the same
        # class share a stabilizer fidelity, and the two 12-classes are distinguished by
        # the Pass 2797 orbit computation.  Here we only need the FAMILY tabulation,
        # which is basis-free, so report the family sizes and leave the join to the
        # certificate consumer.
        fstab = {k: v for k, v in sorted(Counter(fam_of.values()).items())}
        print(f"    family sizes {fstab}  -- four families of nine, one per point of "
              f"the deleted line")
        print("    the Clifford classes are 4 + 8 + 12 + 12, which is NOT a refinement")
        print("    of 9 + 9 + 9 + 9: the group action cuts across the geometry.")
    except Exception:                                   # noqa: BLE001
        pass

    return {"rays": n, "is_srg": bool(is_srg), "srg_parameters": list(params) if params else None,
            "axes_form_a_line": bool(clique),
            "each_magic_ray_meets_the_line_once": dict(counts) == {1: 36},
            "family_sizes": fstab,
            "M36_is_W33_minus_a_line": verdict}


# ===========================================================================
def pass_2836() -> dict:
    print()
    print("=" * 78)
    print("Pass 2836 -- the exact Landauer cost of one support readout")
    print("=" * 78)

    # The support map sends (x_p, z_p, x_f, z_f) in F_3^4 to the 4-bit mask of which
    # coordinates are nonzero.  A mask of weight k has exactly 2^k preimages, and there
    # are C(4,k) masks of weight k.
    print("  fibres of the support map on the 81 frames:")
    tot = 0
    fibres = {}
    for k in range(5):
        cnt, size = comb(4, k), 2 ** k
        fibres[k] = (cnt, size)
        tot += cnt * size
        print(f"    weight {k}: {cnt} mask(s) x {size} preimage(s) = {cnt*size}")
    print(f"    total {tot} (= 3^4)   consistent: {tot == 81}")

    # Information destroyed = H(state | support) = sum (n_i/81) log2 n_i.
    num = sum(comb(4, k) * (2 ** k) * k for k in range(5))     # log2(2^k) = k
    H_cond = Fraction(num, 81)
    print(f"\n  H(state | support) = {num}/81 = {H_cond} bits exactly = "
          f"{float(H_cond):.9f}")

    H_state = log2(81)
    H_supp = H_state - float(H_cond)
    print(f"  H(state)           = log2 81            = {H_state:.9f} bits")
    print(f"  H(support)         = H(state) - H(cond) = {H_supp:.9f} bits")
    print(f"  support channel efficiency = {H_supp:.6f} / 4 = {H_supp/4*100:.3f}%")

    # general q -- the closed form, and its two sanity points
    print("\n  general q:  H(state|support) = 4 (q-1) log2(q-1) / q")
    gen = {}
    for q in (2, 3, 4, 5, 7, 8, 9, 11):
        num_q = sum(comb(4, k) * ((q - 1) ** k) * k for k in range(5))
        exact = num_q * log2(q - 1) / q ** 4 if q > 2 else 0.0
        closed = 4 * (q - 1) * log2(q - 1) / q
        gen[q] = {"exact": exact, "closed_form": closed,
                  "agree": bool(abs(exact - closed) < 1e-12)}
        print(f"    q = {q:2d}:  exact {exact:.9f}   closed form {closed:.9f}   "
              f"agree: {gen[q]['agree']}")

    print("""
  At q = 2 the cost is exactly ZERO -- over F_2 the support IS the state, so a support
  readout destroys nothing.  Every bit of the 8/3 is the price of the third field
  element.  That is the thermodynamic statement of "support for readout, phase for
  execution": the phase is precisely the part you pay to look at.

  LANDAUER.  Erasing H bits costs at least H k_B T ln 2, so one support readout costs
""")
    kB, T = 1.380649e-23, 300.0
    E = float(H_cond) * kB * T * np.log(2)
    print(f"    E >= (8/3) k_B T ln2 = {E:.6e} J at T = 300 K   "
          f"= {E/1.602176634e-19*1e3:.4f} meV")
    print(f"    at 1 GHz readout rate: {E*1e9*1e15:.3f} fW of unavoidable dissipation")

    # the tie to the parallel track's observer
    print(f"""
  AND A BOUND ON THEIR OBSERVER.  The parallel track's Pass 2827 proves that no seven
  support taps suffice to reconstruct the frame and that exactly 48 eight-tap selectors
  do.  The information-theoretic floor is ceil(log2 81) = {int(np.ceil(H_state))} bits,
  because 81 states cannot be labelled by fewer.  So their observer sits exactly ONE BIT
  above the floor -- and their exhaustive search proves that one bit is not slack but
  necessary.  Two independent arguments, one from counting and one from search, meeting
  at 7 and 8.""")

    return {"fibres": {str(k): list(v) for k, v in fibres.items()},
            "H_cond_bits_numerator": num, "H_cond_bits": str(H_cond),
            "H_cond_float": float(H_cond),
            "H_state_bits": H_state, "H_support_bits": H_supp,
            "support_channel_efficiency": H_supp / 4,
            "general_q": {str(k): v for k, v in gen.items()},
            "landauer_joules_at_300K": E,
            "info_floor_bits": int(np.ceil(H_state)),
            "observer_taps_needed": 8}


def main() -> int:
    out = {"pass_2835": pass_2835(), "pass_2836": pass_2836()}
    path = ROOT / "data" / "PART_W33_PASS2835_2836_WITTING_LINE_AND_LANDAUER.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
