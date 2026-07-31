# Passes 1455–1459 — the physical sector IS the Steinberg module, and my own intersecting-family claim is refuted

Five items. One is the strongest physics result of this arc; one destroys a
"breakthrough" I announced two batches ago, using the exact test I proposed for
it.

---

## Pass 1455 (physics) — the harmonic sector is the Steinberg module

Pass 1449 got `dim(harmonic) = 81` and then **failed** to compute its character:
`Permuted(basis, g)` left the space. That failure was the finding — cycles carry
orientation, so the harmonic sector is a submodule of the orientation-**signed**
edge module. Building that action explicitly (`g` sends stored edge `[a,b]` to
`{a^g, b^g}` with sign `−1` exactly when the image inverts):

```text
signed action is a chain map (d1·S = P·d1)     : TRUE
harmonic space is SIGNED-invariant             : TRUE
signed harmonic character computable           : TRUE
  degree                                       : 81
  HARMONIC decomposition (degree, mult)        : [[81, 1]]
  IRREDUCIBLE of degree 81                     : TRUE
```

> **The physical (harmonic) sector of the lattice gauge theory on `W(3,3)` is
> exactly the degree-81 irreducible — the Steinberg module.**

Put beside Pass 1448, the picture closes:

```text
240 edge 1-cochains = 39 exact  (+)  81 harmonic  (+)  120 coexact
                      pure gauge     STEINBERG        constraint
```

The gauge-theoretic decomposition and the representation theory meet in **one
named object**, through a map rather than through a matching integer. That is the
distinction this corpus exists to enforce, and here it is satisfied.

Two things it does **not** say. It is a statement about kinematics only — Pass
1448 showed `b₂ = 0`, so there is still no Hodge star, no `F ∧ ⋆F`, no dynamics.
And it says nothing about physical *interpretation*: "Steinberg module" is a
representation, not a particle content.

**Method note worth keeping.** This result was unreachable three times — Pass
1412, Pass 1449, and implicitly Pass 1441 — for one repeated reason: comparing a
signed object against an unsigned module. Once the signed action was written
down, the computation took seconds.

---

## Pass 1456 — my intersecting-family claim is REFUTED, by my own proposed test

Pass 1441 reported, over 795,691 pairs from 1,262 covers: zero disjoint pairs,
minimum intersection 4, and concluded the covers form an intersecting family so
no resolution can exist. I attached a caveat — that the DFS pool is known
non-uniform and under-draws the `C₂`-heavy region — and proposed a targeted test.

The test was run. **It takes 16 seconds.**

```text
fixed a known cover A (60 frames)
banned all 60 of A's frames; 480 remain
edges with no available frame                : 0
exhaustive search, 148,548 nodes, 16 s
a cover DISJOINT from A exists               : TRUE
```

**So there are disjoint covers, the covers are not an intersecting family, and
the "minimum intersection 4" was an artefact of the sampler — exactly as the
caveat said it might be.** Pass 1441's headline is withdrawn.

What survives: the *observation* that a DFS-generated pool of 1,262 covers
contains no disjoint pair, which is now a statement about the sampler rather
than about the geometry, and a rather stark one — the sampler misses a structure
findable by exhaustive search in 16 seconds.

**The resolution question is reopened.** With the right method (ban a class's 60
frames, recurse, backtrack) it ran past a 740-second budget without deciding.
Open, not excluded, and now with a method that is known to work at depth 1.

---

## Pass 1457 — the `C₂` enrichment is real, and the obvious explanation fails

Corrected actions (an earlier run mixed the point and line permutations, the same
class of bug as Pass 1447; `84` now matches Pass 1442):

```text
class-45 involution fixes :  8 points   32 edges   16 lines   84 frames
class-270 involution fixes:  0 points    8 edges    4 lines   24 frames
```

The natural explanation would be that a `C₂`-invariant cover's fixed-frame count
`f` is forced by edge counting. It is not:

- `4f = 32` would force `f = 8`, but the measured value is `f = 12`;
- and the identity `4f + 8p = 4f + 8·(60−f)/2 = 240` holds for **every** `f`, so
  edge counting imposes no constraint at all.

So the 20% vs 15.6% enrichment is genuine and unexplained. Recorded as such
rather than papered over with the first plausible argument — which is what
testing it was for.

---

## Pass 1458 — the portability scan had its scope backwards

`check_orphan_inserts --portability` scanned **orphans only**. BT1509 is
*promoted* and used `\PSp` with no guard; it compiled solely because BT1408
precedes it in the wrapper and happens to provide the macro. A promoted insert
that breaks a host is strictly worse than an orphan that does — it is in a live
build. Scope widened:

```text
checked 220 inserts (was 189 orphans only)
use host-only macros WITHOUT a guard : 0
```

---

## Pass 1459 — where the Hodge star has to come from

Pass 1448 established there is no `⋆` on the finite complex: `C₁ = 240 ≠ 160 = C₂`
by exactly `|χ|`, and `b₂ = 0` leaves the physical 81 with no dual. The paper's
own framing already names the resolution, and it is worth stating sharply.

In an almost-commutative geometry `M⁴ × F`, the metric structure — volume form,
Hodge star, the integral in the action — lives on the **continuum factor `M⁴`**.
The finite factor `F` contributes an algebra and a module, not a metric. So the
division of labour is:

| supplied by | what |
|---|---|
| the finite side `F` | the algebra `⟨I, A, J⟩`, and the module: **Steinberg, 81-dimensional** (Pass 1455) |
| the continuum side `M⁴` | the star, the volume form, the variational principle |

This is not a rescue of the physics claim; it is a specification of what would
have to be built. The finite side is now *done and named*. What is absent is
absent by computation (`b₂ = 0`), not by oversight, and cannot be repaired
internally.

## Prior art

- [Pass 1448](analysis/w33_pass1448_1454_hodge_maxwell_and_the_missing_star.md) — the Hodge/Maxwell split and the missing star.
- [Pass 1441](analysis/w33_pass1441_1447_intersecting_family_and_the_class45_involution.md) — the intersecting-family claim withdrawn here.
- [Pass 1108 / 1110](analysis/w33_pass1109_1110_sl23_and_steinberg.md) — **own** the identification of the 81 with the Steinberg module.
- Passes 1416–1420 (parallel track) — **own** the signed intertwiner whose necessity this pass re-confirms from the homology side.
