# Passes 1951–1955 — a checker that caught itself twice, and a fifth instance of the pattern

Five items. The first is a tool built to stop a recurring error, which then
committed that error twice during construction and was caught both times by its
own self-test — and then the error recurred a fifth time, one line downstream.

---

## Pass 1951 — `assert_cuts`, and its two self-inflicted failures

Four times in this arc I added something shaped like a constraint that was not
one: heredoc escapes eaten into backspace bytes; the `k<9` symmetry break reused
outside its regime; `|class ∩ K₁₀| ≤ 5`, an average promoted to a bound; and
twice `x[i] ≤ x[g[i]] + 8` over a domain of `0..8`, true for every assignment.

All four have one shape — **it looks like a restriction and restricts nothing** —
and one cheap test catches all of them: *does this constraint remove at least one
assignment that was feasible without it?*

Building that test produced the error twice more:

- **v1** compared solution counts against a cap of 200. Both sides hit the cap,
  so a genuine constraint and a vacuous one scored identically.
- **v2** drew base solutions and asked whether the constraint rejected any. But
  CP-SAT enumerates systematically, so the first 25 solutions of an
  all-different model all satisfied `x0 < x1`, and a *real* constraint read as
  vacuous.

Both are the same failure the function exists to detect, committed inside the
detector. Both were caught only because it carries a self-test on a known-vacuous
and a known-real constraint:

```text
v3:  VACUOUS  x <= 8 over domain 0..8      solutions 504 -> 504
     CUTS     x0 < x1                      solutions 504 -> 252
     verdict: vacuous detected = True, real detected = True
```

> **A checker without a self-test would have shipped, twice.** The self-test is
> not decoration — it is the only thing that distinguished a working detector
> from two broken ones that produced confident output.

---

## Pass 1955 — the geometric lex constraint, verified real for the first time

With a working checker, the constraint that failed three previous attempts:

```text
collineation generators : 40
CUTS  geometric lex-leader on generator 0   solutions 19,355 -> 16,145
```

**It genuinely cuts** — a 17% reduction on the witness model. This is the first
time in this arc that a geometric symmetry break has been demonstrated to do
anything at all.

### And then the fifth instance

The full-model run reported below was assembled **without** the verified
constraint — the branch that builds it adds the clique pinning and the
`AllDifferent`s and never calls `add_lex`:

```text
STATUS UNKNOWN [300 s, 1,883,266 branches, 377,707 conflicts]
```

So that number is the plain pinned model again, and it says nothing about the
geometric break. The failure mode did not go away; **it moved** — from "the
constraint is vacuous" to "the verified constraint was not added." The checker
did its job and the model assembly did not.

Recorded rather than quietly rerun, because a fifth instance of the same family
of error is more informative than a sixth attempt. The next attempt should
assert, inside the solve, that the model's constraint count rose.

---

## Pass 1952 — the internal symmetry group of `V`, in full

From the multiplicity-free split (Pass 1945):

```text
End_PSp(V) = R x R x R x R x C        dim_R = 6
finite unit group = {+-1}^4 x Z6      order 96
```

> The substrate's complete group of internal symmetries — endomorphisms
> commuting with `PSp(4,3)` — is abelian of order **96**, and all of its
> non-`±1` content is the `ℤ₆` on the flux sector.

That places the `ℤ₆` precisely: it is not one symmetry among many, it is the
*only* internal symmetry beyond block signs.

---

## Pass 1953 — the cross-track separator confirms colourlessness

The parallel track's Pass 1943 separates the two `V₉` carrier copies by

```text
A_24 |-> (Hodge eigenvalue 10, character field Q)
A_90 |-> (Hodge eigenvalue  4, character field Q(omega))
```

The 24-sector copy has **rational** character field; the 90-sector copy has
`ℚ(ω)`. Since `ω` acts only where the field is `ℚ(ω)`, this is an independent
confirmation of Pass 1945's prediction: **the `ℤ₃` acts on the 90's copy and not
the 24's.** Two tracks, different methods, same split.

---

## Pass 1954 — the two `ℤ₆`s: one identified, one still open

There are now three order-6 Eisenstein objects in play:

| object | source | status |
|---|---|---|
| `ℤ[ω]^×` in `End_PSp(90)` | this track, Pass 1933 | — |
| `U₆`, "the sixth-order Eisenstein unit on `B+C`" | parallel Pass 1942 | **same `End`; the same `ℤ₆`** |
| `C⁵` hexagons, `240 → 40` | BT1745–1751 | **different construction, unverified** |

The parallel track's `U₆` acts on the same `V₉` copies inside the same
endomorphism ring, so it is this `ℤ₆`. The `E₈` Coxeter `C⁵` fibration is built
from a power of a Coxeter element rather than from an endomorphism ring, and no
map between them is exhibited on either track. That one stays open.

A useful negative from their side: `ℤ[R₄, U₆] = M₃(ℤ)`, with no quaternionic
order and no finite `SU(2)` enhancement — so the `ℤ₆` does not sit inside a
larger arithmetic structure that would give it more physical room.

---

## Prior art

- Passes 1896/1910/1924/1938/1946 — the four earlier instances of the vacuous
  constraint pattern that Pass 1951 generalises.
- Pass 1945 — the endomorphism split Pass 1952 completes and Pass 1953 confirms.
- Passes 1939–1943 (parallel track) — **own** the `A₂₄`/`A₉₀` Hodge-and-field
  separator, the `M₃(ℤ)` classification, and the independent refutation of the
  Gauss-law charge argument.
- BT1745–1751 — **own** the `E₈` `C⁵` hexagon fibration.

## Still open

- `χ(H) = 9`, with a geometric break that is verified *and* actually added.
- Whether the endomorphism `ℤ₆` and the Coxeter `C⁵` `ℤ₆` are the same.
- What the `ℤ₆` is physically, now that both flux (Pass 1944, no torsion) and
  charge (Pass 1943, wrong sector) are ruled out.
