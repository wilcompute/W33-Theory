# Passes 1897–1901 — the outer involution **is** complex conjugation, and `σ_S` is one equation

Five items. Two of them turn verified patterns into derivations, and one answers
"what is this `ℤ/2` actually doing" with a single sentence.

---

## Pass 1900 (physics) — the outer `ℤ/2` of `W(E₆)` is complex conjugation on `Irr(PSp(4,3))`

The outer involution had accumulated three apparently separate jobs: it separates
the two Steinberg extensions (chirality), it conjugates the two degree-45s and so
destroys the constraint sector's phase, and it is the coset containing both
geometric reader classes. Asking what it does *globally*:

```text
Irr(PSp(4,3))                        : 20 irreducibles
non-real-type (FS <> 1)              : 10, degrees 5,5,10,10,30,30,40,40,45,45
irreducibles that FUSE under the outer: 10, degrees 5,5,10,10,30,30,40,40,45,45
SETS EQUAL                           : TRUE
```

> **An irreducible of `PSp(4,3)` fuses under the outer automorphism exactly when
> it is of complex type. The outer `ℤ/2` of `W(E₆)` acts as COMPLEX CONJUGATION
> on `Irr(PSp(4,3))`.**

That collapses the three jobs into one. Conjugation acts trivially on real-type
characters, so on those blocks the outer element can only *sign* them — that is
the chirality bit. On complex-type characters it exchanges conjugates — that is
the fusion, and fusing a conjugate pair is precisely what destroys an invariant
complex structure. **Chirality and phase are the real and the complex parts of a
single conjugation.**

The substrate sits in this picture cleanly:

```text
15, 24, 30, 81 : SIGNED  (extend; each carries a chirality bit)
90             : FUSED   from 45 + 45, both of complex type
```

Four signed, one fused — the two modes, and nothing else.

**A hoped-for stronger claim, refuted.** I expected the 45-pair to be the group's
*only* complex pair, which would have made the substrate's unique phase a
property of the group. It is not: there are **five** conjugate pairs (degrees 5,
10, 30, 40, 45). The substrate's edge module happens to contain exactly one of
them. Checked before claiming.

---

## Pass 1899 — `σ_S` in one equation, with both branches of the parity dichotomy

Passes 1877/1882/1894 built `σ_S`, verified it is a collineation, and showed it
generates `Z(Stab(S))`. Recovering the matrix that induces it:

```text
q=3 : g^2 = mu I, mu = 2, squares mod 3 = {1}       -> mu NON-SQUARE
q=5 : g^2 = mu I, mu = 2, squares mod 5 = {1,4}     -> mu NON-SQUARE
q=7 : g^2 = mu I, mu = 5, squares mod 7 = {1,2,4}   -> mu NON-SQUARE
```

> **`σ_S` is induced by a symplectic `g` with `g² = μI`, `μ` a non-square in
> `F_q*`.**

That is the whole theorem, both directions:

- **`g` is fixed-point-free.** A projective fixed point needs `gv = λv`, hence
  `λ² = μ` with `λ ∈ F_q` — impossible when `μ` is a non-square.
- **`q` even has no `σ_S`.** In a field of characteristic 2 every element is a
  square, so no such `μ` exists. Hence no `σ_S`, hence no candidate frames,
  which is exactly the zero-candidate `q = 2` branch measured in Pass 1877.

One equation replaces three verified data points, and `x² − μ` irreducible means
`g` gives `F_q⁴` an `F_{q²}`-structure whose lines are the spread — the classical
Desarguesian construction, arrived at from the obstruction rather than assumed.

---

## Pass 1898 — the sound version of the bound I got wrong

Pass 1896 showed my asserted `|class ∩ K₁₀| ≤ 5` was false. Replacing the guess
with exact optimisation over actual exact covers:

```text
max |cover cap K10| : 13   (FEASIBLE at 300 s; 13 is attained, optimality not proved)
min |cover cap K10| :  1   (FEASIBLE at 330 s)
```

The nine classes partition the `K₁₀`'s 45 frames, so the *average* is `45/9 = 5`.

> **5 was the mean, not the maximum.** The true spread runs at least `1 … 13`
> around it.

That is the error in one line: I promoted an average to a bound. And it is
precisely the family for which that promotion is least defensible, since Pass
1818 measured the spread family's non-uniformity at `0.9535`.

---

## Pass 1897 — the long run

The spread-variable encoding of Pass 1892 (60,909 branches vs 2.1M for the plain
model) is running with a five-hour cap rather than ten minutes. Reported as
launched, not as a result.

---

## Pass 1901 — the underived-bound sweep

Pass 1896 caught one assumption published without proof, so I swept my own
analysis scripts for asserted inequalities. The hits in recent work are
`add_at_most_one` idioms and loop caps, not mathematical claims; the older
`w33_pass18x` files use `>= 0` and `<= 6` as domain declarations. **No second
instance of the Pass 1896 error was found.**

Recorded as a clean sweep rather than skipped — a negative audit result is worth
the same as a positive one, and the sweep is now a script that can be re-run.

---

## Cross-track note

The parallel track's Passes 1887–1891 construct an exact exceptional-`S₆`
equivariant `J` gluing the `24`- and `90`-sector `V₉` copies, with
`J(A₂₄v) = A₉₀v` and `J² = −I`, and explicitly reconcile it against the
`PSp(4,3)` complex `45 + 45̄` decomposition from Passes 1885/1895. Two remarks
from this side:

- Their `J` lives on a paired `V₉` inside `24 ⊕ 90`, which is a *different*
  object from the `J` on the whole 90 — mine needs only `PSp(4,3)` and is unique
  up to sign (Pass 1895), theirs needs the `S₆` restriction. Both are real; they
  are not the same structure and should not be merged.
- Pass 1900 explains why their `24` and `90` pair up at all: those are the only
  two blocks the outer involution treats differently from each other, one signed
  and one fused.

---

## Prior art

- Passes 1877/1882/1894 — the `σ_S` chain Pass 1899 completes.
- Pass 1885/1895 — the complex 45-pair Pass 1900 places in the group's global
  picture.
- Pass 1818 — the non-uniformity measurement Pass 1898's correction rests on.
- Pass 1896 — the error Pass 1898 repairs and Pass 1901 sweeps for.
- Passes 1887–1891 (parallel track) — **own** the `S₆`-equivariant paired `V₉`
  complex structure.

## Still open

- `χ(H) = 9`. Long run in flight.
- Proving `max |class ∩ K₁₀| = 13` rather than `≥ 13`.
- Whether "outer = complex conjugation" holds for `PSp(4,q)` generally, or is
  special to `q = 3`.
