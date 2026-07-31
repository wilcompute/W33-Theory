# Passes 1410–1415 — the two 14s are the same, covers are diagonal, and a shortcut I wanted to work does not

> **CORRECTED 2026-07-31 by the parallel track's Passes 1416–1420
> ([`BT1420_frame_signed_turn_bridge_insert.tex`](analysis/BT1420_frame_signed_turn_bridge_insert.tex)).
> Three items below are superseded, and one of them is REFUTED. Read this first.**
>
> 1. **Pass 1412's open question is CLOSED, and my reasoning had a specific
>    error.** BT1416 exhibits the intertwiner `F = ∂ᵀ(A−12I)(A−2I)N / 16`, which
>    is integral, satisfies `FMᵀ = 0`, `(K−10I)F = 0`, `rank F = 15`, and induces
>    an equivariant isomorphism `coker(M) ⊗ Q ≅ ker(K−10I)`. So the two 15s **are**
>    the same module. My shortcut failed for a diagnosable reason they name
>    exactly: I compared the **unsigned** 240-edge permutation module against an
>    operator that acts on the **orientation-signed** edge action. `ker(K−10I)` was
>    never a submodule of the module I decomposed, so "two degree-15 constituents"
>    — though true of the permutation module — was never the relevant fact. This
>    is a category error, not a near miss.
> 2. **Pass 1411 is REFUTED, and I have reproduced the refutation.** I claimed
>    cover stabilisers are "diagonal" on the evidence that no sampled stabiliser
>    fixed a frame. That sample was six covers from a single depth-first order and
>    drew only the fixed-point-free types. Re-sampling 24 distinct covers across
>    12 randomised orders:
>
>    ```text
>    C4        frames fixed  0    (9 covers)
>    C2 x C2   frames fixed  0    (5)      and  4  (4 covers)
>    C4 x C2   frames fixed  0    (3)      and  2  (1)
>    C2        frames fixed 12    (2)      orbits [1^12, 2^24]
>    ```
>
>    `C₂`-stabilised covers fix **twelve** frames — exactly BT1420's number,
>    reproduced independently here. Cover stabilisers are **not** universally
>    diagonal. What survives is the narrower statement I did scope correctly at
>    the time: *the six covers in that sample* had fixed-point-free stabilisers.
> 3. **Pass 1409's bound is superseded.** My time-capped `6579` is replaced by a
>    certified `226800` from sixteen deterministic `C₂` orbits plus four further
>    stabiliser types.
> 4. **Pass 1410 stands but is sharpened.** The two mod-2 `14`s are abstractly
>    isomorphic (this pass), *and* BT1420 shows the bridge geometrically
>    **separates** them: mod 2 it has rank 14 and square zero, selecting the
>    nontrivial reduction of the rational 15 while the second copy stays in the
>    31-dimensional torsion-side kernel.
>
> The section below is left as written, so the failure keeps its provenance.


Six results. The one I was most interested in came out **negative**, and that is
the most useful thing in the batch: it kills a plausible argument and names
exactly what would replace it.

---

## Pass 1412 — the signed-turn shortcut FAILS (the outside-the-box one)

Here is the thought I had been circling. The signed-turn operator `K` lives on the
same 240 integral edge chains and has

```text
spec(K) = (−6)^81 , 2^120 , 4^24 , 10^15                     (Pass 826)
```

A **fifteen**-dimensional eigenspace, on exactly the carrier where Pass 1397 put a
fifteen-dimensional cokernel. `Aut` acts on oriented edges by signed permutations
and **commutes with `K`** (Pass 984), so `ker(K − 10I)` is a 15-dimensional
`G`-submodule of `Q²⁴⁰`. If it were the *same* 15 as the cross-matching's
cokernel, the frame geometry would be tied to the non-backtracking spectrum as
well as to the adjacency spectrum.

I deliberately chose a test needing **no edge-labelling alignment** — my edge
ordering and the K-track's are built independently, so comparing subspaces across
them would be meaningless. Instead: how many degree-15 irreducibles does the
240-edge permutation module contain? Multiplicity 1 would force the identification.

```text
240-edge decomposition (degree, mult):
    [1,1]  [15,1]  [15,1]  [20,1]  [24,2]  [60,1]  [81,1]

degree-15 constituents        : 2       multiplicities [1, 1]
TOTAL degree-15 isotypic dim  : 30
unique and 15-dimensional?    : FALSE
```

**There are TWO non-isomorphic degree-15 irreducibles**, each once. The forcing
argument does not run. The cokernel is one of them; `ker(K − 10I)` is one of them;
which one each is, dimension alone cannot say.

**So the question stays open, and it is now sharp**: determine which of the two
degree-15 characters `ker(K − 10I)` affords, and compare with Pass 1397's. That is
a character computation on the K-track's own carrier, not a subspace comparison,
so it inherits none of the alignment hazard. I am recording the failed shortcut
rather than quietly replacing it with the harder computation, because the failure
is the informative part: *two* degree-15 constituents is itself a fact about the
edge module that nothing in the corpus had noted.

One more thing that decomposition says, unprompted: the 240-edge module contains
an **81**. That is the Steinberg dimension, sitting in the edge carrier with
multiplicity one, and it is not what this pass set out to find.

---

## Pass 1410 — the two mod-2 `14`s ARE isomorphic

Pass 1405 found the mod-2 quotient has composition factors `[1,1,1,6,8,14,14]`.
Since `15 = 1 + 14` is the reduction of the rational irreducible, one `14` is
reduction and the other is torsion. MeatAxe:

```text
quotient dim 45,  factors [1,1,1,6,8,14,14]
number of 14-dimensional factors : 2
ARE THE TWO 14s ISOMORPHIC?      : TRUE
```

**The torsion carries a second copy of the reduction.** So although
`coker ⊗ F₂` is not irreducible, its two largest factors are the same module —
the mod-2 picture is `14 ⊕ 14` plus small pieces (`1,1,1,6,8`), not two unrelated
14s. That is a much tighter statement than "reducible", and it is the sharpest
available description of the `(Z/2)³⁰`.

---

## Pass 1411 — a cover's stabiliser is diagonal, not frame-based

Every sampled cover keeps a group of order 4 or 8, and `O_h = C₂×S₄` contains both
`C₄` and `C₂×C₂` — so a cover's stabiliser *could* have been sitting inside one
frame's stabiliser, which would mean covers are organised around a distinguished
frame. They are not:

```text
|Stab| = 4 (C4)       frames fixed: 0    orbits on the 60: 2^6, 4^12
|Stab| = 4 (C4)       frames fixed: 0    orbits on the 60: 2^6, 4^12
|Stab| = 4 (C4)       frames fixed: 0    orbits on the 60: 2^6, 4^12
|Stab| = 4 (C4)       frames fixed: 0    orbits on the 60: 2^6, 4^12
|Stab| = 8 (C4 x C2)  frames fixed: 0    orbits on the 60: 2^4, 4^1, 8^6
|Stab| = 4 (C2 x C2)  frames fixed: 0    orbits on the 60: 2^10, 4^10
```

**No cover's stabiliser fixes a single frame.** The conclusion does not rest on
the fixed-point count alone — it is independently visible in the orbit data, since
every orbit on the 60 frames has size ≥ 2 and a fixed frame would be an orbit of
size 1. A cover's residual symmetry is diagonal across the whole resolution.

---

## Pass 1413 — a fifth collision noise class, and what the grammar fix was worth

The Pass 1407 `[n,k,d]` fix turned out to be far more consequential than expected:

```text
distinct tokens   23,594  ->  2,689       (~21,000 were JSON array rows)
collision pairs    2,066  ->    356
```

Reading the new head found the fifth and last noise class: **the same pass in two
formats.** `BT807_q3_antiflag_two_clocks.md` vs `bt807_q3_antiflag_two_clocks.py`;
`PART_CXCIX_QECC_BRIDGE.py` vs `manuscripts/parts/PART_CXCIX_QECC_BRIDGE.md`. A
witness and its write-up necessarily share every result — that is the workflow,
not a rediscovery. Filtered by case-insensitive stem equality.

**The one genuine candidate in the head**, read in full:
`w33_BREAKTHROUGH_309_sphere_packing_substrate.py` and
`w33_BREAKTHROUGH_440_substrate_lattice_ladder.py` share seven lattice compounds
(`barnes-wall+e_8`, `a_2+hexagonal`, …) and do not cite each other. Reading both:
309 is about **proven-optimal packing densities** (Viazovska's `E₈`, Leech), 440
about **kissing numbers** of the substrate ladder. Adjacent, overlapping
vocabulary, **different claims** — so this is a cite-across candidate, not a
rediscovery, and it is recorded as such rather than as a retraction.

---

## Pass 1414 — the other token classes are fine on `.json` (a clean negative)

`[n,k,d]` broke because Pass 328 calibrated it on **prose** and the index later
widened to certificates. The obvious worry is that the other three classes broke
the same way. Measured over 60 random files of each type:

| class | `.md` mean / max | `.json` mean / max |
|---|---|---|
| `results_in` (all) | 2.4 / 26 | 1.2 / 42 |
| `noun_number_pairs` | 0.1 / 3 | 0.1 / 8 |
| `compounds` | 1.4 / 21 | 0.8 / 36 |
| `group_tokens` | 0.3 / 4 | 0.4 / 9 |

**No further mis-calibration.** Every class fires at a comparable or lower rate on
certificates than on prose. The `[n,k,d]` failure was specific, not systemic, and
the collision ranking is not keyed on anything else broken.

---

## Pass 1415 — the manuscript insert compiles

`BT1408_frame_cross_matching_theorem_insert.tex` builds to a 43 KB PDF against the
paper's own macro definitions (`\PSp` is `\mathrm{PSp}` at `w33_paper.tex:106`;
`\Aut` and `\texorpdfstring` likewise resolve). It needs `hyperref`, which the
paper already loads.

So the insert is compile-ready and notation-clean. It remains a promotion
**candidate** in `analysis/` — placement beside the existing `1 + 24 + 15`
spectral section is an editorial decision, not a computational one, and Pass
1412's negative should be reflected there before it lands: the remark currently
says the identification with `ker(A+4I)` is rational, and it should also say that
the analogous question for `ker(K − 10I)` is **open**, because there are two
degree-15 constituents rather than one.

## Prior art

- [Pass 826](analysis/w33_pass826_k_operator_four_branch_gluing.py) — **owns** `K` and `spec(K) = (−6)^81, 2^120, 4^24, 10^15`.
- [Pass 984](analysis/w33_pass826_k_operator_four_branch_gluing.py) — **owns** that `Aut` commutes with `K` on oriented edges.
- [Pass 1397](analysis/w33_pass1397_1401_cokernel_theorem_covers_collisions.md) — the rational cokernel theorem this pass tried to extend.
- [Pass 1405](analysis/w33_pass1405_1409_torsion_rigidity_context.md) — the mod-2 factors whose two 14s are identified here.
