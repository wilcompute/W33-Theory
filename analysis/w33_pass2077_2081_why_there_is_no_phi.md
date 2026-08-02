# Passes 2077–2081 — why there is no golden ratio, and the phase/obstruction incompatibility is total

The user asked where `φ` could come from. The honest answer is a structural
impossibility rather than a failed search — and the same batch closes the
two-`i` question.

---

## Pass 2077 — `φ` needs exponential growth; this substrate has none

`φ` is the root of `x² = x + 1`. Everywhere it appears it is a **growth rate**:
the entropy of the golden-mean shift (forbidden word `11`), the Perron root of
`[[1,1],[1,0]]`, the limit `F(n+1)/F(n)`, the ratio in a self-similar nested
rectangle. All are statements about **exponential** growth.

The repo's towers:

```text
genus oscillator      v = 4+3h, E = 6+15h, F = 4+10h     LINEAR in h
genus                 g = (n−3)(n−4)/12                   QUADRATIC in n
complete-adj ladder   n = 3,4,7,12,15,16,19,24,...        density 1/3, LINEAR
```

> **A finite object has no growth rate, and every tower here grows
> polynomially.** `φ` requires exponential growth. That is why Pass 2068 found no
> golden eigenvalue — not bad luck, a structural impossibility.

The user's two suggested sources are exactly the ones this rules out. The nested
golden rectangle is a *geometric series* — an infinite self-similar recursion. The
`108°` logarithmic spiral is *exponential in the angle*. Both need an infinite
multiplicative structure; `W(3,3)` is a finite incidence geometry and its towers
are arithmetic progressions.

If `φ` enters this project at all it must be through a **metric realisation** —
an embedding into Euclidean space where lengths and angles exist — not through
the combinatorics. The repo's toroidal-metric lane is where that would live.

---

## Pass 2078 — the `108`, and why it is a count match

`108°` is the regular pentagon's interior angle and the golden gnomon's apex.
`108` also occurs in `W(3,3)`:

```text
frames through a point : 108   (all 40 points)
                       = (q+1) x (frames per line) = 4 x 27
                       = (q+1) q^3
```

> `108 = (q+1)q³` in the substrate; `108°` is a pentagon angle. **Different
> origins, same number** — a count match by this arc's own rule, and one I would
> have taken for a link three batches ago.

---

## Pass 2079 — but pentagonal *order* is genuinely there

`|PSp(4,3)| = 25920 = 2⁶ · 3⁴ · 5`, so elements of order 5 exist. What they do:

```text
one class, size 5184, INNER, fixes 0 points and 0 lines
point-orbit lengths : 5 x 8
```

> **The 40 points partition into eight pentagons** under an order-5 element,
> `40 = 8 × 5`, with no fixed point or line.

So pentagonal *order* is present in the group even though the golden *ratio* is
absent from the spectra. Those are different claims and this pass keeps them
separate: a cyclic group of order 5 does not produce `φ` — `φ` comes from the
`5`-fold *rotation angle* in a metric realisation, which the finite geometry does
not have.

---

## Pass 2080 — the phase/obstruction incompatibility is **total**

Pass 2076 showed `σ_S` inverts the phase. The follow-up question was whether any
of it survives — whether some subgroup containing `σ_S` keeps a complex structure
on the 90:

```text
largest subgroup containing sigma_S that admits an invariant J on the 90:
  NONE among G and its maximal subgroups
for contrast: PSp(4,3) admits J (true) and does NOT contain sigma_S (false)
```

> **No subgroup at that level holds both.** The substrate can have the phase
> (`PSp(4,3)`) or the spread involution (`σ_S`, outer) but not both. The
> incompatibility is not partial — nothing survives on a `σ_S`-invariant piece.

---

## Pass 2081 — the `q ≡ 1 (mod 4)` control case

For `q ≡ 1 (mod 4)`, some non-square `μ` still exists (`q` odd), so `σ_S` still
exists — but `μ ≠ −1`, so `σ_S` is **not** multiplication by `i`. And Pass 1907
measured that `PSp(4,q)` then has **no** complex characters at all (`S4(5)`:
non-real = 0).

> `q = 5` is a substrate with an obstruction and **no phase to lose**. It is the
> clean control for everything Pass 2076 claims: the incompatibility is only
> meaningful where both structures could exist, i.e. at `q ≡ 3 (mod 4)`.

---

## The other items, honestly

- **`i_geom`/`i_rep` at `q = 7, 11`** — not computed. The `D₄` relation was
  derived at `q = 3`; whether it holds across `q ≡ 3 (mod 4)` is untested.
- **The `D₈` reconstruction** — still blocked on GAP's recursion trap. Fourth
  report as incomplete.
- **Sending results to the other track** — the two statements to send are Pass
  2062 (`q+1 = 4`) and Pass 2071/2076 (the `q ≡ 3 mod 4` unification and the
  two-`i` incompatibility). Not yet written as a cross-track note.

---

## Prior art

- Pass 2068 — the measured absence of golden structure that this pass explains.
- `dccxxiii` — the genus oscillator; BT1844 — the ladder.
- Pass 1907 — `PSp(4,q)` complex characters iff `q ≡ 3 (mod 4)` (Gow).
- Pass 2076 — the two-`i` incompatibility this completes.
- The golden-spiral and `108°` suggestions are the user's.

## Still open

- `χ(H) = 9`.
- Whether a metric realisation of `W(3,3)` has golden structure — the only place
  left for it.
