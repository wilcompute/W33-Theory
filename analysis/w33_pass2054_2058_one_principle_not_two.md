# Passes 2054–2058 — one selection principle, not two; and the decimals are base-scoped

Five items. The first is a self-correction I flagged in my own next-steps and
then confirmed; the second stops a numerology drift before it starts.

---

## Pass 2054 — the two `q = 3` principles are **one**

Last batch I recorded two derived selection principles. Reducing both:

```text
A (Pass 2042) : the star acts on edges of K_{q+1}  <=>  (q+1) - 2 = 2  <=>  q+1 = 4
B (Pass 2047) : 2q+1 = q(q+1)/2 + 1                <=>  4q = q(q+1)    <=>  q+1 = 4
```

> **Both reduce to `q + 1 = 4`. They are one principle, not two.**

The honest statement is simply:

> **The substrate is selected by `q + 1 = 4` — its lines are tetrahedra.**

Everything else — the star acting on the middle degree, the Heawood number
landing one past the mod-12 midpoint, the three star-orbits being the three
1-factors — is that one fact wearing different clothes. I was double-counting,
and "two independent coincidences at one value" is a much stronger claim than
"one identity", so the correction matters.

---

## Pass 2055 — the decimal structure is **base-scoped**, and the scoping is not what I expected

The `142857` observations are base-10 facts, so the first question is whether
they can be structural at all for a base-independent object. Checking the order
of 10 mod 7 against other bases:

```text
base   ord_b(7)   period of 1/7   full reptend?
   2          3               3   False
   3          6               6   TRUE     <- the substrate's characteristic
   5          6               6   TRUE
  10          6               6   TRUE
  12          6               6   TRUE
```

```text
1/7 in base 10 : 142857   period 6
1/7 in base  3 : 010212   period 6
1/7 in base  2 : 001      period 3
```

> **`7` being full-reptend is *not* a base-10 artifact — it holds in base 3, the
> substrate's own characteristic, with the same period 6.** What *is* base-10
> specific is the digit string `142857` and the `3-6-9` pattern.

So the scoping splits the user's observation in two:

- **Survives:** `7` has maximal cyclic order mod its own size, in base 3 as well
  as base 10. That is a statement about `7`, not about base 10.
- **Base-10 only:** that the repetend's digits are exactly the terminating
  denominators `{1,2,4,5,8} ∪ {7}`, and that `{3,6,9}` are the ones missing.

And `ord₃(7) = 6 = C(4,2) = ` the tetrahedron's edge count is **the same number,
different objects** — recorded as a count match, not a link, per the rule that
has already retired three claims in this arc.

---

## Pass 2056 — the renumber guard

`scripts/next_pass_number.py` now carries `range_is_free(lo, hi, used)`:

```text
range_is_free(2011, 2015, {2011, 2013})  ->  (False, [2011, 2013])
range_is_free(3000, 3004, {2011})        ->  (True,  [])
```

The gap it closes is specific. The claim path checks the highest number in use
and pushes reservation commits — but a batch that **renumbers after the fact**
bypasses that check entirely. Passes 2011–2015 were claimed and published by one
track at 09:18 and renumbered into by the other at 09:41. Collisions were handled
at claim time and not at renumber time.

Third piece of infrastructure in this arc built from a repeated failure rather
than a plan, after `constraint_audit.py` and `gset_audit.py`.

---

## Pass 2057 — their `D₈` witness: located, not yet used

The parallel track's Pass 2012 reports a literal `D₈` exact-cover witness — twelve
frame orbits of sizes `2,2,4,4,4,4,4,4,8,8,8,8` covering all 240 edges exactly
once. From this side I can see their CI workflow
(`pass2011_2015_decorated_spreads_subgroups_scheme_rook_quadratic.yml`) but have
not located the witness payload itself in the tree.

**Not tested.** The obvious next step — take their parallel class and search for
eight more disjoint from it — is the best-posed attack on `χ(H) = 9` currently
available, and it needs their data rather than a reconstruction. Recorded as
blocked on locating the file, not as attempted.

---

## Pass 2058 — the selection principle, for the draft

For the referee draft, the statement that belongs there is the corrected single
one:

> **`W(3,3)` is distinguished among `W(q,q)` by `q + 1 = 4`: its totally isotropic
> lines are tetrahedra, the unique simplex on which the star acts in middle
> degree, so `σ_S`'s choice of a 1-factor is simultaneously a choice of
> star-orbit.**

Not two principles, and not a coincidence — one identity with one solution.

---

## Prior art

- Pass 2042/2047 — the two principles this pass merges into one.
- `dccxxii`/`dccxxiii` — **own** the `142857` and `3-6-9` observations.
- Passes 2011–2015 (parallel track) — **own** the `D₈` witness and the subgroup
  census.
- The seven-fold and decimal observations are the user's.

## Still open

- `χ(H) = 9`, best attacked from their `D₈` parallel class.
- Whether `q + 1 = 4` has a deeper reason than "the star needs middle degree".
