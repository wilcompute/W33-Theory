# Passes 1892–1896 — `σ_S` is canonical, the 90's phase is canonical, and a bound I published was false

Five items. The correction comes first, because it is about work I pushed two
batches ago.

---

## Pass 1896 — the `≤ 5` bound was **false**, and my model was unsound

The free-cuts model of Pass 1887 included the constraint that a colour class meets
each spread `K₁₀` in **at most 5** frames. I never derived it — I reasoned
`45 / 9 = 5` and assumed uniformity. Measured against real exact covers:

```text
exact covers sampled           : 60
|cover cap K10| observed range : 10 .. 13
asserted bound <= 5 holds      : FALSE
```

Covers meet a spread `K₁₀` in **ten to thirteen** frames, not five. The Pass 1887
model was therefore **unsound**. It returned `UNKNOWN`, so nothing false was
concluded from it, but an unsound model is a defect and this is the record of it.

The error is exactly backwards, and instructive. Assuming a uniform `45/9` split
*is* the free-cut argument, and that argument is valid only when a family's
indicator has zero `(−4)`-eigenvalue mass. Pass 1818 measured the spread family
at **0.9535** — the single most non-uniform family in the graph. I applied the
uniformity argument to the one family I had already proved was maximally
non-uniform.

---

## Pass 1894 — `σ_S` is unique, central, and canonical

Passes 1877/1882 built `σ_S` from the candidate frames and verified it is a
collineation. Is it *the* one?

```text
setwise stabiliser of a spread    : order 1440
subgroup fixing EACH spread line  : order 2 = C2
fixed-point-free involutions there: 1
central in the spread stabiliser  : TRUE
its G-class                       : size 36, OUTER, fixes 10 of 40 lines
```

> **The subgroup of collineations fixing every line of a spread is exactly `C₂`,
> and its generator is `σ_S`.** So `σ_S` is not a construction that happened to
> work — it is the canonical generator of the kernel of
> `Stab(S) → Sym(lines of S)`, and it generates the centre of `Stab(S)`.

The 36 such elements are exactly the size-36 outer class, closing the loop with
Pass 1485 (the class in bijection with the spreads) and Pass 1829 (one of only
two classes sensitive to all four handedness bits). The obstruction's generator,
the spread's centre, and the chirality reader are one canonically defined
involution.

---

## Pass 1895 (physics) — the constraint sector's `U(1)` is canonical

Pass 1885 showed the degree-90 is a complex representation. Is its complex
structure unique?

```text
dim_R End_PSp(90) : 2
constituents      : 45 + 45, both FS = 0, a true conjugate pair
```

A 2-dimensional real algebra containing a square root of `−1` is `ℂ`, so the
invariant complex structures are exactly the elements of `ℂ` squaring to `−1`:

> **`J` and `−J`, and nothing else. The constraint sector's `U(1)` is canonical,
> not merely available** — the only freedom is which of `±J` is called `i`, an
> orientation.

With Pass 1880 (the 81 is parity-obstructed at *every* subgroup), the substrate's
phase structure is now completely determined: exactly one sector carries a phase,
it carries exactly one, and the outer involution of `W(E₆)` is what removes it.

---

## Pass 1893 — `σ_S` cannot be prescribed either

Pass 1887 rejected every order-3 and order-9 automorphism. `σ_S` has order 2 and
is the element now known to drive the obstruction, so it was the natural
candidate:

```text
sigma_S built for all 36 spreads
rejected by the clique test : 36     accepted : 0
```

Every one fails: some 9-clique contains two frames swapped by `σ_S`. In hindsight
that is what Pass 1882 predicts — `σ_S` is what *generates* the obstruction, so
demanding a resolution respect it asks the answer to commute with its own
obstacle.

---

## Pass 1892 — branching on the spread variables: the best encoding so far, still undecided

Pass 1818 ranked the spread-pair family at `0.9535` branching value against
`0.0000` for the free cuts, and every attack so far had branched on frames.
Adding the 36×9 spread-pair counts as explicit variables and forcing the solver
to decide them first:

```text
plain CP-SAT (Pass 1887)      : 2,127,575 branches, 3,622 conflicts, UNKNOWN
free cuts added (Pass 1887)   :   255,166 branches,   163 conflicts, UNKNOWN
spread-variable branching     :    60,909 branches, 1,040 conflicts, UNKNOWN
```

**A 35× reduction in branches over the plain model**, and unlike the free-cuts
run the conflict *rate* went up — the solver is learning rather than drifting.
That is the ordering Pass 1818's measurement predicted, and it is the most
efficient encoding this project has had. It still does not decide `χ(H) = 9`.

---

## Prior art

- Pass 1818 — **owns** the branching-value measurement that both explains Pass
  1896's error and predicts Pass 1892's improvement.
- Pass 1485/1829 — **own** the size-36 class that Pass 1894 identifies as
  `Z(Stab(S))`.
- Pass 1885 — the complex structure whose uniqueness Pass 1895 settles.
- Pass 1887 — the model Pass 1896 corrects.
- Passes 1802/1827 (parallel track) — **own** the XOR/MILP falsifiers; their
  nine-frame symmetry fixing is at `k = 9` and is valid, unlike my `k < 9` reuse
  in Pass 1883.

## Still open

- `χ(H) = 9`. Three encodings, all `UNKNOWN`; the spread-variable one is now the
  cheapest and is the one to push.
- The true maximum of `|class ∩ K₁₀|`, now known to be at least 13.
- Whether `σ_S` generates `Z(Stab(S))` for every odd `q`, not just `q = 3`.
