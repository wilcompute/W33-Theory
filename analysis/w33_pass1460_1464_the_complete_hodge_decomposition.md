# Passes 1460–1464 — the signed edge module decomposes into six irreducibles, multiplicity-free

Five items. One completes the physics arc; one is an audit of my own sampled
claims; two remain open and are reported as open.

---

## Pass 1460 (physics) — the complete Hodge decomposition

Pass 1455 identified the harmonic block. Running the same signed-character
machinery on all three blocks completes it:

```text
EXACT    (gauge,      39) = 15 (+) 24
HARMONIC (physical,   81) = 81                 IRREDUCIBLE
COEXACT  (constraint,120) = 30 (+) 45 (+) 45
                     TOTAL 240, multiplicity-free across six irreducibles
```

**The signed 240-edge module splits into exactly six irreducibles, each once, and
the split aligns precisely with the Hodge blocks.**

Two readings, both exact:

- **The gauge sector is the point module.** `15 ⊕ 24` is precisely the 40-point
  permutation module `1 ⊕ 15 ⊕ 24` with its trivial constituent removed — i.e.
  the `(−4)`- and `(+2)`-eigenspaces of `A`. The Gauss-law count `39 = 40 − 1` is
  not an accident of dimensions; it is that quotient, representation-theoretically.
- **The physical sector is a single irreducible**, the Steinberg module.

So the lattice-gauge decomposition of `W(3,3)` is not merely dimensionally
suggestive; every block is a named `G`-module, and no block repeats.

**A bug caught by a wrong answer.** The first run reported `EXACT: NOT
signed-invariant`, which is impossible for a chain map. Cause:
`VectorSpace(Rationals, TransposedMat(d1))` has rows of length **40**, not 240 —
it built the wrong space entirely and still returned dimension 39, which is why
the number looked right. The row space of `d1` is the correct object. Third
instance this session of a wrong *action* producing a plausible *number*.

---

## Pass 1461 — the resolution search, three methods, still open

`540 = 9 × 60` with edge-multiplicity 9 makes a resolution arithmetically
perfect. Attempts to date:

| method | outcome |
|---|---|
| random-order DFS over covers | no resolution; also produced the false intersecting-family claim |
| ban-and-recurse, frozensets | exceeded 740 s |
| ban-and-recurse, 240-bit / 540-bit masks | exceeded 740 s |

Pass 1456 proved the method is sound at depth 1 — a disjoint cover is found
exhaustively in 16 seconds — so this is a performance wall, not a conceptual one.
**Open, not excluded**, and the honest statement after three attempts.

One observation from the failures worth keeping: the unconstrained enumerator
found **zero** covers in 240 s of deterministic-order search, while the *same*
search with 60 frames banned found one in 16 s. Banning prunes hard. Whatever
solves this will exploit that, not fight it.

---

## Pass 1462 — audit of everything I claimed from a DFS-sampled pool

Pass 1456 showed that sampler misses in 1,262 draws what exhaustive search finds
in 16 seconds. Every claim resting on it needs re-labelling:

| claim | source | status now |
|---|---|---|
| "no two covers are disjoint; minimum intersection 4" | 1,262-cover pool | **REFUTED** (Pass 1456) |
| stabiliser types `C2, C4, C2×C2, C4×C2` exist | 24-cover sample | **stands** — existence survives bias |
| `D8` exists | their census | stands (theirs, not mine) |
| cover-type *proportions* (37.5% C4, 8.3% C2 …) | 24-cover sample | **withdrawn** as a distribution (Pass 1439) |
| "cover stabilisers are diagonal" | 6-cover sample | **REFUTED** (Pass 1426) |
| a `C₂` cover fixes 12 of its 60 frames | 24-cover sample + GAP | stands — verified structurally, and matches BT1420 |

**Three refutations, all from the same sampler, all caught by targeted search or
by the parallel track.** The pattern is now unambiguous: this DFS is fine for
exhibiting objects and worthless for measuring frequencies or asserting
universals.

---

## Pass 1463 — the `12` remains unexplained

Pass 1457 killed the natural explanation: the class-45 involution fixes 32 edges,
so `4f = 32` would force `f = 8`, not 12, and `4f + 8p = 240` holds identically
for every `f`, so edge counting constrains nothing.

The follow-up — enumerate `C₂`-invariant covers and read off their `f` values —
hit the same performance wall as Pass 1461 (0 covers in 240 s unconstrained).
So the enrichment (20% inside a stabilised cover vs 15.6% globally) stands as a
measured fact with no explanation and no counterexample. **Open.**

---

## Pass 1464 — the physics, written into both manuscripts

`BT1408` now carries Theorem (Hodge blocks) and a Remark (no star, and where one
must come from), stating:

- the six-irreducible multiplicity-free split;
- that the harmonic block is the Steinberg module;
- that the gauge block is the point module modulo constants;
- that `C₁ = 240 ≠ 160 = C₂` by exactly `|χ|`, and `b₂ = 0`, so there is no `⋆`,
  no `F ∧ ⋆F`, and no variational dynamics;
- that in `M⁴ × F` the star belongs to the continuum factor, so the finite side's
  contribution is now complete and named — algebra `⟨I, A, J⟩` plus the Steinberg
  module — and the missing piece is missing **by computation**, not omission.

```text
w33_paper.tex        1,513,702 bytes   0 errors
photonic_holonet.tex 1,006,317 bytes   0 errors
```

This is the honest form of the physics claim: the finite geometry delivers an
exact, fully named gauge-theoretic kinematics, and demonstrably cannot deliver
the dynamics on its own.

## Prior art

- [Pass 1455](analysis/w33_pass1455_1459_harmonic_is_steinberg_and_a_refutation_of_my_own.md) — the harmonic block, and the refutation audited above.
- [Pass 1448](analysis/w33_pass1448_1454_hodge_maxwell_and_the_missing_star.md) — `χ`, the Betti numbers, and the missing star.
- [Pass 1108 / 1110](analysis/w33_pass1109_1110_sl23_and_steinberg.md) — **own** the Steinberg identification.
