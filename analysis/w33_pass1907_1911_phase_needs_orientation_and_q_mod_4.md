# Passes 1907–1911 — a phase needs orientation *and* `q ≡ 3 (mod 4)`, and `σ_S` is a similitude

Five items. One is a refutation of my own last headline, one is a correction of
imprecise language in it, and together they turn "the substrate has a phase" into
two independent necessary conditions.

---

## Pass 1907 — "outer = complex conjugation" is a `q = 3` fact, and phase itself is `q ≡ 3 (mod 4)`

Pass 1900 found that in `PSp(4,3)` the irreducibles that fuse under the outer
automorphism are exactly the complex-type ones. Testing whether that is general:

```text
S4(5) : non-real irreducibles 0, fusing 14   SETS EQUAL: FALSE
```

**It fails at `q = 5`, and for a blunt reason** — `PSp(4,5)` has *no* complex-type
irreducibles at all, yet 14 still fuse. So the fusion there is not conjugation,
and the elegant `q = 3` identification does not generalise. My Pass 1900 headline
is a statement about `PSp(4,3)`, not about symplectic groups.

Chasing the blunt reason gives a better result:

```text
S4(3)  |G|=25920        non-real 10   degrees 5,5,10,10,30,30,40,40,45,45
S4(4)  |G|=979200       non-real  0
S4(5)  |G|=4680000      non-real  0
S4(7)  |G|=138297600    non-real 18   degrees 25,25,150,...,1600,1600
S4(9)  |G|=1721606400   non-real  0
```

> **`PSp(4,q)` has complex-type irreducibles exactly when `q ≡ 3 (mod 4)`**
> (tested `q = 3, 4, 5, 7, 9`) — the condition for `−1` to be a non-square in
> `F_q`.

So no `W(q,q)` substrate with `q ≡ 1 (mod 4)` or `q` even can carry a phase in
*any* sector, because the group has no complex representation to carry it.
`q = 3` is the smallest `q` where a phase is possible at all.

---

## Pass 1909 (physics) — a phase requires **orientation**

Of the five complex pairs in `PSp(4,3)` (degrees 5, 10, 30, 40, 45), which are
actually realised?

```text
appearing in the SIGNED 240-edge module          : 45, 45
appearing in the 40-point / 40-line permutation modules : none
```

The second line is not an accident and does not need searching: **a permutation
module is a real module**, since it has a canonical basis permuted by the group,
so it can contain no complex-type constituent whatever.

> **A phase can only live in an orientation-signed module.** Permutation modules
> — points, lines, octets, spreads, frames, the 270 incident pairs — are all real
> and can carry none. In `W(3,3)` the signed edge module carries exactly one of
> the five available pairs, the 45s.

That is the mechanism linking two things that had looked separate all arc: the
orientation sign on edges is not bookkeeping, it is the *only* thing that makes a
phase possible. Combined with Pass 1907, the substrate needs `q ≡ 3 (mod 4)` for a
phase to exist in the group and an orientation to realise it in a module. Two
independent necessary conditions, and `W(3,3)` satisfies both.

---

## Pass 1908 — `σ_S` is a **similitude**, and the 36 are exact

Pass 1899 said `σ_S` is induced by "a symplectic `g` with `g² = μI`, `μ` a
non-square". The word symplectic was wrong — `σ_S` is *outer* in `PGSp(4,3)`, and
outer elements are not symplectic. Counting properly in `GSp(4,3)`:

```text
elements of GSp(4,3) with g^2 = 2I           : 612
   of multiplier 1 (symplectic, hence INNER) : 540
   of NON-SQUARE multiplier (hence OUTER)    :  72
distinct images in PGSp(4,3)                 :  36
   all outer                                 : TRUE
   all fixed-point-free on the 40 points     : TRUE
   class sizes                               : {36}
```

> **The 36 spread involutions are exactly the images of the 72 symplectic
> similitudes with `g² = μI` and non-square multiplier.** A bijection with the 36
> spreads, not merely matching counts.

The corrected condition does double duty, which is why it was worth getting
right: a **non-square multiplier** is precisely what makes `g` outer in `PGSp`,
and `g² = μI` with `μ` a non-square is precisely what makes `g` fixed-point-free.
One equation delivers both, and in characteristic 2 there are no non-squares, so
neither holds — the `q = 2` branch again.

A bonus that closes an older loop: the *other* 540 elements, the symplectic ones
with `g² = −I`, generate **270** cyclic subgroups with normaliser of order 192.
That is exactly the size-270 class and its `D₈ × S₄` centraliser from Passes
1863/1875 — so the 270 ordered incident pairs of the 27 lines are the *inner*
half of the same equation whose outer half is the spreads.

---

## Pass 1911 — the two complex structures are independent, proved

The parallel track has an `S₆`-equivariant `J` on a paired `V₉` inside `24 ⊕ 90`;
Pass 1895 has a `PSp(4,3)`-invariant `J` on the whole 90, unique up to sign. Are
they related?

```text
the order-1440 maximal        : C2 x S6
contained in PSp(4,3)         : FALSE
its intersection with PSp     : order 720
```

The exceptional `S₆` **meets the outer coset**. The outer element sends `J ↦ −J`
(Pass 1900), so no `S₆`-invariant complex structure can be my `J` restricted.

> **The two `J`'s are genuinely independent objects**, not one restricted from
> the other. Mine needs only `PSp(4,3)` and is canonical up to sign; theirs needs
> a group that is not inside `PSp` and lives on a different subspace.

Recorded so the two tracks do not later merge them by name-matching.

---

## Pass 1910 — the exact `K₁₀` maximum

Pass 1898 attained `|cover ∩ K₁₀| = 13` without proving optimality. The clean
decision — is `≥ 14` feasible? — is running; result reported when it returns
rather than guessed. Pass 1896's lesson is precisely not to fill this gap with an
assumption.

---

## Prior art

- Pass 1900 — the `q = 3` identification that Pass 1907 refutes as general.
- Pass 1899 — the imprecise "symplectic" that Pass 1908 corrects to "similitude".
- Passes 1863/1875 — **own** the 270-class and its `D₈ × S₄` centraliser, which
  Pass 1908 reaches from the other side.
- Pass 1895 — the canonical `J` that Pass 1911 separates from the parallel one.
- Passes 1902–1906 (parallel track) — **own** the `S₆`-equivariant paired `V₉`
  structure and the Gaussian lattice classification.

## Still open

- `χ(H) = 9`. Long run in flight.
- Whether `max |class ∩ K₁₀| = 13` exactly.
- Whether "phase iff `q ≡ 3 mod 4`" holds beyond `q = 9`, and whether it is the
  known statement about `Sp(4,q)` character fields rather than a new one — worth
  a literature check before it is called ours.
