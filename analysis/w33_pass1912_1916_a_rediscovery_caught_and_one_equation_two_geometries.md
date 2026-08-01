# Passes 1912–1916 — a rediscovery caught by the check I flagged, and one equation giving two classical geometries

Five items. The first is the one that matters, and it is a retraction.

---

## Pass 1912 — `q ≡ 3 (mod 4)` is **Gow's theorem**, not ours

Pass 1907 concluded that `PSp(4,q)` has complex-type irreducibles exactly when
`q ≡ 3 (mod 4)`, and I flagged it as needing a literature check before it
propagated. Doing the check:

> **When `q ≡ 1 (mod 4)` all irreducible complex characters of `Sp(2n, F_q)` are
> real-valued; this fails when `q ≡ 3 (mod 4)`.**
> — R. Gow, *Real representations of the finite orthogonal and symplectic groups
> of odd characteristic*, J. Algebra **96** (1985), 249–274.

**Pass 1907 is a rediscovery.** The statement is classical, holds for all `n` (not
just `n = 2`), and my `q = 3,4,5,7,9` computation is a re-derivation of a special
case. It is retracted as a novel claim and retained as a verification.

This is failure mode 5 from `CLAUDE.md`, and it is worth noting *how* it was
caught: not by the guard, not by grepping the corpus — the result is not in the
corpus — but by the one line I wrote into Pass 1911's "still open" saying it
needed a literature check before being called ours. **The check is the control,
and it only works if the flag is acted on rather than admired.**

### The genuinely useful thing the search returned

Vinroot's work on *twisted* Frobenius–Schur indicators shows that for `Sp(2n,q)`
with `q` odd there is an involutory automorphism `ι` for which the twisted
indicator `ε_ι(χ) = 1` for **every** irreducible character — a single framework
covering both congruence classes, where the classical indicator splits them.

That is the established setting for Pass 1900. My outer involution of `W(E₆)` is
exactly such an involutory automorphism, so "the outer `ℤ/2` signs the real blocks
and fuses the complex ones" is the classical-indicator shadow of a twisted
indicator that is uniformly `+1`. The right move is to cite that framework rather
than re-derive around it.

---

## Pass 1913 — one equation, two classical geometries, split by a quadratic character

Pass 1908 found the spreads among the solutions of `g² = μI` in `GSp(4,3)`.
Splitting *all* solutions by the multiplier:

```text
g^2 = 2I in GSp(4,3) : 612 solutions

  SQUARE multiplier     : 540 -> 270 images, ALL INNER
       class size 270, order 2, fixing 0 points
       = the 270 ordered incident line-pairs of the cubic surface (Pass 1875)

  NON-SQUARE multiplier :  72 ->  36 images, ALL OUTER
       class size 36
       = the 36 spreads (Pass 1908)
```

> **The quadratic character of the multiplier splits the solutions of `g² = μI`
> into the 270 incident line-pairs of the cubic surface and the 36 spreads.**

One equation, two classical objects, separated by a single quadratic character —
and the same character decides inner versus outer. The 27 lines and the spreads
had appeared in this project as unrelated objects reached by unrelated routes;
they are the two halves of one solution set.

---

## Pass 1914 — the phase-carrying degree generalises

If the phase sector is structural rather than a `q = 3` accident, its degree
should follow a formula. For `q = 3` the complex pair has degree 45, and
`q²(q²+1)/2 = 9·10/2 = 45`:

```text
q=3 : non-real degrees {5, 10, 30, 40, 45}
      q^2(q^2+1)/2 = 45     present: TRUE
      (q^2+1)/2    = 5      present: TRUE
q=7 : non-real degrees {25, 150, 900, 1050, 1200, 1225, 1600}
      q^2(q^2+1)/2 = 1225   present: TRUE
      (q^2+1)/2    = 25     present: TRUE
```

> Both `q²(q²+1)/2` and `(q²+1)/2` are complex-type at `q = 3` **and** `q = 7`.

So the family carrying the substrate's phase is not special to `q = 3` — it
recurs at the next `q ≡ 3 (mod 4)`. Stated as a two-point pattern with a formula,
not as a theorem: two values fit, and given Pass 1912 the honest expectation is
that this is also classical and should be checked against the same literature
before being claimed.

---

## Pass 1915 — symmetry tuning does not help

The spread-variable encoding is symmetry-bound (Pass 1887), so `CP-SAT`'s own
symmetry detection was the obvious lever:

```text
symmetry_level=0 : UNKNOWN   626,356 branches,    124 conflicts
symmetry_level=2 : UNKNOWN 2,899,802 branches, 89,935 conflicts
symmetry_level=4 : UNKNOWN   678,777 branches,    128 conflicts
```

No level decides it, and level 2 is actively worse in branches while producing
far more conflicts. The solver's generic symmetry machinery is not finding the
`51840`-element geometric group. Negative, and it closes off a cheap hope.

---

## Pass 1916 — the mean-as-max sweep

Pass 1896 promoted an average to a bound; Pass 1910 came close to repeating it.
Sweeping both tracks' analysis files for the pattern found **one** instance, the
already-known one: the description of the unsound Pass 1887 model in the Passes
1882–1887 write-up. A correction pointer has been added there in place, so the
record no longer states the false bound without an immediate retraction beside
it.

Every other hit (`45/9`, `540/9`, `240/9`) occurs inside the correction
write-ups themselves, correctly labelled as a mean. **No second live instance.**

---

## Prior art

- **Gow (1985)**, J. Algebra 96, 249–274 — **owns** the `q mod 4` reality
  theorem that Pass 1907 rediscovered.
- Vinroot, *Twisted Frobenius–Schur indicators of finite symplectic groups* — the
  framework Pass 1900 should be phrased in.
- Pass 1875 — **owns** the 270 incident line-pairs; Pass 1908 — the spreads;
  Pass 1913 joins them.
- Pass 1896 — the error Pass 1916 sweeps for.

## Still open

- `χ(H) = 9`. Long run in flight; symmetry tuning ruled out.
- Whether the `q²(q²+1)/2` pattern is also classical — check before claiming.
- Whether any of the other four `q = 3` complex pairs (5, 10, 30, 40) is
  realisable in *some* `W(3,3)` module, given Pass 1909 showed permutation
  modules can carry none.
