# Passes 2065–2070 — the primitive-root containment is a **theorem**, and the phinary lane, scoped

The flagged coincidence from last batch turned out to be provable. The phinary
exploration is recorded with what it does and does not support.

---

## Pass 2065 — every primitive-root Sophie Germain prime is genus-reachable

Last batch I observed that `q ∈ {2, 3, 11, 23, 83}` — Sophie Germain primes with
`q` a primitive root mod `2q+1` — all lie in the genus-reachable set
`q ≡ 2, 3, 11 (mod 12)`, and flagged it as small-list overlap. Extending:

```text
primitive-root Sophie Germain q < 2000 : 32 values
genus-reachable q < 2000               : 81 values
contained ?  TRUE   (32 inside, 0 outside)
```

Zero exceptions in 32 values is not overlap. And it is provable.

**Theorem.** Let `q` and `p = 2q+1` both be prime. If `q` is a primitive root
mod `p`, then `q` is genus-reachable.

*Proof.*

1. `ord_p(q)` divides `p − 1 = 2q`, so it lies in `{1, 2, q, 2q}`. Hence `q` is a
   primitive root iff `q^q ≠ 1` and `q² ≠ 1`, i.e. iff `q` is a **quadratic
   non-residue** mod `p` (and `q ≢ ±1`).

2. `2q = p − 1 ≡ −1 (mod p)`, so `q ≡ −2⁻¹`, giving
   `(q|p) = (−1|p)(2|p)`.

   ```text
   q ≡ 3 (mod 4)  ->  p ≡ 7 (mod 8)  ->  (−1|p) = −1, (2|p) = +1  ->  (q|p) = −1   primitive
   q ≡ 1 (mod 4)  ->  p ≡ 3 (mod 8)  ->  (−1|p) = −1, (2|p) = −1  ->  (q|p) = +1   not
   ```

   So **`q` is a primitive root mod `2q+1` iff `q ≡ 3 (mod 4)`.**

3. Sophie Germain with `q > 3` forces `q ≡ 2 (mod 3)`: if `q ≡ 1 (mod 3)` then
   `2q+1 ≡ 0 (mod 3)`, so `3 | p` and `p` is not prime.

4. `q ≡ 3 (mod 4)` and `q ≡ 2 (mod 3)` give `q ≡ 11 (mod 12)` by CRT — which is
   in the reachable set. The small cases `q = 2` (`p = 5`) and `q = 3` (`p = 7`)
   are reachable directly. ∎

**Verification, `q < 4000`:** 99 Sophie Germain primes, **0 violations** of step
2, step 3 or step 4.

> **`q = 3` is a primitive root mod its own Heawood number `7`, and that property
> *implies* genus-reachability.** Two conditions that looked independent are one
> implication, and the mechanism is `q ≡ 11 (mod 12)` — with `q = 3` as one of the
> two small exceptions.

That is the "something universal" being asked for: a base-independent statement
relating `q` to quantities derived from `q`, proved rather than observed.

---

## Pass 2066 — phinary and Zeckendorf, verified (including my own error)

```text
Zeckendorf, n = 1..4999 with a full Fibonacci list : 0 failures
binary strings of length n with no "11"           : 2,3,5,8,13,21,34,55 = F(n+2)  ✓
rabbit word (0->01, 1->0)                         : contains "11"? False   "000"? False
phi^2 = phi + 1                                   : True
```

The user's recollection is right: **base-φ standard form and Zeckendorf
representation both have no two consecutive 1s**, and that constraint is exactly
what makes the count Fibonacci.

**My own error, recorded.** My first run reported 56 Zeckendorf failures. The
theorem is fine; my Fibonacci list stopped at 89, so `144` was missing and the
greedy algorithm produced consecutive terms. A truncated table, not a
counterexample — and the sort of thing that would have been published as a
refutation of a classical theorem if I had not re-checked.

---

## Pass 2067 — the Fibonacci-anyon bridge is already the repo's

```text
Fibonacci : 28 files      anyon : 14 files      golden : 22 files
Zeckendorf: 0 files
```

`analysis/BT695_fibonacci_register_correction_theorem.md` carries the bridge

```text
K_{3,3}  ->  [9,4,4]  ->  SU(2)_3  ->  Fibonacci anyons
```

and BT695 exists specifically to separate the classical `K₃,₃` cycle code
(`β₁ = 4`) from the quantum register reading from the anyon fusion
representation. So **the Fibonacci-anyon route is BT686/BT695's**, and the
universality it carries (Freedman–Larsen–Wang) is theirs to cite.

**Zeckendorf is genuinely absent** — that vocabulary is new here.

---

## Pass 2068 — but the substrate has no golden structure, and that is a negative

```text
SRG(40,12,2,4) eigenvalues : 12, 2, −4
any eigenvalue = phi or phi^2 ? FALSE
independent sets of K_{q+1} : q + 2  (linear, not Fibonacci)
```

> **The substrate's spectra contain no golden ratio and its natural counts obey
> no Fibonacci recursion.** The `no-two-consecutive` constraint is an
> independent-set condition on a *path*; the substrate's independent-set
> structure is on `H` and on complete graphs, neither of which is path-like.

So the phinary connection, if there is one, does not come through the spectrum or
through the counting — it would have to come through BT695's `K₃,₃` route, which
is a different object from the spread/tetrahedron structures this arc has been
about. Recorded as a negative rather than left as an open invitation.

---

## Pass 2069 — the `D₈` reconstruction: partial

```text
frames 540, H = D8 x S4 order 192
H-subgroup classes of order 2, 4, 8 : 116
```

The enumeration reproduces their setup — 116 classes in the right band — but the
exact-cover search hit a recursion limit before completing. **Partial, not
negative.** The parallel track's Pass 2012 reports 33 successful classes from
this stabiliser; I have reproduced the search space, not yet the result.

---

## Pass 2070 — what I would send the other track

The corrected `q = 3` statement (Pass 2062) plus this one:

> `q = 3` is a primitive root modulo its own Heawood number `2q+1 = 7`, and for
> Sophie Germain primes that property is equivalent to `q ≡ 3 (mod 4)` and
> implies `q ≡ 11 (mod 12)` — hence implies genus-reachability. `q = 3` is one of
> the two exceptions below that congruence.

---

## Prior art

- BT686 / **BT695** — **own** the `K₃,₃ → [9,4,4] → SU(2)₃ → Fibonacci anyon`
  bridge; Freedman–Larsen–Wang own the universality.
- Passes 2011–2015 (parallel track) — **own** the `D₈` witness.
- Pass 2024 — the genus-reachability congruence; Pass 2060 — the primitive-root
  observation this pass proves.
- The phinary / Zeckendorf / Fibonacci-anyon suggestion is the user's.

## Still open

- `χ(H) = 9`.
- Whether anything in the substrate is genuinely golden — the spectrum says no.
