# Passes 1491–1495 — both Hoffman bounds are tight, and H's 4-eigenspace IS the Steinberg

Five items. The resolution question finally has a theory behind it, and the frame
graph turns out to carry the physical sector directly.

---

## Pass 1491 — every exact cover is Hoffman-tight, and covers ARE maximum independent sets

An independent set of `H` is a set of frames pairwise not sharing an edge — i.e.
pairwise disjoint matchings. The maximum size is 60 and `60 × 4 = 240`, so:

> **Maximum independent sets of `H` are exactly the exact covers.**

`H` is 32-regular with spectrum `32¹, 14⁴⁴, 8¹⁵, 4⁸¹, 2⁸⁴, (−4)³¹⁵`, and **both**
Hoffman bounds are met with equality:

```text
chi(H)   >= 1 - d/lambda_min      = 1 - 32/(-4)   = 9    <- a resolution needs 9
alpha(H) <= n(-lambda_min)/(d-lambda_min) = 540*4/36 = 60   <- a class has 60
```

Verified directly on a known cover: `‖A v − λ_min v‖ = 1.5 × 10⁻¹⁴` for
`v = χ_S − (60/540)·1`. So **every cover's centred indicator lies in the
`(−4)`-eigenspace**, and a resolution is nine such vectors in a 315-dimensional
space summing to zero.

That is a *linear* condition the SAT encoding knows nothing about, and it explains
why five searches failed: the solution space, if nonempty, is ratio-tight in both
parameters simultaneously — a rare and very thin configuration.

---

## Pass 1492 (physics) — `H`'s 4-eigenspace is the Steinberg, proved

`H` is a `G`-graph, so its eigenspaces are `G`-modules. The 540-frame permutation
module decomposes as

```text
1 + 15x3 + 20x2 + 24x2 + 30x4 + 60 + 64 + 81x2   = 540
```

The 4-eigenspace has dimension 81, so it is a sum of constituents summing to 81.
Excluding the trivial — which is the Perron eigenvector at eigenvalue 32 — the
available degrees are `15,15,15,20,20,24,24,30,30,30,30,60,64`, and:

```text
ways to write 81 as a sum of those degrees : 0
```

**So the 4-eigenspace must be a single degree-81 irreducible.** Not inferred from
a matching dimension — forced, because no other combination reaches 81.

> **The frame graph's 4-eigenspace is the Steinberg module.**

The physical sector of the gauge theory (Pass 1455), the cokernel of the frame
cross-matching (Pass 1397), and now an eigenspace of the frame adjacency graph
are the same 81. Three independent routes, one module.

For contrast the other eigenspace dimensions are *not* forced: 44 has four
decompositions, 84 has forty. Only the 81 is rigid.

---

## Pass 1493 — the two CNFs agree to the clause

The parallel track's Pass 1521 built the same encoding independently. Comparing
structurally, without reading their solver output:

```text
per-frame       540 * (1 + C(9,2))   = 19,980
per-edge-class  240*9 * (1 + C(9,2)) = 79,920
total predicted                        99,900
mine reported                          99,909   (the 9 extra are symmetry-break units)
```

Two independent derivations of the same instance, agreeing to the clause. Neither
has a verdict; mine is still running.

---

## Pass 1494 — `results_in` is a bundle, and should be split before it is cut

Pass 1488 condemned `group_tokens` at 81.5% and fixed it with a calibrated rarity
cut. The obvious next question is whether `results_in`, at 63%, needs the same.

```text
cut     flag rate
   8       0.0%
  20       7.1%
  25      14.3%
  40      21.4%
none      64.3%
```

A cut would work numerically — and it would be the wrong move. `results_in`
**bundles** several classes: code parameters, slash-sequences, named objects,
compounds, and noun-number pairs. Pass 328 calibrated only the *code-parameter*
part, at 20%. The 63% is a calibrated component plus uncalibrated ones, and a
blanket cut would penalise the part that was already correct.

**Split before cutting.** Recorded as a recommendation rather than applied,
because applying it blind is exactly the error Pass 1488 was about.

---

## Pass 1495 — the sign result, in both manuscripts

`BT1408` now carries a proposition stating that the two degree-81 extensions
differ on six outer classes, two of which are geometric involution classes:

```text
class          size   object    separation
involutions     540   frames    chi = -+3
involutions      36   spreads   chi = -+9   (maximal)
```

with the supporting facts — the size-36 class has centraliser order
`1440 = |PGSp|/36`, fixes no point and exactly ten lines, and a spread is exactly
ten pairwise disjoint lines covering all forty points — plus the full-group
decomposition `15 ⊕ 24 | 81 | 30 ⊕ 90`.

```text
w33_paper.tex        0 errors
photonic_holonet.tex 0 errors
```

## Prior art

- Pass 1521 (parallel track) — the independently built CNF, and the `hoffman` filename that pointed at the ratio bound.
- [Pass 1455](analysis/w33_pass1455_1459_harmonic_is_steinberg_and_a_refutation_of_my_own.md) and [Pass 1397](analysis/w33_pass1397_1401_cokernel_theorem_covers_collisions.md) — the other two routes to the same 81.
- Pass 328 — **owns** the calibration Pass 1494 declines to over-apply.
