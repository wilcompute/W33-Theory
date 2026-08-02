# Passes 2448–2453 — where the phase lives, and why every symmetric attack on `χ(H)=9` was doomed

Pass 2444 split the substrate into two non-isomorphic groups of order 51840: the
**central** doubling `Sp(4,3) = 2.U₄(2)` (chiral, carries the `E₈` tower) and the
**outer** doubling `PGSp(4,3) = U₄(2).2 = W(E₆)` (achiral, carries the codewords). This
batch asks what lives on each side.

---

## Pass 2448 — the **Weil representation straddles both doublings**

Cross-tabulating every irreducible of `2.U₄(2)` by reality against central character:

```text
FAITHFUL  (z -> -I, the CHIRAL / central side)
   real     4   degrees [20, 60, 64, 80]
   COMPLEX 10   degrees [4, 4, 20, 20, 20, 20, 36, 36, 60, 60]

INFLATED  (z -> +I, the ACHIRAL / outer side)
   real    10   degrees [1, 6, 15, 15, 20, 24, 30, 60, 64, 81]
   COMPLEX 10   degrees [5, 5, 10, 10, 30, 30, 40, 40, 45, 45]
```

The inflated complex degrees `[5,10,30,40,45]` are exactly the non-real irreducibles of
`PSp(4,3)` my Pass 2441 measured — independent confirmation.

Now the Weil representation of `Sp(4,3)`, degree `q² = 9`, splitting into its two parity
constituents `(q²−1)/2 = 4` and `(q²+1)/2 = 5`:

```text
degree 4 : 2 irreducibles   faithful  TRUE    complex [true, true]
degree 5 : 2 irreducibles   faithful  FALSE   complex [true, true]
```

> **The Weil representation is the one object that lives on both sides.** Its odd half
> (degree 4) is faithful — the chiral, central doubling. Its even half (degree 5) is
> inflated — the achiral, outer doubling. Both halves are complex.

That answers "which doubling carries the physics": **neither, exclusively.** The
oscillator representation is precisely the object that bridges the two towers that
Pass 2443 proved admit no intertwiner between them. It does so by splitting, not by
mapping.

---

## Pass 2449 — the outer involution **fuses the faithful pair**: chirality is unselectable, in one line

Both doublings sit inside a single group:

```text
|2.U4(2).2| = 103680 = 2 x 51840
```

Inducing each faithful degree-4 into it:

```text
chi(1) = 4  induced to 2.U4(2).2 is irreducible  ->  TRUE   (the outer coset MOVES it)
chi(1) = 4  induced to 2.U4(2).2 is irreducible  ->  TRUE
for contrast, the two degree-45s of U4(2)        ->  TRUE, TRUE
```

> **The outer involution exchanges the two faithful degree-4 Weil constituents — the two
> chiralities of the `E₈` carrier.** The element that generates the resolution
> obstruction *is* the one that swaps handedness.

This is the one-line proof of the closed selection-layer result (Pass 346, `T` with
`det = −1` swaps `S±`), now at the level of characters rather than a specific matrix,
and it simultaneously re-derives my Pass 2076 (`σ_S` swaps the two degree-45s) as the
same phenomenon one floor down.

---

## Pass 2450 — **no 9-colouring of `H` is group-equivariant**

A genuinely new obstruction, and it explains a long run of failures.

```text
maximal subgroup indices of U4(2).2 : [2, 27, 36, 40, 40, 45]
```

There is **no index 3 and no index 9**. The reason is structural: `U₄(2)` is simple with
minimal faithful permutation degree **27**, so any action of `G` on `≤ 9` points must
have kernel containing `U₄(2)` — otherwise `U₄(2)` would embed in `S₉` with degree
`9 < 27`. Hence `G` acts on the 9 colours through `G/U₄(2) = C₂`, and **every colour
orbit has size 1 or 2**.

Now `9` is odd, so at least one orbit has size 1 — some colour class would be
`G`-invariant. But `G` is **transitive** on the 540 frames (`51840/540 = 96`), so it has
no invariant proper nonempty subset.

> **Contradiction. If `χ(H) = 9` holds, no 9-colouring has any nontrivial `G`-symmetry
> permuting its colour classes.** Every colouring lies in a `G`-orbit of size at least 2,
> and the colouring itself is asymmetric.

This is why nine solver configurations and every symmetry-reduced attack returned
`UNKNOWN`: **symmetry reduction is not merely unhelpful here, it is searching a provably
empty set.** Future attempts must search asymmetric colourings directly — which is
exactly what the parallel track's Pass 2412 orbit-free enumeration does, and is the
right shape.

---

## Pass 2451 — chirality vs contextuality: the honest verdict

Pass 2442 found the chiral tower sits over the ovoid-free (Kochen–Specker uncolourable)
40 and the achiral tower over the 36-ovoid one. Is that a theorem or a coincidence?

**It is an alignment on a complete two-element universe, and it cannot be upgraded.**

- There are exactly **two** generalised quadrangles of order `(3,3)` up to isomorphism —
  `W(3)` and `Q(4,3)` — and they are dual to each other (Payne–Thas). So the "family" is
  already exhausted; there is no third example to test against.
- There is **no `q`-general version**, because the `C₆`/`S₃` fibre split depends on the
  240 `E₈` roots fibring 6:1 over 40 points, and there is no `E₈` tower at `q = 5` (156
  points) or `q = 7`.
- **No mechanism was found.** Counting does not forbid an ovoid on the chiral side: an
  ovoid is 10 of 40 points, whose preimage would be `10 × 6 = 60` roots, an integer with
  no divisibility obstruction. Whatever forbids it is finer than the fibration.

Recorded as a **measured co-occurrence on a 2-element set**, not a theorem. Stating it
as a law would be exactly the over-read failure mode this repo has produced before.

---

## Pass 2452 — the Fibonacci descent as a datapath, SAT-proved

Pass 2439 proved `M = R₄²U₆` negates the A-sector `(1,0,0)` and induces `[[0,−1],[−1,1]]`
on the quotient. As hardware that is a two-register machine:

```text
a_out = -a_in            the A-sector (the 24) merely flips sign : period 2
b_out = -c_in            the BC-pair (the 90) advances by the
c_out =  c_in - b_in     Fibonacci matrix : grows like phi^n
```

Yosys 0.67 SAT over all inputs in range:

```text
Solving problem with 1208 variables and 3376 clauses..
SAT proof finished - no model found: SUCCESS!
```

The proved assertions include `a2 == a0` (the A-sector has period exactly 2) and, the
real content, **`c3 == c2 + c1` and `c2 == c1 + c0`** — the Fibonacci recursion
`a(n) = a(n−1) + a(n−2)` discharged directly in the netlist, which is the characteristic
polynomial `t² − t − 1` read off the datapath.

Eight unrolled stages synthesise to `134 SB_CARRY + 163 SB_LUT4` on iCE40.

> **The substrate's golden word is a periodic register bolted to a `φ`-growing one**, and
> the split is the reducible characteristic polynomial made physical.

**Scope:** a faithful encoding of a proved fact, not independent evidence for it.

---

## Pass 2453 — ledger

Claims added this batch and how each is discharged:

| claim | discharged by |
|---|---|
| Weil halves land on opposite doublings | GAP character table, `2.U₄(2)` |
| outer coset fuses the faithful degree-4 pair | GAP induction into `2.U₄(2).2` |
| no index-3 or index-9 subgroup of `U₄(2).2` | GAP `Maxes`, plus the degree-27 argument |
| no `G`-equivariant 9-colouring | the above + transitivity on 540 frames |
| A-sector period 2, BC-pair Fibonacci | Yosys SAT, 1208 vars / 3376 clauses |
| chirality/contextuality alignment | **not** promoted — 2-element universe |

---

## Prior art

- Pass 2414 (parallel track) — the central-character obstruction; Pass 2443 showed it is
  my antipode dichotomy.
- Pass 2412 (parallel track) — the 394,200-cover enumeration. Pass 2450 explains why its
  orbit-free shape is the correct one.
- Pass 346 — chirality hostable but unselectable. Pass 2449 gives it a character proof.
- Pass 2076 (mine) — `σ_S` swaps the two degree-45s; the same phenomenon one floor down.
- Payne–Thas — exactly two `GQ(3,3)`s, dual to each other.
- Minimal faithful permutation degree of `U₄(2)` is 27 — classical.

## Still open

- `χ(H) = 9` itself. Now known to require an **asymmetric** colouring, which narrows the
  search shape but not the size. Still blocked on the parallel track's frozen cover
  bitsets for the packing step.
- Whether the chirality/contextuality alignment has a mechanism. No progress; recorded
  as unexplained co-occurrence.
