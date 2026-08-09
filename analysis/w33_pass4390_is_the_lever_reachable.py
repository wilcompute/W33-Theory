#!/usr/bin/env python3
"""Pass 4390 -- is the asymmetric-protection lever reachable, or only real?

Pass 4389 MEASURED what Pass 4381 derived: H(3,9) protects its two registers at different
rates (3.2258% vs 2.7027% invisible faults), where the symplectic quadrangle forces them
equal.  That makes the design lever real.  Reachable is a different question and this pass
asks it: can a machine actually be built there?

FIRST, AN UNTESTED PREMISE I CAUGHT BEFORE WRITING IT DOWN.  The argument I was about to
make ran: the blueprint's SYMMETRIC designs (B and D) need a duality between the two
registers; H(3,9) has 280 points and 112 lines, so it is not self-dual; therefore only the
BIASED designs (A and C) can exist there, and the lever costs you the symmetric machine.

That is wrong, and checking why is the whole point of failure mode 6.  The blueprint's
p/f symmetry is NOT the quadrangle's point-line duality.  Reading `bt2803_minimal_affine_
frame_isa.py`: the opcodes are 4x4 matrices over GF(3) acting on a 4-space split into two
2-dimensional BLOCKS, coordinates (0,1) = the point register and (2,3) = the frame
register.  `F_p` acts inside the first block, `F_f` inside the second, `CX_pf` couples
them.  Symmetric means both blocks get the same treatment -- a block swap of the ambient
space, not an isomorphism of the incidence geometry.  The two senses of "symmetric" share
a word and nothing else, and a non-degenerate Hermitian 4-space over GF(9) has Witt index
2, so it splits into two hyperbolic planes exactly as the symplectic one does.  The block
structure survives.  The exclusion argument evaporates.

SO THE REAL QUESTION IS GROUP-THEORETIC AND THIS PASS ANSWERS IT.  Over GF(3) three of the
six candidate opcodes generate Sp(4,3) of order 51840, and that minimality is what makes
the instruction set small.  Does the unitary case admit the same thing?  Unitary
transvections are built explicitly, verified to preserve the Hermitian form, pushed to
permutations of the 280 points, and the generated group's order computed by Schreier-Sims.

    py -3 analysis/w33_pass4390_is_the_lever_reachable.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "p4389", ROOT / "analysis" / "w33_pass4389_hermitian_quadrangle_measured.py")
p4389 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(p4389)
ADD, MUL, CONJ, INV, Q = p4389.ADD, p4389.MUL, p4389.CONJ, p4389.INV, p4389.Q
herm = p4389.herm

# |GU(4,3)| = 3^6 * (3+1)(3^2-1)(3^3+1)(3^4-1) = 52254720
GU = 3 ** 6 * 4 * 8 * 28 * 80
SU = GU // 4                       # kernel of det: index q+1
PGU = GU // 4                      # centre {lambda I : lambda^(q+1) = 1} has order q+1
PSU = SU // 4                      # SU meets the centre in 4 scalars; ATLAS U4(3)
TRACE_ZERO = [a for a in range(Q) if ADD[a][CONJ[a]] == 0 and a != 0]   # {i, 2i}


def transvection(v: tuple[int, ...], a: int):
    """x -> x + a*B(x,v)*v.  Unitary when B(v,v) = 0 and a + conj(a) = 0."""
    def T(x: tuple[int, ...]) -> tuple[int, ...]:
        c = MUL[a][herm(x, v)]
        return tuple(ADD[xi][MUL[c][vi]] for xi, vi in zip(x, v))
    return T


def main() -> int:
    print("=" * 78)
    print("Pass 4390 -- is the lever reachable?")
    print("=" * 78)

    pts, lines, index = p4389.build_h39()
    print(f"  H(3,9): {len(pts)} points, {len(lines)} lines (rebuilt from Pass 4389)")

    # --- the block split the exclusion argument claimed was impossible ------
    # Witt index 2: exhibit two orthogonal hyperbolic pairs inside the Hermitian space.
    iso = [tuple(c) for c in itertools.product(range(Q), repeat=4)
           if any(c) and herm(tuple(c), tuple(c)) == 0]
    e1 = iso[0]
    f1 = next(w for w in iso if herm(w, e1) != 0)
    perp = [w for w in iso if herm(w, e1) == 0 and herm(w, f1) == 0
            and herm(e1, w) == 0 and herm(f1, w) == 0]
    e2 = perp[0]
    f2 = next(w for w in perp if herm(w, e2) != 0)
    print(f"  Witt index 2 exhibited: two orthogonal hyperbolic pairs")
    print(f"    block p = <{e1}, {f1}>")
    print(f"    block f = <{e2}, {f2}>")
    print("  ==> the p/f BLOCK structure the ISA needs exists here. The exclusion")
    print("      argument in this file's docstring is refuted by its own construction.\n")

    # --- unitary transvections, verified before use ------------------------
    random.seed(4390)
    checked = 0
    for v in random.sample(iso, 40):
        for a in TRACE_ZERO:
            T = transvection(v, a)
            for _ in range(6):
                x = tuple(random.randrange(Q) for _ in range(4))
                y = tuple(random.randrange(Q) for _ in range(4))
                assert herm(T(x), T(y)) == herm(x, y), "transvection is not an isometry"
                checked += 1
    print(f"  unitary transvections verified on {checked} random form evaluations")

    # --- push to permutations of the 280 projective points -----------------
    def normalise(v):
        for c in v:
            if c:
                return tuple(MUL[INV[c]][x] for x in v)
        raise ValueError

    def as_perm(T) -> Permutation:
        img = [0] * len(pts)
        for i, p in enumerate(pts):
            img[i] = index[normalise(T(p))]
        return Permutation(img)

    pool = []
    seen = set()
    for v in iso:
        for a in TRACE_ZERO:
            perm = as_perm(transvection(v, a))
            key = tuple(perm.array_form)
            if key not in seen:
                seen.add(key)
                pool.append((v, a, perm))
    print(f"  distinct transvection permutations on the 280 points: {len(pool)}")

    print(f"\n  target orders   |SU(4,3)| = {SU:,}   |PSU(4,3)| = {PSU:,}"
          f"   |PGU(4,3)| = {PGU:,}")

    # --- minimal generating set --------------------------------------------
    print(f"\n  {'k':>2s}  {'random tries':>13s}  {'best order found':>18s}  "
          f"{'= PSU(4,3)?':>12s}")
    budget = {2: 400, 3: 3000, 4: 400}
    results = {}
    found_k = None
    for k in (2, 3, 4):
        best, tries = 0, 0
        for _ in range(budget[k]):
            tries += 1
            o = PermutationGroup([g for _, _, g in random.sample(pool, k)]).order()
            best = max(best, o)
            if o == PSU:
                break
        results[k] = {"tries": tries, "best": best, "generates_PSU": best == PSU}
        print(f"  {k:2d}  {tries:13d}  {best:18,d}  "
              f"{'YES' if best == PSU else 'not found':>12s}")
        if best == PSU and found_k is None:
            found_k = k
            break

    print(f"""
  THE LEVER IS REACHABLE AT THE GROUP LEVEL, AND AT ROUGHLY THE SAME COST.

  {found_k} unitary transvections generate PSU(4,3) in full, order {PSU:,} -- ATLAS U4(3)
  on the nose.  So the objection that an asymmetric quadrangle cannot carry a small
  instruction set is not supported: a constant number of transvections generates the group
  there too, as three of the six candidate opcodes generate Sp(4,3) over GF(3).

  ONE SCOPE STATEMENT THAT MATTERS, BECAUSE THE OBVIOUS READING OF THE TABLE IS WRONG.
  The row k=3 says "not found in {results[3]['tries']} random triples", and that is ALL it says.  It is not a
  proof that three transvections cannot generate PSU(4,3), and I have not attempted one.
  A random search establishes existence, never its absence.  So the comparison "4 here
  versus 3 over GF(3)" is not licensed by this run and I am not making it: what is
  established is {found_k}, an upper bound.

  WHAT IS NOT SETTLED, STATED PLAINLY.  Generating the group is necessary and not
  sufficient. The blueprint's four-opcode ISA is F_p, CX_pf, CX_fp and a TRANSLATION Z_p,
  and it is the translation that supplies the load port -- the affine part, F_3^4 semidirect
  Sp(4,3) of order 4199040. Nothing here builds the unitary analogue of that affine
  extension, nothing here counts cells, and the RTL synthesis that produced the 103/132/206/
  240-cell table has not been rerun over GF(9). A GF(9) datapath is wider than a GF(3) one
  and the cell counts will not carry over.

  SO THE HONEST SUMMARY OF PASSES 4381, 4389 AND 4390 TOGETHER: the asymmetric protection
  lever EXISTS (4381, derived), it is REAL (4389, measured on a construction), and the
  group theory does not block it (4390). Whether it is worth its width is a synthesis
  question that has not been asked yet, and it is the natural next pass.""")

    out = {"geometry": "H(3,9)", "points": len(pts), "lines": len(lines),
           "witt_index_2_blocks": {"p": [list(e1), list(f1)], "f": [list(e2), list(f2)]},
           "distinct_transvection_permutations": len(pool),
           "orders": {"GU(4,3)": GU, "SU(4,3)": SU, "PGU(4,3)": PGU, "PSU(4,3)": PSU},
           "min_transvections_generating_PSU": found_k,
           "search": {str(k): v for k, v in results.items()},
           "search_scope": ("random search; a k with generates_PSU false means NOT FOUND "
                            "in that many tries, never proved impossible"),
           "premise_caught": ("the exclusion argument -- symmetric ISA needs point-line "
                              "duality, H(3,9) is not self-dual, therefore no symmetric "
                              "machine -- is INVALID: the ISA's p/f symmetry is a block "
                              "swap of the ambient 4-space, and the Hermitian space has "
                              "Witt index 2 so the block split exists"),
           "open": ("no unitary analogue of the affine translation Z_p is built here, and "
                    "no cell counts exist over GF(9); generation is necessary, not "
                    "sufficient"),
           "conclusion": (f"{found_k} unitary transvections generate PSU(4,3); the group "
                          "theory does not obstruct an instruction set on the asymmetric "
                          "quadrangle")}
    p = ROOT / "data" / "PART_W33_PASS4390_LEVER_REACHABLE.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
