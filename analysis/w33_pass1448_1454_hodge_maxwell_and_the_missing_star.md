# Passes 1448–1454 — the clique complex is a bouquet of 81 circles, the Hodge star does not exist, and BT773 is vindicated in the right group

Seven items: two physics, five follow-ups. The physics result is the strongest
thing in the batch and it is a **constraint**, not a licence.

---

## Pass 1448 (physics) — the full Hodge/Maxwell structure, computed for the first time

Every totally isotropic line of `W(3,3)` is a **4-clique**, hence a 3-simplex. So
the clique complex is genuinely 3-dimensional, and nothing in the corpus had
computed its boundary tower — Pass 682 stops at `H₁` using `d₁, d₂` only.

```text
C0 = 40      C1 = 240      C2 = 160      C3 = 40
chi = 40 - 240 + 160 - 40 = -80
rank d1 = 39   rank d2 = 120   rank d3 = 40
BETTI:  b0 = 1   b1 = 81   b2 = 0   b3 = 0        (alternating sum = -80 ✓)
```

**The complex is homotopy-equivalent to a bouquet of 81 circles.** `b₂ = b₃ = 0`
is not a small remark: it is what kills the physics reading below.

### The Maxwell decomposition is exact

```text
240 edge 1-cochains  =  39 exact  (+)  81 HARMONIC  (+)  120 coexact
                        pure gauge      physical         constraint
```

This is precisely the lattice-gauge-theory split. `39 = 40 − 1` is the Gauss-law
count (gauge transformations modulo the global one), `81 = 3⁴` is the physical
sector, `120` is the constraint surface. The substrate supports the **kinematics**
of a gauge theory exactly, with no fitting.

### But the Hodge star does not exist, and that is decisive

A Hodge star needs `C_k ≅ C_{3−k}`. Cell by cell:

```text
C0 =  40   vs   C3 =  40      OK
C1 = 240   vs   C2 = 160      FAILS  -- and 240 - 160 = 80 = |chi|
```

The failure is *exactly* the Euler characteristic. Worse, on the physical sector
itself `⋆` would map `H¹ → H²`, and **`b₂ = 0`**. So:

> **The 81 physical modes have no Hodge dual. There is no `⋆F`, hence no
> `F ∧ ⋆F` action, hence no variational dynamics on this complex.**

This is a real constraint on the programme. The substrate gives the *kinematics*
of gauge theory (a clean gauge/physical/constraint split) and withholds the
*dynamics* (no metric, no volume form, no action). Any physical reading must
supply `⋆` from outside — which is exactly the missing ingredient the repository's
own evidence tiers describe as "the map that must be built".

### The Einstein claim, checked

`w33_paper_body.tex §Bose–Mesner as Einstein's Equation` asserts
`A² + λA − 2^q I = μJ`. It is **exactly true**: for `SRG(40,12,2,4)`,
`A² = 12I + 2A + 4(J−I−A)`, i.e. `A² + 2A − 8I = 4J`, with `k − μ = 8 = 2³`. The
paper itself calls the Einstein labelling "a dimensional shadow", and that is the
right description — the identity lives in the 3-dimensional Bose–Mesner algebra
`⟨I, A, J⟩`, and a *field* equation needs a variational principle, which needs a
measure, which needs `⋆`. Pass 1448 says `⋆` is not there.

### The optics dictionary, made concrete

| operation | on the complex | photonic realisation |
|---|---|---|
| dot product `⟨a,b⟩` | sum over 240 edges | balanced-homodyne overlap; the intensity difference at a 50:50 beamsplitter's two ports |
| wedge / cup `a ∧ b` | `C¹ × C¹ → C²`, `(a∧b)(ijk) = a(ij)b(jk)` | a **product of two amplitudes** — unreachable with linear optics; needs `χ⁽²⁾` nonlinearity |
| Hodge `⋆` | `C_k → C_{3−k}` | a π/2 quadrature rotation (`⋆² = −1` ↔ two quarter-wave plates = a sign flip) |

The dictionary makes the obstruction concrete rather than abstract: **the missing
`⋆` is the missing phase reference.** A linear interferometer computes dot
products for free, the cup product costs a nonlinearity, and the Hodge star — the
thing this complex does not have — is precisely the element an optical
implementation would have to supply as an external local oscillator.

---

## Pass 1449 (physics) — the harmonic sector is a *signed* object, and that is why

The harmonic subspace was computed independently in GAP: `dim = 81`, confirming
`b₁` by a second route. Its **character could not be computed** with the
unsigned permutation action — `Permuted(basis, g)` leaves the space.

That is not a bug to route around; it is the finding. Cycles carry orientation,
so the harmonic sector lives in the **orientation-signed** edge module, not the
permutation module. Which means:

> The harmonic 81 and `ker(K−10I)` are invisible to unsigned reasoning **for the
> same reason**. Pass 1412 failed on exactly this, and Passes 1416–1420 fixed it
> with a signed intertwiner.

So "harmonic = Steinberg" is **not established here** — it needs the signed
character, precisely as `ker(K−10I)` did. Recorded as open rather than asserted.

In the optics dictionary this is the statement that **the physical modes carry a
phase, not just an intensity**: an intensity-only (unsigned) description cannot
see the physical sector at all.

---

## Pass 1450 — BT773 is right, in `PGSp(4,3)`

Pass 1442 noted `PSp(4,3)` has only 315 involutions (classes 270, 45), so BT773's
"540 cubes, one per 3A₁ involution" could not be counted there. Settled:

```text
PSp(4,3),  order 25920 : involution classes  45, 270          total 315
PGSp(4,3), order 51840 : involution classes  36, 45, 270, 540 total 891
                                                        ^^^ a class of exactly 540
```

**BT773 is vindicated and its group is now named.** The 540 frames correspond to
the 540-element involution class of the *full* group `PGSp(4,3)`, consistent with
BT773's own `51840 = 540 × 2 × 48`. The scope note from Pass 1442 stands as a
narrowing, not a refutation.

---

## Pass 1451 — the `C₂` involution's fixed frames are enriched inside a cover

```text
fixes 84 of the 540 frames globally      = 15.6%
fixes 12 of a stabilised cover's 60      = 20.0%
enrichment                               = 1.29x
540 = 84 + 2*228   (84 fixed + 228 transpositions)  ✓
```

A `C₂` cover's twelve fixed frames are *not* a random slice of the 84 — they are
over-represented by 1.29×. That enrichment is the structure that would explain why
83% of covers are `C₂`-stabilised, and it is **not yet explained**.

---

## Pass 1452 — BT1509 was compiling only by accident

`BT1509_census_morita_m20_insert.tex` uses `\PSp` and defines nothing. It is
`\input` by both manuscripts at line 10 — immediately after `BT1408` at line 9,
which my portability fix had given `\providecommand{\PSp}`. **Both manuscripts
were compiling only because my insert happens to come first.** Reorder or remove
`BT1408` and both builds break.

My own portability sweep missed it because it scans **orphans**, and BT1509 is
promoted. Guard added directly; BT1509 now compiles standalone (0 errors in a
bare host), and both manuscripts still build clean.

---

## Pass 1453 — what is NOT done

Two of my five remain open and are stated as open rather than quietly dropped:

- **Re-attacking the intersecting-family result from the `C₂`-heavy region.** Pass
  1441's "no two covers are disjoint" rests on a sampler known to under-draw
  exactly that region. The re-attack — seeding from a class-45 involution's 84
  fixed frames — is designed but not run.
- **Why the intersection floor is exactly 4.** No counting argument yet. Two
  covers sharing `k` frames agree on `4k` edges and must re-cover the remaining
  `240 − 4k` disjointly from both sides; why `k = 0,1,2,3` are all impossible is
  not established.

---

## Pass 1454 — the honest summary of the physics

The substrate delivers, exactly and without fitting:

- a gauge/physical/constraint split `39 ⊕ 81 ⊕ 120` on 240 edges;
- a physical sector of dimension `81 = 3⁴`;
- a Bose–Mesner identity that is algebraically exact;
- `χ = −80`, `b₂ = b₃ = 0`.

It does **not** deliver a Hodge star, hence no volume form, no action, no
dynamics — and the obstruction is quantitative (`240 ≠ 160`, by exactly `|χ|`)
rather than a matter of interpretation. That is the sharpest statement this
programme can currently make about its own physics: **kinematics yes, dynamics
no, and here is the exact missing object.**

## Prior art

- [Pass 682](analysis/w33_pass682_flatblock_h1_branch_separation.py) — **owns** `H₁ = Z^81` and `H₁ = ker(K+6I)`.
- [BT773](analysis/BT773_involution_cube_theorem.md) — **owns** the 540/involution bijection, vindicated above in `PGSp(4,3)`.
- Passes 1416–1420 (parallel track) — **own** the signed intertwiner whose necessity Pass 1449 re-derives from a second direction.
- `w33_paper_body.tex §Bose–Mesner as Einstein's Equation` — the identity checked above.
