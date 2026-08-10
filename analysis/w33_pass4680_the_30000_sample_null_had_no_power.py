#!/usr/bin/env python3
"""Pass 4680 -- the three-copy distillation null result cannot rule out what it is read as ruling out.

The "Still open" section states open problem 2 with unusual care, and one line in it is a
search result:

    "At three copies the same condition is not obviously satisfiable either: 30,000 sampled
     stabilizer groups on six qubits produced no witness. Not a proof -- the space is far too
     large to enumerate -- but two independent searches now point the same way."

The hedge is correct as far as it goes.  What is missing is the number that says HOW far it
goes, and that number is computable in closed form rather than estimated.

THE SPACE IS EXACTLY COUNTABLE.  The maximal stabilizer groups on n qubits are in bijection
with the stabilizer states, and there are

    N(n) = 2^n * prod_{k=1}^{n} (2^k + 1)

of them.  At n = 6 that is 315,057,600.  So 30,000 samples is 0.0095% of the space, and the
power of the search against a witness set of size W follows immediately:

    P(find at least one) = 1 - (1 - W/N)^30000

which is 0.95% if there are a hundred witnesses and 9.1% if there are a thousand.  To reach
95% power the witness set would have to number 31,500 -- one in ten thousand of all
stabilizer groups on six qubits.

SO THE NULL EXCLUDES ONLY ABUNDANT WITNESSES, AND THE OBJECT SOUGHT IS NOT ABUNDANT.  The
condition is exact: annihilate EVERY single-error input while preserving the clean one.
Exact algebraic conditions are not satisfied on generic points; they cut out thin subvarieties.
A witness of that kind, if it exists, is overwhelmingly likely to sit in the regime where this
search had a one-in-a-hundred chance of seeing it.

That is not a criticism of the conclusion -- the conclusion may well be right.  It is a
correction to the EVIDENCE: "two independent searches point the same way" reads as
accumulating support, and a search with 1% power contributes almost none.

    py -3 analysis/w33_pass4680_the_30000_sample_null_had_no_power.py
"""

from __future__ import annotations

import sys
from math import prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

SAMPLES = 30_000
THRESHOLD = (8 - 2 * 3 ** 0.5) / 9


def n_stabilizer_groups(n: int) -> int:
    """Maximal stabilizer groups on n qubits = number of stabilizer states."""
    return 2 ** n * prod(2 ** k + 1 for k in range(1, n + 1))


def power(W: int, N: int, s: int) -> float:
    """P(at least one of W witnesses appears in s uniform draws with replacement)."""
    return 1.0 - (1.0 - W / N) ** s


def main() -> int:
    print("=" * 78)
    print("Pass 4680 -- what could the 30,000-sample search actually have found?")
    print("=" * 78)

    print(f"\n  {'n':>3s}  {'stabilizer groups on n qubits':>32s}")
    counts = {}
    for n in (4, 5, 6, 7):
        counts[n] = n_stabilizer_groups(n)
        print(f"  {n:3d}  {counts[n]:32,d}")

    N = counts[6]
    print(f"\n  sampled {SAMPLES:,} of {N:,}  =  {100 * SAMPLES / N:.5f}% of the space")

    print(f"\n  {'witnesses W':>12s} {'density':>11s} {'P(search finds one)':>21s}")
    rows = []
    for W in (1, 10, 100, 1_000, 10_000, 31_500):
        p = power(W, N, SAMPLES)
        rows.append({"witnesses": W, "density": W / N, "power": p})
        print(f"  {W:12,d} {W / N:11.2e} {p:20.2%}")

    # how many samples WOULD be needed?
    print(f"\n  samples needed for 95% power against W witnesses:")
    need = {}
    import math
    for W in (1, 10, 100, 1_000):
        s = math.ceil(math.log(0.05) / math.log(1 - W / N))
        need[W] = s
        print(f"    W = {W:>6,}   {s:>16,d} draws"
              f"   ({100 * s / N:6.2f}% of the space)")

    print(f"""
  THE NULL IS NEARLY POWERLESS AGAINST A RARE WITNESS, AND RARE IS WHAT IS EXPECTED.

  The sought object must annihilate EVERY single-error input while preserving the clean
  one. That is an exact algebraic condition, and exact conditions cut out thin sets -- they
  are not satisfied on generic points. If the witness set numbers in the hundreds, this
  search had a {power(100, N, SAMPLES):.1%} chance of seeing it; if it numbers ten, {power(10, N, SAMPLES):.2%}.

  So the sentence "two independent searches now point the same way" should read: one search
  was exhaustive and decisive (5,355 codes x 4 syndromes x 4 ray classes at two copies, zero
  super-linear branches -- a genuine bound on that family), and the other had of order one
  per cent power. They are not two comparable pieces of evidence, and adding them together
  overstates the case for a conjecture that may nonetheless be true.

  THE PROPOSED FIX IS RIGHT, AND HERE IS THE QUANTITATIVE REASON.  The section already says
  what is missing: "an exhaustive search over a chosen code family rather than a random
  one." The power calculation says why random sampling cannot be rescued by drawing more --
  reaching 95% power against a hundred witnesses needs {need[100]:,} draws, which is
  {100 * need[100] / N:.0f}% of the entire space. At that point one should enumerate rather than sample.

  AND A CONCRETE FAMILY TO CHOOSE, WHICH IS THE NOVEL PART.  An exact condition of this kind
  is stable under symmetry: if a stabilizer group S satisfies it, so does gSg^-1 for any
  Clifford g commuting with the error model. Witnesses therefore come in ORBITS, never
  singly. Two consequences:

    * A uniform sample over groups is the wrong measure -- it wastes almost every draw on
      re-testing the interior of orbits already visited.
    * The right enumeration is over ORBIT REPRESENTATIVES under the symmetry the protocol
      already has. That divides the search by the orbit size, and the orbit size is the
      order of the stabilising subgroup -- typically large for the highly structured codes
      a witness would have to be.

  So the recommendation is sharper than "enumerate a family": enumerate orbit
  representatives under the symmetry group of the error model, and the count that matters
  is the number of ORBITS, not the {N:,} groups.""")

    out = {
        "boundary": ("this pass computes the statistical power of a search reported "
                     "elsewhere; it does NOT settle the open problem, run any new search, "
                     "or claim a witness exists. The power model assumes uniform sampling "
                     "with replacement over maximal stabilizer groups -- if the reported "
                     "sampling was non-uniform or structured, the power differs and the "
                     "sampling procedure would need to be read"),
        "stabilizer_group_counts": {str(n): counts[n] for n in counts},
        "samples": SAMPLES,
        "space_n6": N,
        "fraction_sampled": SAMPLES / N,
        "power_by_witness_count": rows,
        "samples_for_95pct_power": {str(k): v for k, v in need.items()},
        "acceptance_threshold": THRESHOLD,
        "conclusion": (
            "30,000 uniform samples cover 0.0095% of the 315,057,600 maximal stabilizer "
            "groups on six qubits and have 0.95% power against a hundred-witness set. The "
            "null excludes only abundant witnesses, while the exact annihilation condition "
            "predicts a thin one. The two-copy exhaustive result is decisive; the "
            "three-copy sample is not comparable evidence"),
        "recommendation": (
            "enumerate ORBIT REPRESENTATIVES under the symmetry group of the error model "
            "rather than sampling groups: exact conditions are symmetry-stable so witnesses "
            "occur in orbits, and uniform sampling spends nearly every draw inside orbits "
            "already visited"),
    }
    p = ROOT / "data" / "PART_W33_PASS4680_DISTILLATION_SEARCH_POWER.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
